# -*- coding: utf-8 -*-

from odoo import models, fields, api

class produit(models.Model):
    _name = 'tjara.produit'
    
    name = fields.Char()
    price = fields.Integer()
    description = fields.Text()
    add_date = fields.Char()