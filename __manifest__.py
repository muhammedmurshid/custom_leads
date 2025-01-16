{
    'name': 'Leads',
    'version': '1.0.0',
    'summary': 'Leads',
    'description': """
        A more detailed description of the module.
    """,
    'author': 'Murshid',
    'website': 'https://www.yourwebsite.com',
    'category': 'Specific Category',
    'license': 'LGPL-3',
    'depends': [
        'base','website', 'openeducat_core'  # List of module dependencies

        # Add other module dependencies here
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/leads.xml',
        'views/source.xml',
        'views/connection.xml',
        'views/convert_lead.xml',
        'views/student.xml'

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
