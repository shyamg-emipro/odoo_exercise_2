from odoo import models, fields, api, exceptions


class State(models.Model):
    _name = "res.state.ept"
    _description = "Res State Ept"

    name = fields.Char(string="Name", help="Name of the state")
    code = fields.Char(string="Code", help="State Short Code")
    country_id = fields.Many2one(comodel_name="res.country.ept", string="Country", help="get Countries")
    cities = fields.One2many(comodel_name="res.city.ept", inverse_name="state_id", string="City", help="get Cities")

    # Code Below is used to understand the Odoo ORM Methods
    # @api.model
    # def create(self, vals):
    #     # vals['country_id'] = 1
    #     if not vals.get('code', False):
    #         vals.update({'code': ' - '})
    #     new = super(State, self).create(vals)
    #     self.env['res.city.ept'].create({"name": new.name, "state_id": new.id})
    #     return new

    @api.constrains('code')
    def check_code_is_unique(self):
        if self.search([('code', '=', self.code), ('id', '!=', self.id)]):
            raise exceptions.ValidationError("Country code must be unique!")