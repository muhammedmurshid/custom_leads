from odoo import fields, models, api, _, tools
from odoo.http import request
from odoo.exceptions import ValidationError, UserError



class ConnectionForm(models.TransientModel):
    _name = 'connect.form'

    lead_quality = fields.Selection(
        [('hot', 'Hot'),
         ('warm', 'Warm'), ('cold', 'Cold'),
         ('bad_lead', 'Bad Lead'), ('not_responding', 'Not Responding'), ('crash_lead', 'Crash Lead'),
         ('nil', 'Nil')],
        string='Lead Quality')
    expected_joining_date = fields.Date(string="Expected Joining Date")
    lead_id = fields.Many2one('leads.logic', string="Lead")

    subject = fields.Char(string="Subject")
    task_owner_id = fields.Many2one('res.users', string="Task Owner")
    due_date = fields.Date(string="Due Date")
    status = fields.Selection(
        [('not_started', 'Not Started'),
         ('deferred', 'Deffered'), ('in_progress', 'In Progress'),
         ('completed', 'Completed'), ('waiting_for_input', 'Waiting for Input')],
        string='Status')
    priority = fields.Selection(
        [('high', 'High'),
         ('highest', 'Highest'), ('low', 'Low'),
         ('lowest', 'Lowest'), ('normal', 'Normal')],
        string='Priority')
    description = fields.Text(string="Description")
    date = fields.Datetime(string="Date Time")

    def act_connect(self):
        print('hi')


class NotConnectionForm(models.TransientModel):
    _name = 'not.connect.form'

    notes = fields.Text(string="Notes")
    lead_id = fields.Many2one('leads.logic', string="Lead")

class ConvertLead(models.TransientModel):
    _name = 'convert.lead'

    amount = fields.Float(string="Amount")
    lead_id = fields.Many2one('leads.logic', string="Deal Name")
    closing_date = fields.Date(string="Closing Date")
    lead_owner_id = fields.Many2one('res.users', string="Lead Owner")

    def act_convert(self):
        self.lead_id.write({
            'amount': self.amount,
            'closing_date': self.closing_date,
            'state': 'deal',
            'current_status': 'deal'
        })

class LostLead(models.TransientModel):
    _name = 'lost.lead.form'

    lead_id = fields.Many2one('leads.logic', string="Lead")
    reason = fields.Text(string="Lost Reason")

    def act_lost_lead(self):
        self.lead_id.write({
            'state': 'lost',
            'lost_reason': self.reason,
            'current_status': 'lost'
        })

class QualifiedLead(models.TransientModel):
    _name = 'qualified.lead.form'

    lead_id = fields.Many2one('leads.logic', string="Lead")
    title = fields.Many2one('res.partner.title')
    first_name = fields.Char(string="First Name", required=1)
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name", required=1)
    name = fields.Char(string="Name")
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Gender', required=True, default='m')
    birth_date = fields.Date('Birth Date', required=1)
    email = fields.Char(string="Email", required=1)
    course = fields.Many2one('op.course', string="Course")
    batch_id = fields.Many2one('op.batch', string="Batch", required=1)
    mobile = fields.Char(string="Mobile")

    @api.onchange('email')
    def _validate_email(self):
        if self.email and not tools.single_email_re.match(self.email):
            raise ValidationError(_('Invalid Email! Please enter a valid email address.'))

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(
                self.last_name
            )
        else:
            self.name = str(self.first_name) + " " + str(
                self.middle_name) + " " + str(self.last_name)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    def act_admission(self):
        self.lead_id.write({
            'state': 'qualified',
            'admission_status': True,
            'admission_date': fields.Datetime.now(),

        })
        student = self.env['op.student'].create({
            'title': self.title.id,
            'name': self.name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'email': self.email,
            'batch_id': self.batch_id.id,
            'course_id': self.course.id,
            'state':'confirm',
            'mobile': self.mobile,
            'admission_officer_id': self.lead_id.lead_owner.user_id.id
        })