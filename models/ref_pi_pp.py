# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ref_pi_pp(models.Model):
    _name = 'tjara.ref_pi_pp' # Ref purchase_inquiry _ purchase order _ product package

#     ref_po_pp_id = fields.Many2one('tjara.ref_po_pp', required=True, index=True)
    
#     name = fields.Char(related="ref_po_pp_id.product_package_id.name", string='Product Name')
    
    name = fields.Char(string='ref pi pp', default='Provider Inquiry / Product Package')
    product_package_id = fields.Many2one('tjara.product_package', ondelete='cascade', required=True, index=True)
    purchase_inquiry_id = fields.Many2one('tjara.purchase_inquiry', ondelete='cascade', required=True, index=True)
    
    qte = fields.Integer(string='Number Package', required=True)
    qte_prpk = fields.Float(related='product_package_id.qte', digits=(12, 3), help="Qte or Nbr per package", store=True, string="Qte ou Nbr", readonly=True)
    unity = fields.Selection(related='product_package_id.package_id.unity', store=True, string="Unity", readonly=True)
    qte_prpk_unity = fields.Char(string="Qte or Nbr / Unity", store=True, compute="_compute_qte_prpk_unity")
    qte_total = fields.Integer(string='Total Quantity', compute='_compute_qte_total', store=True)
    qte_total_unity = fields.Char(string="Total Qte/Unity", compute="_compute_qte_total_unity", store=True)
    
    initial_price = fields.Float(string='Initial Price', digits=(12, 3), help="Initial Price", required=True)
    ht_price = fields.Float(string='HT Price', digits=(12, 3), help="Ht Price", store=True, compute="compute_ht_price", readonly=True)
    price = fields.Float(string='Price', digits=(12, 3), help="Price", store=True, compute="compute_price", readonly=True)
    
    discount = fields.Float(string='Discount (%)', digits=(4, 2), help="Discount", default=0)
    tax = fields.Float(string='Tax (%)', digits=(4, 2), help="Tax", default=0)
    
#     _sql_constraints = [
#         ('check_qte', 'Error', 'Please set a valid quantity'),
# #         ('check_discount', 'Error', 'Please set a valid discount'),
# #         ('check_tax', 'Error', 'Please set a valid tax'),
# #         ('product_unique', 'unique(product_package_id,purchase_inquiry_id)', 'There is some duplicated products...!')
#     ]
    
    @api.multi
    @api.depends('initial_price', 'discount')
    def compute_ht_price(self):
        for rec in self:
            initial_price = rec.initial_price
            if(rec.discount >= 0)and(rec.discount <= 100):
                rec.ht_price = (initial_price*(100 - rec.discount))/100
            else:
                rec.ht_price = initial_price
    
    @api.multi
    @api.depends('ht_price', 'tax')
    def compute_price(self):
        for rec in self:
            if(rec.tax >= 0)and(rec.tax <= 100):
                rec.price = rec.ht_price*(1 + rec.tax/100)
            else:
                rec.price = rec.ht_price
    
    @api.constrains('discount')
    @api.multi
    def check_discount(self):
        for rec in self:
            if(rec.discount < 0)or(rec.discount > 100):
                raise ValidationError("Please set a valid discount : %s" % rec.discount)
            
    @api.constrains('tax')
    @api.multi
    def check_tax(self):
        for rec in self:
            if(rec.tax < 0)or(rec.tax > 100):
                raise ValidationError("Please set a valid tax : %s" % rec.tax)
            
    @api.constrains('qte')
    @api.multi
    def check_qte(self):
        for rec in self:
            if(rec.qte < 1):
                raise ValidationError("Please set a valid quantity : %s" % rec.qte)

    @api.depends('qte_prpk', 'qte')
    @api.multi
    def _compute_qte_total(self):
        for rec in self:
            if(isinstance(rec.qte, int))and(isinstance(rec.qte_prpk, float)):
                rec.qte_total = rec.qte * rec.qte_prpk
    
    @api.multi
    @api.depends('qte', 'qte_prpk', 'unity')
    def _compute_qte_total_unity(self):
        for rec in self:
            if((rec.unity)and(isinstance(rec.qte_total, int))):
                rec.qte_total_unity = str(rec.qte * rec.qte_prpk) + " " + rec.unity
        
    @api.multi
    @api.depends('qte_prpk', 'unity')
    def _compute_qte_prpk_unity(self):
        for rec in self:
            if((rec.unity)and(isinstance(rec.qte_prpk, float))and(rec.qte_prpk > 0)):
                rec.qte_prpk_unity = str(rec.qte_prpk) + str(rec.unity) + " / Package"
#     price = fields.Float(string='Price')
#     
#     product = fields.Char(related="ref_po_pp_id.product_package_id.name", string='Product Name', store=True)
#     qte = fields.Integer(related="ref_po_pp_id.qte", string='Quantité / Nombre', store=True)
#     qte_prpk = fields.Integer(related='ref_po_pp_id.qte_prpk', store=True, string="Qte ou Nbr")
#     unity = fields.Selection(related='ref_po_pp_id.unity', store=True, string="Unité")
#     qte_prpk_unity = fields.Char(related="ref_po_pp_id.qte_prpk_unity", store=True)
#     qte_total = fields.Integer(related="ref_po_pp_id.qte_total", string='Quantité totale', store=True)
#     qte_total_unity = fields.Char(related="ref_po_pp_id.qte_total_unity", string="Quantité Totale", store=True)