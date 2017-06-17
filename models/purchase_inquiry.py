# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class purchase_inquiry(models.Model):
    _name = 'tjara.purchase_inquiry'
    
    name = fields.Char(string='Purchase Inquiry Name', default=lambda self: self._get_next_purchaseInquiryname(), store=True, readonly=True)
#     state = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'), ('received', 'Received'), ('accepted', 'Accepted'), ('refused', 'Refused')], string='State', default='draft')
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='cascade', string="Purchase Order", index=True)
    ref_pi_pp_ids = fields.One2many('tjara.ref_pi_pp', 'purchase_inquiry_id', ondelete='cascade', string="Ref pi po pp")
#     purchase_order_state = fields.Selection(related='purchase_order_id.state', string="Purchase Order State")
#     product = fields.Char(related='purchase_order_id.product_package_id.name', store=True, string="Product", readonly=True)
#     qte_total_unity = fields.Char(related='purchase_order_id.qte_total_unity', store=True, string="Qte/Nbr Total", readonly=True)
#     qte = fields.Integer(related='purchase_order_id.qte', store=True, string="Qte/Nbr Package", readonly=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Fournisseur", index=True, required=True)
    
    total_initial_price = fields.Float(string="Total Initial Price", digits=(12, 3), compute="compute_all_price", readonly=True, store=True)
    total_ht_price = fields.Float(string="Total HT Price", digits=(12, 3), compute="compute_all_price", readonly=True, store=True)
    total_price = fields.Float(string="Total Price", digits=(12, 3), compute="compute_all_price", readonly=True, store=True)
    is_created = fields.Boolean(string='Created', default=False)
#     @api.onchange('ref_pi_pp_ids')
#     def onchange_ref_pi_pp_ids(self):
#         self.purchase_order_id = False

#     @api.onchange('purchase_order_id')
#     def onchange_purchase_order_id(self):
#         for rec in self.ref_pi_pp_ids:
#             rec = False
    
    @api.onchange('purchase_order_id')
    def onchange_purchase_order_id(self):
        record_list = []
        for purchase_order in self.purchase_order_id:
                if(purchase_order.ref_po_pp_ids):
                    for ref in purchase_order.ref_po_pp_ids:
                        record = (0, 0, {
                            'product_package_id':ref.product_package_id.id,
                            'qte':ref.qte,
                            'qte_prpk':ref.qte_prpk,
                            'initial_price':ref.product_package_id.usual_price*ref.qte 
                        })
                        record_list.append(record)
#                         productslist.append()
        return {
                'value': {
                        'ref_pi_pp_ids': record_list
                    }
            }
    
    @api.depends('ref_pi_pp_ids', 'ref_pi_pp_ids.initial_price', 'ref_pi_pp_ids.discount', 'ref_pi_pp_ids.tax')
    def compute_all_price(self):
        total_ht_price = 0
        total_price = 0
        total_initial_price = 0
        for ref_pi_pp in self.ref_pi_pp_ids:
            total_initial_price = total_initial_price + ref_pi_pp.initial_price
            this_ht_price = (ref_pi_pp.initial_price*(100 - ref_pi_pp.discount))/100
            total_ht_price = total_ht_price + this_ht_price
            total_price = total_price + this_ht_price*(1 + ref_pi_pp.tax/100)
        self.total_ht_price = total_ht_price
        self.total_price = total_price
        self.total_initial_price = total_initial_price
    
