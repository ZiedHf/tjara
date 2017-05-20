# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError

class purchase_invoice(models.Model):
    _name = 'tjara.purchase_invoice'
        
    name = fields.Char(string='Provider Order')
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    provider_order_ids = fields.One2many('tjara.provider_order', 'purchase_invoice_id', string="Provider Order")
#     provider_order_ids = fields.Many2one('tjara.provider_order', ondelete='cascade', string="Provider Order")
#     provider_order_ids = fields.Many2many('tjara.provider_order', ondelete='cascade', string="Provider Order")
#     product_package_ids = fields.Many2many('tjara.product_package', string="Product", readonly=True)
#     product_package_ids = fields.Many2many('account.payment', 'account_invoice_payment_rel', 'invoice_id', 'payment_id', string="Payments", copy=False, readonly=True)
    name_products = fields.Html(string="List des produits", compute='product_names')
    
    @api.depends('provider_order_ids')
    @api.multi
    def product_names(self):
        name_products = ''
        if(self.provider_order_ids.ids):
            provider_order_ids = self.provider_order_ids.ids
            for record in provider_order_ids:
                provider_order = self.env['tjara.provider_order'].browse([record])
                product_package = provider_order.product_id
                name_products = '<b>Produit</b>'+name_products + provider_order.product_id.name + '<br/>'
#                 self.env.cr.execute("""
#                     INSERT INTO public.tjara_product_package_tjara_purchase_invoice_rel(
#                     tjara_purchase_invoice_id, tjara_product_package_id)
#                     VALUES (%s,%s);
#                          """,[result.id, product_package.id])
        self.name_products = name_products

    
    
#     @api.multi
#     @api.onchange('provider_order_ids')
#     def test_function(self):
#         if(self.provider_order_ids.ids):
#             provider_order_ids = self.provider_order_ids.ids
#             for record in provider_order_ids:
#                 provider_order = self.env['tjara.provider_order'].browse([record])
#                 product_package = provider_order.product_id
#                 self.env.cr.execute("""
#                 INSERT INTO public.tjara_product_package_tjara_purchase_invoice_rel(
#             tjara_purchase_invoice_id, tjara_product_package_id)
#     VALUES (%s,%s);
#                  """,[self.next_by_id('tjara.purchase_invoice'), product_package.id])
#                 dictionary = {
#                         'tjara_product_package_id':product_package.id,
#                         'tjara_purchase_invoice_id':self.id
# #                         'name':product_package.name,
# #                         'price':provider_order.price,
# #                         'qte':product_package.qte,
# #                         'qte_prpk':provider_order.qte_prpk,
# #                         'qte_prpk_unity':provider_order.qte_prpk_unity,
# #                         'qte_total':provider_order.qte_total,
# #                         'qte_total_unity':provider_order.qte_total_unity,
# #                         'unity':provider_order.unity
#                     }
#                 return (0, False, dictionary)
#             
            
            #vals = ({'date_added': current_time, 'active': True})

# class PurchaseInvoiceRelationWithProduct(models.Model):
#     _name = "tjara.pirwp"
#     _auto = False
# 
#     product_package_ids = fields.Many2one(comodel_name='tjara.product_package', string='Product')
#     provider_order_ids = fields.Many2one(comodel_name='event.registration', string='Registration')
#     
#     attendee_id = fields.Many2one(comodel_name='event.registration', string='Registration')
#     question_id = fields.Many2one(comodel_name='event.question', string='Question')
#     answer_id = fields.Many2one(comodel_name='event.answer', string='Answer')
#     event_id = fields.Many2one(comodel_name='event.event', string='Event')
# 
#     @api.model_cr
#     def init(self):
#         """ Event Question main report """
#         tools.drop_view_if_exists(self._cr, 'event_question_report')
#         self._cr.execute(""" CREATE VIEW event_question_report AS (
#             SELECT
#                 att_answer.id as id,
#                 att_answer.event_registration_id as attendee_id,
#                 answer.question_id as question_id,
#                 answer.id as answer_id,
#                 question.event_id as event_id
#             FROM
#                 event_registration_answer as att_answer
#             LEFT JOIN
#                 event_answer as answer ON answer.id = att_answer.event_answer_id
#             LEFT JOIN
#                 event_question as question ON question.id = answer.question_id
#             GROUP BY
#                 attendee_id,
#                 event_id,
#                 question_id,
#                 answer_id,
#                 att_answer.id
#         )""")