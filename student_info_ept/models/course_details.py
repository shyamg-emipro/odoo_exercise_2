from odoo import models, fields


class Course(models.Model):
    _name = "course.ept"
    _description = "Course Ept"

    name = fields.Char(string="Name", help="Name of the Course")
    students = fields.Many2many(comodel_name="student.ept")
    