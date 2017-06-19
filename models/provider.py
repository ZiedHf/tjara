# -*- coding: utf-8 -*-

from odoo import models, fields, api

class provider(models.Model):
    _name = 'tjara.provider'
    
    name = fields.Char(string="Provider Name")
    adresse = fields.Char(string="Provider Adresse")
    tel = fields.Char(string="Tel")
    fax = fields.Char(string="Fax")
    description = fields.Text(string="Description")
    product_ids = fields.Many2many('tjara.product', ondelete='set null', string="Products", index=True)
#     purchase_inquiry_id = fields.Many2one('tjara.purchase_inquiry', ondelete='cascade', string="Fournisseur", index=True, required=True)