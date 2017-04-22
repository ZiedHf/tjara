# -*- coding: utf-8 -*-

from odoo import models, fields, api

class produit(models.Model):
    _name = 'tjara.produit'
    
    name = fields.Char(string="Nom du produit", required=True)
    price = fields.Integer(string="Prix en unité", required=True)
    description = fields.Text(string="Description du produit")
    add_date = fields.Date(string="Date d'ajout au stock")