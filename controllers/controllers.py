# -*- coding: utf-8 -*-
from odoo import http

# class Tjara(http.Controller):
#     @http.route('/tjara/tjara/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tjara/tjara/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tjara.listing', {
#             'root': '/tjara/tjara',
#             'objects': http.request.env['tjara.tjara'].search([]),
#         })

#     @http.route('/tjara/tjara/objects/<model("tjara.tjara"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tjara.object', {
#             'object': obj
#         })