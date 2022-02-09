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
        products = self.env['product.ept'].search([])
        for product in products:
            new_product = product.with_context({'location': self.location_id})
            new_product.calculate_stock()
            if new_product.product_stock != 0:
                self.inventory_line_ids.create({
                    'inventory_id': self.id,
                    'product_id': new_product.id,
                    'available_qty': new_product.product_stock,
                    'counted_product_qty': 0
                })
        self.state = "In-Progress"

    def validate_inventory(self):
        line_location = self.location_id
        inventory_location = self.env['stock.location.ept'].search([('location_type', '=', 'Inventory Loss')], limit=1)

        for line in self.inventory_line_ids:
            if line.difference < 0:
                destination_location = line_location
                source_location = inventory_location
            elif line.difference > 0:
                destination_location = inventory_location
                source_location = line_location
            else:
                continue

            values = {
                'name': line.product_id.name + ": " + source_location.name + " -> " + destination_location.name,
                'product_id': line.product_id.id,
                'uom_id': line.product_id.uom_id.id,
                'source_location_id': source_location.id,
                'destination_location_id': destination_location.id,
                'qty_to_deliver': abs(line.difference),
                'qty_done': abs(line.difference),
                'state': 'Done',
                'stock_inventory_id': self.id
            }
            self.env['stock.move.ept'].create(values)

        self.state = "Done"

    def cancel_inventory(self):
        self.state = "Cancelled"
