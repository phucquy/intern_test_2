from odoo import api, models, fields
from odoo.exceptions import ValidationError

class MassUpdateWarranty(models.TransientModel):
    _name = 'mass.update.warranty'

    date_from = fields.Date("Date from")
    date_to = fields.Date("Date to")
    product_warranty = fields.Char("Warranty Code", compute='update_mass_warranty',readonly="1")

    @api.constrains('date_to', 'date_from')
    def _check_date(self):
        for rec in self:
            date_to = rec.date_to
            date_from = rec.date_from
            print("check warrranty from wizard")
            if date_from and date_to:
                if date_to < date_from:
                    raise ValidationError(('Ngày bắt đầu phải trước ngày kết thúc.'))


    def update_mass_warranty(self):
        date_from = self.date_from
        date_to = self.date_to
        self.product_warranty = ''
        if date_from and date_to :
            if date_from < date_to:
                date_from = date_from.strftime('%d%m%-y')
                date_to = date_to.strftime('%d%m%-y')
                self.product_warranty = 'PWR/' + str(date_to) + '/' + str(date_from)
        else:
            self.product_warranty = ''
        list = self.env['product.template'].browse(self._context['active_ids'])
        for rec in list:
            rec.date_from = self.date_from
            rec.date_to = self.date_to
            rec.product_warranty = self.product_warranty

