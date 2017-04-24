# -*- coding: utf-8 -*-

from odoo import models, fields, api

class product(models.Model):
    _name = 'tjara.product'
    
    name = fields.Char(string="Nom du produit", required=True)
    description = fields.Text(string="Description du produit")
    add_date = fields.Date(string="Date d'ajout au stock")
    provider_ids = fields.Many2many('tjara.provider', ondelete='set null', string="Provider", index=True)
    client_ids = fields.Many2many('tjara.client', ondelete='set null', string="Client", index=True)