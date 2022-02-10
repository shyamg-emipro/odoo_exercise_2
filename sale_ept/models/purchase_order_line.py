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
    stock_move_ids = fields.One2many(string="Stock Moves", help="Stock Moves associated with this purchase order line.",
                                     comodel_name="stock.move.ept", inverse_name="purchase_line_id")
    delivered_qty = fields.Float(string="Delivered Quantity", help="Quantity that has been received form the vendor",
                                 compute="find_delivered_qty")
    cancelled_qty = fields.Float(string="Cancelled Quantity", help="Number of quantity that has been cancelled",
                                 compute="find_delivered_qty")

    def find_delivered_qty(self):
        for order in self:
            delivered = 0
            cancelled = 0
            for move in order.stock_move_ids:
                if move.state == "Done":
                    delivered += move.qty_done
                elif move.state == "Cancelled":
                    cancelled += move.qty_to_deliver
            order.delivered_qty = delivered
            order.cancelled_qty = cancelled

    @api.onchange('product_id')
    def generate_product_name(self):
        self.name = self.product_id.description
