from odoo import models, fields, exceptions, api


class MergeOrders(models.TransientModel):
    _name = "sale.order.merge"
    _description = "Merge Sale Order"

    merge_options = fields.Selection(   # Options shown to user
        string="Options",
        selection=[
            ('1', 'Create new and cancel other'),
            ('2', 'Create new and delete other'),
            ('3', 'Merge into existing and cancel other'),
            ('4', 'Merge into existing and delete other')
        ])
    merge_into = fields.Many2one(   # Order in which user want to Merge
        comodel_name="sale.order",
        string="Merge Into",
        help="Sale Order in which other sale order is going to be merged",
        domain=lambda self: [('id', 'in', self._context.get('active_ids'))]
    )

    @api.model
    def default_get(self, fields):
        return super(MergeOrders, self).default_get(fields)

    def merge_sale_order(self):
        """
            This method perform operation on buttons click of the wizard.
            - gets the selected orders and verifies that they are all in draft state and must be from same customer
            - if selected option (merge_option) is from 1 or 2 (create new order) it creates new order
                - and adds order line of all selected order in newly created order.
            - else:
                - merge order in specified order (merge_into) and
                    - adds order line of all selected order in specified order(merge_into)
            it cancel other order if option 1 or 3 is selected
            it deletes other orders if option 2 or 4 is selected
        """
        active_ids = self.env['sale.order'].browse(self._context.get('active_ids'))
        # Raises Error if all selected orders are not from same customer or state is not  in draft
        if not all(active_ids[0].partner_id == order.partner_id and order.state == 'draft' for order in active_ids):
            raise exceptions.UserError("All sale order must be in draft state and must be from the same customer!")

        if self.merge_options in ['1', '2']:
            new_order = self.env['sale.order'].new({'partner_id': active_ids[0].partner_id})
            new_order.onchange_partner_id()

            order_lines = active_ids.order_line.get_order_lines()   # gets the prepared order lines from the method of sale.order.line
            # creates a sale order with order lines of all selected orders
            new_order.create({
                'pricelist_id': new_order.pricelist_id.id,
                'payment_term_id': new_order.payment_term_id.id,
                'partner_id': new_order.partner_id.id,
                'partner_invoice_id': new_order.partner_invoice_id.id,
                'partner_shipping_id': new_order.partner_shipping_id.id,
                'team_id': new_order.team_id.id,
                'order_line': order_lines
            })

            # cancel selected order if option is 1 else delete
            if self.merge_options == '1':
                active_ids.action_cancel()
            else:
                active_ids.unlink()

        if self.merge_options in ['3', '4']:
            # gets prepared order lines from the method of sale.order.line
            order_lines = active_ids.order_line.get_order_lines()
            # deletes existing order line in specified sale order (merge_into)
            self.merge_into.order_line.unlink()

            # adds (write) prepared order lines into specified sale order
            self.merge_into.write({
                'order_line': order_lines
            })

            active_ids -= self.merge_into   # removes specified order from list of selected order

            # cancel other order if options is 3 else delete
            if self.merge_options == '3':
                active_ids.action_cancel()
            else:
                active_ids.unlink()
