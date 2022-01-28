from odoo import models, fields


class Course(models.Model):
    _name = "course.ept"
    _description = "Course Ept"

    name = fields.Char(string="Name", help="Name of the Course")
    student_ids = fields.Many2many(comodel_name="student.ept", relation="student_course_rel", column1="course_id", column2="student_id", string="Students", help="Students enrolled in this Course!")
    