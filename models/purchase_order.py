# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class purchase_order(models.Model):
    _name = 'tjara.purchase_order'
    
#     name = fields.Char(string='Purchase Name', default=lambda self: self.env['ir.sequence'].next_by_code('tjara.purchase_order.seq'))
    name = fields.Char(string='Purchase Name', default=lambda self: self._get_next_purchasename(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('accepted', 'Accepted'), ('inprogress', 'In progress'), ('done', 'Done'), ('canceled', 'Canceled')], string='State', default='draft')
    ref_po_pp_ids = fields.One2many('tjara.ref_po_pp', 'purchase_order_id', ondelete='cascade', string="Ref po pp", required=True)
    priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string='Priority', default='medium')
    add_date = fields.Date(string="Date")
    purchase_inquiry_ids = fields.One2many('tjara.purchase_inquiry', 'purchase_order_id', string="Purchase Inquiry")
    is_created = fields.Boolean(string='Created', default=False)
    provider_id = fields.Many2one('tjara.provider', string="Provider suggested", ondelete="cascade")
    

    @api.model
    def _get_next_purchasename(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.purchase_order.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_order.seq')
        vals['is_created'] = True
        
#         for ref_line in vals['ref_po_pp_ids']:
#             
            
        result = super(purchase_order, self).create(vals)
        return result 

#     @api.onchange('product_package_id', 'qte_prpk')
#     @api.depends('qte')
#     def _compute_qte_total(self):
#         for rec in self:
#             if(isinstance(rec.qte, int))and(isinstance(rec.qte_prpk, int)):
#                 rec.qte_total = rec.qte * rec.qte_prpk
#     
#     @api.depends('qte', 'qte_prpk', 'unity')
#     def _compute_qte_total_unity(self):
#         for rec in self:
#             if((rec.unity)and(isinstance(rec.qte_total, int))):
#                 rec.qte_total_unity = str(rec.qte * rec.qte_prpk) + " " + rec.unity
#         
#     @api.multi
#     @api.depends('qte_prpk', 'unity')
#     def _compute_qte_prpk_unity(self):
#         for rec in self:
#             if((rec.unity)and(isinstance(rec.qte_prpk, int))and(rec.qte_prpk > 0)):
#                 rec.qte_prpk_unity = str(rec.qte_prpk) + str(rec.unity) + " / Package"
                
    #This function is triggered when the user clicks on the button 'Set to concept'
    @api.one
    def draft_progressbar(self):
        self.write({
            'state': 'draft',
        })
     
    #This function is triggered when the user clicks on the button 'In progress'
    @api.one
    def accepted_progressbar(self):
        self.write({
        'state': 'accepted'
        })
        
    #This function is triggered when the user clicks on the button 'Set to started'
    @api.one
    def inprogress_progressbar(self):
        self.write({
        'state': 'inprogress'
        })
     
    #This function is triggered when the user clicks on the button 'Done'
#     @api.one
#     def done_progressbar(self):
#         self.write({
#         'state': 'done',
#         })
        
    @api.one
    @api.model
    def createPO_progressbar(self):
        if((self.state == 'done')):
            raise ValidationError("This provider order is done.")
        elif((self.state == 'canceled')):
            raise ValidationError("This provider order is canceled.")
        elif((self.state == 'inprogress')):
            record = self.env['tjara.provider_order'].create({
                    'purchase_order_id':self.id,
                    'product':self.product_package_id,
                    'unity':self.unity,
                    'qte_total_unity':self.qte_total_unity,
                    'qte_total':self.qte_total,
                    'qte':self.qte,
                    'qte_prpk':self.qte_prpk,
                    'qte_prpk_unity':self.qte_prpk_unity
                })
        else:
            raise ValidationError("This provider order is not in progress yet.")
        
    #This function is triggered when the user clicks on the button 'Done'
    @api.one
    @api.model
    def done_progressbar(self):
        if(self.provider_order_ids):
            isset_provider_order = True
            invoiced_provider_order = False
            for rec in self.provider_order_ids:
                if(rec.state == 'inprogress'):
                    isset_provider_order = False
                if(rec.state == 'invoiced'):
                    invoiced_provider_order = True

            if(not(isset_provider_order)):
                raise ValidationError("Some provider order still not done or canceled yet !")
            elif(not(invoiced_provider_order)):
                raise ValidationError("There is no invoiced provider order !")
            else:
                self.write({
                    'state': 'done',
                })
        else:
            raise ValidationError("You need to create a provider order to this purchase order before.")
    
    @api.multi
    @api.returns('self')
    def return_confirmation(self):
        return {
            'name': 'Are you sure?',
            'type': 'ir.actions.act_window',
            'res_model': 'tjara.confirm_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
        
    @api.multi
    def canceled_progressbar(self):
        self.write({
            'state': 'canceled',
        })
#         #check if there is provider orders done or in progress
#         isset_provider_orders = True
#         for rec in self.provider_order_ids:
#             if((rec.state == 'done')or(rec.state == 'inprogress')or(rec.state == 'invoiced')):
#                 isset_provider_orders = False
#                 break
#         
#         if(not(isset_provider_orders)):
#             raise ValidationError("You can't cancel this purchase order. There is provider orders in progress, done or invoiced.")
#             return False
#         
#         #check if there is provider orders done or in progress    
#         isset_purchase_inquiries = True
#         for rec in self.purchase_inquiry_ids:
#             if((rec.state == 'sent')or(rec.state == 'received')):
#                 isset_purchase_inquiries = False
#                 break
#         
#         if(not(isset_purchase_inquiries)):    
#             return {
#                 'name': 'Are you sure?',
#                 'type': 'ir.actions.act_window',
#                 'res_model': 'tjara.confirm_wizard',
#                 'view_mode': 'form',
#                 'view_type': 'form',
#                 'target': 'new',
#                 'context':{'active_id': self.id}
#             }
#         
#         self.set_state_to_canceled(False)

    @api.multi
    def set_purchaseinqueries_to_refused(self, purchase_order_id):
        provider_order = self.browse([purchase_order_id])
        for purchase_inquiry in provider_order.purchase_inquiry_ids:
            purchase_inquiry.state = 'refused'
        self.set_state_to_canceled(provider_order)
        
    @api.multi
    def nothingfunction(self, purchase_order_id):
        print 'Dont do anything here'

    @api.multi
    def set_state_to_canceled(self, provider_order):
        if(provider_order):
            provider_order.state = 'canceled'
        else:
            self.write({
                'state': 'canceled',
            })
            
#     @api.one
#     def create_purchase_inquiry(self):
#         if(self.state == 'inprogress'):
#             record = self.env['tjara.purchase_inquiry'].create({
#                 'purchase_order_id':self.id
#             })
#             if(record):
#                 for ref in self.ref_po_pp_ids:
#                     record_ref_pi = self.env['tjara.ref_pi_pp'].create({
#                         'purchase_order_id':record.id,
#                         'ref_po_pp_id':ref.id
#                     })
            