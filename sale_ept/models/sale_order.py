from odoo import models, fields


class SaleOrder(models.Model):
    _name = "sale.order.ept"
    _description = "Sale Order"

    order_no = fields.Char(string="Order No", help="Order Number", required=True)
    partner_id = fields.Many2one(string="Partner", comodel_name="res.partner.ept", help="Partner who placed this order")
    partner_invoice_id = fields.Many2one(string="Invoice Address", comodel_name="res.partner.ept", help="Partner who's address type is Invoice")
    partner_shipping_id = fields.Many2one(string="Shipping Address", comodel_name="res.partner.ept", help="Partner who's address type is Shipping")
    date = fields.Date(string="Date", help="Date at which the order is placed")
    order_lines = fields.One2many(string="Order Lines",
                                  help="Order Lines of the current order",
                                  comodel_name="sale.order.line.ept",
                                  inverse_name="order_no")
    salesperson = fields.Many2one(string="Sales Person", help="Sales person who negotiated this order", comodel_name="res.users")
    state = fields.Selection(string="State",
                             help="State of the order",
                             selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'), ('Cancelled', 'Cancelled')])
