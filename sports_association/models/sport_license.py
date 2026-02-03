from odoo import models, fields

class SportIssue(models.Model):
    _name = 'sport.license'
    _description = 'Sport License'

    name = fields.Char(string='Name', required=True)
    reference = fields.Char(string='Reference')
    partner_id = fields.Many2one('res.partner', string='Partner')
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    
