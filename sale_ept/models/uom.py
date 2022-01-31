from odoo import models, fields


class Uom(models.Model):
    _name = "product.uom.ept"
    _description = "Product UOM"

    name = fields.Char(string="UOM", help="Unit of Measure of the Product")
    uom_category_id = fields.Many2one(string="Category", help="Category of the UOM", comodel_name="product.uom.category.ept")
