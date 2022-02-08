from odoo import models, fields, api


class StockInventoryLine(models.Model):
    _name = "stock.inventory.line.ept"
    _description = "Stock Inventory Line"

    inventory_id = fields.Many2one(string="Inventory", help="Inventory of the current line",
                                   comodel_name="stock.inventory.ept")
    product_id = fields.Many2one(string="Product", help="Product in the Inventory", comodel_name="product.ept")
    available_qty = fields.Float(string="System Quantity", help="Quantity of the product according to the system", readonly=True)
    counted_product_qty = fields.Float(string="Actual Quantity", help="Actual available Product quantity", digits=(6, 2))
    difference = fields.Float(string="Difference", help="Difference in the system quantity and actual quantity", compute="calculate_difference", store=False)

    def calculate_difference(self):
        pass
