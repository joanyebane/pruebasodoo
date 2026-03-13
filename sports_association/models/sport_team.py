from odoo import models, fields
from odoo.fields import Command

class SportTeam(models.Model):
    _name = 'sport.team'
    _description = 'Sport Team'

    name = fields.Char(string='Name', required=True)
    sport_id = fields.Many2one('sport.sport', string='Sport')
    player_ids = fields.One2many('sport.player', 'team_id', string='Players')
    logo = fields.Image('Logo')
#botón de añadir a un equipo todos los jugadores que no tienen equipo (están libres) y menores de 30 años
    player_count = fields.Integer('Player Count', compute='_compute_player_count')

    def _compute_player_count(self):
        for record in self:
            record.player_count = len(record.player_ids)

    #def action_add_players(self):
        #for record in self:
# sin esta moficiación, el botón al pulsarlo por segunda vez, eliminaba a los jugadores
    def action_add_players(self):
        for team in self:
            players = self.env['sport.player'].search([
                ('team_id', '=', False),
                ('age', '<', 30),
        ])
        if players:
            players.write({'team_id': team.id})
            
            #players = self.env['sport.player'].search([('team_id', '=', False,), ('age', '<', 30)])
            # record.player_ids = [Command.set(players.ids)]

    def action_view_players(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Players',
            'res_model': 'sport.player',
            'view_mode': 'tree,form',
            'domain': [('team_id', '=', self.id)],
        }