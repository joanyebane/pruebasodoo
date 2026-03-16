from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class IncidentRequest(models.Model):
    def _is_incident_manager(self):
        return self.user_has_groups("incidencias.group_incident_manager") or self.user_has_groups("base.group_system")

    _name = "incidencias.request"
    _description = "Incidencia"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(
        string="Referencia",
        readonly=True,
        copy=False,
        default=lambda self: _("Nueva"),
        tracking=True,
    )
    subject = fields.Char(string="Asunto", required=True, tracking=True)
    description = fields.Text(string="Descripción", required=True, tracking=True)
    requester_id = fields.Many2one(
        "res.users",
        string="Solicitante",
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
        readonly=True,
    )
    assigned_id = fields.Many2one("res.users", string="Responsable", tracking=True)
    request_date = fields.Datetime(
        string="Fecha de solicitud",
        readonly=True,
        copy=False,
        tracking=True,
    )
    start_date = fields.Datetime(string="Inicio", tracking=True)
    end_date = fields.Datetime(string="Fin", tracking=True)
    estimated_time = fields.Float(string="Tiempo estimado")
    priority = fields.Selection(
        [
            ("low", "Bajo"),
            ("medium", "Medio"),
            ("high", "Alto"),
            ("very_high", "Muy alto"),
        ],
        string="Prioridad",
        default="medium",
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ("new", "Nueva"),
            ("in_progress", "En curso"),
            ("resolved", "Resuelta"),
            ("closed", "Cerrada"),
        ],
        string="Estado",
        default="new",
        tracking=True,
    )
    reply_ids = fields.One2many("incidencias.reply", "incident_id", string="Respuestas")

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        is_manager = self._is_incident_manager()
        for vals in vals_list:
            if vals.get("name", _("Nueva")) == _("Nueva"):
                vals["name"] = sequence.next_by_code("incidencias.request") or _("Nueva")
            vals["request_date"] = fields.Datetime.now()
            vals.setdefault("requester_id", self.env.user.id)
            if not is_manager and any(field in vals for field in ["assigned_id", "start_date", "end_date"]):
                raise AccessError(_("Solo un responsable puede definir responsable, inicio o fin."))
        return super().create(vals_list)

    def write(self, vals):
        if "request_date" in vals:
            raise AccessError(_("La fecha de solicitud se rellena automáticamente y no es modificable."))

        if not self._is_incident_manager() and any(
            field in vals for field in ["assigned_id", "start_date", "end_date", "state", "reply_ids"]
        ):
            raise AccessError(_("No tienes permisos para modificar responsable, fechas, estado o respuestas."))

        return super().write(vals)

    def action_start(self):
        self.write({"state": "in_progress", "start_date": fields.Datetime.now()})

    def action_resolve(self):
        self.write({"state": "resolved", "end_date": fields.Datetime.now()})

    def action_close(self):
        self.write({"state": "closed"})

    def action_reset(self):
        self.write({"state": "new", "start_date": False, "end_date": False})
