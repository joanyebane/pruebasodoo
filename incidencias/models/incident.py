from odoo import api, fields, models, _


class IncidentRequest(models.Model):
    _name = "incidencias.request"
    _description = "Incidencia"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(string="Referencia", readonly=True, copy=False, default=lambda self: _("Nueva"), tracking=True)
    subject = fields.Char(string="Asunto", required=True, tracking=True)
    description = fields.Text(string="Descripción", required=True)
    requester_id = fields.Many2one("res.users", string="Solicitante", default=lambda self: self.env.user, required=True, tracking=True)
    assigned_id = fields.Many2one("res.users", string="Responsable", tracking=True)
    request_date = fields.Datetime(string="Fecha de solicitud", default=fields.Datetime.now, required=True, tracking=True)
    start_date = fields.Datetime(string="Inici")
    end_date = fields.Datetime(string="Fin")
    estimated_hours = fields.Float(string="Horas estimadas")
    spent_hours = fields.Float(string="Horas dedicadas", compute="_compute_spent_hours", store=True)
    state = fields.Selection([
        ("new", "Nueva"),
        ("in_progress", "En curso"),
        ("resolved", "Resuelta"),
        ("closed", "Cerrada"),
    ], string="Estado", default="new", tracking=True)
    reply_ids = fields.One2many("incidencias.reply", "incident_id", string="Respuestas")

    @api.depends("reply_ids.hours")
    def _compute_spent_hours(self):
        for incident in self:
            incident.spent_hours = sum(incident.reply_ids.mapped("hours"))

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", _("Nueva")) == _("Nueva"):
                vals["name"] = sequence.next_by_code("incidencias.request") or _("Nueva")
        return super().create(vals_list)

    def action_start(self):
        self.write({"state": "in_progress", "start_date": fields.Datetime.now()})

    def action_resolve(self):
        self.write({"state": "resolved", "end_date": fields.Datetime.now()})

    def action_close(self):
        self.write({"state": "closed"})

    def action_reset(self):
        self.write({"state": "new", "start_date": False, "end_date": False})
