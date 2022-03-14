from odoo import models, fields


class StockPickingTemplate(models.AbstractModel):
    _name = "report.sale_order_extended.stock_picking_custom_template_2"

    def get_products_do_by_location(self):
        pass

    def _get_report_values(self, docids, data=None):
        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('sale_order_extended.stock_picking_custom_template')
        # get the records selected for this rendering of the report
        obj = self.env['stock.picking'].browse(docids)
        # return a custom rendering context
        return {
            'docs': obj,
            'doc_model': 'stock.picking',
            'doc_ids': docids,
            'self': self
        }