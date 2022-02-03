from odoo import models, fields, api


class Team(models.Model):
    _name = "crm.team.ept"
    _description = "CRM Team"

    name = fields.Char(string="Name", help="Name of the team")
    team_leader = fields.Many2one(comodel_name="res.users", string="Team Leader", help="Team Leader of the team")
