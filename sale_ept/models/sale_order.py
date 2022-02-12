from odoo import models, fields, api, exceptions


class SaleOrder(models.Model):
    _name = "sale.order.ept"
    _description = "Sale Order"
    _rec_name = "order_no"

    order_no = fields.Char(string="Order No", help="Order Number", readonly=True)
    partner_id = fields.Many2one(string="Partner", comodel_name="res.partner.ept", help="Partner who placed this order")
    partner_invoice_id = fields.Many2one(string="Invoice Address", comodel_name="res.partner.ept",
                                         help="Partner who's address type is Invoice")
    partner_shipping_id = fields.Many2one(string="Shipping Address", comodel_name="res.partner.ept",
                                          help="Partner who's address type is Shipping")
    date = fields.Date(string="Date", help="Date at which the order is placed", default=fields.Datetime.today())
    order_lines = fields.One2many(string="Order Lines",
                                  help="Order Lines of the current order",
                                  comodel_name="sale.order.line.ept",
                                  inverse_name="order_id")
    salesperson = fields.Many2one(string="Sales Person", help="Sales person who negotiated this order",
                                  comodel_name="res.users")
    state = fields.Selection(string="State",
                             help="State of the order",
                             selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')],
                             default="Draft")
    total_weight = fields.Float(string="Total Weight", help="Total Weight of the order", digits=(8, 2),
                                compute="calculate_total_weight")
    total_volume = fields.Float(string="Total Volume", help="Total Volume of the order", digits=(8, 2),
                                compute="calculate_total_volume")
    order_total = fields.Float(string="Order Total", help="Total amount of the order", compute="calculate_order_total",
                               store=True)
    lead_id = fields.Many2one(comodel_name="crm.lead.ept", string="Lead", help="Lead details of this order")
    warehouse_id = fields.Many2one(string="Warehouse",
                                   help="Warehouse from which product is going to be delivered to the customer",
                                   comodel_name="stock.warehouse.ept",
                                   required=True)
    picking_ids = fields.One2many(string="Delivery Orders", help="Delivery Orders associated with this Sale Order", comodel_name="stock.picking.ept", inverse_name="sale_order_id")
    total_tax = fields.Float(string="Total Tax", help="Finds the total Tax on all order lines",
                             digits=(6, 2), compute="find_total_tax", store=True)
    total_amount = fields.Float(string="Total Amount", help="Total Amount to be paid by the customer",
                                digits=(6, 2), compute="get_total_amount", store=True)

    @api.model
    def create(self, vals):
        if not vals.get('order_no', False):
            vals['order_no'] = self.env['ir.sequence'].next_by_code(sequence_code="sale.order.ept") or False
        return super(SaleOrder, self).create(vals)

    def calculate_total_weight(self):
        for order in self:
            total_weight = 0
            for line in order.order_lines:
                total_weight += line.product_id.weight * line.quantity
            order.total_weight = total_weight

    def calculate_total_volume(self):
        for order in self:
            total_volume = 0
            for line in order.order_lines:
                total_volume += line.product_id.volume * line.quantity
            order.total_volume = total_volume

    @api.depends('order_lines.subtotal_without_tax')
    def calculate_order_total(self):
        for order in self:
            order_total = 0
            for line in order.order_lines:
                order_total += line.subtotal_without_tax
            order.order_total = order_total

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id.id:
            partner_id = self.partner_id
            partners = partner_id.child_ids
            if not partners:
                if partner_id.address_type == "Invoice" or "Shipping":
                    self.partner_invoice_id = partner_id
                    self.partner_shipping_id = partner_id
                else:
                    raise exceptions.ValidationError("No customer found with Invoice address or Shipping Address!")
            else:
                invoice = partners.filtered(lambda partner: partner.address_type == "Invoice")
                shipping = partners.filtered(lambda partner: partner.address_type == "Shipping")
                if not invoice and not shipping:
                    raise exceptions.ValidationError("No customer found with Invoice address or shipping address!")
                elif not invoice:
                    self.partner_invoice_id = shipping[0]
                    self.partner_shipping_id = shipping[0]
                else:
                    self.partner_invoice_id = invoice[0]
                    self.partner_shipping_id = invoice[0]

    def confirm_sale_order(self):
        stock_locations = {}
        source_location = self.warehouse_id
        destination_location = self.env['stock.location.ept'].search([('location_type', '=', 'Customer')], limit=1)

        if not destination_location.id:
            raise exceptions.UserError("No, Customer Location found, Please create customer location record to continue!")
            return False
        if not source_location.id:
            raise exceptions.UserError("No, Warehouse Location found, Please select Warehouse location to continue!")
            return False

        for line in self.order_lines:
            if line.warehouse_id:
                source_location = line.warehouse_id
            else:
                source_location = self.warehouse_id
            if not stock_locations.get(source_location.id, False):
                stock_locations.update({source_location.id: []})

            stock_locations[source_location.id].append((0, 0, {
                'name': line.product_id.name + ": " + source_location.stock_location_id.name + " -> " + destination_location.name,
                'product_id': line.product_id.id,
                'uom_id': line.uom_id.id,
                'source_location_id': source_location.stock_location_id.id,
                'destination_location_id': destination_location.id,
                'qty_to_deliver': line.quantity,
                'sale_line_id': line.id,
            }))

        for warehouse_location_id, moves in stock_locations.items():
            sale_order_data = {'partner_id': self.partner_shipping_id.id,
                               'transaction_type': 'Out',
                               'sale_order_id': self.id,
                               'move_ids': moves}
            self.env['stock.picking.ept'].create(sale_order_data)

        self.order_lines.state = "Confirmed"
        self.state = "Confirmed"

    def cancel_sale_order(self):
        delivery_orders = self.env['stock.picking.ept'].search([('sale_order_id', '=', self.id)])
        if not delivery_orders:
            self.order_lines.state = "Cancelled"
            self.state = "Cancelled"
        else:
            for order in delivery_orders:
                if order.state != "Cancelled":
                    raise exceptions.UserError("First Cancel the Delivery Order!")
                    break
            else:
                self.order_lines.state = "Cancelled"
                self.state = "Cancelled"


    def draft_sale_order(self):
        self.order_lines.state = "Draft"
        self.state = "Draft"

    def done_sale_order(self):
        self.order_lines.state = "Done"
        self.state = "Done"

    def show_delivery_order_ept(self):
        action = self.env['ir.actions.actions']._for_xml_id("sale_ept.action_stock_picking_ept_out_window")

        delivery_orders = self.picking_ids

        if len(delivery_orders) > 1:
            action['domain'] = [('id', 'in', delivery_orders.ids)]
        elif delivery_orders:
            form_view = [(self.env.ref("sale_ept.view_stock_picking_ept_form").id, 'form')]
            action['views'] = form_view
            action['res_id'] = delivery_orders.id
        else:
            raise exceptions.UserError("No Delivery Order is created for this sale order")
            return False
        return action

    def show_stock_moves(self):
        action = self.env['ir.actions.actions']._for_xml_id("sale_ept.action_stock_move_ept_window")

        stock_moves = self.picking_ids.move_ids

        if len(stock_moves) > 1:
            action['domain'] = [('id', 'in', stock_moves.ids)]
        elif stock_moves:
            form_view = [(self.env.ref("sale_ept.view_stock_move_ept_form").id, 'form')]
            action['views'] = form_view
            action['res_id'] = stock_moves.id
        else:
            raise exceptions.UserError("No Stock Move is created for this sale order")
            return False
        return action

    @api.depends('order_lines')
    def get_total_amount(self):
        for order in self:
            total_amount = 0
            for line in order.order_lines:
                total_amount += line.subtotal_with_tax
            order.total_amount = total_amount

    @api.depends('order_lines.subtotal_with_tax')
    def find_total_tax(self):
        for order in self:
            total_tax = 0
            for line in order.order_lines:
                total_tax += line.subtotal_with_tax - line.subtotal_without_tax
            order.total_tax = total_tax
