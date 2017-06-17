# -*- coding: utf-8 -*-

from odoo import models, fields, api

class depot(models.Model):
    _name = 'tjara.depot'
    
    name = fields.Char(string='Depot Name', required=True)
    stock_ids = fields.One2many('tjara.stock', 'depot_id', string='Stocks')