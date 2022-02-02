from odoo import models, fields, api
from odoo.exceptions import UserError


class Partner(models.Model):
    _name = "res.partner.ept"
    _description = "Res Partner"

    name = fields.Char(string="Name", help="Name of the partner")
    street1 = fields.Char(string="Street1", help="Street address of the partner")
    street2 = fields.Char(string="Street2", help="Address line 2 of the partner")
    country = fields.Many2one(string="Country", comodel_name="res.country.ept", help="Country where partner lives")
    state = fields.Many2one(string="State", comodel_name="res.state.ept", help="State where partner lives")
    city = fields.Many2one(string="City", comodel_name="res.city.ept", help="City where partner lives")
    zip_code = fields.Char(string="Zipcode", help="Zipcode of the partner's address")
    email = fields.Char(string="Email", help="Email address of the partner")
    mobile = fields.Char(string="Mobile", help="Mobile number of the partner")
    phone = fields.Char(string="Phone", help="Phone number of the partner")
    photo = fields.Image(string="Photo", help="Partner's Image")
    website = fields.Char(string="Website", help="Website of the partner")
    active = fields.Boolean(string="Active", help="Whether the partner is active or not", default=True)
    parent_id = fields.Many2one(string="Parent Partner", comodel_name="res.partner.ept", help="Parent Partner of the current partner")
    child_ids = fields.One2many(string="Child Partners", comodel_name="res.partner.ept", inverse_name="parent_id", help="Child partners of the current partner")
    address_type = fields.Selection(string="Address Type",
                                    help="Address type of the partner",
                                    selection=[('Invoice', 'Invoice'), ('Shipping', 'Shipping'), ('Contact', 'Contact')])

    def create_new_country(self):
        country = self.country
        new = country.create({'name': 'Germany', 'code': 'DE'})
        print(new)
        state = self.state.create({"name": "Berlin", "code": "BR", "country_id": new.id})
        print(state)

    def write(self, vals):
        print(self)
        print(vals)
        return super(Partner, self).write(vals)

    # def name_get(self):
    #     data = []
    #     for country in self.country:
    #         data.append((
    #             country.id,
    #             country.name + " - " + country.code
    #         ))
    #     return data

    def unlink(self):
        if self.child_ids:
            raise UserError("First Delete the children.")
        return super(Partner, self).unlink()
