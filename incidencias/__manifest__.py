{
    "name": "Gestión de Incidencias",
    "summary": "Solicitud y seguimiento colaborativo de incidencias",
    "version": "16.0.1.0.0",
    "category": "Services/Helpdesk",
    "author": "Tu Empresa",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/incident_sequence.xml",
        "views/incident_views.xml",
        "wizards/incident_reply_wizard_views.xml",
        "report/incident_report.xml",
    ],
    "application": True,
    "installable": True,
}
