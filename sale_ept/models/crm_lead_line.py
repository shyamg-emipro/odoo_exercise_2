from odoo import models, fields, api


class LeadLine(models.Model):
    _name = "crm.lead.line.ept"
    _description = "CRM Lead Line"

    name = fields.Char(string="Description", help="Description or name of the product")
    product_id = fields.Many2one(comodel_name="product.ept", string="Product", help="Product of the lead line")
    expected_sell_qty = fields.Float(string="Quantity", help="Expected sell quantity of the product")
    uom_id = fields.Many2one(comodel_name="product.uom.ept", string="UOM", help="Unit of Measure of the product")
    lead_id = fields.Many2one(comodel_name="crm.lead.ept", string="Lead", help="Lead of the current lead line")
