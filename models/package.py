# -*- coding: utf-8 -*-

from odoo import models, fields, api

class package(models.Model):
    _name = 'tjara.package'
    
    name = fields.Char(string="Package Name", required=True)
    unity = fields.Selection((('Kg', 'Kg'), ('L', 'L'), ('Piece', 'Piece'), ('M', 'M')), string="Unity", required=True)
    description = fields.Text(string="Package description")
    product_package_ids = fields.One2many('tjara.product_package', 'package_id', ondelete='cascade',  string='Product')
    
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'This name is already exists...!')
    ]