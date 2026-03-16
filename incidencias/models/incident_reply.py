from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class IncidentReply(models.Model):
    _name = "incidencias.reply"
    _description = "Respuesta de incidencia"
    _order = "create_date asc"

    incident_id = fields.Many2one(
        "incidencias.request", string="Incidencia", required=True, ondelete="cascade"
    )
    user_id = fields.Many2one(
        "res.users", string="Usuario", required=True, default=lambda self: self.env.user
    )
    reply_date = fields.Datetime(string="Fecha", default=fields.Datetime.now, required=True)
    message = fields.Text(string="Respuesta", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.user_has_groups("incidencias.group_incident_manager"):
            raise AccessError(_("Solo un responsable puede añadir respuestas."))
        replies = super().create(vals_list)
        for reply in replies:
            reply.incident_id.message_post(
                body=_("<b>Respuesta de %s:</b><br/>%s") % (reply.user_id.name, reply.message)
            )
        return replies

    def write(self, vals):
        if not self.user_has_groups("incidencias.group_incident_manager"):
            raise AccessError(_("Solo un responsable puede modificar respuestas."))
        return super().write(vals)

    def unlink(self):
        if not self.user_has_groups("incidencias.group_incident_manager"):
            raise AccessError(_("Solo un responsable puede eliminar respuestas."))
        return super().unlink()
