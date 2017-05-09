# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class purchase_inquiry(models.Model):
    _name = 'tjara.purchase_inquiry'
    
    name = fields.Char(string='Purchase Inquiry Name', default=lambda self: self._get_next_purchaseInquiryname(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'), ('received', 'Received'), ('accepted', 'Accepted'), ('refused', 'Refused')], string='State', default='draft')
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='cascade', string="Purchase Order", index=True, required=True, domain=[('state', '=', 'inprogress')])
    product = fields.Char(related='purchase_order_id.product_package_id.name', store=False, string="Product", readonly=True)
    qte_total_unity = fields.Char(related='purchase_order_id.qte_total_unity', store=False, string="Qte/Nbr Total", readonly=True)
    qte = fields.Integer(related='purchase_order_id.qte', store=False, string="Qte/Nbr Package", readonly=True)
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
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_inquiry.seq')
        result = super(purchase_inquiry, self).create(vals)
        return result 

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
            self.write({
            'state': 'accepted'
            })
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