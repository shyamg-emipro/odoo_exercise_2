from odoo import models, fields, api


class SalesBySalesperson(models.AbstractModel):
    _name = "report.sale_order_extended.report_sales_by_salesperson"
    _description = "Sales By Salesperson Report"

    def get_sale_orders_grouped_by_salesperson(self, salespersons, from_date, to_date):
        salesperson_ids = self.env['res.users'].browse(salespersons)
        salesperson_wise_orders = {}
        for person in salesperson_ids:
            domain = [('user_id', '=', person.id)]
            if from_date:
                domain.append(('date_order', '>=', from_date))
            if to_date:
                domain.append(('date_order', '<=', to_date))
            orders_of_person = self.env['sale.order'].search(domain)
            salesperson_wise_orders[person] = orders_of_person
        return salesperson_wise_orders

    def _get_report_values(self, docids, data=None):
        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('sale_order_extended.report_sales_by_salesperson')
        # get the records selected for this rendering of the report
        obj = self.env['sale.order'].browse(docids)
        grouped_sale_orders = self.get_sale_orders_grouped_by_salesperson(data.get('salesperson'), data.get('from_date'), data.get('to_date'))
        # return a custom rendering context
        return {
            'docs': obj,
            'doc_model': 'sale.order',
            'doc_ids': docids,
            'self': self,
            'grouped_sale_orders': grouped_sale_orders,
            'from_date': data.get('from_date'),
            'to_date': data.get('to_date')
        }
