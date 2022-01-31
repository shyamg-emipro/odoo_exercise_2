from odoo import models, fields


class UomCategory(models.Model):
    _name = "product.uom.category.ept"
    _description = "Product UOM Category"

    name = fields.Char(string="Category", help="Category for the unit of measure")
    uom_ids = fields.One2many(string="UOMs", comodel_name="product.uom.ept", inverse_name="uom_category_id")
