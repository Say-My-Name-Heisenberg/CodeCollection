{
    'name': 'Vendor Registration Form',
    'version': '18.9',
    'category': 'Contact',
    'summary': 'Vendor Registration',
    'sequence': '10',
    'license': 'AGPL-3',
    'author': 'Atheer',
    'maintainer': 'Atheer',
    'website': 'www.Atheerit.com',
    'depends': [
        'base','website','km_purchase_order'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/vendor_registration_templates.xml',
        'views/vendor_registration.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            'vendor_registration_form/static/src/js/dynamic_state.js',
            'vendor_registration_form/static/docs/*',
        ],
    },
    'auto_install': False,
}
