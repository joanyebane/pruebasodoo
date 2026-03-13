from odoo.tests import common
from odoo import fields, models

class TestSportIssue(common.TransactionCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.user = self.env.ref('base.user_admin')
        self.issue = self.env ['sport.issue'].create({'name': 'Issue 1', 'state': 'open'})

    def test_compute_assigned(self):
        self.issue.user_id = False
        self.assertFalse(self.issue.assigned)
        self.issue.user_id = self.user
        self.assertTrue(self.issue.assigned)

    def test_inverse_assigned(self):
        self.issue.assigned = False
        self.assertFalse(self.issue.user_id)
        self.issue.assigned = True
        self.assertEqual(self.issue.user_id, self.env.user)

    def test_action_draft(self):
        self.issue.state = 'open'
        self.issue.action_draft()
        self.assertEqual(self.issue.state, 'draft')
