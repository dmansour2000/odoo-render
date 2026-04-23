# -*- coding: utf-8 -*-
{
    'name': 'Customer Churn Prediction',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Machine Learning-based Customer Churn Prediction',
    'description': """
Customer Churn Prediction
=========================
This module adds machine learning capabilities to predict which customers are at risk of churning:
- Analyzes customer behavior, order patterns, and support history
- Identifies at-risk customers before they leave
- Provides visual indicators in customer views
- Generates reports on churn risk by customer segment
""",
    'author': 'Dina Mansour',
    'website': '',
    'depends': [
        'base',
        'crm',
        'sale_management',
        'account',
        # 'helpdesk',  # Optional, will use if available
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron_churn_prediction_data.xml',
        'views/partner_churn_prediction_view.xml',
        'views/res_partner_view.xml',
    ],
    'external_dependencies': {
        'python': ['pandas', 'numpy', 'scikit-learn'],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
