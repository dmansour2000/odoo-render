# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    churn_risk = fields.Float(string='Churn Risk', default=0.0, help="Probability that the customer will churn (0-1)")
    churn_risk_date = fields.Datetime(string='Risk Calculation Date')
    is_at_risk = fields.Boolean(string='At Risk of Churning', compute='_compute_is_at_risk')

    @api.depends('churn_risk')
    def _compute_is_at_risk(self):
        model = self.env['res.partner.churn.model'].search([('active', '=', True)], limit=1)
        threshold = model.churn_threshold if model else 0.5

        for partner in self:
            partner.is_at_risk = partner.churn_risk >= threshold

    @api.model
    def _cron_calculate_churn_risk(self):
        """Scheduled action to calculate churn risk for all customers"""
        # Get the active model
        model = self.env['res.partner.churn.model'].search([('active', '=', True)], limit=1)
        if not model:
            return

        # Get customers with at least one sale order
        customers = self.env['sale.order'].search([
            ('state', 'in', ['sale', 'done']),
        ]).mapped('partner_id')

        for partner in customers:
            churn_risk = model.predict_churn_risk(partner)
            partner.write({
                'churn_risk': churn_risk,
                'churn_risk_date': fields.Datetime.now()
            })