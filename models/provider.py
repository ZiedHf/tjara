# -*- coding: utf-8 -*-

from odoo import models, fields, api

class provider(models.Model):
    _name = 'tjara.provider'
    
    name = fields.Char(string="Nom du fournisseur", required=True)
    adresse = fields.Char(string="Adresse du fournisseur")
    tel = fields.Char()
    fax = fields.Char()
    description = fields.Text()
    product_ids = fields.Many2many('tjara.product', ondelete='set null', string="Products", index=True)