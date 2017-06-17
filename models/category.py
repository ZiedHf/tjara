# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class category(models.Model):
    _name = 'tjara.category'
    
    name = fields.Char(string="Category", required=True)
    description = fields.Text(string="Category Description")
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'This name is already exists...!')
    ]