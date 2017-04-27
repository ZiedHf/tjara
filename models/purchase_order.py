# -*- coding: utf-8 -*-

from odoo import models, fields, api

class purchase_order(models.Model):
    _name = 'tjara.purchase_order'
    
    name = fields.Char(string='Purchase Name', required=True)
    state = fields.Selection(['Draft', 'Accepted'], string='State', required=True)
    product_package_id = fields.Many2one('tjara.product_package', ondelete='cascade', string="Product _ Package", index=True, required=True)
    purchase_inquiry_ids = fields.One2many('tjara.purchase_inquiry', ondelete='cascade', string="Demande", index=True)
    provider_id = fields.One2many('tjara.provider', ondelete='cascade', string="Demande", index=True)