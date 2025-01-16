from odoo import fields,models,api, _

class LeadsSources(models.Model):
    _name = 'leads.sources'
    _inherit = 'mail.thread'
    _description = 'Leads Sources'

    name = fields.Char('Name', required=True)
    digital_lead = fields.Boolean('Digital Lead', default=False)