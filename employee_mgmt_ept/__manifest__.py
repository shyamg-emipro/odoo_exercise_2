{
    'name': 'employee_mgmt_ept',
    'summary': 'Employee Management Ept',
    'description': """
        Requirement 3
    """,
    'depends': ['base'],
    'data': ['security/employee_mgmt_security.xml', 'security/ir.model.access.csv', 'views/department.xml', 'views/shift.xml', 'views/employee.xml', 'views/leave.xml'],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}

