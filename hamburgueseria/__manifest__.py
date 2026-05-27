{
    'name': 'Hamburguesería',
    'version': '16.0.1.0.0',
    'summary': 'Sistema de Pedidos para Hamburguesería',
    'description': """
        Módulo para gestionar pedidos de una hamburguesería.
        Incluye gestión de productos, personalización de pedidos,
        control de estados y proceso de devoluciones.
    """,
    'author': 'Yadiel',
    'category': 'Industries',
    'depends': ['base', 'mail'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/demo_data.xml',
        'views/ingredient_views.xml',
        'views/product_views.xml',
        'views/order_views.xml',
        'wizard/return_wizard_views.xml',
        'report/sales_report.xml',
        'report/sales_report_template.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
