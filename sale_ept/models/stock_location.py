from odoo import models, fields, api


class StockLocation(models.Model):
    _name = "stock.location.ept"
    _description = "Stock Locations"

    name = fields.Char(string="Name", help="Name of the location", required=True)
    parent_id = fields.Many2one(string="Parent Location", help="Parent location of the stock",
                                comodel_name="stock.location.ept")
    location_type = fields.Selection(string="Type",
                                     help="Type of the Stock Location",
                                     selection=[('Vendor', 'Vendor'),
                                                ('Customer', 'Customer'),
                                                ('Internal', 'Internal'),
                                                ('Inventory Loss', 'Inventory Loss'),
                                                ('Production', 'Production'),
                                                ('Transit', 'Transit'),
                                                ('View', 'View')])
    is_scrap_location = fields.Boolean(string="Is Scrap Location", help="Specifies whether the location is scrap location or not")

    def name_get(self):
        result = []
        for location in self:
            name = location.name + " - " + location.location_type
            result.append((location.id, name))
        return result
