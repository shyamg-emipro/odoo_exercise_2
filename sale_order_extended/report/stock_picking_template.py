from odoo import models, fields


class StockPickingTemplate(models.AbstractModel):
    _name = "report.sale_order_extended.stock_picking_custom_template"

    def get_product_delivery_orders(self, obj, location_id=False):
        product_ids = obj.move_line_ids_without_package.product_id.ids
        products = self.env['product.product'].browse(product_ids)
        product_delivery_orders = {}
        for product in products:
            do_qty = {}
            deliver_orders = obj.filtered(lambda d: product.id in d.move_line_ids_without_package.product_id.ids)
            for do in deliver_orders:
                if location_id:
                    moves = do.move_line_ids_without_package.filtered(lambda move: move.product_id.id == product.id and move.location_id.id == location_id.id)
                else:
                    moves = do.move_line_ids_without_package.filtered(lambda move: move.product_id.id == product.id)
                total_qty = sum([move.product_uom_qty for move in moves])
                do_qty[do] = total_qty
            product_delivery_orders[(product, product.product_template_attribute_value_ids,)] = do_qty
        return product_delivery_orders

    def _get_report_values(self, docids, data=None):
        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('sale_order_extended.stock_picking_custom_template')
        # get the records selected for this rendering of the report
        obj = self.env['stock.picking'].browse(docids)
        product_do_qty = self.get_product_delivery_orders(obj)
        # return a custom rendering context
        return {
            'docs': obj,
            'doc_model': 'stock.picking',
            'doc_ids': docids,
            'product_do_qty': product_do_qty,
        }