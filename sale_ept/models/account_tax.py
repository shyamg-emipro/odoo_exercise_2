from odoo import models, fields, api


class AccountTax(models.Model):
    _name = "account.tax.ept"
    _description = "Account Tax Ept"

    name = fields.Char(string="Name", help="Name of the Tax")
    tax_use = fields.Selection(string="Tax Use",
                               help="Where the given tax is going to be applied",
                               selection=[('None', 'None'), ('Sales', 'Sales'), ('Purchase', 'Purchase')],
                               default="None")
    tax_value = fields.Float(string="Amount", help="Amount of tax")
    tax_amount_type = fields.Selection(string="Amount Type", help="Type of the tax amount",
                                       selection=[('Percentage', 'Percentage'), ('Fixed', 'Fixed')],
                                       default="Percentage")
