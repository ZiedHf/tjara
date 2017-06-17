# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class voucher_entry(models.Model):
    _name = 'tjara.voucher_entry'
        
    name = fields.Char(string='Voucher Entry', default=lambda self: self._get_next_voucherentry(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('done', 'Done'), ('canceled', 'Canceled')], string='State', default='draft')
    provider_order_id = fields.Many2one('tjara.provider_order', ondelete='cascade', string="Provider Order", index=True, required=True, readonly=True)
#     ref_voucher_entry_ids = fields.One2many('tjara.ref_provider_order_pp', 'voucher_entry_id', ondelete='cascade', string="Ref po pp", readonly=True)
    ref_ve_pp_ids = fields.One2many('tjara.ref_ve_pp', 'voucher_entry_id', ondelete='cascade', string="Ref ve pp") 
    is_created = fields.Boolean(string='Created', default=False)
    
    provider_id = fields.Many2one(related='provider_order_id.provider_id', readonly=True)
    date_order = fields.Date(related="provider_order_id.date_order", string="Entry to stock on", readonly=True)
    datefinal_order = fields.Date(related="provider_order_id.datefinal_order", string="Expiration date", readonly=True)
    description = fields.Text(string="Description")
    
    depot_id = fields.Many2one('tjara.depot', ondelete='cascade', string='Depot', index=True)
                     
    @api.one
    def addToStock(self):
        if(not(self.provider_order_id)):
            raise ValidationError("There is no provider order declared !")
        elif(not(self.ref_ve_pp_ids)):
            raise ValidationError("There is no product in this voucher entry !")
        elif(not(self.provider_id)):
            raise ValidationError("The provider order is not declared !")
        elif(not(self.depot_id)):
            raise ValidationError("The depot is not declared !")
        elif(self.state == 'done'):
            raise ValidationError("This voucher entry is done !")
        else:
            stock = self.env['tjara.stock']
            for ref_product in self.ref_ve_pp_ids:
                if((isinstance(ref_product.product_package_id.id, int))and(isinstance(self.depot_id.id, int))):
                    stock_id = stock.search(['&', ('product_package_id', '=', ref_product.product_package_id.id), ('depot_id', '=', self.depot_id.id)])
                    if(not(stock_id)):
                        stock.create({
                                'depot_id':self.depot_id.id,
                                'product_package_id':ref_product.product_package_id.id,
                                'in_stock':ref_product.qte_total
                            })
                    else:
                        this_stock = stock.browse([stock_id._ids[0]])
                        this_stock.in_stock = this_stock.in_stock + ref_product.qte_total
                    self.state = 'done'
                    
    @api.model
    def _get_next_voucherentry(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.voucher_entry.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
     
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.voucher_entry.seq')
        vals['is_created'] = True
        result = super(voucher_entry, self).create(vals)
        return result