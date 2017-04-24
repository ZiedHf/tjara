# -*- coding: utf-8 -*-

from odoo import models, fields, api

class client(models.Model):
    _name = 'tjara.client'
    
    name = fields.Char(string="Nom du client", required=True)
    adresse = fields.Char(string="Adresse du client")
    tel = fields.Char()
    fax = fields.Char()
    description = fields.Text()
    product_ids = fields.Many2many('tjara.product', ondelete='set null', string="Products", index=True)