# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=W0622
from odoo import api, fields, models


class InventoryClosingQueueJobBatch(models.Model):
    _name = "inventory_closing_queue_job_batch"
    _description = "Inventory Closing Queue Job Batch"

    inventory_closing_id = fields.Many2one(
        string="#Inventory Closing",
        comodel_name="inventory_closing",
        required=True,
        ondelete="cascade",
    )

    @api.depends(
        "job_id.result",
        "job_id.exc_info",
    )
    def _get_job_result(self):
        for rec in self:
            rec.job_result = rec.job_id.result or rec.job_id.exc_info

    job_batch_id = fields.Many2one(
        comodel_name="queue.job.batch",
        string="#Job Batch",
        copy=False,
    )
    job_count = fields.Integer(
        string="Job Count",
        related="job_batch_id.job_count",
    )
    finished_job_count = fields.Float(
        string="Completeness",
        related="job_batch_id.finished_job_count",
    )
    job_batch_state = fields.Selection(
        string="Status", related="job_batch_id.state", store=True
    )
