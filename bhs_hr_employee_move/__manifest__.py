# -*- coding: utf-8 -*-

{
    'name': 'Employees Transfer Record',
    'version': '15.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
        Create record when employee changes department or trainee transfer to employee.
    """,
    'author': 'Bac Ha Software',
    'company': 'Bac Ha Software',
    'website': 'https://bachasoftware.com',
    'maintainer': 'Bac Ha Software',
    'depends': ['hr', 'hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'views/department_move_view.xml',
        'views/transfer_intern_view.xml'

    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}