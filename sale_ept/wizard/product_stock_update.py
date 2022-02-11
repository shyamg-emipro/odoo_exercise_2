from odoo import models, fields, api


class StockUpdate(models.TransientModel):
    _name = "product.stock.update.ept"
    _description = "Product Stock Update"

    location_id = fields.Many2one(string="Location", help="Location where we want to update the stock",
                                  comodel_name="stock.location.ept")
    available_stock = fields.Float(string="System Quantity", help="Quantity available according to system")
    counted_qty = fields.Float(string="Counted Quantity", help="Enter stock quantity that you have counted")
    difference_qty = fields.Float(string="Difference", help="Difference in System and counted quantity", compute="find_difference")

    @api.onchange('location_id')
    def find_product_stock(self):
        current_product = self.env['product.ept'].browse(self.env.context['active_ids'][0])
        self.available_stock = current_product.with_context(location=self.location_id).product_stock

    @api.depends('counted_qty')
    def find_difference(self):
        for product_stock in self:
            product_stock.difference_qty = product_stock.counted_qty - product_stock.available_stock

    def update_stock(self):
        product = self.env['product.ept'].browse(self.env.context['active_ids'][0])
        inventory = self.env['stock.inventory.ept'].create({
            'name': 'Update Stock of ' + product.name,
            'location_id': self.location_id.id
        })
        self.env['stock.inventory.line.ept'].create({
            'inventory_id': inventory.id,
            'product_id': product.id,
            'available_qty': self.available_stock,
            'counted_product_qty': self.counted_qty
        })
        inventory.validate_inventory()
