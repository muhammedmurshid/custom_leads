from odoo import fields, models, _, api

class StudentFormInherit(models.Model):
    _inherit = 'op.student'

    admission_officer_id = fields.Many2one('res.users', string="Admission Officer")
    branch_id = fields.Many2one('op.branch', string="Branch")
