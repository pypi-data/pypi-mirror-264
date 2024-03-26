# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = [
        "stock.valuation.layer",
    ]

    @api.depends(
        "job_id.result",
        "job_id.exc_info",
    )
    def _compute_job_result(self):
        for rec in self:
            rec.job_result = rec.job_id.result or rec.job_id.exc_info

    job_id = fields.Many2one(
        comodel_name="queue.job",
        string="Job",
        copy=False,
    )
    job_state = fields.Selection(string="Status", related="job_id.state", store=True)
    job_result = fields.Text(
        string="Result", compute="_compute_job_result", store=False
    )
