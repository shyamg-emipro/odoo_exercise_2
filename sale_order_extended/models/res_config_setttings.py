from odoo import models, fields, api


class SaleOrderExtendedSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_dummy_field_a = fields.Char(string="Dummy Field A", default_model="sale.order", default="Testing")
    dummy_field_b = fields.Char(string="Dummy Field B", config_parameter="sale.dummy_field_b")
    sale_extended_id = fields.Many2one(comodel_name="sale.order", string="Sale Order", config_parameter="sale.sale_id")
    dummy_field_c = fields.Many2one(related="sale_extended_id.partner_id", readonly=False)
    group_self_generated = fields.Boolean(string="Self generated Orders", implied_group='sale_order_extended.group_dummy_group')

    @api.onchange('dummy_field_b')
    def set_dummy_field_b(self):
        self.env['ir.config_parameter'].set_param('sale.dummy_field_b', 'Hello World!')

    # @api.onchange('sale_id')
    # def set_dummy_field_b(self):
    #     self.env['ir.config_parameter'].set_param('sale.sale_id', 1)
