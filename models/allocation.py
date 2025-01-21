from odoo import fields, models, api, _

class AllocationTeleCallersWizard(models.TransientModel):
    _name = 'allocation.tele_callers.wizard'
    _description = 'Allocation'

    # @api.onchange('assign_to')
    # def _onchange_leads_users(self):
    #     users = self.env.ref('custom_leads.group_lead_tele_callers').users
    #     lead_users = []
    #     for j in users:
    #         print(j.name, 'j')
    #         lead_users.append(j.id)
    #     domain = [('id', 'in', lead_users)]
    #     return {'domain': {'assign_to': domain}}

    assign_to = fields.Many2one('res.users', string='Telecaller')

    def action_add_assigned_user(self):
        print(self._context['parent_obj'], 'parent_obj')

        leads = self.env['leads.logic'].sudo().search([('id', '=', self._context['parent_obj'])])
        for rec in leads:
            print(rec, 'recccc')
            rec.sudo().write({
                'tele_caller_id': self.assign_to.id,
                # 'lead_quality': 'nil',
                # 'leads_assign': False,
                'assigned_date': fields.Datetime.now(),
                # 'over_due': False
            })
            rec.activity_schedule('custom_leads.mail_activity_lead_tasks', user_id= rec.tele_caller_id.id,
                                  note=f' You have been assigned new lead.')

    def action_add_assign_to_lead_owner(self):
        print(self._context['parent_obj'], 'parent_obj')

        leads = self.env['leads.logic'].sudo().search([('id', '=', self._context['parent_obj'])])
        for rec in leads:
            print(rec, 'recccc')
            rec.sudo().write({
                'lead_owner': self.assign_to.employee_id.id,
                # 'lead_quality': 'nil',
                # 'leads_assign': False,
                'assigned_date': fields.Datetime.now(),
                # 'over_due': False
            })
            rec.activity_schedule('custom_leads.mail_activity_lead_tasks', user_id=rec.lead_owner.user_id.id,
                                  note=f' You have been assigned new lead.')