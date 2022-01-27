from odoo import models,fields


class City(models.Model):
    _name = "res.city.ept"
    _description = "Res City Ept"

    name = fields.Char(string="Name", help="Name of the city")
    state_id = fields.Many2one(comodel_name="res.state.ept", string="State")
