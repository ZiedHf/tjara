# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from __builtin__ import list

class product(models.Model):
    _name = 'tjara.product'
    
    name = fields.Char(string=_("Product Name"), required=True)
    description = fields.Text(string="Product Description")
    add_date = fields.Date(string="Add date")
    product_package_ids = fields.One2many('tjara.product_package', 'product_id', ondelete='cascade',  string='Package')
    
    categories_ids = fields.Many2many('tjara.category', string='Category', ondelete='cascade')
    sectors_ids = fields.Many2many('tjara.sector', string='Sector', ondelete='cascade')
    
    other_name = fields.Char(string="Other name")
    french_name = fields.Char(string="French name")
    english_name = fields.Char(string="English name")
    code = fields.Char(string="Code Product")
    ngp = fields.Char(string="NGP")
    
    weight = fields.Char(string="Weight")
    width = fields.Char(string="Width")
    height = fields.Char(string="Height")
    length = fields.Char(string="Length")
    
    purchase_price = fields.Float(string="Purchase Price", digits=(12, 3))
    sale_price = fields.Float(string="Sale Price", digits=(12, 3))
    sale_margin = fields.Float(string="Sale Margin", digits=(12, 3))
    
    is_created = fields.Boolean(string='Created', default=False)
    
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'This name is already exists...!')
    ]
    
    @api.model
    def create(self, vals):
        vals['is_created'] = True
        result = super(product, self).create(vals)
        return result 
        
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