# -*- coding: utf-8 -*-

from odoo import models, fields, api

import product
import sector
import category
import provider
import client
import package
import product_package
import stock
import depot
import purchase_order
import ref_po_pp
import purchase_inquiry
import ref_pi_pp
import provider_order
import voucher_entry
import ref_provider_order_pp
import ref_ve_pp


# import purchase_invoice
# import purchase_payment
# import provider_regulation
# import wizards

# class tjara(models.Model):
#     _name = 'tjara.tjara'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100