# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError

class purchase_invoice(models.Model):
    _name = 'tjara.purchase_invoice'
        
    name = fields.Char(string='Purchase Invoice', default=lambda self: self._get_next_purchaseInvoiceName(), store=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('canceled', 'Canceled'), ('done', 'Done')], string='State', default='draft')
    provider_order_ids = fields.One2many('tjara.provider_order', 'purchase_invoice_id', string="Provider Order", required=True)
    provider_id = fields.Many2one('tjara.provider', ondelete='cascade', string="Provider", index=True, required=True)
    invoice_price = fields.Float(digits=(12, 3), string='Invoice Price', compute='_invoice_price', store=True)
    is_created = fields.Boolean(string='Created', default=False)
    
    
    @api.depends('provider_order_ids')
    def _invoice_price(self):
        invoice_price = 0
        for provider_order in self.provider_order_ids:
            invoice_price = invoice_price + provider_order.total_price
        self.invoice_price = invoice_price
    
    @api.model
    def _get_next_purchaseInvoiceName(self):
        sequence = self.env['ir.sequence'].search([('code','=','tjara.purchase_invoice.seq')])
        next= sequence.get_next_char(sequence.number_next_actual)
        return next
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tjara.purchase_invoice.seq')
        vals['is_created'] = True
        result = super(purchase_invoice, self).create(vals)
        return result 
    
#     @api.depends('provider_order_ids')
#     @api.multi
#     def product_names(self):
#         name_products = ''
#         if(self.provider_order_ids.ids):
#             provider_order_ids = self.provider_order_ids.ids
#             name_products = '<table class="o_list_view table table-condensed table-striped">'
#             name_products += '<thead>'
#             name_products += '<tr>'
#             name_products += '<th data-id="name" class="o_column_sortable">Products Name</th>'
#             name_products += '</tr>'
#             name_products += '</thead>'
#             name_products += '<tbody>'
#             for record in provider_order_ids:
#                 provider_order = self.env['tjara.provider_order'].browse([record])
#                 product_package = provider_order.product_id
#                 name_products += '<tr><td data-field="name" class="o_readonly">'+provider_order.product_id.name+'</td></tr>'
# #                 name_products = '<b>Produit</b>'+name_products + provider_order.product_id.name + '<br/>'
#             name_products += '</tbody>'
#             name_products += '<tfoot><tr><td></td><td class="o_list_record_delete"></td></tr></tfoot>'
#         self.name_products = name_products
#     
#     @api.depends('provider_order_ids')
#     @api.multi
#     def _total_price(self):
#         for purchase_invoice in self:
#             total_price = 0
#             for provider_order in purchase_invoice.provider_order_ids:
#                 total_price += provider_order.price
#             purchase_invoice.total_price = total_price
#     
    @api.onchange('provider_id')
    def _onchange_provider_id(self):
        res = {}
        if(self.provider_id.id):
#             domain = [('state', '=', 'done'), ('provider_id', '=', self.provider_id.id)]
            domain = [('provider_id', '=', self.provider_id.id)]
            res['domain'] = {'provider_order_ids': domain}
#         else:
#             domain = [('state', '=', 'done')]
#         res['domain'] = {'provider_order_ids': domain}
        res['value'] = {'provider_order_ids': False}
        return res

#     @api.one
#     def canceled_progressbar(self):
#         if(self.state == 'done'):
#             raise ValidationError("This purchase invoice is done.")
#             return False
#         else:
#             if(self.provider_order_ids):
#                 total_price_canceled = 0
#                 po_canceled = '<div class="o_cannot_create">'
#                 po_canceled = '<div class="table-responsive">'
#                 po_canceled = '<table class="o_list_view table table-condensed table-striped">'
#                 po_canceled += '<thead>'
#                 po_canceled += '<tr>'
#                 po_canceled += '<th data-id="name" class="o_column_sortable">Provider Orders Names</th>'
#                 po_canceled += '<th data-id="product_id" class="o_column_sortable">Product Names</th>'
#                 po_canceled += '<th data-id="qte_total_unity" class="o_column_sortable">Qte Total</th>'
#                 po_canceled += '<th data-id="price" class="o_column_sortable">Price</th>'
#                 po_canceled += '</tr>'
#                 po_canceled += '</thead>'
#                 po_canceled += '<tfoot><tr><td></td><td></td><td></td><td></td></tr></tfoot>'
#                 po_canceled += '<tbody>'
#                 for provider_order_id in self.provider_order_ids.ids:
#                     provider_order = self.env['tjara.provider_order'].browse(provider_order_id) 
#                     provider_order.state = 'done'
#                     total_price_canceled += provider_order.price
#                     po_canceled += '<tr>'
#                     po_canceled += '<td data-field="name" class="o_readonly">'
#                     po_canceled += '<a href="/web?id='+str(provider_order.id)+'&model=tjara.provider_order#id='+str(provider_order.id)+'&view_type=form&model=tjara.provider_order">'+provider_order.name+'</a>'
#                     po_canceled += '</td>'
#                     po_canceled += '<td class="o_readonly">'+provider_order.product_id.name+'</td>'
#                     po_canceled += '<td class="o_readonly">'+provider_order.qte_total_unity+'</td>'
#                     po_canceled += '<td class="o_readonly">'+str(provider_order.price)+'</td>'
#                     po_canceled += '</tr>'
#                 po_canceled += '</div></div>'
#                 self.write({
#                     'state': 'canceled',
#                     'po_canceled': po_canceled,
#                     'total_price_canceled':total_price_canceled,
#                     'provider_order_ids':False
#                 })    
#                 