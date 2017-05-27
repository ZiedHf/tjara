# -*- coding: utf-8 -*-
{
    'name': "T-jara",

    'summary': """
        Application de gestion commerciale.
        """,

    'description': """
        Application de gestion commerciale.
    """,

    'author': "Khidma Company",
    'website': "http://www.khidma.tn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
#         'views/views.xml',
#         'views/templates.xml',
        'views/purchase_inquiry.xml',
        'views/sequences.xml',
        'views/product_package.xml',
        'views/purchase_order.xml',
        'views/product.xml',
        'views/provider.xml',
        'views/client.xml',
        'views/package.xml',
        'views/stock.xml',
        'views/depot.xml',
        'views/provider_order.xml',
        'views/purchase_invoice.xml',
        'views/purchase_payment.xml',
        'views/provider_regulation.xml',
        'views/menu.xml',
        'views/wizards.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
#         'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}