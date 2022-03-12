from odoo import models, fields, api


class SaleOrderLineExtended(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    new_warehouse_id = fields.Many2one(comodel_name="stock.warehouse", string="Warehouse")
    parent_id = fields.Many2one(comodel_name="sale.order.line", string="Parent Line", help="Parent Order Line of the current order line")
    cost_price = fields.Float(string="Cost", compute="_get_cost_price", store=True)
    margin = fields.Float(string="Profit", help="Margin on this product", compute="_calculate_margin")
    margin_in_percentage = fields.Float(string="Profit Percentage", help="Shows margin on this product in percentage", compute="_calculate_margin")

    # def create(self, vals):
    #     for item in vals:
    #         item['cost_price'] = self.env['product.product'].browse(item['product_id']).standard_price
    #     return super(SaleOrderLineExtended, self).create(vals)

    @api.depends('price_unit')
    def _get_cost_price(self):
        for line in self:
            line.write({'cost_price': line.product_id.standard_price})

    def unlink(self):
        for line in self:
            child = self.env['sale.order.line'].search([('parent_id', '=', line.id)], limit=1)
            if child:
                child.unlink()
        return super(SaleOrderLineExtended, self).unlink()

    def _calculate_margin(self):
        for line in self:
            margin = 0
            margin_percentage = 0
            margin = line.price_subtotal - line.cost_price * line.product_uom_qty
            if margin > 0:
                margin_percentage = margin * 100 / line.price_subtotal
            elif margin == 0:
                margin_percentage = 0
            else:
                if line.cost_price <= 0:
                    margin_percentage = -100
                else:
                    margin_percentage = margin * 100 / (line.cost_price * line.product_uom_qty)
            line.margin = margin
            line.margin_in_percentage = margin_percentage

    def _prepare_procurement_values(self, group_id=False):
        procurement_values = super(SaleOrderLineExtended, self)._prepare_procurement_values(group_id)
        if self.new_warehouse_id:
            procurement_values['warehouse_id'] = self.new_warehouse_id
        return procurement_values

    # def find_unique_products(self):
    #
    #     return products

    def get_order_lines(self):
        """
            This method groups sale order line based on product id, price  and taxes
            It does this by creating a dictionary with key as a tuple: (product id, price, taxes)
            and value as a (0, 0, {order line data}) triplet.
             Ex:
                  {(24, 900, tax_id(3,4)): (0, 0, {
                         'product_id': 45,
                         'product_template_id': 12,
                         'name': 'Book Self',
                         'product_uom_qty': 2,
                         'tax_id': tax_id(3,4)
                       }), (): (), ...
                  }

            returns: values of prepared dictionary in list (list of tuple)
             Ex:
               [
                    (0, 0, {
                            'product_id': 45,
                            'product_template_id': 12,
                            'name': 'Book Self',
                            'product_uom_qty': 2,
                            'tax_id': tax_id(3,4)
                            }
                    ),
                    (),
                    ...
               ]
        """
        order_lines = {}
        for line in self:
            new_line = self.env['sale.order.line'].new({'product_id': line.product_id.id})
            new_line.product_id_change()
            # line below gets the value of (product id, price, taxes) for the current line
            # from the order_lines dictionary if found then returns value else returns (0, 0, {})
            found_similar = order_lines.get((line.product_id.id, line.price_unit, line.tax_id), (0, 0, {}))
            # line below gets the 3rd element from the found_similar tuple
            product_qty = found_similar[2].get('product_uom_qty', 0)
            order_lines[(line.product_id.id, line.price_unit, line.tax_id)] = (0, 0, {
                'product_id': line.product_id.id,
                'product_template_id': new_line.product_template_id.id,
                'name': new_line.name,
                'product_uom_qty': product_qty + line.product_uom_qty,  # Adds the line product qty to value of the current key
                'tax_id': line.tax_id
            })
        return list(order_lines.values())
