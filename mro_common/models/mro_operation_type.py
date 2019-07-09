# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MroOperationType(models.Model):
    _name = "mro.operation_type"
    _description = "MRO Operation Type"

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
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
    )
    note = fields.Text(
        string="Note",
    )
    mro_operation_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm MRO Operation",
        comodel_name="res.groups",
        relation="rel_mro_op_type_confirm_op",
        column1="type_id",
        column2="group_id",
    )
    mro_operation_approve_grp_ids = fields.Many2many(
        string="Allow To Approve MRO Operation",
        comodel_name="res.groups",
        relation="rel_mro_op_type_approve_op",
        column1="type_id",
        column2="group_id",
    )
    mro_operation_start_grp_ids = fields.Many2many(
        string="Allow To Confirm MRO Operation",
        comodel_name="res.groups",
        relation="rel_mro_op_type_start_op",
        column1="type_id",
        column2="group_id",
    )
    mro_operation_done_grp_ids = fields.Many2many(
        string="Allow To Finish MRO Operation",
        comodel_name="res.groups",
        relation="rel_mro_op_type_done_op",
        column1="type_id",
        column2="group_id",
    )
    mro_operation_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel MRO Operation",
        comodel_name="res.groups",
        relation="rel_mro_op_type_cancel_op",
        column1="type_id",
        column2="group_id",
    )
    mro_operation_restart_grp_ids = fields.Many2many(
        string="Allow To Restart MRO Operation",
        comodel_name="res.groups",
        relation="rel_mro_op_type_restart_op",
        column1="type_id",
        column2="group_id",
    )
