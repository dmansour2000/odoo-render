# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields, api, _
import logging
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

import pickle
import base64
import tempfile
import os
from datetime import timedelta

from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ChurnPredictionModel(models.Model):
    _name = 'res.partner.churn.model'
    _description = 'Customer Churn Prediction Model'

    name = fields.Char(string='Model Name', required=True, default= f'Churn Prediction Model {fields.Datetime.now()}')
    model_data = fields.Binary(string='Trained Model', attachment=True)
    feature_list = fields.Text(string='Features Used')
    accuracy = fields.Float(string='Model Accuracy')
    last_trained = fields.Datetime(string='Last Trained')
    active = fields.Boolean(default=True)
    churn_threshold = fields.Float(string='Churn Risk Threshold', default=0.5,
                                   help="Probability threshold above which a customer is considered at risk")

    def train_model(self):
        """Train a new churn prediction model using historical customer data"""
        existing_model = self.filtered(lambda m: m.active)
        if not existing_model:
            raise UserError(_('You should active this model before train it !!.'))

        # Get the date 6 months ago
        six_months_ago = fields.Date.today() - timedelta(days=180)

        # Get all customers who have made at least one quotation
        customers_with_orders = self.env['sale.order'].search([
            ('state', '=', 'draft'),
        ]).mapped('partner_id')

        # Check which customers haven't created a quotation in the last 6 months
        active_customers = self.env['sale.order'].search([
            ('state', '=', 'draft'),
            ('date_order', '>=', six_months_ago),
        ]).mapped('partner_id')

        # Customers who created quotations before but not in the last 6 months are considered churned
        churned_customers = customers_with_orders - active_customers

        if len(customers_with_orders) < 100:
            raise UserError(_('Not enough customer data to train a reliable model (minimum 100 records)'))

        # Prepare the dataset
        data = []

        for partner in customers_with_orders:
            try:
                # Basic information about the customer
                all_orders = self.env['sale.order'].search([
                    ('partner_id', '=', partner.id),
                    ('state', '=', 'draft'),
                ])

                if not all_orders:
                    continue

                # Orders in the last year
                one_year_ago = fields.Date.today() - timedelta(days=365)
                recent_orders = self.env['sale.order'].search([
                    ('partner_id', '=', partner.id),
                    ('state', '=', 'draft'),
                    ('date_order', '>=', one_year_ago),
                ])

                # Calculate features
                last_order_date = max(all_orders.mapped('date_order'))
                days_since_last_order = (fields.Date.today() - last_order_date.date()).days

                total_order_amount = sum(all_orders.mapped('amount_total'))
                avg_order_value = total_order_amount / len(all_orders) if all_orders else 0

                # Gather all features (only order patterns and financial metrics remain)
                customer_data = {
                    'partner_id': partner.id,
                    'days_since_last_order': days_since_last_order,
                    'total_orders': len(all_orders),
                    'recent_orders': len(recent_orders),
                    'total_order_amount': total_order_amount,
                    'avg_order_value': avg_order_value,
                    'churned': 1 if partner in churned_customers else 0
                }

                data.append(customer_data)
            except Exception as e:
                _logger.error(f"Error processing customer {partner.name}: {str(e)}")
                continue

        # Convert to pandas DataFrame
        df = pd.DataFrame(data).sample(frac=1).reset_index(drop=True)

        if df.empty or len(df) < 100:
            raise UserError(_('Not enough processed data to train a model (minimum 100 records)'))

        # Handle missing values
        df = df.fillna(0)

        # Separate features and target
        X = df.drop(['partner_id', 'churned'], axis=1)
        y = df['churned']

        # Splitting the dataset into the Training set and Test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        # Training the Random Forest Classification model on the Training set
        classifier = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)
        classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = classifier.predict(X_test)

        # Calculate accuracy on training data
        accuracy = accuracy_score(y_test, y_pred)

        # Save the model using a cross-platform temporary file approach
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as temp_file:
            model_filename = temp_file.name
            pickle.dump(classifier, temp_file)

        # Read the saved model
        with open(model_filename, 'rb') as file:
            model_data = base64.b64encode(file.read())

        # Clean up
        try:
            os.remove(model_filename)
        except Exception as e:
            _logger.warning(f"Could not remove temporary file: {str(e)}")

        # Create or update model record
        vals = {
            'model_data': model_data,
            'feature_list': str(list(X.columns)),
            'accuracy': accuracy,
            'last_trained': fields.Datetime.now(),
            'active': True
        }

        if existing_model:
            existing_model.write(vals)
            return existing_model

    def predict_churn_risk(self, partner):
        """Predict churn risk for a specific partner"""
        try:
            if not self.model_data:
                return self.churn_threshold  # Default risk if no model

            # Load the model
            model_data = base64.b64decode(self.model_data)
            model = pickle.loads(model_data)

            # Extract features from the partner
            all_orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'draft'),
            ])

            if not all_orders:
                return 0.7  # Higher risk for customers with no quotations

            # Orders in the last year
            one_year_ago = fields.Date.today() - timedelta(days=365)
            recent_orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'draft'),
                ('date_order', '>=', one_year_ago),
            ])

            # Calculate features
            last_order_date = max(all_orders.mapped('date_order'))
            days_since_last_order = (fields.Date.today() - last_order_date.date()).days

            total_order_amount = sum(all_orders.mapped('amount_total'))
            avg_order_value = total_order_amount / len(all_orders) if all_orders else 0

            # Gather all features (only order patterns and financial metrics remain)
            partner_data = {
                'days_since_last_order': days_since_last_order,
                'total_orders': len(all_orders),
                'recent_orders': len(recent_orders),
                'total_order_amount': total_order_amount,
                'avg_order_value': avg_order_value,
            }

            # Convert to DataFrame (single row)
            df = pd.DataFrame([partner_data])

            # Get probability of churn
            churn_risk = model.predict_proba(df)[0][1]  # Probability of class 1 (churned)
            return churn_risk

        except Exception as e:
            _logger.error(f"Error predicting churn risk: {str(e)}")
            return self.churn_threshold  # Default risk on error

    def write(self, vals):
        for rec in self:
            if vals.get("active", False):
                if self.search([('active', '=', True), ('id', '!=', rec.id)], limit=1):
                    raise UserError(_('Must be only one model active!'))

        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get("active", False):
            if self.search([('active', '=', True)], limit=1):
                raise UserError(_('Must be only one model active!'))

        return super().create(vals)
