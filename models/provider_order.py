# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from amount_to_text_fr import amount_to_text_fr

class provider_order(models.Model):
    _name = 'tjara.provider_order'
        
    name = fields.Char(string='Provider Order', default=lambda self: self._get_next_providerOrdername(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('done', 'Done'), ('canceled', 'Canceled'), ('invoiced', 'Invoiced')], string='State', default='draft')
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='cascade', string="Purchase Order", index=True)
    purchase_inquiry_id = fields.Many2one('tjara.purchase_inquiry', ondelete='cascade', string="Purchase Inquiry", index=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
    
    ref_provider_order_pp_ids = fields.One2many('tjara.ref_provider_order_pp', 'provider_order_id', ondelete='cascade', string="Ref po pp")
    voucher_entry_id = fields.Many2one('tjara.voucher_entry', ondelete='cascade', string="Voucher Entry", index=True)
    
    is_created = fields.Boolean(string='Created', default=False)
    
    total_initial_price = fields.Float(string="Total Initial Price", digits=(12, 3), compute="_compute_total_initial_price", readonly=True)
    total_ht_price = fields.Float(string="Total HT Price", digits=(12, 3), compute="_compute_total_ht_price", readonly=True)
    total_price = fields.Float(string="Total Price", digits=(12, 3), compute="_compute_total_price", readonly=True)
#     total_price = fields.Float(digits=(12, 3), help="Prix", string="Prix", compute="_compute_total_price", readonly=True, store=True)
    amount_to_text = fields.Char(string='Price In Words', store=True, readonly=True, compute='_compute_amount_to_text')
    
    
    date_order = fields.Date(string="Date de demande")
    datefinal_order = fields.Date(string="Date d'expiration")
    description = fields.Text(string="Description")

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self:self.env.user.company_id.currency_id)
# domain=lambda self: [('reconcile', '=', True), ('user_type_id.id', '=', self.env.ref('account.data_account_type_current_assets').id)],

#     purchase_invoice_id = fields.Many2many('tjara.purchase_invoice', ondelete='cascade', string="Purchase Invoice")
#     purchase_invoice_id = fields.Many2one('tjara.purchase_invoice', ondelete='cascade', string="Purchase Invoice", readonly=True)
    
    @api.depends('total_price')
    @api.one
    def _compute_amount_to_text(self):
        self.amount_to_text = amount_to_text_fr(self.total_price, self.env.user.company_id.currency_id.symbol)
    
    @api.depends('ref_provider_order_pp_ids.ht_price')
    @api.multi
    def _compute_total_ht_price(self):
        for purchase_inquiry in self:
            total_ht_price = 0
            if(purchase_inquiry.ref_provider_order_pp_ids):
                for ref_pi_pp in purchase_inquiry.ref_provider_order_pp_ids:
                    total_ht_price = total_ht_price + ref_pi_pp.ht_price
            purchase_inquiry.total_ht_price = total_ht_price
    
    @api.depends('ref_provider_order_pp_ids.initial_price')
    @api.multi
    def _compute_total_initial_price(self):
        for purchase_inquiry in self:
            total_initial_price = 0
            if(purchase_inquiry.ref_provider_order_pp_ids):
                for ref_pi_pp in purchase_inquiry.ref_provider_order_pp_ids:
                    total_initial_price = total_initial_price + ref_pi_pp.initial_price
            purchase_inquiry.total_initial_price = total_initial_price
            
    @api.depends('ref_provider_order_pp_ids.price')
    @api.multi
    def _compute_total_price(self):
        for provider_order in self:
            total_price = 0
            if(provider_order.ref_provider_order_pp_ids):
                for ref_provider_order_pp in provider_order.ref_provider_order_pp_ids:
                    total_price = total_price + ref_provider_order_pp.price
            provider_order.total_price = total_price
                    
# #     @api.depends('unity', 'qte_prpk', 'qte_total')
#     @api.depends('qte', 'qte_prpk')
#     def _compute_qte_total(self):
#         for rec in self:
#             if((isinstance(rec.qte, int))and(isinstance(rec.qte, int))):
#                 rec.qte_total = rec.qte * rec.qte_prpk
# 
#     @api.depends('qte', 'qte_prpk', 'unity')
#     def _compute_qte_total_unity(self):
#         for rec in self:
#             if((rec.unity)and(isinstance(rec.qte_total, int))):
#                 rec.qte_total_unity = str(rec.qte * rec.qte_prpk) + " " + rec.unity
# 
# #     @api.multi
# #     def _get_value_qte_total_unity(self):
# #         for rec in self:
# #             rec.qte_total_unity = str(rec.qte_total) + " " + rec.unity
#         
#                         
    @api.model
    def _get_next_providerOrdername(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.provider_order.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
     
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.provider_order.seq')
        vals['is_created'] = True
        result = super(provider_order, self).create(vals)
        return result 

    @api.one
    @api.model
    def createVoucherEntry(self):
        record = self.env['tjara.voucher_entry'].create({
                'provider_order_id':self.id
            })
        for ref in self.ref_provider_order_pp_ids:
            self.env['tjara.ref_ve_pp'].create({
                'voucher_entry_id':record.id,
                'product_package_id':ref.product_package_id.id,
                'qte':ref.qte
            })
        self.write({
            'voucher_entry_id': record.id,
            'state':'done'
            })
#         for ref in self.ref_provider_order_pp_ids:
#             ref.voucher_entry_id = record.id
# 
# 
#     @api.one
#     def draft_progressbar(self):
#         if(self.state != 'invoiced'):
#             if(self.provider_id.id):
#                 self.write({
#                 'state': 'draft'
#                 })
#             else:
#                 raise ValidationError("Please set a provider to this order.")
#         else:
#                 raise ValidationError("This provider order is invoiced !")
    @api.one
    def inprogress_progressbar(self):
        if(self.state == 'draft'):
            self.write({
            'state': 'inprogress'
            })
#             
#     
#     @api.one
#     def canceled_progressbar(self):
#         if(self.state != 'invoiced'):
#             self.write({
#             'state': 'canceled'
#             })
#         else:
#             raise ValidationError("This provider order is invoiced !")
#         
#     @api.one
#     def done_progressbar(self):
#         if(self.price <= 0):
#             raise ValidationError("Please set a price to this provider order !")
#         elif(not(self.provider_id.id)):
#             raise ValidationError("Please set a valid provider to this provider order !")
#         elif(self.state == 'invoiced'):
#             raise ValidationError("This provider order is invoiced !")
#         else:
#             self.write({
#             'state': 'done'
#             })
    