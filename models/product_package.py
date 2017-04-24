# -*- coding: utf-8 -*-

from odoo import models, fields, api

class product_package(models.Model):
    _name = 'tjara.product_package'
    
    name = fields.Char(string="Produit + Emballage", default="Unknown", compute='_compute_name')
    product_id = fields.Many2one('tjara.product', ondelete='cascade', string="Product", index=True, required=True)
    package_id = fields.Many2one('tjara.package', ondelete='cascade', string="Package", index=True, required=True)
    price = fields.Integer(string="Prix d'unité", required=True)
    description = fields.Text(string="Description d'emballage")
    
    @api.depends('product_id', 'package_id')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.product_id.name + " - " + rec.package_id.name            
