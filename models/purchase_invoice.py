# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError

class purchase_invoice(models.Model):
    _name = 'tjara.purchase_invoice'
        
    name = fields.Char(string='Purchase Invoice', default=lambda self: self._get_next_purchaseInvoiceName(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    provider_order_ids = fields.One2many('tjara.provider_order', 'purchase_invoice_id', string="Provider Order", required=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
    total_price = fields.Float(digits=(12, 3), string='Total Price', compute='_total_price')
#     provider_order_ids = fields.Many2one('tjara.provider_order', ondelete='cascade', string="Provider Order")
#     provider_order_ids = fields.Many2many('tjara.provider_order', ondelete='cascade', string="Provider Order")
#     product_package_ids = fields.Many2many('tjara.product_package', string="Product", readonly=True)
#     product_package_ids = fields.Many2many('account.payment', 'account_invoice_payment_rel', 'invoice_id', 'payment_id', string="Payments", copy=False, readonly=True)
    name_products = fields.Html(string="List des produits", compute='product_names')
    po_canceled = fields.Html(string="Provider Orders")
    total_price_canceled = fields.Float(digits=(12, 3), string='Total Price', default=0, readonly=True)
    pricetoshow = fields.Float(digits=(12, 3), string='Total Price', compute='total_price_toshow')
    purchase_payment_id = fields.Many2one('tjara.purchase_payment', ondelete='cascade', string='Purchase Payment', readonly=True)
    is_created = fields.Boolean(string='Created', default=False)
    
    
    @api.depends('total_price', 'total_price_canceled')
    @api.multi
    def total_price_toshow(self):
        for rec in self:
            if(rec.total_price > 0):
                rec.pricetoshow = rec.total_price
            else:
                rec.pricetoshow = rec.total_price_canceled
    
    @api.model
    def _get_next_purchaseInvoiceName(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.purchase_invoice.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
        if(vals['provider_order_ids'][0]):
            res = []
#             for provider_order_ids in vals['provider_order_ids']:
            slicedlist = [item[1] for item in vals['provider_order_ids']]
            for provider_order_id in slicedlist:
                provider_order = self.env['tjara.provider_order'].browse(provider_order_id)
                res.append(provider_order.provider_id.id) 
                provider_order.state = 'invoiced'
            if(len(set(res)) > 1):
                raise ValidationError("The provider orders belong to different providers.")
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_invoice.seq')
                vals['is_created'] = True
                result = super(purchase_invoice, self).create(vals)
                return result 
        else:
            raise ValidationError("You need to set provider orders to this purchase invoice.")
    
    @api.depends('provider_order_ids')
    @api.multi
    def product_names(self):
        name_products = ''
        if(self.provider_order_ids.ids):
            provider_order_ids = self.provider_order_ids.ids
            name_products = '<table class="o_list_view table table-condensed table-striped">'
            name_products += '<thead>'
            name_products += '<tr>'
            name_products += '<th data-id="name" class="o_column_sortable">Products Name</th>'
            name_products += '</tr>'
            name_products += '</thead>'
            name_products += '<tbody>'
            for record in provider_order_ids:
                provider_order = self.env['tjara.provider_order'].browse([record])
                product_package = provider_order.product_id
                name_products += '<tr><td data-field="name" class="o_readonly">'+provider_order.product_id.name+'</td></tr>'
#                 name_products = '<b>Produit</b>'+name_products + provider_order.product_id.name + '<br/>'
            name_products += '</tbody>'
            name_products += '<tfoot><tr><td></td><td class="o_list_record_delete"></td></tr></tfoot>'
        self.name_products = name_products
    
    @api.depends('provider_order_ids')
    @api.multi
    def _total_price(self):
        for purchase_invoice in self:
            total_price = 0
            for provider_order in purchase_invoice.provider_order_ids:
                total_price += provider_order.price
            purchase_invoice.total_price = total_price
    
    @api.onchange('provider_id')
    def _onchange_provider_id(self):
        res = {}
        if(self.provider_id.id):
            domain = [('state', '=', 'done'), ('provider_id', '=', self.provider_id.id)]
        else:
            domain = [('state', '=', 'done')]
        res['domain'] = {'provider_order_ids': domain}
        res['value'] = {'provider_order_ids': False}
        return res

    @api.one
    def canceled_progressbar(self):
        if(self.state == 'done'):
            raise ValidationError("This purchase invoice is done.")
            return False
        else:
            if(self.provider_order_ids):
                total_price_canceled = 0
                po_canceled = '<div class="o_cannot_create">'
                po_canceled = '<div class="table-responsive">'
                po_canceled = '<table class="o_list_view table table-condensed table-striped">'
                po_canceled += '<thead>'
                po_canceled += '<tr>'
                po_canceled += '<th data-id="name" class="o_column_sortable">Provider Orders Names</th>'
                po_canceled += '<th data-id="product_id" class="o_column_sortable">Product Names</th>'
                po_canceled += '<th data-id="qte_total_unity" class="o_column_sortable">Qte Total</th>'
                po_canceled += '<th data-id="price" class="o_column_sortable">Price</th>'
                po_canceled += '</tr>'
                po_canceled += '</thead>'
                po_canceled += '<tfoot><tr><td></td><td></td><td></td><td></td></tr></tfoot>'
                po_canceled += '<tbody>'
                for provider_order_id in self.provider_order_ids.ids:
                    provider_order = self.env['tjara.provider_order'].browse(provider_order_id) 
                    provider_order.state = 'done'
                    total_price_canceled += provider_order.price
                    po_canceled += '<tr>'
                    po_canceled += '<td data-field="name" class="o_readonly">'
                    po_canceled += '<a href="/web?id='+str(provider_order.id)+'&model=tjara.provider_order#id='+str(provider_order.id)+'&view_type=form&model=tjara.provider_order">'+provider_order.name+'</a>'
                    po_canceled += '</td>'
                    po_canceled += '<td class="o_readonly">'+provider_order.product_id.name+'</td>'
                    po_canceled += '<td class="o_readonly">'+provider_order.qte_total_unity+'</td>'
                    po_canceled += '<td class="o_readonly">'+str(provider_order.price)+'</td>'
                    po_canceled += '</tr>'
                po_canceled += '</div></div>'
                self.write({
                    'state': 'canceled',
                    'po_canceled': po_canceled,
                    'total_price_canceled':total_price_canceled,
                    'provider_order_ids':False
                })    
                
#     @api.multi
#     @api.onchange('provider_order_ids')
#     def _onchange_provider_order_ids(self):
#         provider_orders_list = []
#         for rec in self.provider_order_ids:
#             provider_orders_list.append(rec.id)
#         if(len(set(provider_orders_list)) > 1):
#             raise ValidationError("The provider orders must belong to the same provider !")
#             return false


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