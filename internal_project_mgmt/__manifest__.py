{
    'name': 'Internal Project Management',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Manajemen proyek internal perusahaan',
    "author": "Riyan Andriyanto",
    'depends': ['base', 'project', 'hr'],
    'data': [
        'security/internal_project_mgmt_security.xml',
        'security/ir.model.access.csv',
        'views/project_internal_views.xml',
        'views/project_task_internal_views.xml',
    ],
    'installable': True,
    'application': False,
}
