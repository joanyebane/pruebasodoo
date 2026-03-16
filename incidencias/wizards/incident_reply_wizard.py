from odoo import _, fields, models
from odoo.exceptions import AccessError


class IncidentReplyWizard(models.TransientModel):
    _name = "incidencias.reply.wizard"
    _description = "Asistente para responder incidencias"

    message = fields.Text(string="Respuesta", required=True)

    def action_add_reply(self):
        if not self.user_has_groups("incidencias.group_incident_manager"):
            raise AccessError(_("Solo un responsable puede añadir respuestas."))

        incident = self.env["incidencias.request"].browse(self.env.context.get("active_id"))
        if incident:
            self.env["incidencias.reply"].create(
                {
                    "incident_id": incident.id,
                    "message": self.message,
                }
            )
        return {"type": "ir.actions.act_window_close"}
