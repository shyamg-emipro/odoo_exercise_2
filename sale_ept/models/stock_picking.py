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

    def create(self, vals):
        if not vals.get('name', False):
            if vals.get('transaction_type', False) == 'In':
                vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code="incoming.shipment.ept") or False
            elif vals.get('transaction_type', False) == 'Out':
                vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code="delivery.order.ept") or False
        return super(StockPicking, self).create(vals)

    def validate(self):
        for move in self.move_ids:
            if not move.state == "Done":
                raise exceptions.UserError("First make sure that Product quantities is Delivered or Received")
                return False
        if self.transaction_type == "In":
            self.purchase_order_id.done_purchase_order()
        else:
            self.sale_order_id.done_sale_order()
        self.state = "Done"

    def cancel_order(self):
        self.state = "Cancelled"
