from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _name = "sale.order.line.ept"
    _description = "Sale Order Line"

    order_id = fields.Many2one(string="Order No", comodel_name="sale.order.ept", help="Order number of the order line")
    product_id = fields.Many2one(string="Product", comodel_name="product.ept", help="Product that is bought")
    name = fields.Text(string="Description", help="Description about the product")
    quantity = fields.Float(string="Quantity", help="Quantity of the Product", digits=(6, 2))
    unit_price = fields.Float(string="Unit Price", help="Unit price of the product", digits=(6, 2))
    state = fields.Selection(string="State", help="State of the order line",
                             selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'), ('Cancelled', 'Cancelled')],
                             default="Draft")
    uom_id = fields.Many2one(string="UOM", help="Unit of measure of the product",
                             comodel_name="product.uom.ept")
    subtotal_without_tax = fields.Float(string="Subtotal", help="Sub total of the order line",
                                        compute="calculate_subtotal", store=True)
    stock_move_ids = fields.One2many(string="Stock Moves", help="Stock Moves associated with this sale order line.",
                                     comodel_name="stock.move.ept", inverse_name="sale_line_id")
    delivered_qty = fields.Float(string="Delivered Quantity", help="Quantity that has been delivered to the customer",
                                 compute="find_delivered_qty")
    cancelled_qty = fields.Float(string="Cancelled Quantity", help="Number of quantity that has been cancelled",
                                 compute="find_delivered_qty")
    warehouse_id = fields.Many2one(string="Warehouse",
                                   help="Warehouse from which product is going to be delivered to the customer",
                                   comodel_name="stock.warehouse.ept")
    tax_ids = fields.Many2many(string="Customer Taxes", help="Taxes that are applicable on this product",
                               comodel_name="account.tax.ept", domain=[('tax_use', '=', 'Sales')])
    subtotal_with_tax = fields.Float(string="Subtotal (Tax included)", help="Subtotal of the purchase product with tax",
                                     digits=(6, 2), compute="calculate_subtotal_with_tax", store=True)

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
    def onchange_product_id(self):
        self.quantity = 1
        self.unit_price = self.product_id.sale_price
        self.uom_id = self.product_id.uom_id.id
        self.tax_ids = self.product_id.tax_ids
        if not self.product_id.description:
            self.name = self.product_id.name
        else:
            self.name = self.product_id.description

    @api.depends('quantity', 'unit_price')
    def calculate_subtotal(self):
        for line in self:
            line.subtotal_without_tax = line.quantity * line.unit_price

    @api.depends('quantity', 'unit_price', 'tax_ids', 'product_id')
    def calculate_subtotal_with_tax(self):
        for line in self:
            total_tax = 0
            for tax in line.tax_ids:
                if tax.tax_amount_type == "Percentage":
                    total_tax += tax.tax_value * line.subtotal_without_tax / 100
                else:
                    total_tax += tax.tax_value
            line.subtotal_with_tax = line.subtotal_without_tax + total_tax
