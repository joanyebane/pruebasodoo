from odoo import models, fields, api
from odoo.fields import Command
from odoo.exceptions import ValidationError #importamos la clase ValidationError para lanzar un error si el coste es negativo

class SportIssue(models.Model):
    _name = 'sport.issue'
    _description = 'Sport Issue'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin'] #para que las incidencias tengan el chat de la derecha y se puedan asignar actividades

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date', default=fields.Date.context_today) #fecha por defecto del día actual cuando se crea una nueva incidencia
    assistance = fields.Boolean(string='Assistance', help='Show if the issue has assistance')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('done', 'Done')],
            string='State',
            default='draft',
            group_expand='_group_expand_state',
            tracking=True
    )
#para que las columnas del kanban no desaparezcan si no tienen ninguna incidencia
    def _group_expand_state(self, states, domain, order):
        """Show all kanban columns even if they are empty."""
        selection = self._fields["state"].selection
        return [key for key, label in selection]
    
    user_id = fields.Many2one('res.users', string='User')
#un integer, sin más
    sequence = fields.Integer(string='Sequence', default='10')
#definimos que la casilla solución será un html
    solution = fields.Html('Solution')

    clinic_id = fields.Many2one('sport.clinic', string='Clinic')

    tag_ids = fields.Many2many('sport.issue.tag', string='Tags')

    color = fields.Integer(string='Color')
#en los campos "related" y "compute", si queremos que se guarde en la base de datos hay que poner store=True
    assigned = fields.Boolean('Assigned', compute='_compute_assigned', inverse='_inverse_assigned', search='_search_assigned', store=True)
#Con tracking=True se muestra en el chatter(mixin) cuando se modifica el coste
    cost = fields.Float(string='Cost', tracking=True)
#user_phone es el teléfono. solo se puede modificar dentro del usuario pero tambien aparece en la incidencia. Con readonly=False se podría editar desde fuera
    user_phone = fields.Char('user_phone') #, related='user_id.phone')

    action_ids = fields.One2many('sport.issue.action', 'issue_id', string='Actions to do')
# constraint para que el nombre de la incidencia sea único
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The name of the issue must be unique.'),
    ]

    player_id = fields.Many2one('sport.player', string='Player')
#validación para que el coste no pueda ser negativo
    @api.constrains('cost')
    def _check_cost(self):
        for record in self:
            if record.cost < 0:
                raise ValidationError('Cost cannot be negative')

#con el onchange, si se selecciona un usuario, se muestra su teléfono en la incidencia, y si se deselecciona, se borra el teléfono
    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id:
            self.user_phone = self.user_id.phone
        else:
            self.user_phone = False

#con el onchange, si se selecciona una clínica, se marca la casilla de asistencia, y si se deselecciona, se desmarca la casilla de asistencia
    @api.onchange('clinic_id')
    def _onchange_clinic_id(self):
        for record in self:
            if record.clinic_id:
                record.assistance = True
            else:
                record.assistance = False

#aparece la casilla assigned en incidencias
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = bool(record.user_id)
#el inverse assigned permite desmarcar y marcar la casilla de forma manual
    def _inverse_assigned(self):
        for record in self:
            if not record.assigned:
                record.user_id = False
            else:
                record.user_id = self.env.user
#búsqueda de filtros avanzada
        def _search_assigned(self, operator, value):
            if operator == '=':
                return [('user_id', operator, value)]
            else:
                return []

#botón To open
    def action_draft(self):
        self.state = 'draft'
    def action_open(self):
        self.state = 'open'
    def action_done(self):
        for record in self:
            if not record.date:
                raise UserError ('You cannot mark an issue as done if it does not have a date.')
            record.state = 'done'
            msg_body = f'La incidencia ha pasado del estado {record.state} con fecha {record.date}'
            record.message_post(body=msg_body)
#botón para a la hora de crear una incidencia añadir una etiqueta, si existe la etiqueta, la pone, sinó la crea. Borra las etiquetas que haya y añade la nueva.
    def action_add_tag(self):
        for record in self:
            import pdb;pdb.set_trace
            tag_ids = self.env['sport.issue.tag'].search([('name', 'ilike', record.name)])
            if tag_ids:
                record.tag_ids = [Command.set(tag_ids.ids)]
            else:
                record.tag_ids = [Command.create({'name': record.name})]