# -*- coding: utf-8 -*-

from odoo import models, fields, api

class purchase_order(models.Model):
    _name = 'tjara.purchase_order'
    
#     name = fields.Char(string='Purchase Name', default=lambda self: self.env['ir.sequence'].next_by_code('tjara.purchase_order.seq'))
    name = fields.Char(string='Purchase Name', default=lambda self: self._get_next_purchasename(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('accepted', 'Accepted'), ('inprogress', 'In progress'), ('done', 'Done')], string='State', default='draft')
#     product_package_ids = fields.Many2many('tjara.product_package', ondelete='cascade', string="Product _ Package", index=True)
    product_package_id = fields.Many2one('tjara.product_package', ondelete='cascade', string="Product _ Package", index=True, required=True) 
    qte = fields.Integer(string='Quantité / Nombre', required=True)
    qte_prpk = fields.Integer(related='product_package_id.qte', store=True, string="Qte ou Nbr")
    unity = fields.Selection(related='product_package_id.package_id.unity', store=True, string="Unité")
    qte_prpk_unity = fields.Char(string="Qte ou Nbr / Unité", store=True, compute="_compute_qte_prpk_unity")
    qte_total = fields.Integer(string='Quantité totale', compute='_compute_qte_total', store=True)
    qte_total_unity = fields.Char(string="Quantité Totale", compute="_compute_qte_total_unity", store=True)
    purchase_inquiry_ids = fields.One2many('tjara.purchase_inquiry', 'purchase_order_id', string="Demande d'offre")
    provider_order_ids = fields.One2many('tjara.provider_order', 'purchase_order_id', string="Provider Order")

    @api.model
    def _get_next_purchasename(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.purchase_order.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_order.seq')
        result = super(purchase_order, self).create(vals)
        return result 

    @api.onchange('product_package_id', 'qte_prpk')
    @api.depends('qte')
    def _compute_qte_total(self):
        for rec in self:
            if(isinstance(rec.qte, int))and(isinstance(rec.qte_prpk, int)):
                rec.qte_total = rec.qte * rec.qte_prpk
    
    @api.depends('unity')
    @api.onchange('qte_total')
    def _compute_qte_total_unity(self):
        for rec in self:
            if((rec.unity)and(isinstance(rec.qte_total, int))):
                rec.qte_total_unity = str(rec.qte_total) + " " + rec.unity
        
    @api.onchange('qte_prpk', 'unity')
    def _compute_qte_prpk_unity(self):
        for rec in self:
            if((rec.unity)and(isinstance(rec.qte_prpk, int))and(rec.qte_prpk > 0)):
                rec.qte_prpk_unity = str(rec.qte_prpk) + str(rec.unity) + " / Package"
                
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
    @api.one
    def done_progressbar(self):
        self.write({
        'state': 'done',
        })
        
    #This function is triggered when the user clicks on the button 'Done'
    @api.one
    @api.model
    def done_progressbar(self):
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
#         result = super(purchase_order, self).create(vals)
        self.write({
        'state': 'done',
        })