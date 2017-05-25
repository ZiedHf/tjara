# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class purchase_inquiry(models.Model):
    _name = 'tjara.purchase_inquiry'
    
    name = fields.Char(string='Purchase Inquiry Name', default=lambda self: self._get_next_purchaseInquiryname(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'), ('received', 'Received'), ('accepted', 'Accepted'), ('refused', 'Refused')], string='State', default='draft')
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='cascade', string="Purchase Order", index=True, required=True, domain=[('state', '=', 'inprogress')])
    purchase_order_state = fields.Selection(related='purchase_order_id.state', string="Purchase Order State")
    product = fields.Char(related='purchase_order_id.product_package_id.name', store=True, string="Product", readonly=True)
    qte_total_unity = fields.Char(related='purchase_order_id.qte_total_unity', store=True, string="Qte/Nbr Total", readonly=True)
    qte = fields.Integer(related='purchase_order_id.qte', store=True, string="Qte/Nbr Package", readonly=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Fournisseur", index=True, required=True)
    price = fields.Float(digits=(12, 3), help="Prix", string="Prix")
    date_inquiry = fields.Date(string="Date de demande")
    datefinal_inquiry = fields.Date(string="Date d'expiration")
    description = fields.Text(string="Description")

        
    @api.model
    def _get_next_purchaseInquiryname(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.purchase_inquiry.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    @api.depends('purchase_order_id')
    def create(self, vals):
        state = self.env['tjara.purchase_order'].search([('id', '=', vals['purchase_order_id'])]).state
        if(state == 'inprogress'):
            vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_inquiry.seq')
            result = super(purchase_inquiry, self).create(vals)
            return result
        else:
            raise ValidationError('The purchase order is not in progress yet.')

    #This function is triggered when the user clicks on the button 'Set to concept'
    @api.one
    def draft_progressbar(self):
        self.write({
            'state': 'draft',
        })
     
    #This function is triggered when the user clicks on the button 'In progress'
    @api.one
    def sent_progressbar(self):
        self.write({
        'state': 'sent'
        })
        
    #This function is triggered when the user clicks on the button 'Set to started'
    @api.one
    def received_progressbar(self):
        if(self.price > 0):
            self.write({
            'state': 'received'
            })
        else:
            raise ValidationError('You need to add the price to this purchase inquiry.')
            #return {'warning': {'title': 'Warning', 'message': 'You need to add the price to this purchase inquiry.'}}
     
    #This function is triggered when the user clicks on the button 'Done'
    @api.one
    def accepted_progressbar(self):
        if(self.price > 0):
            record = self.env['tjara.provider_order'].create({
                'purchase_order_id':self.purchase_order_id.id,
                'product':self.product,
                'unity':self.purchase_order_id.unity,
                'qte_total_unity':self.qte_total_unity,
                'qte_total':self.purchase_order_id.qte_total,
                'qte':self.qte,
                'qte_prpk':self.purchase_order_id.qte_prpk,
                'qte_prpk_unity':self.purchase_order_id.qte_prpk_unity,
                'provider_id':self.provider_id.id,
                'price':self.price,
                'date_inquiry':self.date_inquiry,
                'datefinal_inquiry':self.datefinal_inquiry
            })
            if(record):
                self.write({
                'state': 'accepted'
                })
            else:
                raise ValidationError('An error occurred during the creation of the provider order, please try again.')
        else:
            raise ValidationError('You need to add the price to this purchase inquiry.')
        
    #This function is triggered when the user clicks on the button 'Done'
    @api.one
    def refused_progressbar(self):
        if(self.price > 0):
            self.write({
            'state': 'refused'
            })
        else:
            raise ValidationError('You need to add the price to this purchase inquiry.')
        
    @api.one
    @api.model
    def createPO_progressbar(self):
        if((self.state != 'accepted')):
            raise ValidationError("This purchase inquiry is not accepted.")
        elif((self.state == 'accepted')):
            record = self.env['tjara.provider_order'].create({
                    'purchase_order_id':self.purchase_order_id.id,
                    'product':self.product,
                    'unity':self.purchase_order_id.unity,
                    'qte_total_unity':self.qte_total_unity,
                    'qte_total':self.purchase_order_id.qte_total,
                    'qte':self.qte,
                    'qte_prpk':self.purchase_order_id.qte_prpk,
                    'qte_prpk_unity':self.purchase_order_id.qte_prpk_unity,
                    'provider_id':self.provider_id.id,
                    'price':self.price,
                    'date_inquiry':self.date_inquiry,
                    'datefinal_inquiry':self.datefinal_inquiry
                })
        else:
            raise ValidationError("This provider order is not in progress yet.")