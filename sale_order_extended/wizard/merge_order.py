from odoo import models, fields, exceptions


class MergeOrders(models.TransientModel):
    _name = "sale.order.merge"
    _description = "Merge Sale Order"

    merge_options = fields.Selection(
        string="Options",
        selection=[
            ('1', 'Create new and cancel other'),
            ('2', 'Create new and delete other'),
            ('3', 'Merge into existing and cancel other'),
            ('4', 'Merge into existing and delete other')
        ])
    merge_into = fields.Many2one(
        comodel_name="sale.order",
        string="Merge Into",
        help="Sale Order in which other sale order is going to be merged",
        domain=lambda self: [('id', 'in', self._context.get('active_ids'))]
    )

    def merge_sale_order(self):
        active_ids = self.env['sale.order'].browse(self._context.get('active_ids'))
        if not all(active_ids[0].partner_id==order.partner_id and order.state=='draft' for order in active_ids):
            raise exceptions.UserError("All sale order must be in draft state and must be from the same customer!")

        if self.merge_options in ['1', '2']:
            new_order = self.env['sale.order'].new({'partner_id': active_ids[0].partner_id})
            new_order.onchange_partner_id()

            order_lines = active_ids.order_line.get_order_lines()
            new_order.create({
                'pricelist_id': new_order.pricelist_id.id,
                'payment_term_id': new_order.payment_term_id.id,
                'partner_id': new_order.partner_id.id,
                'partner_invoice_id': new_order.partner_invoice_id.id,
                'partner_shipping_id': new_order.partner_shipping_id.id,
                'team_id': new_order.team_id.id,
                'order_line': order_lines
            })

            if self.merge_options=='1':
                for old_order in active_ids:
                    old_order.state = 'cancel'
            else:
                active_ids.unlink()

        if self.merge_options in ['3', '4']:
            order_lines = active_ids.order_line.get_order_lines()
            self.merge_into.order_line.unlink()

            self.merge_into.write({
                'order_line': order_lines
            })

            active_ids -= self.merge_into
            if self.merge_options=='3':
                for old_order in active_ids:
                    old_order.state = 'cancel'
            else:
                active_ids.unlink()
