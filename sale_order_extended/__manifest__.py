{
    'name': 'sale_order_extended',
    'summary': 'Sale Order Extended',
    'description': """
        Requirement 15
    """,
    'depends': ['base', 'sale_crm', 'product'],
    'data': ['views/sale_order.xml', 'data/crm_tags.xml', 'views/product_product.xml', 'views/sale_order_line.xml',
             'wizard/merge_order.xml'],
    'demo': [],
    'installable': True,
    'application': True,
    'auto-install': False
}
