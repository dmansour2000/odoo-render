
{
    "name": "Sale Order Product Recommendation",
    "summary": "Recommend products to sell to customer based on history",
    "version": "1.0.0.0",
    "category": "Sales",
    "website": "",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/sale_order_recommendation_view.xml",
        "views/res_config_settings_views.xml",
        "views/sale_order_view.xml",
    ],
}
