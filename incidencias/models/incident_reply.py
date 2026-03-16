from odoo import fields, models


class IncidentReply(models.Model):
    _name = "incidencias.reply"
    _description = "Respuesta de incidencia"
    _order = "create_date asc"

    incident_id = fields.Many2one("incidencias.request", string="Incidencia", required=True, ondelete="cascade")
    user_id = fields.Many2one("res.users", string="Usuario", required=True, default=lambda self: self.env.user)
    reply_date = fields.Datetime(string="Fecha", default=fields.Datetime.now, required=True)
    message = fields.Text(string="Respuesta", required=True)
    hours = fields.Float(string="Horas")
