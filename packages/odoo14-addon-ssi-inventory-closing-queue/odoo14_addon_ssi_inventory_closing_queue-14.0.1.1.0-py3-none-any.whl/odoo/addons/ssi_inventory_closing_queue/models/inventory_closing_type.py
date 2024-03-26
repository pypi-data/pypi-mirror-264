# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class InventoryClosingType(models.Model):
    _inherit = "inventory_closing_type"

    batch_job_limit = fields.Integer(
        string="Batch Job Limit",
        default=100,
    )
