from odoo import models, fields, api, exceptions


class PurchaseOrder(models.Model):
    _name = "purchase.order.ept"
    _description = "Purchase Order"

    warehouse_id = fields.Many2one(string="Warehouse", help="Warehouse location in which purchased product is going to be placed",
                                   comodel_name="stock.warehouse.ept")
    partner_id = fields.Many2one(string="Vendor/Supplier", help="Vendor or supplier that is going to supply the products to us",
                                 comodel_name="res.partner.ept")
    order_date = fields.Date(string="Date", help="Date of the Order", default=fields.Datetime.today())
    name = fields.Char(string="Name", help="Unique identifier of the Purchase Order", readonly=True)
    state = fields.Selection(string="State", help="State of the purchase order",
                             selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'), ('Cancelled', 'Cancelled')],
                             default="Draft")
    purchase_order_line_ids = fields.One2many(string="Purchase Order Lines", help="Products Purchased in this order",
                                              comodel_name="purchase.order.line.ept",
                                              inverse_name="purchase_order_id")

    @api.model
    def create(self, vals):
        if not vals.get('name', False):
            vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code="purchase.order.ept") or False
        return super(PurchaseOrder, self).create(vals)

    def confirm_purchase_order(self):
        stock_moves_data = []
        source_location = self.env['stock.location.ept'].search([('location_type', '=', 'Vendor')], limit=1)
        destination_location = self.warehouse_id.stock_location_id
        if not source_location.id:
            raise exceptions.UserError("No Vendor Location found, Please create Vendor Location record to continue!")
            return False
        if not destination_location.id:
            raise exceptions.UserError("No Warehouse Location found, Please select Warehouse Location to continue!")
            return False
        for line in self.purchase_order_line_ids:
            stock_moves_data.append((0, 0, {
                'name': "Product Name: " + source_location.name + " -> " + destination_location.name,
                'product_id': line.product_id.id,
                'uom_id': line.uom_id.id,
                'source_location_id': source_location.id,
                'destination_location_id': destination_location.id,
                'qty_to_deliver': line.quantity,
                'purchase_line_id': line.id
            }))
        purchase_order_data = {
            'partner_id': self.partner_id.id,
            'purchase_order_id': self.id,
            'transaction_type': "In",
            'move_ids': stock_moves_data
        }
        self.env['stock.picking.ept'].create(purchase_order_data)
        self.state = "Confirmed"

    def cancel_purchase_order(self):
        purchase_order = self.env['stock.picking.ept'].search([('purchase_order_id', '=', self.id)])
        if not purchase_order:
            self.state = "Cancelled"
        else:
            if purchase_order.state == "Cancelled":
                self.state = "Cancelled"
            else:
                raise exceptions.UserError("First Cancel the Incoming Shipment!")

    def draft_purchase_order(self):
        self.state = "Draft"

    def done_purchase_order(self):
        for line in self.purchase_order_line_ids:
            line.state = "Done"
        self.state = "Done"
