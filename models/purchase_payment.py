# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class purchase_payment(models.Model):
    _name = 'tjara.purchase_payment'
        
    name = fields.Char(string='Purchase Invoice', default=lambda self: self._get_next_purchasePaymentname(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    purchase_invoice_ids = fields.One2many('tjara.purchase_invoice', 'purchase_payment_id', string="Purchase Payment")
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
#     provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True)
#     total_price = fields.Float(digits=(12, 3), string='Total Price', compute='_total_price')
#     provider_order_ids = fields.Many2one('tjara.provider_order', ondelete='cascade', string="Provider Order")
#     provider_order_ids = fields.Many2many('tjara.provider_order', ondelete='cascade', string="Provider Order")
#     product_package_ids = fields.Many2many('tjara.product_package', string="Product", readonly=True)
#     product_package_ids = fields.Many2many('account.payment', 'account_invoice_payment_rel', 'invoice_id', 'payment_id', string="Payments", copy=False, readonly=True)

    @api.onchange('provider_id')
    def _onchange_provider_id(self):
        res = {}
        if(self.provider_id.id):
            domain = [('state', '=', 'draft'), ('provider_id', '=', self.provider_id.id)]
        else:
            domain = [('state', '=', 'draft')]
        res['domain'] = {'purchase_invoice_ids': domain}
        res['value'] = {'purchase_invoice_ids': False}
        return res

    @api.model
    def _get_next_purchasePaymentname(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.purchase_payment.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_payment.seq')
        result = super(purchase_payment, self).create(vals)
        return result 