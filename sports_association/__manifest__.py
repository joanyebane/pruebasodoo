# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sports Association",
    "summary": "Manage sports association members.",
    "version": "17.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "development_status": "Alpha|Beta|Production/Stable|Mature",
    "category": "Sports",
    "author": "Joan, Empresa",
    # see https://odoo-community.org/page/maintainer-role for a description of the maintainer role and responsibilities
    "maintainers": ["your-github-login"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
    "base", "web", "portal"
    ],

    "data": ["data/sport_license_data.xml",
            "security/groups.xml",
            "security/ir.model.access.csv",
            "views/sport_issue_views.xml",
            "views/sport_issue_tag_views.xml",
            "views/sport_clinic_views.xml",
            "views/sport_player_views.xml",
            "views/sport_sport_views.xml",
            "views/sport_team_views.xml",
            "views/sport_ticket_views.xml",
            "views/sport_issue.xml",
            "wizards/sport_create_issue.xml",
            "report/sport_issue_report.xml",
            ]
}

