from odoo import fields, api, models


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_price = fields.Monetary("Warranty Price", readonly=True, compute="_calculate_warranty_price")

    @api.depends('price_subtotal')
    def _calculate_warranty_price(self):
        for order in self:
            order.product_price =''
            if order.product_id:
                print("tinh gia san pham " + str(order.product_id))
                print(str(order.product_id.status))
                if order.product_id.warranty_time == 'Expired':
                    order.product_price = order.price_subtotal * 0.9
                    order.discount = 10

                elif order.product_id.warranty_time == '0 days':
                    order.discount = 10
                    order.product_price = order.price_subtotal * 0.9
                else:
                    order.discount = 0
                    order.product_price = order.price_subtotal





class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'

    discount_total_warranty = fields.Monetary("Discount Total With Warranty",
                                              readonly=True, store=True, compute='_compute_discount_total_warranty')

    @api.depends('order_line')
    def _compute_discount_total_warranty(self):
        for rec in self:
            estimated_total = 0.0
            for line in rec.order_line:
                estimated_total += line.product_price
        rec.update({
            'discount_total_warranty' : estimated_total
        })