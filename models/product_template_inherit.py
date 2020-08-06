from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template Inherit'

    date_from = fields.Date("Date from")
    date_to = fields.Date("Date to")
    product_warranty = fields.Char("Warranty Code", compute='_compute_warranty_code', readonly="1")
    status = fields.Char('Status', default="invalid", readonly="1")
    warranty_time = fields.Char('Warranty Time', default="0 days", compute='_compute_warranty_time', readonly="1", store=True)

    @api.constrains('date_to', 'date_from')
    def _check_date(self):
        for rec in self:
            date_to = rec.date_to
            date_from = rec.date_from
            if date_from and date_to :
                if date_to < date_from:
                    raise ValidationError(('Ngày bắt đầu phải trước ngày kết thúc.'))

    @api.depends('date_to')
    def _compute_warranty_time(self):
        for rec in self:
            current_date = datetime.today().date()
            date_to = rec.date_to
            w_time = ''
            if date_to:
                if date_to > current_date:
                    date_to = datetime.strptime(str(date_to), "%Y-%m-%d").date()
                    rd = relativedelta(date_to, current_date)
                    if rd.years == 0 and rd.months == 0:
                        w_time = str(rd.days) + "days"
                    elif rd.years == 0 and rd.months != 0:
                        w_time = str(rd.months) + "m" + " " + str(rd.days) + "d"
                    elif rd.years != 0 and rd.months == 0:
                        w_time = str(rd.years) + "y" + " " + str(rd.days) + "d"
                    else:
                        w_time = str(rd.years) + "y" + " " + str(rd.months) + "m" + " " + str(rd.days) + "d"
                else:
                    w_time ='Expired'
            rec.warranty_time = w_time


    @api.depends('date_to', 'date_from')
    def _compute_warranty_code(self):
        for rec in self:
            date_from = rec.date_from
            date_to = rec.date_to

            rec.product_warranty = ''
            rec.status = "invalid"
            if date_from and date_to:
                if date_to > date_from:
                    date_from = date_from.strftime('%d%m%-y')
                    date_to = date_to.strftime('%d%m%-y')
                    rec.product_warranty = 'PWR/' + str(date_from) + "/" + str(date_to)
                    rec.status = "valid"
