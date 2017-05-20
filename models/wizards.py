# -*- coding: utf-8 -*-

from odoo import models, fields, api

class confirm_wizard(models.TransientModel):
    _name = 'tjara.confirm_wizard'

    yes_no = fields.Char(default='Some purchase inquiries not accepted or refused yet. Do you want to proceed and set them as refused ?')

    @api.multi
    def yes(self):
        self.env['tjara.purchase_order'].set_purchaseinqueries_to_refused(self._context['active_id'])

    @api.multi
    def no(self):
        self.env['purchase_order'].nothingfunction(self._context['active_id'])