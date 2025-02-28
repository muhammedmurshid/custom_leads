from odoo import fields,models, api, _
from odoo.exceptions import UserError


class WelcomeMail(models.TransientModel):
   """This model is used for sending WhatsApp messages through Odoo."""
   _name = 'welcome.mail'
   _description = "Welcome Mail Wizard"

   lead_id = fields.Many2one('leads.logic', string="Lead")
   message = fields.Text(string="message", required=True)
   mail_id = fields.Char(related="lead_id.email_address", string="Mail", readonly=0)

   def act_sent_mail(self):
       for record in self:
           if not record.mail_id:
               raise UserError("No email address found for this lead.")

           mail_values = {
               'subject': "Welcome to Logic Education!",
               'body_html': f"<p>{record.message}</p>",
               'email_to': record.mail_id,
               'email_from': 'info@logiceducation.org',
               'auto_delete': True,
           }

           self.lead_id.sended_welcome_mail = True

           mail = self.env['mail.mail'].create(mail_values)
           mail.send()
