# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Inventory Closing Queue",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "queue_job_batch",
        "ssi_inventory_closing",
        "base_automation",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_actions_server_data.xml",
        "data/base_automation_data.xml",
        "data/policy_template_data.xml",
        "views/inventory_closing_views.xml",
        "views/inventory_closing_type_views.xml",
        "views/stock_valuation_layer_views.xml",
    ],
    "demo": [],
    "images": [],
}
