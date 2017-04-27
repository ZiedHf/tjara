# -*- coding: utf-8 -*-

from odoo import models, fields, api

class depot(models.Model):
    _name = 'tjara.depot'
    
    name = fields.Char(string='Nom Depot', required=True)