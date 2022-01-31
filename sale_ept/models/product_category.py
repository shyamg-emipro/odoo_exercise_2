from odoo import models, fields


class ProductCategory(models.Model):
    _name = "product.category.ept"
    _description = "Product Category"

    name = fields.Char(string="Name", required=True, help="Name of the Product Category")
    parent_id = fields.Many2one(string="Parent Category", comodel_name="product.category.ept", help="Parent Category of the Current Product Category")
