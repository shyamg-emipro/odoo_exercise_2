from odoo import models, fields, api, exceptions


class StockPicking(models.Model):
    _name = "stock.picking.ept"
    _description = "Stock Picking"

    name = fields.Char(string="Name", help="Stock Picking unique identifier", readonly=True)
    partner_id = fields.Many2one(string="Partner", help="Partner for which stock picking is generated",
                                 comodel_name="res.partner.ept")
    state = fields.Selection(string="State", help="state of the Stock Picking",
                             selection=[('Draft', 'Draft'),
                                        ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')],
                             default="Draft")
    sale_order_id = fields.Many2one(string="Sale Order", help="It shows that Sale Order is  confirmed",
                                    comodel_name="sale.order.ept")
    purchase_order_id = fields.Many2one(string="Purchase Order", help="It shows that Purchase Order is confirmed",
                                        comodel_name="purchase.order.ept")
    transaction_type = fields.Selection(string="Transaction Type", help="Specify the type of the transaction that is going to be performed",
                                        selection=[('In', 'In'), ('Out', 'Out')])
    move_ids = fields.One2many(string="Stock Moves", help="Specify the movement of stock",
                               comodel_name="stock.move.ept", inverse_name="picking_id")
    transaction_date = fields.Date(string="Date", help="Date of the transaction",
                                   default=fields.Datetime.today())
    back_order_id = fields.Many2one(string="Back Order", help="Parent Picking", comodel_name="stock.picking.ept")

    def create(self, vals):
        if not vals.get('name', False):
            if vals.get('transaction_type', False) == 'In':
                vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code="incoming.shipment.ept") or False
            elif vals.get('transaction_type', False) == 'Out':
                vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code="delivery.order.ept") or False
        return super(StockPicking, self).create(vals)

    def validate(self):
        new_moves = []
        all_done_move = []
        for move in self.move_ids:
            if not move.qty_to_deliver == move.qty_done:
                if move.qty_done != 0:
                    move.create({
                        'name': move.name,
                        'product_id': move.product_id.id,
                        'uom_id': move.uom_id.id,
                        'source_location_id': move.source_location_id.id,
                        'destination_location_id': move.destination_location_id.id,
                        'qty_to_deliver': move.qty_to_deliver - move.qty_done,
                        'sale_line_id': move.sale_line_id.id or False,
                        'purchase_line_id': move.purchase_line_id.id or False,
                        'picking_id': move.picking_id.id
                    })
                    move.state = "Done"
                    move.qty_to_deliver = move.qty_done
                    new_moves.append(move)
            else:
                move.state = "Done"
                move.qty_to_deliver = move.qty_done
                all_done_move.append(move)

        if new_moves:
            new_moves += all_done_move
            new_order = self.create({
                'partner_id': self.partner_id.id,
                'sale_order_id': self.sale_order_id.id or False,
                'purchase_order_id': self.purchase_order_id.id or False,
                'transaction_type': self.transaction_type,
                'state': "Done"
            })
            for new_move in new_moves:
                new_move.picking_id = new_order.id
            self.back_order_id = new_order.id
        else:
            if all_done_move:
                self.state = "Done"
                if self.transaction_type == "Out":
                    self.sale_order_id.done_sale_order()
                else:
                    self.purchase_order_id.done_purchase_order()
            else:
                raise exceptions.UserError("You have to deliver at least 1 product to validate!")

    def cancel_order(self):
        for move in self.move_ids:
            move.state = "Cancelled"
        self.state = "Cancelled"
