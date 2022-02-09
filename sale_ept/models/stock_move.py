from odoo import models, fields, api, exceptions


class StockMove(models.Model):
    _name = "stock.move.ept"
    _description = "Stock Moves"

    name = fields.Char(string="Description", help="Description about the stock move")
    product_id = fields.Many2one(string="Product", help="Product whose stock is going to move",
                                 comodel_name="product.ept")
    uom_id = fields.Many2one(string="UOM", help="Unit of Measure of the Product",
                             comodel_name="product.uom.ept")
    source_location_id = fields.Many2one(string="Source Location", help="Source Location of the stock move",
                                         comodel_name="stock.location.ept")
    destination_location_id = fields.Many2one(string="Destination Location", help="Destination Location of the stock move", comodel_name="stock.location.ept")
    qty_to_deliver = fields.Float(string="Demand", help="Demand of the Product", readonly=True, digits=(6, 2))
    qty_done = fields.Float(string="Done Quantities", help="Number of Quantities that has been done", digits=(6, 2))
    state = fields.Selection(string="State", help="State of the Stock Move",
                             selection=[('Draft', 'Draft'), ('Done', 'Done'), ('Cancelled', 'Cancelled')],
                             default="Draft")
    sale_line_id = fields.Many2one(string="Sale Order Line", help="Sale Order Line Move",
                                   comodel_name="sale.order.line.ept")
    purchase_line_id = fields.Many2one(string="Purchase Order Line", help="Purchase Order Line Move",
                                       comodel_name="purchase.order.line.ept")
    stock_inventory_id = fields.Many2one(string="Inventory", help="Inventory Movement",
                                         comodel_name="stock.inventory.ept")
    picking_id = fields.Many2one(string="Stock Picking", help="Stock Sale or Purchase Movement",
                                 comodel_name="stock.picking.ept")

    # Do not call ORM methods in onchange methods..
    # @api.onchange('qty_done')
    # def change_state(self):
    #     if self.qty_done == self.qty_to_deliver:
    #         self.state = "Done"
    #     elif self.qty_done > self.qty_to_deliver:
    #         raise exceptions.UserError("You are not allowed to enter quantity more then the actual Demand!")
