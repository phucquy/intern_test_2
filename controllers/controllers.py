# -*- coding: utf-8 -*-
# from odoo import http


# class ProductTask(http.Controller):
#     @http.route('/product_task/product_task/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_task/product_task/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_task.listing', {
#             'root': '/product_task/product_task',
#             'objects': http.request.env['product_task.product_task'].search([]),
#         })

#     @http.route('/product_task/product_task/objects/<model("product_task.product_task"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_task.object', {
#             'object': obj
#         })
