from odoo import models, fields, api


class StockWarehouse(models.Model):
    _name = "stock.warehouse.ept"
    _description = "Stock Warehouse"

    name = fields.Char(string="Name", help="Name of the warehouse", required=True)
    short_code = fields.Char(string="Short Code", help="Short code fro the warehouse", required=True)
    address_id = fields.Many2one(string="Address", help="Address of the warehouse", comodel_name="res.partner.ept")
    stock_location_id = fields.Many2one(string="Stock Location", help="Location of the Stock",
                                        comodel_name="stock.location.ept",
                                        domain="[('location_type', '=', 'Internal')]")
    view_location_id = fields.Many2one(string="View Location", help="View Location of the Stock",
                                       comodel_name="stock.location.ept",
                                       domain="[('location_type', '=', 'View')]")
