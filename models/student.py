from odoo import fields, models, _, api

class StudentFormInherit(models.Model):
    _inherit = 'op.student'

    admission_officer_id = fields.Many2one('res.users', string="Admission Officer")
    branch_id = fields.Many2one('op.branch', string="Branch")
    admission_date = fields.Date(string="Admission Date")


class MailFormInherit(models.Model):
    _inherit = 'mail.activity'

    lead_id = fields.Many2one('leads.logic', string="Lead")