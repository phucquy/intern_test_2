# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template Inherit'

    date_from = fields.Date("Date from")
    date_to = fields.Date("Date to")
    product_warranty = fields.Char("Warranty Code", compute="_check_valid_date")

    @api.constrains('date_from')
    def _check_valid_date(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                print("from "+rec.date_from)
                print("to "+rec.date_to)
                if rec.date_from > rec.date_to:
                    raise ValidationError("Ngày bắt đầu phải trước ngày kết thúc")

    @api.onchange('date_from', 'date_to')
    def _compute_warranty_code(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                if rec.date_from < rec.date_to:
                    # print(rec.date_from.strftime('%d-%m-%Y'))
                    str_date_from = str(rec.date_from)
                    arr_date_from = str_date_from.split("-")
                    value_from = arr_date_from[2] + arr_date_from[1] + arr_date_from[0]

                    str_date_to = str(rec.date_to)
                    arr_date_to = str_date_to.split("-")
                    value_to = arr_date_to[2] + arr_date_to[1] + arr_date_to[0]

                    rec.product_warranty = "PWR/" + value_from + "/" + value_to

