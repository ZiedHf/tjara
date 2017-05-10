# -*- coding: utf-8 -*-

from odoo import models, fields, api

class provider_order(models.Model):
    _name = 'tjara.provider_order'
        
    name = fields.Char(string='Provider Order', default=lambda self: self._get_next_providerOrdername(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='restrict', string="Purchase Order", index=True, required=True, domain=[('state', '=', 'inprogress')], readonly=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
#     provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
    product = fields.Char(related='purchase_order_id.product_package_id.name', store=True, string="Product", readonly=True)
    unity = fields.Selection(related='purchase_order_id.unity', store=True, string="Unité", readonly=True)
    qte_total_unity = fields.Char(related='purchase_order_id.qte_total_unity', store=True, string="Qte/Nbr Total", readonly=True)
    qte_total = fields.Integer(related='purchase_order_id.qte_total', store=True, string="Qte/Nbr", readonly=True)
    qte = fields.Integer(related='purchase_order_id.qte', store=True, string="Qte/Nbr Package", readonly=True)
    qte_prpk = fields.Integer(related='purchase_order_id.qte_prpk', store=True, string="Qte ou Nbr")
    qte_prpk_unity = fields.Char(related='purchase_order_id.qte_prpk_unity', store=True, string="Qte ou Nbr / Unité", readonly=True)
    
    price = fields.Float(digits=(12, 3), help="Prix", string="Prix")
    date_order = fields.Date(string="Date de demande")
    datefinal_order = fields.Date(string="Date d'expiration")
    description = fields.Text(string="Description")
    
    @api.model
    def _get_next_providerOrdername(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.provider_order.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.provider_order.seq')
        result = super(provider_order, self).create(vals)
        return result 
