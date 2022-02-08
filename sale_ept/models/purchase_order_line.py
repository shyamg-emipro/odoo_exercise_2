from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line.ept"
    _description = "Purchase Order Line"

    purchase_order_id = fields.Many2one(string="Purchase Order", help="Purchase order of the current Order line",
                                        comodel_name="purchase.order.ept")
    product_id = fields.Many2one(string="Product", help="Product that we are going to purchase",
                                 comodel_name="product.ept")
    name = fields.Char(string="Description", help="Description about the product")
    quantity = fields.Float(string="Quantity", help="Quantity of the product",
                            digits=(6, 2))
    cost_price = fields.Float(string="Cost Price", help="Price at which we are going to buy the product")
    state = fields.Selection(string="State", help="Sate of the purchase order line",
                             selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'), ('Cancelled', 'Cancelled')],
                             default="Draft")
    uom_id = fields.Many2one(string="UOM", help="Unit of Measure", comodel_name="product.uom.ept")

    @api.onchange('product_id')
    def generate_product_name(self):
        self.name = self.product_id.description
