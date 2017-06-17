# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from __builtin__ import str

class product_package(models.Model):
    _name = 'tjara.product_package'
    
    name = fields.Char(string="Name", default="Unknown", compute='_compute_name', store=True)
    product_id = fields.Many2one('tjara.product', ondelete='cascade', string="Product", index=True, required=True)
    package_id = fields.Many2one('tjara.package', ondelete='cascade', string="Package", index=True, required=True)
#     weight = fields.Float(digits=(8, 3), help="Weight")
    qte = fields.Float(string="Quantity / Number", digits=(12, 3), help="Qte or Nbr per package", required=True)
    description = fields.Text(string="Package Description")
#     purchase_order_ids = fields.One2many('tjara.purchase_order', ondelete='cascade', string="Demande d'achat", index=True)
    ref_po_pp_ids = fields.One2many('tjara.ref_po_pp', 'product_package_id', ondelete='cascade', string="Product _ Package", required=True)
    stock_ids = fields.One2many('tjara.stock', 'product_package_id', ondelete='cascade', string="Stocks", required=True)
    
    usual_price = fields.Float(string="Usual Price", digits=(12, 3))
    code = fields.Char(string="Code Product package")
    weight = fields.Char(string="Weight")
    width = fields.Char(string="Width")
    height = fields.Char(string="Height")
    length = fields.Char(string="Length")
    
    _sql_constraints = [
        ('ligne_unique', 'unique (product_id, package_id)', 'Package is already exists for this product...!')
    ]
    
    @api.depends('product_id', 'package_id', 'qte')
    def _compute_name(self):
        for rec in self:
            if((isinstance(rec.product_id.name, unicode))and(isinstance(rec.package_id.name, unicode))and(isinstance(rec.qte, float))):
                rec.name = rec.product_id.name + " - " + rec.package_id.name + " / " + str(rec.qte)

    @api.onchange('package_id')
    def onchange_product_package(self):
        for object in self:
            if object.product_id:
                existing_ids = self.env["tjara.product_package"].search([('package_id', '=', object.package_id.id), ('product_id.name', '=', object.product_id.name)], limit=1)
                if len(existing_ids) > 0:
                    self.package_id = {}
                    return {'warning': {'title': ('Warning'), 'message': ('This package is already exist.')}}