# -*- coding: utf-8 -*-

from odoo import models, fields, api

class package(models.Model):
    _name = 'tjara.package'
    
    name = fields.Char(string="Nom d'emballage", required=True)
    #product_package_ids = fields.Many2one('tjara.product_package', ondelete='cascade', string="Package", index=True)
    unity = fields.Char(string="Unité", required=True)
    description = fields.Text(string="Description d'emballage")