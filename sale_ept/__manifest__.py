{
    'name': 'sale_ept',
    'summary': 'Sale Ept',
    'description': """
        Requirement 4
    """,
    'depends': ['base', 'res_localization_ept'],
    'data': ['security/sale_ept_security.xml', 'security/ir.model.access.csv', 'views/product_category.xml', 'views/product.xml', 'views/uom_category.xml', 'views/uom.xml', 'views/partner.xml', 'views/sale_order.xml'],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
