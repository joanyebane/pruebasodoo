from odoo import fields, models


class IncidentReplyWizard(models.TransientModel):
    _name = "incidencias.reply.wizard"
    _description = "Asistente para responder incidencias"

    message = fields.Text(string="Respuesta", required=True)
    hours = fields.Float(string="Horas")

    def action_add_reply(self):
        incident = self.env["incidencias.request"].browse(self.env.context.get("active_id"))
        if incident:
            self.env["incidencias.reply"].create({
                "incident_id": incident.id,
                "message": self.message,
                "hours": self.hours,
            })
        return {"type": "ir.actions.act_window_close"}
