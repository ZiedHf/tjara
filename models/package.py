# -*- coding: utf-8 -*-

from odoo import models, fields, api

class package(models.Model):
    _name = 'tjara.package'
    
    name = fields.Char(string="Nom d'emballage")
    unity = fields.Selection((('Kg', 'Kg'), ('L', 'L'), ('Piece', 'Piece'), ('M', 'M')), string="Unité", required=True)
    description = fields.Text(string="Description d'emballage")