from odoo import models, fields


class SaleOrderLineExtended(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    parent_id = fields.Many2one(comodel_name="sale.order.line", string="Parent Line", help="Parent Order Line of the current order line")
    cost_price = fields.Float(related="product_id.standard_price", string="Cost")
    margin = fields.Float(string="Margin", help="Margin on this product", compute="_calculate_margin", store=False)

    def unlink(self):
        for line in self:
            child = self.env['sale.order.line'].search([('parent_id', '=', line.id)], limit=1)
            if child:
                child.unlink()
        return super(SaleOrderLineExtended, self).unlink()

    def _calculate_margin(self):
        # for line in self:
        pass
