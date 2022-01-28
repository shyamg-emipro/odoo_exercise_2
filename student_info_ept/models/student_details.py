from odoo import models, fields


class Student(models.Model):
    _name = "student.ept"
    _description = "Student Ept"

    name = fields.Char(string="Name", help="Name of the student")
    student_class = fields.Char(string="Class", help="Class in which student is studying")
    birthdate = fields.Date(string="Date of Birth", help="Birthdate of the student")
    course_ids = fields.Many2many(comodel_name="course.ept", relation="student_course_rel", column1="student_id", column2="course_id", string="Course", help="Courses that student have taken!")
