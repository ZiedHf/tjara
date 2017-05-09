# -*- coding: utf-8 -*-

from odoo import models, fields, api

class provider_order(models.Model):
    _name = 'tjara.provider_order'
    
    name = fields.Char(string='Provider Order', default=lambda self: self._get_next_pProviderOrdername(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='cascade', string="Purchase Order", index=True, required=True, domain=[('state', '=', 'inprogress')])
    product = fields.Char(related='purchase_order_id.product_package_id.name', store=False, string="Product", readonly=True)
    qte_total_unity = fields.Char(related='purchase_order_id.qte_total_unity', store=False, string="Qte/Nbr Total", readonly=True)
    qte = fields.Integer(related='purchase_order_id.qte', store=False, string="Qte/Nbr Package", readonly=True)
    price = fields.Float(digits=(12, 3), help="Prix", string="Prix")
    date_order = fields.Date(string="Date de demande")
    datefinal_order = fields.Date(string="Date d'expiration")
    description = fields.Text(string="Description")