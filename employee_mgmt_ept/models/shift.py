from odoo import models, fields


class Shift(models.Model):
    _name = "employee.department.shift.ept"
    _description = "Employee Department Shift Ept"

    shift = fields.Selection(string="Shift",
                             help="Shift of the employee",
                             selection=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('Night', 'Night')])
    employees = fields.One2many(comodel_name="employee.ept", inverse_name="shift_id", string="Employee", help="Employees working in this shift")
    _rec_name = "shift"
