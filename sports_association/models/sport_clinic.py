from odoo import models, fields

class SportClinic(models.Model):
    _name = 'sport.clinic'
    _description = 'Sport Clinic'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='phone')
    email = fields.Char(string='email')
    issue_ids = fields.One2many('sport.issue', 'clinic_id', string='issues')
    available = fields.Boolean('Available')
    issue_count = fields.Integer('Issue Count', compute='_compute_issue_count')

    def _compute_issue_count(self):
        for record in self:
            record.issue_count = len(record.issue_ids)

    def action_check_assistance(self):
        for record in self.issue_ids:
            record.assistance = True
#self.issue_ids.write({'assistance':True});

#smartbutton issues, esto hace que al hacer click en el botón de incidencias de la clínica, se muestren solo las incidencias relacionadas con esa clínica, y no todas las incidencias
    def action_view_issues(self):

        return {
            'name': 'Issues',
            'type': 'ir.actions.act_window',
            'res_model': 'sport.issue',
            'view_mode': 'tree,form',
            'domain': [('clinic_id', '=', self.id)],
        }
