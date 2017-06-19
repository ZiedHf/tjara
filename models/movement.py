# -*- coding: utf-8 -*-

from odoo import models, fields, api

class movement(models.Model):

    _name = 'tjara.movement'
    
    name = fields.Char(string='Movement', default=lambda self: self._get_next_movementname(), store=True, readonly=True)
    type_movement = fields.Selection([('entry', 'Entry'), ('exit', 'Exit'), ('canceled', 'Canceled')], string='Type', required=True)
    date = fields.Date(string='Movement Creating Date', default=fields.datetime.now())
    
    product_id = fields.Many2one('tjara.product_package', string='Product', required=True)
    voucher_entry_id = fields.Many2one(string='Voucher Entry', comodel_name='tjara.voucher_entry', required=True)
    depot_id = fields.Many2one('tjara.depot', string='Depot', required=True)
    stock_id = fields.Many2one('tjara.stock', string='Stock', required=True)
    
    qte = fields.Float(string='Quantity', required=True)
    qte_total_unity = fields.Char(string="Total Quantity", required=True)
    is_created = fields.Boolean(string='Created', default=False)
#     bonlivraison_id=fields.Many2one(
#         string='Réf bon de livraison',
#         comodel_name='gctjara.bonlivraison'
#     )
    @api.model
    def _get_next_movementname(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.movement.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
     
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.movement.seq')
        vals['is_created'] = True
        result = super(movement, self).create(vals)
        return result