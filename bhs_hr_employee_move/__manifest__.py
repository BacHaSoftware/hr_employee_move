# -*- coding: utf-8 -*-

{
    'name': 'Employees Transfer Management',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'summary': """
        Internal Employees Transfer Record
    """,
    'description': """Internal Employees Transfer Record""",
    'author': 'Bac Ha Software',
    'company': 'Bac Ha Software',
    'website': 'https://bachasoftware.com',
    'maintainer': 'Bac Ha Software',
    'depends': ['hr', 'hr_recruitment', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/department_move_view.xml',
        'views/transfer_intern_view.xml'

    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}