from odoo import models, fields, api


class ProductProductExtended(models.Model):
    _name = "product.product"
    _inherit = "product.product"

    deposit_product_id = fields.Many2one(comodel_name="product.product", string="Deposit", help="Deposit that needs to be taken for this product")
    deposit_product_qty = fields.Integer(string="Deposit Quantity", help="Quantity of deposit for this product")
