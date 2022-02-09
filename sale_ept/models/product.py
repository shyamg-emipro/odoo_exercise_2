from odoo import models, fields, api


class Product(models.Model):
    _name = "product.ept"
    _description = "Product"

    name = fields.Char(string="Name", required=True, help="Name of the Product")
    sku = fields.Char(string="SKU", required=True, help="Stock Keeping Unit of the Product")
    weight = fields.Float(string="Weight", help="Weight of the product", digits=(6, 2))
    length = fields.Float(string="Length", help="Length of the Product", digits=(6, 2))
    volume = fields.Float(string="Volume", help="Volume of the product", digits=(6, 2))
    width = fields.Float(string="Width", help="Width of the Product", digits=(6, 2))
    barcode = fields.Char(string="Barcode", help="Barcode of the product")
    product_type = fields.Selection(string="Type",
                                    help="Type of the product",
                                    selection=[('Storable', 'Storable'), ('Consumable', 'Consumable'), ('Service', 'Service')])
    sale_price = fields.Float(string="Sale Price",
                              help="Sale price of the Product",
                              digits=(8, 2),
                              default=1.00)
    cost_price = fields.Float(string="Cost Price",
                              help="Cost price of the Product",
                              digits=(8, 2),
                              default=1.00)
    category_id = fields.Many2one(string="Product Category",
                                  help="Category of the given Product",
                                  comodel_name="product.category.ept")
    uom_id = fields.Many2one(string="Unit Of Measures",
                             help="Product Unit of measure",
                             comodel_name="product.uom.ept")
    description = fields.Text(string="Description", help="Description about the product")
    product_stock = fields.Float(string="Stock", help="Available stock of the product", compute="calculate_stock", store=False, readonly=True)

    @api.depends('sku')
    def calculate_stock(self):
        stock_locations = self.env.context.get('location', False)
        if not stock_locations:
            stock_locations = self.env['stock.warehouse.ept'].search([]).stock_location_id

        for product in self:
            total_stock = 0
            stock_moves = self.env['stock.move.ept'].search([('product_id', '=', product.id)])

            for location in stock_locations:
                for move in stock_moves:
                    if move.destination_location_id == location:
                        total_stock += move.qty_done
                    elif move.source_location_id == location:
                        total_stock -= move.qty_done
            product.product_stock = total_stock
            # print(product.product_stock)

        # for product in self:
        #     product_move = self.env['stock.move.ept'].search([('product_id', '=', product.id)])
        #     total_stock = 0
        #     location = stock.env.context.get('location', False)
        #     if location:
        #         for move in product_move:
        #             if product.destination_location_id.id == location.id:
        #                 total_stock += product.qty_done
        #             elif product.source_location_id.id == location.id:
        #                 total_stock -= product.qty_done
        #         stock.product_stock = total_stock
        #     stock.product_stock = total_stock
