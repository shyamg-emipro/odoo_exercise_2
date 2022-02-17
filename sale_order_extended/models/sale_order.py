from odoo import models, fields


class SaleOrderExtended(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    lead_id = fields.Many2one(string="Lead", help="Lead from which current sale order is generated",
                              comodel_name="crm.lead")

    def action_confirm(self):
        product = self.env.ref("sale_order_extended.crm_tags_product_product_extended")
        order_line = self.env["sale.order.line"].new({'product_id': product.id})
        order_line.product_id_change()
        self.order_line .create({
            'order_id': self.id,
            'product_id': product.id,
            'name': order_line.name,
            'price_unit': order_line.price_unit
        })
        return super(SaleOrderExtended, self).action_confirm()

    def add_deposit(self):
        for line in self.order_line:
            product = line.product_id
            if product.deposit_product_id:
                child = self.order_line.filtered(lambda ol: line.id == ol.parent_id.id)
                if child:
                    child[0].product_uom_qty = product.deposit_product_qty * line.product_uom_qty
                    child[0].price_unit = product.deposit_product_id.list_price
                else:
                    deposit_product = product.deposit_product_id
                    new_line = line.new({'product_id': deposit_product.id})
                    new_line.product_id_change()
                    new_line.product_uom_qty = product.deposit_product_qty * line.product_uom_qty
                    line.create({
                        'order_id': self.id,
                        'parent_id': line.id,
                        'product_id': deposit_product.id,
                        'name': new_line.name,
                        'price_unit': deposit_product.list_price,
                        'product_uom_qty': new_line.product_uom_qty

                    })

    def show_reserved_order_lines(self):
        products = self.order_line.product_id
        action = self.env['ir.actions.actions']._for_xml_id("sale_order_extended.action_sale_order_line_extended_window")
        action['domain'] = [('id', 'not in', self.order_line.ids), ('product_id', 'in', products.ids)]
        return action
