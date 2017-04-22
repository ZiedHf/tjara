# -*- coding: utf-8 -*-

from odoo import models, fields, api

class fournisseur(models.Model):
    _name = 'tjara.fournisseur'
    
    name = fields.Char(string="Nom du fournisseur", required=True)
    adresse = fields.Char(string="Adresse du fournisseur")
    tel = fields.Integer()
    fax = fields.Integer()
    description = fields.Text()