from odoo import models, fields


class Country(models.Model):
    _name = "res.country.ept"
    _description = "Res Country Ept"

    name = fields.Char(string="Name", help="Name of the Country")
    code = fields.Char(string="Code", help="Country Short Code")
    state = fields.One2many(comodel_name="res.state.ept", inverse_name="country_id")

    def name_get(self):
        data = []
        for country in self:
            display_value = country.name + " - " + ("N/A" if not country.code else country.code)
            data.append((country.id, display_value))
        return data
