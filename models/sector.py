# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class sector(models.Model):
    _name = 'tjara.sector'
    
    name = fields.Char(string="Sector", required=True)
    description = fields.Text(string="Sector Description")
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'This name is already exists...!')
    ]
    