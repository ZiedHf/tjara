# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class provider_regulation(models.Model):
    _name = 'tjara.provider_regulation'
        
    name = fields.Char(string='Provider Regulation', default=lambda self: self._get_next_providerRegulationName(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    purchase_payment_id = fields.Many2one('tjara.purchase_payment', ondelete='cascade', string='Purchase Payment', domain=[('state', 'in', ['draft', 'inprogress'])], required=True)
    provider_id = fields.Many2one(related='purchase_payment_id.provider_id', string="Provider", readonly=True)
    total_price = fields.Float(related='purchase_payment_id.total_price', string='Total Price', readonly=True)
    total_price_pr = fields.Float(related='purchase_payment_id.total_price_pr', string='Amount payed', readonly=True)
    amount_to_pay = fields.Float(related='purchase_payment_id.amount_to_pay', string='Amount to pay', readonly=True) 
    price = fields.Float(digits=(12, 3), string='Amount', default=0)
    is_created = fields.Boolean(string='Created', default=False)
    
    @api.one
    @api.constrains('price')
    def _check_description(self):
        if self.price <= 0:
            raise ValidationError('Please set an amount to this provider regulation...!')
    
    @api.model
    def _get_next_providerRegulationName(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.provider_regulation.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
        if(vals['purchase_payment_id']):
            
            purchase_payment = self.env['tjara.purchase_payment'].browse(vals['purchase_payment_id'])
            if(not(purchase_payment)):
                raise ValidationError("A valid purchase payment is required.")
                return False
            print purchase_payment.amount_to_pay
            print vals['price']
            
            if(purchase_payment.amount_to_pay - vals['price'] > 0):
                purchase_payment.state = 'inprogress' 
            else:
                purchase_payment.state = 'done'
                
            vals['name'] = self.env['ir.sequence'].next_by_code('tjara.provider_regulation.seq')
            vals['is_created'] = True
            vals['state'] = 'done'
            result = super(provider_regulation, self).create(vals)
            return result