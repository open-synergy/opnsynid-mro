# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class MroOperationMaintenanceCommon(models.AbstractModel):
    _name = "mro.operation_maintenance_common"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _order = "sequence, id"
    _description = "Abstract Model for MRO Operation Maintenance"

    @api.multi
    def _compute_policy(self):
        _super = super(MroOperationMaintenanceCommon, self)
        _super._compute_policy()

    @api.multi
    def _compute_allowed_mro_object_ids(self):
        for document in self:
            result_ids = []
            if document.operation_id:
                criteria = [
                    ("id", "child_of", document.operation_id.mro_object_id.id),
                ]
                model_name = str(document.mro_object_id._name)
                result_ids = self.env[model_name].search(criteria).ids
            document.allowed_mro_object_ids = result_ids

    name = fields.Char(
        string="# Document",
        default="/",
        help="MRO maintenance document number",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    operation_id = fields.Many2one(
        string="# MRO Operation",
        comodel_name="mro.operation_common",
        required=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
    )
    kind = fields.Selection(
        string="Type",
        selection=[
            ("preventive", "Preventive"),
            ("corrective", "Cirrective"),
        ],
        readonly=True,
    )
    allowed_mro_object_ids = fields.Many2many(
        string="Allowed MRO Objects",
        comodel_name="mro.object_common",
        compute="_compute_allowed_mro_object_ids",
    )
    mro_object_id = fields.Many2one(
        string="MRO Object",
        comodel_name="mro.object_common",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Activity",
        comodel_name="mro.operation_maintenance_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    scheduled_date_start = fields.Datetime(
        string="Schedule Date Start",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    scheduled_date_end = fields.Datetime(
        string="Schedule Date End",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    real_date_start = fields.Datetime(
        string="Real Date Start",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    real_date_end = fields.Datetime(
        string="Real Date End",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    note = fields.Text(
        string="Note",
    )
    operation_state = fields.Selection(
        string="Operation State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Ready To Start"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Ready To Start"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )
    start_ok = fields.Boolean(
        string="Can Start",
        compute="_compute_policy",
    )
    done_ok = fields.Boolean(
        string="Can Finish",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    start_user_id = fields.Many2one(
        string="Start By",
        comodel_name="res.users",
        readonly=True,
    )
    start_date = fields.Datetime(
        string="Start Date",
        readonly=True,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
    )

    @api.constrains(
        "scheduled_date_start",
        "scheduled_date_end"
    )
    def _check_schedule_date(self):
        strWarning = _(
            "Schedule Date Start must be "
            "greater than Schedule Date End")
        scheduled_date_start =\
            self.scheduled_date_start
        scheduled_date_end =\
            self.scheduled_date_end
        if scheduled_date_start and scheduled_date_end:
            if scheduled_date_start > scheduled_date_end:
                raise UserError(strWarning)

    @api.constrains(
        "real_date_start",
        "real_date_end"
    )
    def _check_real_date(self):
        strWarning = _(
            "Real Date Start must be "
            "greater than Real Date End")
        real_date_start =\
            self.real_date_start
        real_date_end =\
            self.real_date_end
        if real_date_start and real_date_end:
            if real_date_start > real_date_end:
                raise UserError(strWarning)

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())

    @api.multi
    def action_start(self):
        for document in self:
            document.write(document._prepare_start_data())

    @api.multi
    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_start_data(self):
        return {
            "state": "open",
            "start_date": fields.Datetime.now(),
            "start_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_done_data(self):
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "approve_date": False,
            "approve_user_id": False,
            "start_date": False,
            "start_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    @api.onchange(
        "operation_id",
    )
    def onchange_mro_object_id(self):
        self.mro_object_id = False

    @api.model
    def create(self, values):
        _super = super(MroOperationMaintenanceCommon, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write({
            "name": sequence,
        })
        return result

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(MroOperationMaintenanceCommon, self)
        _super.unlink()
