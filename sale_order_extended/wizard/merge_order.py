from odoo import models, fields


class MergeOrders(models.TransientModel):
    _name = "sale.order.merge"
    _description = "Merge Sale Order"

    merge_options = fields.Selection(string="Options",
                                     selection=[
                                         ('1', 'Create new and cancle other'),
                                         ('2', 'Create new and delete other'),
                                         ('3', 'Merge into existing and cancle other'),
                                         ('4', 'Merge into existing and delete other')
                                     ])
    merge_into = fields.Many2one(comodel_name="sale.order", string="Merge Into",
                                 help="Sale Order in which other sale order is going to be merged")