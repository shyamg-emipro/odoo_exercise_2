from odoo import models, fields, api, http
from odoo.http import request


class SalesBySalesperson(models.TransientModel):
    _name="sales.by.salesperson"
    _description = "Sales By Sales Person"

    from_date = fields.Datetime(string="From Date", help="Starting date of the the sales analysis")
    to_date = fields.Datetime(string="To Date", help="Ending date of the sales analysis")
    salesperson = fields.Many2many(comodel_name="res.users", string="Salespersons", help="Select salesperson for which you want to perform the sales analysis.")

    def get_sales_analysis_report(self):
        # report = request.env['ir.actions.report']._get_report_from_name('sale_order_extended.report_sales_by_salesperson')
        # context = dict(request.env.context)
        # pdf = report._render_qweb_pdf(self._context.get('active_ids'), data={'from_date': self.from_date, 'to_date': self.to_date, 'salesperson': self.salesperson.ids})
        # pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        # return http.HttpRequest.make_response(http.HttpRequest, pdf, headers=pdfhttpheaders)
        action = self.env['ir.actions.actions']._for_xml_id('sale_order_extended.action_sale_order_extended_sales_by_salesperson')
        action['data'] = {'from_date': self.from_date, 'to_date': self.to_date, 'salesperson': self.salesperson.ids}
        return action

        # return http.request.env['ir.ui.view'].render_template("sale_order_extended.report_sales_by_salesperson", {'data': {'from_date': self.from_date, 'to_date': self.to_date, 'salesperson': self.salesperson}})