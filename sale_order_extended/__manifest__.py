{
    'name': 'sale_order_extended',
    'summary': 'Sale Order Extended',
    'description': """
        Requirement 15
    """,
    'depends': ['base', 'sale_crm', 'product'],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'views/sale_order.xml',
             'data/crm_tags.xml',
             'views/product_product.xml',
             'views/sale_order_line.xml',
             'wizard/merge_order.xml',
             'views/res_config_settings.xml',
             'report/saleorder_report.xml',
             'report/saleorder_template.xml',
             'report/stock_picking_template.xml',
             'report/stock_picking_views_ext.xml',
             'wizard/sales_by_salesperson.xml',
             'report/sales_by_salesperson_template.xml'
             ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto-install': False
}
