# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ref_po_pp(models.Model):
    _name = 'tjara.ref_po_pp' # Ref purchase order _ product package
    
    name = fields.Char(string='ref po pp', store=True, readonly=True)
    product_package_id = fields.Many2one('tjara.product_package', ondelete='cascade', required=True, index=True)
    purchase_order_id = fields.Many2one('tjara.purchase_order', ondelete='cascade', required=True, index=True)
    
    qte = fields.Integer(string='Number Package', required=True)
    qte_prpk = fields.Float(related='product_package_id.qte', store=True, digits=(12, 3), help="Qte or Nbr per package", string="Qte ou Nbr", readonly=True)
    unity = fields.Selection(related='product_package_id.package_id.unity', store=True, string="Unity", readonly=True)
    qte_prpk_unity = fields.Char(string="Qte or Nbr / Unity", store=True, compute="_compute_qte_prpk_unity")
    qte_total = fields.Integer(string='Total Quantity', compute='_compute_qte_total', store=True)
    qte_total_unity = fields.Char(string="Total Quantity", compute="_compute_qte_total_unity", store=True)
    
    @api.constrains('product_package_id', 'purchase_order_id')
    def check_qte(self):
        if(rec.qte < 1):
            raise ValidationError("Please set a valid quantity : %s" % rec.qte)
            
            
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