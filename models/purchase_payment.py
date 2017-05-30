# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError

class purchase_payment(models.Model):
    _name = 'tjara.purchase_payment'
        
    name = fields.Char(string='Purchase Invoice', default=lambda self: self._get_next_purchasePaymentname(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    purchase_invoice_ids = fields.One2many('tjara.purchase_invoice', 'purchase_payment_id', string="Purchase Invoice", readonly=True)
    
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
    total_price = fields.Float(digits=(12, 3), string='Total Price', readonly=True, compute='_compute_total_price', store=True, default=0)
    is_created = fields.Boolean(string='Created', default=False)
    pi_canceled = fields.Html(string='Purchase Invoice', default='')
    total_price_canceled = fields.Float(digits=(12, 3), string='Total Price Canceled', readonly=True)
    pricetoshow = fields.Float(digits=(12, 3), string='Total Price', readonly=True, compute='_total_price_toshow', store=True)
    total_price_pr = fields.Float(digits=(12, 3), string='Total Price Provider Regulations', readonly=True, compute='_total_price_pr', store=True, default=0)
    amount_to_pay = fields.Float(digits=(12, 3), string='Amount To Pay', readonly=True, compute='_amount_to_pay', store=True)

    total_price_pr2 = fields.Float(related="total_price_pr", string='Total Price Provider Regulations')
    amount_to_pay2 = fields.Float(related="amount_to_pay", string='Amount To Pay')
    total_price2 = fields.Float(related="total_price", string='Total Price')
    total_price_canceled2 = fields.Float(related="total_price_canceled", string='Total Price Canceled')
    
    provider_regulation_ids = fields.One2many('tjara.provider_regulation', 'purchase_payment_id', string="Provider Regulation")
    
    @api.depends('provider_regulation_ids', 'total_price', 'total_price_pr')
    def _amount_to_pay(self):
        if((isinstance(self.total_price, float))and(isinstance(self.total_price_pr, float))):
            self.amount_to_pay = self.total_price - self.total_price_pr
        else:
            self.amount_to_pay = 0

    @api.depends('provider_regulation_ids')
    def _total_price_pr(self):
        total_price_pr = 0
        if(self.provider_regulation_ids):
            for provider_regulation in self.provider_regulation_ids:
                if(provider_regulation.state == 'done'):
                    total_price_pr = total_price_pr + provider_regulation.price
        self.total_price_pr = total_price_pr
          
    @api.depends('total_price', 'total_price_canceled')
    def _total_price_toshow(self):
        if((isinstance(self.total_price, float))and(self.total_price > 0)):
            self.pricetoshow = self.total_price
        elif((isinstance(self.total_price_canceled, float))and(self.total_price_canceled > 0)):
            self.pricetoshow = self.total_price_canceled
        else:
            self.pricetoshow = 0
                 
    @api.depends('purchase_invoice_ids')
    def _compute_total_price(self):
        total_price = 0
        for purchase_invoice in self.purchase_invoice_ids:
            total_price = total_price + purchase_invoice.total_price
        self.total_price = total_price
                 
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
            if(len(set(providers)) > 1):
                raise ValidationError("The purchase invoice belong to different providers !")
            else:
                for purchase_invoice_id in purchase_invoice_ids:
                    purchase_invoice = self.env['tjara.purchase_invoice'].browse(purchase_invoice_id)
                    purchase_invoice.state = 'inprogress'
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
                    pi_canceled += '<li>'+purchase_invoice.name+' ==> '+ str(purchase_invoice.total_price) +'</li>'
                pi_canceled += '</ul>'
                self.write({
                    'state': 'canceled',
                    'provider_order_ids':False,
                    'pi_canceled':pi_canceled,
                    'total_price_canceled':total_price_canceled,
                })
         