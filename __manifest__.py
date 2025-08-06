{
    'name': 'Customer Sales Analysis',
    'version': '1.0',
    'category': 'Sales',
    'depends': ['base', 'sale'],
    'data': [
        'data/paper_format.xml',
        'reports/report_sale_analysis.xml',      # Template first
        'reports/report_sale_analysis_action.xml', # Then action
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
}