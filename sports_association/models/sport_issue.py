from odoo import models, fields

class SportIssue(models.Model):
    _name = 'sport.issue'
    _description = 'Sport Issue'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    assistance = fields.Boolean(string='Assistance', help='Show if the issue has assistance')
    state = fields.Selection(
        [
            ('draft','Draft'),
            ('open','Open'),
            ('done', 'Done')],
            string='State',
            default='draft',
    )

    user_id = fields.Many2one('res.users', string='User')
#un integer, sin más
    sequence = fields.Integer(string='Sequence', default='10')
#definimos que la casilla solución será un html
    solution = fields.Html('Solution')

    clinic_id = fields.Many2one('sport.clinic', string='Clinic')

    tag_ids = fields.Many2many('sport.issue.tag', string='Tags')

#botón To open
    def action_draft(self):
        self.state = 'draft'
    def action_open(self):
        self.state = 'open'
    def action_done(self):
        self.state = 'done'