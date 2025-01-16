from tokenize import String

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta

class LeadsForm(models.Model):
    _name = 'leads.logic'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Leads'
    _rec_name = 'name'
    _order = 'id desc'

    leads_source = fields.Many2one('leads.sources', string='Leads Source', required=True)
    name = fields.Char(string='Lead Name', required=True)
    email_address = fields.Char(string='Email Address')
    phone_number = fields.Char(string='Mobile Number', required=True)
    probability = fields.Float(string='Probability')
    admission_status = fields.Boolean(string='Admission', readonly=False)
    date_of_adding = fields.Date(string='Date of Adding', default=fields.Datetime.now)
    last_update_date = fields.Datetime(string='Last Updated Date')
    course_id = fields.Char(string='Course')
    reference_no = fields.Char("Reference", default=lambda self: _('New'),
                               copy=False, readonly=True, tracking=True)
    # touch_ids = fields.One2many('leads.own.touch.points', 'touch_id', string='Touch Points')
    lead_quality = fields.Selection(
        [('new', 'New'), ('waiting_for_admission', 'Waiting for Admission'), ('admission', 'Admission'), ('hot', 'Hot'),
         ('warm', 'Warm'), ('cold', 'Cold'),
         ('bad_lead', 'Bad Lead'), ('not_responding', 'Not Responding'), ('crash_lead', 'Crash Lead'),
         ('nil', 'Nil')],
        string='Lead Quality', default='new')
    lost_reason = fields.Text(string="Lost Reason")
    lead_status = fields.Selection(
        [('not_responding', 'Not Responding'),
         ('already_enrolled', 'Already Enrolled'), ('joined_in_another_institute', 'Joined in another institute'),
         ('nil', 'Nil')],
        string='Lead Status',
    )
    place = fields.Char('Place')
    # leads_assign = fields.Many2one('hr.employee', string='Assign to', )
    lead_owner = fields.Many2one('hr.employee', string='Lead Owner', default=lambda self: self.env.user.employee_id)
    seminar_lead_id = fields.Integer()
    admission_date = fields.Datetime(string="Admission Date")
    phone_number_second = fields.Char(string='Phone Number')
    branch_id = fields.Char(string="Branch")
    course_interested = fields.Char(string="Course Interested")
    academic_year_of_course_attend = fields.Selection([('2023-2024','2023-2024'), ('2024-2025','2024-2025'), ('2025-2026','2025-2026')], string="Academic Year of Course attended")
    batch_id = fields.Char(string="Batch")
    course_type = fields.Selection(
        [('indian', 'Indian'), ('international', 'International'), ('crash', 'Crash'), ('repeaters', 'Repeaters'),
         ('nil', 'Nil')],
        string='Course Type')
    state = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('deal', 'Deal'), ('qualified', 'Qualified'),
         ('lost', 'Lost')],
        string='State',
        default='new', tracking=True)
    last_studied_course = fields.Char(string='Last Studied Course')
    incoming_source = fields.Selection(
        [('social_media', 'Social Media'), ('google', 'Google'), ('hoardings', 'Hoardings'), ('tv_ads', 'TV Ads'),
         ('through friends', 'Through Friends'), ('whatsapp', 'WhatsApp'), ('other', 'Other')],
        string='How did you hear about us?')
    incoming_source_checking = fields.Boolean(string='Incoming Source Checking', )
    college_name = fields.Char(string='College/School')
    lead_referral_staff_id = fields.Many2one('res.users', string='Lead Referral Staff')
    referred_by = fields.Selection([('staff', 'Staff'), ('student', 'Student'), ('other', 'Other')],
                                   string='Referred By')
    # campaign_name = fields.Char(string='Campaign Name')
    campaign = fields.Selection(
        [('CA Weekend Thrissur', 'CA Weekend Thrissur'), ('CA Weekend Ernakulam', 'CA Weekend Ernakulam'),
         ('CA Weekend Trivandrum', 'CA Weekend Trivandrum'), ('CA Weekend Calicut', 'CA Weekend Calicut'),
         ('CA Weekend Perintalmanna', 'CA Weekend Perintalmanna')], string='Campaign')
    country = fields.Selection(
        [('india', 'India'), ('germany', 'Germany'), ('canada', 'Canada'), ('usa', 'USA'), ('australia', 'Australia'),
         ('italy', 'Italy'), ('france', 'France'), ('united_kingdom', 'United Kingdom'),
         ('saudi_arabia', 'Saudi Arabia'), ('ukraine', 'Ukraine'), ('united_arab_emirates', 'United Arab Emirates'),
         ('china', 'China'), ('japan', 'Japan'), ('singapore', 'Singapore'), ('indonesia', 'Indonesia'),
         ('russia', 'Russia'), ('oman', 'Oman'), ('nepal', 'Nepal'), ('japan', 'Japan')],
        string='Country', default='india')
    referred_by_id = fields.Many2one('hr.employee', string='Referred Person')
    referred_by_name = fields.Char(string='Referred Person')
    referred_by_number = fields.Char(string='Referred Person Number')
    batch_preference = fields.Char(string='Batch Preference')
    tele_caller_id = fields.Many2one('res.users', String="Tele Caller")

    lead_qualification = fields.Selection(
        [('plus_one_science', 'Plus One Science'), ('plus_two_science', 'Plus Two Science'),
         ('plus_two_commerce', 'Plus Two Commerce'), ('plus_one_commerce', 'Plus One Commerce'),
         ('commerce_degree', 'Commerce Degree'),
         ('other_degree', 'Other Degree'), ('working_professional', 'Working Professional')],
        string='Lead qualification')
    adm_id = fields.Integer(string='Admission Id')
    student_id = fields.Many2one('op.student', string='Student Id')

    district = fields.Selection([('wayanad', 'Wayanad'), ('ernakulam', 'Ernakulam'), ('kollam', 'Kollam'),
                                 ('thiruvananthapuram', 'Thiruvananthapuram'), ('kottayam', 'Kottayam'),
                                 ('kozhikode', 'Kozhikode'), ('palakkad', 'Palakkad'), ('kannur', 'Kannur'),
                                 ('alappuzha', 'Alappuzha'), ('malappuram', 'Malappuram'), ('kasaragod', 'Kasaragod'),
                                 ('thrissur', 'Thrissur'), ('idukki', 'Idukki'), ('pathanamthitta', 'Pathanamthitta'),
                                 ('abroad', 'Abroad'), ('other', 'Other'), ('nil', 'Nil')],
                                string='District', required=True)
    referred_teacher = fields.Many2one('res.users', string='Referred Teacher')
    over_due = fields.Boolean(string='Over Due')
    remarks = fields.Char(string='Remarks')
    parent_number = fields.Char('Parent Number')
    closing_date = fields.Date(string="Closing Date")
    amount = fields.Float(string="Amount")
    mode_of_study = fields.Selection([('online', 'Online'), ('offline', 'Offline'), ('nil', 'Nil')],
                                     string='Mode of Study',
                                     required=True)
    assigned_date = fields.Date(string='Assigned Date', readonly=1)
    platform = fields.Selection(
        [('facebook', 'Facebook'), ('instagram', 'Instagram'), ('website', 'Website'), ('just_dial', 'Just Dial'),
         ('other', 'Other')],
        string='Platform')
    current_status = fields.Selection([('new_lead', 'New Lead'), ('not_responding', 'Not Responding'), ('deal', 'Deal'), ('admission', 'Admission'), ('lost', 'Lost')], string="Current Status", default="new_lead")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the student model """
        for vals in vals_list:
            if vals.get('reference_no', _('New')) == _('New'):
                vals['reference_no'] = (self.env['ir.sequence'].
                                  next_by_code('leads.logic'))
        return super().create(vals_list)

    def act_attempt_to_connect(self):
        self.current_status = 'not_responding'
        self.state = 'in_progress'

    def act_connected(self):
        print('hi')
        return {'type': 'ir.actions.act_window',
                'name': _('Connect'),
                'res_model': 'connect.form',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_lead_id': self.id, 'default_task_owner_id': self.lead_owner.user_id.id}, }

    def act_not_connected(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Connect'),
                'res_model': 'not.connect.form',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_lead_id': self.id,}, }

    def act_lost_lead(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Lost'),
                'res_model': 'lost.lead.form',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_lead_id': self.id,}, }

    def act_convert(self):
        print('hi')
        return {'type': 'ir.actions.act_window',
                'name': _('Deal'),
                'res_model': 'convert.lead',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_lead_id': self.id, 'default_lead_owner_id': self.lead_owner.user_id.id }, }

    def act_admission(self):
        print()
        return {'type': 'ir.actions.act_window',
                'name': _('Admission'),
                'res_model': 'qualified.lead.form',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_lead_id': self.id}, }
