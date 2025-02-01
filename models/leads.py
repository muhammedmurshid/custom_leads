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

    leads_source = fields.Many2one('leads.sources', string='Leads Source')
    source_name = fields.Char(string="Source")
    name = fields.Char(string='Lead Name', )
    email_address = fields.Char(string='Email')
    phone_number = fields.Char(string='Mobile',)
    probability = fields.Float(string='Probability')
    admission_status = fields.Boolean(string='Admission', readonly=1)
    date_of_adding = fields.Date(string='Date of Adding', default=fields.Datetime.now, readonly=1)
    last_update_date = fields.Datetime(string='Last Updated Date')
    course_id = fields.Many2one('op.course',string='Course')
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
    crash_user_id = fields.Many2one('res.users', string="Crash User")
    lead_status = fields.Selection(
        [('not_responding', 'Not Responding'),
         ('already_enrolled', 'Already Enrolled'), ('joined_in_another_institute', 'Joined in another institute'),
         ('nil', 'Nil')],
        string='Lead Status',
    )
    place = fields.Char('Place')
    # leads_assign = fields.Many2one('hr.employee', string='Assign to', )
    lead_owner = fields.Many2one('hr.employee', string='Lead Owner', default=lambda self: self.env.user.employee_id.id)
    seminar_lead_id = fields.Integer()
    admission_date = fields.Datetime(string="Admission Date", readonly=1)
    phone_number_second = fields.Char(string='Phone Number')
    branch_id = fields.Many2one('op.branch', string="Branch")
    course_interested = fields.Char(string="Course Interested")
    academic_year_of_course_attend = fields.Selection([('2023-2024','2023-2024'), ('2024-2025','2024-2025'), ('2025-2026','2025-2026')], string="Academic Year of Course attended")
    course_type = fields.Selection(
        [('indian', 'Indian'), ('international', 'International'), ('crash', 'Crash'), ('repeaters', 'Repeaters'),
         ('nil', 'Nil')],
        string='Course Type')
    state = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('not_connected', 'Not Connected'), ('deal', 'Deal'), ('qualified', 'Qualified'),
         ('lost', 'Lost')],
        string='State',
        default='new', tracking=True)
    last_studied_course = fields.Char(string='Last Studied Course')
    incoming_source = fields.Selection(
        [('social_media', 'Social Media'), ('google', 'Google'), ('hoardings', 'Hoardings'), ('tv_ads', 'TV Ads'),
         ('through friends', 'Through Friends'), ('whatsapp', 'WhatsApp'), ('re_admission', 'Re-Admission'),('other', 'Other')],
        string='Incoming Calls / Walk In Source')
    incoming_source_checking = fields.Boolean(string='Incoming Source Checking', )
    academic_year = fields.Selection([('2024-2025', '2024-2025'), ('2025-2026', '2025-2026')], string="Academic Year")
    college_name = fields.Char(string='College/School')
    title = fields.Char(string="Title")
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
    booking_amount = fields.Float(string="Booking Amount")
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
                                     string='Mode of Study')
    assigned_date = fields.Date(string='Assigned Date', readonly=1)
    digital_lead = fields.Boolean(string="Digital Lead")
    digital_lead_source = fields.Selection([('just_dial', 'Just Dial'), ('youtube_google', 'Youtube - Google'), ('whatsapp_campaign', 'Whatsapp Campaign'), ('messenger', 'Messenger'), ('facebook', 'Facebook'), ('linkedin', 'Linkedin'), ('instagram', 'Instagram'), ('whatsapp_meta', 'Whatsapp Meta'), ('website', 'Website'), ('google', 'Google')], string="Digital Lead Source")
    platform = fields.Selection(
        [('facebook', 'Facebook'), ('instagram', 'Instagram'), ('website', 'Website'), ('just_dial', 'Just Dial'),
         ('other', 'Other')],
        string='Platform')
    expected_joining_date = fields.Date(string="Expected Joining Date")
    not_response_note = fields.Text(string="Not Respond Reason")
    current_status = fields.Selection([('new_lead', 'New Lead'), ('not_responding', 'Not Responding'), ('need_follow_up', 'Need Follow-Up'), ('deal', 'Deal'), ('admission', 'Admission'), ('lost', 'Lost')], string="Current Status", default="new_lead")
    call_response = fields.Text(string="Response")
    transitions = fields.Selection([('future_lead', 'Future Lead'), ('junk_lead', 'Junk Lead'), ('not_qualified', 'Not Qualified'), ('qualified', 'Qualified')], string="Transitions", tracking=1)
    # @api.model_create_multi
    # def create(self, vals_list):
    #     """ Create a sequence for the student model """
    #     for vals in vals_list:
    #         if vals.get('reference_no', _('New')) == _('New'):
    #             vals['reference_no'] = (self.env['ir.sequence'].
    #                               next_by_code('leads.logic'))
    #     return super().create(vals_list)

    @api.onchange('leads_source')
    def _onchange_leads_source(self):
        if self.leads_source:
            self.source_name = self.leads_source.name
            if 'incoming' in self.source_name.lower() or 'walk in' in self.source_name.lower():
                # Do something when 'incoming' is in the source name
                self.incoming_source_checking = True

            else:
                self.incoming_source_checking = 0
                self.incoming_source = False
            if self.leads_source.digital_lead == 1:
                self.digital_lead = 1
            else:
                self.digital_lead = 0
                self.digital_lead_source = False

    @api.onchange('lead_quality')
    def _onchange_leads_quality(self):
        if self.lead_quality:
            if self.lead_quality != 'crash_lead':
                self.crash_user_id = False

    @api.onchange('branch_id')
    def _onchange_branch(self):
        if self.branch_id:
            print(f"Branch ID: {self.branch_id.id}")
            domain = [('branch', '=', self.branch_id.id)]
            print(f"Domain applied: {domain}")
            return {
                'domain': {
                    'batch_id': domain,
                }
            }
        else:
            print("No branch selected")
            return {
                'domain': {
                    'batch_id': [],
                }
            }
    batch_id = fields.Many2one('op.batch', string="Batch", domain="[('branch', '=', branch_id)]")

    def act_call_back(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Connect'),
                'res_model': 'connect.form',
                'target': 'new',
                'view_mode': 'form',
                'context': {'default_lead_id': self.id, 'default_task_owner_id': self.lead_owner.user_id.id}, }

    @api.constrains('phone_number')
    def _check_duplicate_phone_number(self):
        for record in self:
            if record.phone_number:
                duplicate = self.search([('phone_number', '=', record.phone_number), ('id', '!=', record.id)])
                if duplicate:
                    raise ValidationError(
                        _('The phone number %s already exists. Please use a different number.') % record.phone_number)

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
                'context': {'default_lead_id': self.id, 'default_task_owner_id': self.lead_owner.user_id.id}, }

    def act_not_connected(self):
        act = self.env['mail.activity'].search([('res_model', '=', 'leads.logic')])
        for i in act:
            print(i.res_model, 'model')
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
        if self.batch_id and self.branch_id and self.course_id:
            return {'type': 'ir.actions.act_window',
                    'name': _('Deal'),
                    'res_model': 'convert.lead',
                    'target': 'new',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {'default_lead_id': self.id, 'default_lead_owner_id': self.lead_owner.user_id.id,  }, }
        else:
            raise UserError(_('Please ensure that Batch, Branch, and Course are selected before proceeding.'))

    def act_admission(self):
        print()
        if self.batch_id and self.branch_id and self.course_id:
            return {'type': 'ir.actions.act_window',
                    'name': _('Admission'),
                    'res_model': 'qualified.lead.form',
                    'target': 'new',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {'default_lead_id': self.id,
                                'default_batch_id': self.batch_id.id,
                                'default_course_id': self.course_id.id,
                                'default_branch_id': self.branch_id.id,
                                'default_mobile': self.phone_number,
                                'default_email': self.email_address},}
        else:
            raise UserError(_('Please ensure that Batch, Branch, and Course are selected before proceeding.'))

    def act_return_to_new_lead(self):
        self.state = 'new'

    @api.model
    def allocate_leads(self, lead_ids):
        # Fetch tele-callers who can handle leads
        tele_caller_group = self.env.ref('custom_leads.group_lead_tele_callers')
        if tele_caller_group:  # Update the module name
            tele_callers = self.env['res.users'].search([('groups_id', 'in', [tele_caller_group.id])])
        else:
            return []
        # Fetch lead users for inbound source
        lead_user_group = self.env.ref('custom_leads.group_lead_users')  # Update the module name
        if lead_user_group:
            lead_users = self.env['res.users'].search([('groups_id', 'in', [lead_user_group.id])])
        else:
            return []
        lead_objects = self.browse(lead_ids)
        if not tele_callers and not lead_users:
            raise ValueError("No users available to allocate leads.")

        # Logic for outbound and inbound leads
        for lead in lead_objects:
            if lead.leads_source.source == 'outbound_source':
                print('out')
                # Assign to tele-callers in FIFO order
                tele_caller_list = tele_callers.sorted(key=lambda tc: tc.create_date)
                tele_caller_count = len(tele_caller_list)
                tele_caller_id = tele_caller_list[lead.id % tele_caller_count].id
                lead.write({'tele_caller_id': tele_caller_id})

            elif lead.leads_source.source == 'inbound_source':
                print('in')
                # Assign to lead users in FIFO order
                lead_user_list = lead_users.sorted(key=lambda user: user.create_date)
                lead_user_count = len(lead_user_list)
                lead_user_id = lead_user_list[lead.id % lead_user_count].id
                print(lead_user_id, 'user_id')
                user = self.env['res.users'].search([('id', '=', lead_user_id)])
                lead.write({'lead_owner': user.employee_id.id})

    @api.model
    def create(self, values):
        if values.get('reference_no', _('New')) == _('New'):
            values['reference_no'] = self.env['ir.sequence'].next_by_code(
                'leads.logic') or _('New')
        # Create the lead
        lead = super(LeadsForm, self).create(values)

        # Allocate the lead to tele-callers or lead users
        self.allocate_leads([lead.id])

        # Notify the assigned tele-caller, if any
        if lead.tele_caller_id:
            # Create the notification
            notification_ids = [(0, 0, {
                'res_partner_id': lead.tele_caller_id.partner_id.id,
                'notification_type': 'inbox'
            })]

            # Create the mail message
            self.env['mail.message'].create({
                'message_type': "notification",
                'body': f"Lead '{lead.name}' has been assigned to you.",
                'subject': "Lead Assigned",
                'model': 'leads.logic',
                'res_id': lead.id,
                'partner_ids': [(4, lead.tele_caller_id.partner_id.id)],
                'author_id': self.env.user.partner_id.id,
                'notification_ids': notification_ids,
            })

        return lead

    updated_remarks = fields.Text(string="Updated Remarks")

    # @api.constrains('updated_remarks', 'lead_quality')
    # def _check_updated_remarks(self):
    #     for record in self:
    #         if record.lead_quality:
    #             if record.lead_quality == 'bad_lead':
    #                 if not record.updated_remarks:
    #                     raise ValidationError("Updated Remarks is required when Lead Quality is 'Bad Lead'.")
    #                 if len(record.updated_remarks) < 140:
    #                     raise ValidationError("Updated Remarks must be at least 140 characters long.")

    def action_bulk_lead_allocation_tele_callers(self):
        active_ids = self.env.context.get('active_ids', [])
        print(active_ids, 'current rec')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Allocation',
            'res_model': 'allocation.tele_callers.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'parent_obj': active_ids}

        }