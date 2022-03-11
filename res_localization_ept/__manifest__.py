{
    'name': 'res.localization.ept',
    'summary': 'Res Localization Ept',
    'description': """
        Odoo Exercise 2
        Requirement 1
    """,
    'depends': ['base'],
    'data': [
        'security/localization_security.xml',
        'security/ir.model.access.csv',
        'views/country.xml',
        'views/states.xml',
        'views/city.xml',
        'report/localization_report.xml',
        'report/localization_template.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
