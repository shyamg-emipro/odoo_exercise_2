from odoo import models, fields


class Leave(models.Model):
    _name = "employee.leave.ept"
    _description = "Employee Leave Ept"

    employee_id = fields.Many2one(comodel_name="employee.ept", string="Employee", help="Employee whose leave is")
    department_id = fields.Many2one(comodel_name="employee.department.ept", related="employee_id.department_id", readonly=True, string="Department", help="Department in which employee is working")
    start_date = fields.Date(string="Start Date", help="Date at which leave starts")
    end_date = fields.Date(string="End Date", help="Date at which leave ends")
    status = fields.Selection(string="Status",
                              help="Status of the leave",
                              selection=[('Draft', 'Draft'), ('Approved', 'Approved'), ('Refused', 'Refused'), ('Cancelled', 'Cancelled')],
                              default="Draft")
    description = fields.Char(string="Description", help="Description of the leave reason", required=True)