from odoo import models, fields, api

class SportPlayer(models.Model):
    _name = 'sport.player'
    _description = 'Sport Player'
    _inherits = {'res.partner': 'partner_id'}
#Inherits, name y partner_id, se han modificado para que al crear un jugador, se cree un partner con el mismo nombre y se relacione con el jugador creado.
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
    team_id = fields.Many2one('sport.team', string='Team')
    birthdate = fields.Date ('Birthdate', copy=False) #copy False para que al duplicar el jugador no se copie nada excepto el nombre y el equipo
    age = fields.Integer('Age', compute='_compute_age', store=True, copy=False)
    starter = fields.Boolean('Starter', copy=False)
    position = fields.Char('Position', copy=False)
#Un campo que se trae el nombre del deporte del equipo seleccionado
    sport_name = fields.Char ('Sport', related='team_id.sport_id.name', store="True", copy=False)
#permite archivar y desarchivar jugadores
    active = fields.Boolean('Active', default=True)

#Campo de cumpleaños en jugadores que calcula la edad y la guarda en la bbdd    
    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                record.age = (fields.Date.today() - record.birthdate).days / 365
            else:
                record.age = 0