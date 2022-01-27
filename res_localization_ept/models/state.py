from odoo import models, fields


class State(models.Model):
    _name = "res.state.ept"
    _description = "Res State Ept"

    name = fields.Char(string="Name", help="Name of the state")
    code = fields.Char(string="Code", help="State Short Code")
    country_id = fields.Many2one(comodel_name="res.country.ept", string="Country", help="get Countries")
    cities = fields.One2many(comodel_name="res.city.ept", inverse_name="state_id", string="City", help="get Cities")
