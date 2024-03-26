# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class InventoryClosing(models.Model):
    _inherit = "inventory_closing"

    _after_approved_method = False

    queue_job_batch_ids = fields.One2many(
        string="Queue Job Batch(s)",
        comodel_name="inventory_closing_queue_job_batch",
        inverse_name="inventory_closing_id",
    )

    @api.depends(
        "queue_job_batch_ids",
        "queue_job_batch_ids.job_batch_state",
    )
    def _compute_all_job_finished(self):
        for rec in self:
            job_not_finish_ids = rec.queue_job_batch_ids.filtered(
                lambda x: x.job_batch_state != "finished"
            )
            if len(job_not_finish_ids) > 0:
                rec.all_job_finished = False
            else:
                rec.all_job_finished = True

    all_job_finished = fields.Boolean(
        string="All Job Finished",
        compute="_compute_all_job_finished",
        store=True,
    )

    def _check_all_finished(self):
        self.ensure_one()
        result = True
        for job_batch in self.queue_job_batch_ids:
            if job_batch.job_batch_state != "finished":
                result = False
                break
        return result

    def _prepare_ic_queue_job_batch_data(self, batch_id):
        data = {
            "inventory_closing_id": self.id,
            "job_batch_id": batch_id,
        }
        return data

    def create_ic_queue_job_batch(self, batch_id):
        self.ensure_one()
        obj_ic_queue_job_batch = self.env["inventory_closing_queue_job_batch"]
        obj_ic_queue_job_batch.create(self._prepare_ic_queue_job_batch_data(batch_id))
        return True

    def _create_aml_from_svl(self, svl_ids, index):
        self.ensure_one()
        queue_job_obj = self.env["queue.job"]
        str_group = "[%s] Inventory Closing Batch for ID %s" % (str(index), self.id)
        batch = self.env["queue.job.batch"].get_new_batch(str_group)
        for svl in svl_ids:
            description = "Create AML From SVL for ID %s" % (self.id)
            job = (
                svl.with_context(job_batch=batch)
                .with_delay(description=_(description))
                ._create_accounting_entry()
            )
            criteria = [("uuid", "=", job.uuid)]
            job_id = queue_job_obj.search(criteria, limit=1, order="id desc").id
            svl.update(
                {
                    "job_id": job_id,
                }
            )
        batch.enqueue()
        self.create_ic_queue_job_batch(batch.id)

    @ssi_decorator.post_done_action()
    def _01_update_svl_journal(self):
        self.ensure_one()
        return True

    @ssi_decorator.post_done_action()
    def _02_create_aml_from_svl(self):
        self.ensure_one()
        return True

    @ssi_decorator.post_approve_action()
    def _01_post_update_svl_journal(self):
        self.ensure_one()
        for move in self.stock_move_ids:
            if not move.journal_id:
                move.picking_id.write(
                    {
                        "journal_id": self.journal_id.id,
                    }
                )

    @ssi_decorator.post_approve_action()
    def _02_post_create_aml_from_svl(self):
        self.ensure_one()
        svl_ids = self.stock_valuation_layer_ids.filtered(lambda x: not x.job_id)
        if svl_ids:
            batch_job_limit = self.type_id.batch_job_limit
            for index, i in enumerate(range(0, len(svl_ids), batch_job_limit), start=1):
                self._create_aml_from_svl(svl_ids[i : i + batch_job_limit], index)
        else:
            self._requeue_job_batch()

    def _requeue_job_batch(self):
        self.ensure_one()
        svl_ids = self.stock_valuation_layer_ids.filtered(
            lambda x: x.job_state != "done"
        )
        if svl_ids:
            for svl in svl_ids:
                svl.job_id.requeue()

    def action_requeue(self):
        for record in self.sudo():
            record._requeue_job_batch()
