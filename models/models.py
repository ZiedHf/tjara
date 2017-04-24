# -*- coding: utf-8 -*-

from odoo import models, fields, api

import product
import provider
import client
import package
import product_package
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