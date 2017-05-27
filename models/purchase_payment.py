# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError

class purchase_payment(models.Model):
    _name = 'tjara.purchase_payment'
        
    name = fields.Char(string='Purchase Invoice', default=lambda self: self._get_next_purchasePaymentname(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    purchase_invoice_ids = fields.One2many('tjara.purchase_invoice', 'purchase_payment_id', string="Purchase Invoice", required=True)
    provider_regulation_ids = fields.One2many('tjara.provider_regulation', 'purchase_payment_id', string="Provider Regulation", readonly=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
    total_price = fields.Float(digits=(12, 3), string='Total Price', compute='_compute_total_price')
    is_created = fields.Boolean(string='Created', default=False)
    pi_canceled = fields.Html(string='Purchase Invoice', readonly=True)
    total_price_canceled = fields.Float(digits=(12, 3), string='Total Price', default=0)
    pricetoshow = fields.Float(digits=(12, 3), string='Total Price', compute='_total_price_toshow')
    total_price_pr = fields.Float(digits=(12, 3), string='Total Price Provider Regulations', default=0, compute='_total_price_pr')
    amount_to_pay = fields.Float(digits=(12, 3), string='Amount To Pay', default=0, compute='_amount_to_pay')

    @api.depends('total_price_pr', 'total_price')
    @api.multi
    def _amount_to_pay(self):
        for purchase_payment in self:
            purchase_payment.amount_to_pay = purchase_payment.total_price - purchase_payment.total_price_pr

    @api.depends('provider_regulation_ids')
    @api.multi
    def _total_price_pr(self):
        for purchase_payment in self:
            total_price_pr = 0
            if(purchase_payment.provider_regulation_ids):
                for provider_regulation in purchase_payment.provider_regulation_ids:
                    total_price_pr += provider_regulation.price
            purchase_payment.total_price_pr += total_price_pr
          
    @api.depends('total_price', 'total_price_canceled')
    @api.multi
    def _total_price_toshow(self):
        for rec in self:
            if(rec.total_price > 0):
                rec.pricetoshow = rec.total_price
            else:
                rec.pricetoshow = rec.total_price_canceled
                 
    @api.depends('purchase_invoice_ids')
    def _compute_total_price(self):
        for rec in self:
            total_price = 0
            for purchase_invoice in rec.purchase_invoice_ids:
                total_price += purchase_invoice.total_price
            rec.total_price = total_price
                 
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
        if(vals['purchase_invoice_ids'][0]):
            providers = []
            purchase_invoice_ids = [item[1] for item in vals['purchase_invoice_ids']]
            for purchase_invoice_id in purchase_invoice_ids:
                purchase_invoice = self.env['tjara.purchase_invoice'].browse(purchase_invoice_id)
                providers.append(purchase_invoice.provider_id.id)
            print len(providers)
            print set(providers)
            print len(set(providers))
            if(len(set(providers)) > 1):
                raise ValidationError("The purchase invoice belong to different providers !")
            else:
                for purchase_invoice_id in purchase_invoice_ids:
                    purchase_invoice = self.env['tjara.purchase_invoice'].browse(purchase_invoice_id)
#                     purchase_invoice.state = 'inprogress'
                vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_payment.seq')
                vals['is_created'] = True
                result = super(purchase_payment, self).create(vals)
                return result
        else:
            raise ValidationError("You need to set at least one purchase invoice to this purchase payment.")
          
    @api.one
    def canceled_progressbar(self):
        if(self.state == 'done'):
            raise ValidationError("This purchase payment is done.")
            return False
        else:
            if(self.purchase_invoice_ids):
                total_price_canceled = 0
                pi_canceled = '<ul>'
                for purchase_invoice_id in self.purchase_invoice_ids.ids:
                    purchase_invoice = self.env['tjara.purchase_invoice'].browse(purchase_invoice_id) 
                    purchase_invoice.state = 'draft'
                    total_price_canceled += purchase_invoice.total_price
                    print purchase_invoice.name
                    pi_canceled += '<li>'+purchase_invoice.name+' ==> '+ str(purchase_invoice.total_price) +'</li>'
                pi_canceled += '</ul>'
                print pi_canceled
                self.write({
                    'state': 'canceled',
                    'provider_order_ids':False,
                    'pi_canceled':pi_canceled,
                    'total_price_canceled':total_price_canceled,
                })
         