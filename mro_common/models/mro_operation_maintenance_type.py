# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class MroOperationMaintenanceType(models.Model):
    _name = "mro.operation_maintenance_type"
    _description = "MRO Operation Maintenance Type"

    name = fields.Char(
        string="Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    kind = fields.Selection(
        string="Kind",
        selection=[
            ("preventive", "Preventive"),
            ("corrective", "Cirrective"),
        ],
        required=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
    )
    note = fields.Text(
        string="Note",
    )
    mro_maintenance_start_grp_ids = fields.Many2many(
        string="Allow To Confirm MRO Maintenance",
        comodel_name="res.groups",
        relation="rel_mro_mtn_type_start_mtn",
        column1="type_id",
        column2="group_id",
    )
    mro_maintenance_done_grp_ids = fields.Many2many(
        string="Allow To Finish MRO Maintenance",
        comodel_name="res.groups",
        relation="rel_mro_mtn_type_done_mtn",
        column1="type_id",
        column2="group_id",
    )
    mro_maintenance_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel MRO Maintenance",
        comodel_name="res.groups",
        relation="rel_mro_mtn_type_cancel_mtn",
        column1="type_id",
        column2="group_id",
    )
    mro_maintenance_restart_grp_ids = fields.Many2many(
        string="Allow To Restart MRO Maintenance",
        comodel_name="res.groups",
        relation="rel_mro_mtn_type_restart_mtn",
        column1="type_id",
        column2="group_id",
    )
