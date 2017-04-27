# -*- coding: utf-8 -*-

from odoo import models, fields, api

class purchase_inquiry(models.Model):
    _name = 'tjara.purchase_inquiry'
    
    name = fields.Char(string='Purchase Name', required=True)
    state = fields.Selection(['Draft', 'Accepted'], string='State', required=True)
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='cascade', string="Product _ Package", index=True, required=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Fournisseur", index=True, required=True)