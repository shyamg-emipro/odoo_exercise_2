from odoo import models, fields


class SaleOrderLineExtended(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    parent_id = fields.Many2one(comodel_name="sale.order.line", string="Parent Line", help="Parent Order Line of the current order line")
    cost_price = fields.Float(related="product_id.standard_price", string="Cost")
    margin = fields.Float(string="Profit", help="Margin on this product", compute="_calculate_margin")
    margin_in_percentage = fields.Float(string="Profit Percentage", help="Shows margin on this product in percentage", compute="_calculate_margin")
    def unlink(self):
        for line in self:
            child = self.env['sale.order.line'].search([('parent_id', '=', line.id)], limit=1)
            if child:
                child.unlink()
        return super(SaleOrderLineExtended, self).unlink()

    def _calculate_margin(self):
        for line in self:
            margin = 0
            margin_percentage = 0
            margin = line.price_subtotal - line.cost_price * line.product_uom_qty
            if margin > 0:
                margin_percentage = margin * 100 / line.price_subtotal
            elif margin == 0:
                margin_percentage = 0
            else:
                if line.cost_price <= 0:
                    margin_percentage = -100
                else:
                    margin_percentage = margin * 100 / line.cost_price
            line.margin = margin
            line.margin_in_percentage = margin_percentage
