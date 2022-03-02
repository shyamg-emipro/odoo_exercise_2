from odoo import models, fields, exceptions, api


class SaleOrderExtended(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    lead_id = fields.Many2one(string="Lead", help="Lead from which current sale order is generated",
                              comodel_name="crm.lead")
    is_all_picking_completed = fields.Boolean(string="Sale Order is Done",
                                              help="True if all Delivery orders of current sale order is either done or cancelled.",
                                              compute="_compute_is_all_picking_completed",
                                              search="find_completed_sale_order",
                                              store=False)
    total_margin = fields.Float(string="Total Profit", help="Total profit margin of this sale order.", compute="_get_total_profit")
    total_margin_percentage = fields.Float(string="Total Profit Percentage", help="Total profit margin percentage", compute="_get_total_profit")
    product_tmpl_ids = fields.Many2many(comodel_name="product.template", string="Product", help="Select Product to get It's variants.")

    @api.onchange('product_tmpl_ids')
    def get_product_variants(self):
        # products = self.product_tmpl_ids.product_variant_ids.filtered(lambda p: sum([stocks.reserved_quantity for stocks in p.stock_quant_ids]) > 1)
        products = self.product_tmpl_ids.product_variant_ids.filtered(
            lambda p: p.virtual_available > 1)
        order_lines = []
        for pid in products.ids:
            order_line = self.env["sale.order.line"].new({'product_id': pid})
            order_line.product_id_change()
            order_lines.append((0, 0, {
                'product_id': pid,
                'name': order_line.name,
                'product_uom_qty': 1,
                'price_unit': order_line.product_id.list_price
            }))
        self.order_line = order_lines

    def _get_total_profit(self):
        for order in self:
            total_margin_percentage = 0
            total_profit = 0
            for line in order.order_line:
                total_profit += line.margin
            if total_profit > 0:
                total_margin_percentage = total_profit * 100 / order.amount_total
            elif total_profit == 0:
                total_margin_percentage = 0
            else:
                if order.amount_total <= 0:
                    total_margin_percentage = -100
                else:
                    total_margin_percentage = total_profit * 100 / (order.amount_total - total_profit)
            order.total_margin = total_profit
            order.total_margin_percentage = total_margin_percentage

    def action_confirm(self):
        # product = self.env.ref("sale_order_extended.crm_tags_product_product_extended")
        # order_line = self.env["sale.order.line"].new({'product_id': product.id})
        # order_line.product_id_change()
        # self.order_line .create({
        #     'order_id': self.id,
        #     'product_id': product.id,
        #     'name': order_line.name,
        #     'price_unit': order_line.price_unit
        # })
        return super(SaleOrderExtended, self).action_confirm()

    def add_deposit(self):
        for line in self.order_line:
            product = line.product_id
            if product.deposit_product_id:
                child = self.order_line.filtered(lambda ol: line.id == ol.parent_id.id)
                if child:
                    child[0].product_uom_qty = product.deposit_product_qty * line.product_uom_qty
                    child[0].price_unit = product.deposit_product_id.list_price
                else:
                    deposit_product = product.deposit_product_id
                    new_line = line.new({'product_id': deposit_product.id})
                    new_line.product_id_change()
                    new_line.product_uom_qty = product.deposit_product_qty * line.product_uom_qty
                    line.create({
                        'order_id': self.id,
                        'parent_id': line.id,
                        'product_id': deposit_product.id,
                        'name': new_line.name,
                        'price_unit': deposit_product.list_price,
                        'product_uom_qty': new_line.product_uom_qty

                    })

    def show_reserved_order_lines(self):
        products = self.order_line.product_id
        action = self.env['ir.actions.actions']._for_xml_id("sale_order_extended.action_sale_order_line_extended_window")
        action['domain'] = [('id', 'not in', self.order_line.ids), ('product_id', 'in', products.ids), ('move_ids.state', '=', "assigned")]
        return action

    def confirm_validate(self):
        self.action_confirm()
        self.picking_ids.move_lines._set_quantities_to_reservation()
        self.picking_ids.with_context(skip_backorder=True).button_validate()

    def _compute_is_all_picking_completed(self):
        for order in self:
            if set([picking.state for picking in order.picking_ids]) & {'draft', 'waiting', 'confirmed', 'assigned'}:
                order.is_all_picking_completed = False
            else:
                order.is_all_picking_completed = True

    def find_completed_sale_order(self, operator, value):
        query = """
            select id from sale_order where id not in (select sale_id from stock_picking where state not in ('done', 'cancel') and sale_id is not null group by sale_id);
        """
        # select sale_id from stock_picking where state in ('done', 'cancel') and sale_id is not null group by sale_id;
        self._cr.execute(query)
        get_res = list(map(lambda li: li[0], self._cr.fetchall()))
        return [('id', 'in', get_res)]