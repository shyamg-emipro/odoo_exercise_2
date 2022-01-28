from odoo import models, fields


class Employee(models.Model):
    _name = "employee.ept"
    _description = "Employee Ept"

    name = fields.Char(string="Name", help="Name of the Employee", required=True)
    department_id = fields.Many2one(comodel_name="employee.department.ept", required=True, string="Department", help="Department in which employee is working")
    shift_id = fields.Many2one(comodel_name="employee.department.shift.ept", required=True, string="Shift", help="Shift in which employee is working")
    job_position = fields.Char(string="Position", help="Position or Designation entitled to the employee")
    salary = fields.Float(string="Salary", help="Salary of the Employee")
    hire_date = fields.Date(string="Hiring Date", help="Date at which employee is hired")
    gender = fields.Selection(string="Gender",
                              help="Gender of the Employee",
                              selection=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')])
    job_type = fields.Selection(string="Job Type",
                                help="Type of the job",
                                selection=[('Permanent', 'Permanent'), ('Ad Hoc', 'Ad Hoc')])
    is_manager = fields.Boolean(string="Is Manager", help="Is current employee is Manager")
    manager_id = fields.Many2one(comodel_name="employee.ept", string="Manager", help="Manager of the group of employees")
    related_user = fields.Many2one(comodel_name="res.users", string="User", help="User of the employee")
    employees = fields.One2many(comodel_name="employee.ept", readonly=True, inverse_name="manager_id", string="Employees", help="Employees of current user manager")
    increment = fields.Float(string="Increment", help="Increment of the employee", digits=(4, 2))
