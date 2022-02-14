from odoo import models, fields


class SaleOrderExtended(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    lead_id = fields.Many2one(string="Lead", help="Lead from which current sale order is generated",
                              comodel_name="crm.lead")
