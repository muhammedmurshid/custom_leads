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
        'base','website', 'openeducat_core', 'logic_base_17'  # List of module dependencies

        # Add other module dependencies here
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/leads.xml',
        'views/source.xml',
        'views/connection.xml',
        'views/convert_lead.xml',
        'views/student.xml',
        'views/allocation.xml',
        'data/actions.xml'

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
