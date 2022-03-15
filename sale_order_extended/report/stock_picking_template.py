from odoo import models, fields


class StockPickingTemplate(models.AbstractModel):
    _name = "report.sale_order_extended.stock_picking_custom_template"

    def get_grouped_do(self, selected_delivery_orders, group_by_location=True):
        moves = selected_delivery_orders.move_line_ids_without_package
        grouped_products = {}
        for move in moves:
            grouped_do = {}
            location = ""
            if group_by_location:
                location = move.location_id.complete_name
            found_grouped_products = grouped_products.get(location, {})
            found_grouped_do = found_grouped_products.get((
                move.product_id, move.product_id.product_template_attribute_value_ids), {})
            product_qty = found_grouped_do.get(move.picking_id, 0)
            found_grouped_do.update({move.picking_id: product_qty + move.product_uom_qty})
            grouped_do[(move.product_id, move.product_id.product_template_attribute_value_ids)] = found_grouped_do
            found_grouped_products.update(grouped_do)
            grouped_products[location] = found_grouped_products
        if group_by_location:
            return grouped_products
        return grouped_products[location]

    def _get_report_values(self, docids, data=None):
        # get the report action back as we will need its data
        report = self.env[
            'ir.actions.report']._get_report_from_name('sale_order_extended.stock_picking_custom_template')
        # get the records selected for this rendering of the report
        obj = self.env['stock.picking'].browse(docids)
        # return a custom rendering context
        return {
            'docs': obj,
            'doc_model': 'stock.picking',
            'doc_ids': docids,
            'self': self
        }
