# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class provider_order(models.Model):
    _name = 'tjara.provider_order'
        
    name = fields.Char(string='Provider Order', default=lambda self: self._get_next_providerOrdername(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('done', 'Done'), ('canceled', 'Canceled'), ('invoiced', 'Invoiced')], string='State', default='draft')
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='cascade', string="Purchase Order", index=True, required=True, domain=[('state', '=', 'inprogress')], readonly=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True)
#     provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
    product = fields.Char(related='purchase_order_id.product_package_id.name', store=True, string="Product", readonly=True)
    product_id = fields.Many2one(related='purchase_order_id.product_package_id', store=True, string="Product", readonly=True)
    unity = fields.Selection(related='purchase_order_id.unity', store=True, string="Unité", readonly=True)
#     qte_total_unity = fields.Char(related='purchase_order_id.qte_total_unity', store=True, string="Qte/Nbr Total", readonly=True)
    qte_total_unity = fields.Char(string="Qte/Nbr Total", compute="_compute_qte_total_unity", readonly=True)
    qte_total = fields.Integer(string="Qte/Nbr", compute="_compute_qte_total", readonly=True)
    qte = fields.Integer(string="Qte/Nbr Package", help="Qte")
    qte_prpk = fields.Integer(related='purchase_order_id.qte_prpk', store=True, string="Qte ou Nbr", readonly=True)
    qte_prpk_unity = fields.Char(related='purchase_order_id.qte_prpk_unity', store=True, string="Qte ou Nbr / Unité", readonly=True)
    
    price = fields.Float(digits=(12, 3), help="Prix", string="Prix")
    date_order = fields.Date(string="Date de demande")
    datefinal_order = fields.Date(string="Date d'expiration")
    description = fields.Text(string="Description")
    
#     purchase_invoice_id = fields.Many2many('tjara.purchase_invoice', ondelete='cascade', string="Purchase Invoice")
    purchase_invoice_id = fields.Many2one('tjara.purchase_invoice', ondelete='cascade', string="Purchase Invoice")
    
#     @api.depends('unity', 'qte_prpk', 'qte_total')
    @api.depends('qte', 'qte_prpk')
    def _compute_qte_total(self):
        for rec in self:
            if((isinstance(rec.qte, int))and(isinstance(rec.qte, int))):
                rec.qte_total = rec.qte * rec.qte_prpk

    @api.depends('qte', 'qte_prpk', 'unity')
    def _compute_qte_total_unity(self):
        for rec in self:
            if((rec.unity)and(isinstance(rec.qte_total, int))):
                rec.qte_total_unity = str(rec.qte * rec.qte_prpk) + " " + rec.unity

#     @api.multi
#     def _get_value_qte_total_unity(self):
#         for rec in self:
#             rec.qte_total_unity = str(rec.qte_total) + " " + rec.unity
        
                        
    @api.model
    def _get_next_providerOrdername(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.provider_order.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.provider_order.seq')
        result = super(provider_order, self).create(vals)
        return result 


    @api.one
    def draft_progressbar(self):
        if(self.state != 'invoiced'):
            if(self.provider_id.id):
                self.write({
                'state': 'draft'
                })
            else:
                raise ValidationError("Please set a provider to this order.")
        else:
                raise ValidationError("This provider order is invoiced !")
    @api.one
    def inprogress_progressbar(self):
        if(self.state == 'invoiced'):
            raise ValidationError("This provider order is invoiced !")
        elif(not(self.provider_id.id)):
            raise ValidationError("Please set a valid provider to this provider order !")
        elif(self.price <= 0):
            raise ValidationError("Please set a price to this provider order !")
        else:
            self.write({
            'state': 'inprogress'
            })
            
    
    @api.one
    def canceled_progressbar(self):
        if(self.state != 'invoiced'):
            self.write({
            'state': 'canceled'
            })
        else:
            raise ValidationError("This provider order is invoiced !")
        
    @api.one
    def done_progressbar(self):
        if(self.price <= 0):
            raise ValidationError("Please set a price to this provider order !")
        elif(not(self.provider_id.id)):
            raise ValidationError("Please set a valid provider to this provider order !")
        elif(self.state == 'invoiced'):
            raise ValidationError("This provider order is invoiced !")
        else:
            self.write({
            'state': 'done'
            })
    