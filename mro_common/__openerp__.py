# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Common MRO Feature",
    "version": "8.0.1.2.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_print_policy",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/mro_operation_maintenance_type_views.xml",
        "views/mro_operation_type_views.xml",
        "views/mro_operation_common_views.xml",
        "views/mro_operation_maintenance_common_views.xml",
    ],
}
