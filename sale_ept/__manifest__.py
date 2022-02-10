{
    'name': 'sale_ept',
    'summary': 'Sale Ept',
    'description': """
        Requirement 4
    """,
    'depends': ['base', 'res_localization_ept'],
    'data': ['security/sale_ept_security.xml',
             'security/ir.model.access.csv',
             'views/product_category.xml',
             'views/product.xml',
             'views/uom_category.xml',
             'views/uom.xml',
             'views/partner.xml',
             'views/sale_order.xml',
             'views/crm_team.xml',
             'views/crm_lead.xml',
             'views/stock_warehouse.xml',
             'views/stock_location.xml',
             'views/stock_picking.xml',
             'views/purchase_order.xml',
             'views/stock_moves.xml',
             'views/stock_inventory.xml',
             'views/product_update_stock.xml'],
    'demo': ['data/ir_sequence_data.xml'],
    'installable': True,
    'application': True,
    'auto_install': False
}
