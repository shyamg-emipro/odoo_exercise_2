from odoo import models, fields


class Department(models.Model):
    _name = "employee.department.ept"
    _description = "Employee Department Ept"

    name = fields.Char(string="Name", help="Name of the department", required=True)
    employees = fields.One2many(comodel_name="employee.ept", inverse_name="department_id", string="Employees", help="Employees in the department")
    manager_id = fields.Many2one(comodel_name="res.users", string="Manager", help="User of manager for current department")