#     @api.multi
#     @api.depends('ref_pi_pp_ids.initial_price')
#     def compute_total_initial_price(self):
#         for purchase_inquiry in self:
#             total_initial_price = 0
#             if(purchase_inquiry.ref_pi_pp_ids):
#                 for ref_pi_pp in purchase_inquiry.ref_pi_pp_ids:
#                     total_initial_price = total_initial_price + ref_pi_pp.initial_price
#             purchase_inquiry.total_initial_price = total_initial_price
    
    
#     @api.multi
#     @api.depends('ref_pi_pp_ids')
#     def compute_total_price(self):
#         for purchase_inquiry in self:
#             total_price = 0
#             if(purchase_inquiry.ref_pi_pp_ids):
#                 for ref_pi_pp in purchase_inquiry.ref_pi_pp_ids:
#                     total_price = total_price + ref_pi_pp.price
#             purchase_inquiry.total_price = total_price
                    
        
    @api.model
    def _get_next_purchaseInquiryname(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.purchase_inquiry.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
#         state = self.env['tjara.purchase_order'].search([('id', '=', vals['purchase_order_id'])]).state
        vals['is_created'] = True
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_inquiry.seq')
#         set(vals['ref_pi_pp_ids']) & set(vals['name'])

        result = super(purchase_inquiry, self).create(vals)
        return result
#         else:
#             raise ValidationError('The purchase order is not in progress yet.')

#     @api.onchange('purchase_order_id')
    @api.one
    def import_products(self):
        if(not(self.purchase_order_id)):
            raise ValidationError("Please set a valid purchase order !")
#         elif(self.ref_pi_pp_ids):
#             raise ValidationError("Please pursuit this purchase inquiry or delete the product(s) in the list !")
        else:
            #verify if there is no duplicated product
#             pr_list_pi = []
#             pr_list_po = []
#             for ref_pi_pp_id in self.ref_pi_pp_ids:
#                 pr_list_pi.append(ref_pi_pp_id.product_package_id.id)
#             for ref_po_pp_id in self.purchase_order_id.ref_po_pp_ids:
#                 pr_list_po.append(ref_po_pp_id.product_package_id.id)
#              
#             if(bool(set(pr_list_pi) & set(pr_list_po))):
#                 raise ValidationError('The purchase inquiry already contains some products of the provider order.')
            
            for purchase_order in self.purchase_order_id:
                if(purchase_order.ref_po_pp_ids):
                    for ref in purchase_order.ref_po_pp_ids:
#                         if(ref.product_package_id.id in pr_list_pi):
                        record = self.env['tjara.ref_pi_pp'].create({
                            'product_package_id':ref.product_package_id.id,
                            'purchase_inquiry_id':self.id,
                            'qte':ref.qte,
                            'qte_prpk':ref.qte_prpk,
                            'price':0 
                        })


#     #This function is triggered when the user clicks on the button 'Set to concept'
#     @api.one
#     def draft_progressbar(self):
#         self.write({
#             'state': 'draft',
#         })
#      
#     #This function is triggered when the user clicks on the button 'In progress'
#     @api.one
#     def sent_progressbar(self):
#         self.write({
#         'state': 'sent'
#         })
#         
#     #This function is triggered when the user clicks on the button 'Set to started'
#     @api.one
#     def received_progressbar(self):
#         if(self.price > 0):
#             self.write({
#             'state': 'received'
#             })
#         else:
#             raise ValidationError('You need to add the price to this purchase inquiry.')
#             #return {'warning': {'title': 'Warning', 'message': 'You need to add the price to this purchase inquiry.'}}
#      
#     #This function is triggered when the user clicks on the button 'Done'
#     @api.one
#     def accepted_progressbar(self):
#         if(self.price > 0):
#             record = self.env['tjara.provider_order'].create({
#                 'purchase_order_id':self.purchase_order_id.id,
#                 'product':self.product,
#                 'unity':self.purchase_order_id.unity,
#                 'qte_total_unity':self.qte_total_unity,
#                 'qte_total':self.purchase_order_id.qte_total,
#                 'qte':self.qte,
#                 'qte_prpk':self.purchase_order_id.qte_prpk,
#                 'qte_prpk_unity':self.purchase_order_id.qte_prpk_unity,
#                 'provider_id':self.provider_id.id,
#                 'price':self.price,
#                 'date_inquiry':self.date_inquiry,
#                 'datefinal_inquiry':self.datefinal_inquiry
#             })
#             if(record):
#                 self.write({
#                 'state': 'accepted'
#                 })
#             else:
#                 raise ValidationError('An error occurred during the creation of the provider order, please try again.')
#         else:
#             raise ValidationError('You need to add the price to this purchase inquiry.')
#         
#     #This function is triggered when the user clicks on the button 'Done'
#     @api.one
#     def refused_progressbar(self):
#         if(self.price > 0):
#             self.write({
#             'state': 'refused'
#             })
#         else:
#             raise ValidationError('You need to add the price to this purchase inquiry.')
#         
#     @api.one
#     @api.model
#     def createPO_progressbar(self):
#         if((self.state != 'accepted')):
#             raise ValidationError("This purchase inquiry is not accepted.")
#         elif((self.state == 'accepted')):
#             record = self.env['tjara.provider_order'].create({
#                     'purchase_order_id':self.purchase_order_id.id,
#                     'product':self.product,
#                     'unity':self.purchase_order_id.unity,
#                     'qte_total_unity':self.qte_total_unity,
#                     'qte_total':self.purchase_order_id.qte_total,
#                     'qte':self.qte,
#                     'qte_prpk':self.purchase_order_id.qte_prpk,
#                     'qte_prpk_unity':self.purchase_order_id.qte_prpk_unity,
#                     'provider_id':self.provider_id.id,
#                     'price':self.price,
#                     'date_inquiry':self.date_inquiry,
#                     'datefinal_inquiry':self.datefinal_inquiry
#                 })
#         else:
#             raise ValidationError("This provider order is not in progress yet.")