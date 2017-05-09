# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from __builtin__ import str
import sys
import types
from pprint import pprint

class product_package(models.Model):
    _name = 'tjara.product_package'
    
    name = fields.Char(string="Name", default="Unknown", compute='_compute_name')
    product_id = fields.Many2one('tjara.product', ondelete='cascade', string="Produit", index=True)
    package_id = fields.Many2one('tjara.package', ondelete='cascade', string="Emballage", index=True)
#     weight = fields.Float(digits=(8, 3), help="Weight")
    qte = fields.Integer(string="Quantité / Nombre", required=True)
    description = fields.Text(string="Description d'emballage")
#     purchase_order_ids = fields.One2many('tjara.purchase_order', ondelete='cascade', string="Demande d'achat", index=True)
    purchase_order_ids = fields.One2many('tjara.purchase_order', 'product_package_id', string="Demande d'achat")
    
    _sql_constraints = [
        ('ligne_unique', 'unique (product_id, package_id)', 'Package is already exists for this product...!')
    ]
    
    @api.depends('product_id', 'package_id', 'qte')
    def _compute_name(self):
        for rec in self:
            if((isinstance(rec.product_id.name, unicode))and(isinstance(rec.package_id.name, unicode))and(isinstance(rec.qte, int))):
                rec.name = rec.product_id.name + " - " + rec.package_id.name + " / " + str(rec.qte)

    @api.onchange('package_id')
    def onchange_product_package(self):
        for object in self:
            if object.product_id:
                existing_ids = self.env["tjara.product_package"].search([('package_id', '=', object.package_id.id), ('product_id.name', '=', object.product_id.name)], limit=1)
                if len(existing_ids) > 0:
                    self.package_id = {}
                    return {'warning': {'title': ('Warning'), 'message': ('This package is already exist.')}}
#             if object.search([('package_id', '=', object.package_id.id),('product_id', '=', object.product_id.id)]): //// 
#                 return {'warning': {'title': _('Warning'), 'message': _('your message.')}}
#     @api.multi
#     @api.onchange("package_id")
#     def onchange_package_id(self):
#         for package in self.package_id:
#             print package
#         for object in self:
#             if object.product_id:
#                 existing_ids = self.env["tjara.product_package"].search([('package_id','=',object.package_id.id), ('product_id','=',object.product_id.id)], limit=1)
#                 if len(existing_ids) > 0:
#                     raise exceptions.Warning(_('Package is already exists for this product...!'))            
#         print('--------Check--------')
#         for object in self:
#             if object.product_id:
#                 print('product_id : ')
#                 print(object.product_id.id)
#                 existing_ids = self.env["tjara.product_package"].search([('package_id','=',object.package_id.id)], limit=1)
#                 print('existing_ids : ')
#                 print(existing_ids)
#                 if len(existing_ids) > 0:
#                      raise exceptions.Warning(_('Package is already exists for this product...!'))
#     @api.constrains('product_id', 'package_id')
#     def _check_product_package_ids(self):
#         for record in self:
# #             print(record.product_package_ids)
# #             print(type(record.product_package_ids))
#             product_package_list = list()
#             for package in record.product_package_ids:
#                 product_package_list.append(package.id)
#              
#             print(product_package_list)
# #             if record.age > 20:
# #                 raise ValidationError("Your record is too old: %s" % record.age)