# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from __builtin__ import list

class product(models.Model):
    _name = 'tjara.product'
    
    name = fields.Char(string="Nom du produit")
    description = fields.Text(string="Description du produit")
    add_date = fields.Date(string="Date d'ajout au stock")
    provider_ids = fields.Many2many('tjara.provider', ondelete='cascade', string="Provider", index=True)
    client_ids = fields.Many2many('tjara.client', ondelete='cascade', string="Client", index=True)
    product_package_ids = fields.One2many('tjara.product_package', 'product_id', string='Package')
        
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'This name is already exists...!')
    ]
    
#     @api.multi
#     @api.onchange('package_id')
#     def onchange_package_id(self):
#         for object in self:
#             if object.product_id:
#                 print('product_id : ')
#                 print(object.product_id.id)
#                 existing_ids = self.env["tjara.product_package"].search([('package_id','=',object.package_id.id)], limit=1)
#                 print('existing_ids : ')
#                 print(existing_ids)
#                 if len(existing_ids) > 0:
#                      raise exceptions.Warning(_('Package is already exists for this product...!'))
#     @api.constrains('product_package_ids')
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