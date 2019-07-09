# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class MroObjectCommon(models.AbstractModel):
    _name = "mro.object_common"
    _description = "MRO Object Common"

    @api.multi
    def _compute_num_of_operation(self):
        for document in self:
            document.num_of_operation = len(document.operation_ids)

    @api.multi
    def _compute_num_of_maintenance(self):
        for document in self:
            document.num_of_maintenance = len(document.maintenance_ids)

    parent_id = fields.Many2one(
        string="Parent MRO Object",
        comodel_name="mro.object_common",
    )
    operation_ids = fields.One2many(
        string="MRO Operations",
        comodel_name="mro.operation_common",
        inverse_name="mro_object_id",
    )
    maintenance_ids = fields.One2many(
        string="MRO Maintenances",
        comodel_name="mro.operation_maintenance_common",
        inverse_name="mro_object_id",
    )
    num_of_operation = fields.Integer(
        string="Num. of MRO Operations",
        compute="_compute_num_of_operation",
    )
    num_of_maintenance = fields.Integer(
        string="Num. of MRO Maintenances",
        compute="_compute_num_of_maintenance",
    )

    @api.multi
    def action_open_mro_operation(self):
        self.ensure_one()
        return False

    @api.multi
    def action_open_mro_maintenance(self):
        self.ensure_one()
        return False

    @api.multi
    def _get_mro_operation_waction(self, waction_xml_id):
        self.ensure_one()
        waction = self.env.ref(waction_xml_id).read()[0]
        waction["domain"] = [
            ("mro_object_id", "=", self.id),
        ]
        waction["context"] = {
            "default_mro_object_id": self.id,
        }
        return waction

    @api.multi
    def _get_mro_maintenance_waction(self, waction_xml_id):
        self.ensure_one()
        waction = self.env.ref(waction_xml_id).read()[0]
        waction["domain"] = [
            ("mro_object_id", "=", self.id),
        ]
        return waction
