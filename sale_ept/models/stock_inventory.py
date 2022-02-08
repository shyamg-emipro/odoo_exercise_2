from odoo import models, fields, api


class StockInventory(models.Model):
    _name = "stock.inventory.ept"
    _description = "Stock Inventory"

    name = fields.Char(string="Name", help="Name of the Inventory", required=True)
    state = fields.Selection(string="State", help="State of the Inventory",
                             selection=[('Draft', 'Draft'), ('In-Progress', 'In-Progress'), ('Done', 'Done'), ('Cancelled', 'Cancelled')],
                             default="Draft")
    location_id = fields.Many2one(string="Location", help="Location where you want to make adjustments", comodel_name="stock.location.ept")
    inventory_date = fields.Date(string="Date", help="Date at which inventory adjustments are made", default=fields.Datetime.today())
    inventory_line_ids = fields.One2many(string="Inventory Lines", help="Products in which you want to make adjustments", comodel_name="stock.inventory.line.ept", inverse_name="inventory_id")
    stock_move_ids = fields.One2many(string="Stock Moves", help="Stock Movements of the current location", comodel_name="stock.move.ept", inverse_name="stock_inventory_id")

    def start_inventory(self):
        pass

    def validate_inventory(self):
        pass

    def cancel_inventory(self):
        pass
