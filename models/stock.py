# -*- coding: utf-8 -*-

from odoo import models, fields, api
from validate import is_string

class stock(models.Model):
    _name = 'tjara.stock'
    
    name = fields.Char(string='Stock name', default='Unknown', compute='_compute_name', store=True)
    depot_id = fields.Many2one('tjara.depot', ondelete='cascade', string="Depot", index=True, required=True)
    product_package_id = fields.Many2one('tjara.product_package', ondelete='cascade', string="Product _ Package", index=True, required=True)
    unity = fields.Selection(related='product_package_id.package_id.unity', string="Unity", index=True, required=True)
    in_stock = fields.Float(string="Stock", required=True)
    
    _sql_constraints = [
        ('relation_unique', 'unique (depot_id, product_package_id)', 'This relation is already exists...!')
    ]
    
    @api.depends('product_package_id', 'depot_id')
    def _compute_name(self):
        for rec in self:
            try:
                rec.name = rec.depot_id.name + " _ " + rec.product_package_id.name
            except TypeError:
                rec.name = 'Unknown'
                