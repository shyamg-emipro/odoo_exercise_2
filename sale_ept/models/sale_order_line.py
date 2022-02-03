from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _name = "sale.order.line.ept"
    _description = "Sale Order Line"

    order_no = fields.Many2one(string="Order No", comodel_name="sale.order.ept", help="Order number of the order line")
    product_id = fields.Many2one(string="Product", comodel_name="product.ept", help="Product that is bought")
    name = fields.Text(string="Description", help="Description about the product")
    quantity = fields.Float(string="Quantity", help="Quantity of the Product", digits=(6, 2))
    unit_price = fields.Float(string="Unit Price", help="Unit price of the product", digits=(6, 2))
    state = fields.Selection(string="State", help="State of the order line",
                             selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])
    uom_id = fields.Many2one(string="UOM", help="Unit of measure of the product",
                             comodel_name="product.uom.ept")
    subtotal_without_tax = fields.Float(string="Sub Total", help="Sub total of the order line",
                                        compute="calculate_subtotal", store=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.quantity = 1
        self.unit_price = self.product_id.sale_price

    @api.depends('quantity', 'unit_price')
    def calculate_subtotal(self):
        for line in self:
            line.subtotal_without_tax = line.quantity * line.unit_price
