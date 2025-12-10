"""
Paystub Document Generator
"""

import os
import glob
import random
from datetime import datetime, timedelta
import sys

# Add parent directory to path for base_generator import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from base_generator import BaseDocumentGenerator


class PaystubGenerator(BaseDocumentGenerator):
    """Generator for paystub documents with round-robin template selection."""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.template_index = 0
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load all HTML templates from the templates folder."""
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        template_files = glob.glob(os.path.join(templates_dir, '*.html'))
        if not template_files:
            raise FileNotFoundError(f"No HTML templates found in {templates_dir}")
        return sorted(template_files)  # Sort for consistent ordering
    
    def get_html_template_path(self):
        """Return the next template path using round-robin selection."""
        template_path = self.templates[self.template_index]
        self.template_index = (self.template_index + 1) % len(self.templates)
        return template_path
    
    def generate_pay_period(self):
        """Generate a realistic pay period."""
        # Generate a pay period ending recently
        end_date = self.fake.date_between(start_date='-30d', end_date='today')
        
        # Determine pay frequency (bi-weekly is most common)
        pay_frequency = random.choice(['weekly', 'bi-weekly', 'semi-monthly', 'monthly'])
        
        if pay_frequency == 'weekly':
            start_date = end_date - timedelta(days=6)
        elif pay_frequency == 'bi-weekly':
            start_date = end_date - timedelta(days=13)
        elif pay_frequency == 'semi-monthly':
            start_date = end_date - timedelta(days=14)
        else:  # monthly
            start_date = end_date - timedelta(days=29)
        
        return start_date, end_date, pay_frequency
    
    def generate_pay_amounts(self, hourly_rate, regular_hours, overtime_hours):
        """Generate pay amounts with simple calculations."""
        regular_pay = regular_hours * hourly_rate
        overtime_pay = overtime_hours * hourly_rate * 1.5
        gross_pay = regular_pay + overtime_pay
        return regular_pay, overtime_pay, gross_pay
    
    def generate_realistic_payroll_amounts(self, gross_pay):
        """Generate realistic but simplified payroll amounts."""
        # Use simplified percentages for quick calculation
        federal_tax = gross_pay * random.uniform(0.15, 0.25)
        state_tax = gross_pay * random.uniform(0.03, 0.08)
        social_security = gross_pay * 0.062  # Fixed FICA rate
        medicare = gross_pay * 0.0145  # Fixed Medicare rate
        
        # Optional deductions with simple faker-style generation
        health_insurance = random.uniform(50, 300) if random.random() > 0.3 else 0
        retirement = gross_pay * random.uniform(0.03, 0.08) if random.random() > 0.4 else 0
        
        total_deductions = federal_tax + state_tax + social_security + medicare + health_insurance + retirement
        net_pay = gross_pay - total_deductions
        
        return {
            'federal_tax': federal_tax,
            'state_tax': state_tax,
            'social_security': social_security,
            'medicare': medicare,
            'health_insurance': health_insurance,
            'retirement': retirement,
            'total_deductions': total_deductions,
            'net_pay': net_pay
        }
    
    def generate_color_scheme(self):
        """Generate a random color scheme to avoid color-based bias."""
        # Generate neutral business color schemes
        schemes = [
            {'primary': '#2c3e50', 'secondary': '#ecf0f1', 'accent': '#34495e'},  # Dark blue-gray
            {'primary': '#27ae60', 'secondary': '#ecf0f1', 'accent': '#2ecc71'},  # Green
            {'primary': '#8e44ad', 'secondary': '#ecf0f1', 'accent': '#9b59b6'},  # Purple  
            {'primary': '#e74c3c', 'secondary': '#ecf0f1', 'accent': '#c0392b'},  # Red
            {'primary': '#f39c12', 'secondary': '#ecf0f1', 'accent': '#d68910'},  # Orange
            {'primary': '#17a2b8', 'secondary': '#ecf0f1', 'accent': '#138496'},  # Teal
            {'primary': '#495057', 'secondary': '#f8f9fa', 'accent': '#6c757d'},  # Gray
            {'primary': '#6f42c1', 'secondary': '#f8f9fc', 'accent': '#5a32a3'},  # Indigo
        ]
        return random.choice(schemes)
    
    def generate_ytd_amounts(self, payroll_amounts, periods_elapsed):
        """Generate year-to-date amounts with realistic variance."""
        variance = random.uniform(0.85, 1.15)  # Add some realistic variance
        return {
            'ytd_gross': payroll_amounts['gross_pay'] * periods_elapsed * variance,
            'ytd_federal_tax': payroll_amounts['federal_tax'] * periods_elapsed * variance,
            'ytd_net': payroll_amounts['net_pay'] * periods_elapsed * variance
        }
    
    def generate_fake_data(self):
        """Generate fake data for paystub."""
        # Generate color scheme to avoid color bias
        colors = self.generate_color_scheme()
        
        # Employee information
        employee_name = self.fake.name()
        employee_id = random.randint(1000, 9999)
        
        # Company information
        company_name = self.fake.company()
        company_address = self.fake.address().replace('\n', '<br>')
        
        # Pay period information
        start_date, end_date, pay_frequency = self.generate_pay_period()
        
        # Pay information
        hourly_rate = random.uniform(15, 45)
        
        # Calculate hours based on pay frequency
        if pay_frequency == 'weekly':
            regular_hours = random.uniform(35, 40)
            overtime_hours = random.uniform(0, 8)
        elif pay_frequency == 'bi-weekly':
            regular_hours = random.uniform(70, 80)
            overtime_hours = random.uniform(0, 16)
        elif pay_frequency == 'semi-monthly':
            regular_hours = random.uniform(75, 85)
            overtime_hours = random.uniform(0, 12)
        else:  # monthly
            regular_hours = random.uniform(150, 170)
            overtime_hours = random.uniform(0, 20)
        
        # Generate pay amounts
        regular_pay, overtime_pay, gross_pay = self.generate_pay_amounts(hourly_rate, regular_hours, overtime_hours)
        
        # Calculate realistic deductions using base class
        payroll_amounts = self.generate_realistic_payroll_amounts(gross_pay)
        payroll_amounts['gross_pay'] = gross_pay
        
        # Year-to-date calculations
        periods_in_year = {'weekly': 52, 'bi-weekly': 26, 'semi-monthly': 24, 'monthly': 12}
        periods_elapsed = random.randint(1, periods_in_year[pay_frequency])
        ytd_amounts = self.generate_ytd_amounts(payroll_amounts, periods_elapsed)
        
        return {
            'company_name': company_name,
            'company_address': company_address,
            'employee_name': employee_name,
            'employee_id': employee_id,
            'pay_period_start': start_date.strftime('%m/%d/%Y'),
            'pay_period_end': end_date.strftime('%m/%d/%Y'),
            'pay_date': (end_date + timedelta(days=random.randint(1, 7))).strftime('%m/%d/%Y'),
            'pay_frequency': pay_frequency.title(),
            'hourly_rate': f"{hourly_rate:.2f}",
            'regular_hours': f"{regular_hours:.1f}",
            'regular_pay': f"{regular_pay:.2f}",
            'overtime_hours': f"{overtime_hours:.1f}",
            'overtime_rate': f"{hourly_rate * 1.5:.2f}",
            'overtime_pay': f"{overtime_pay:.2f}",
            'gross_pay': f"{gross_pay:.2f}",
            'federal_tax': f"{payroll_amounts['federal_tax']:.2f}",
            'state_tax': f"{payroll_amounts['state_tax']:.2f}",
            'social_security': f"{payroll_amounts['social_security']:.2f}",
            'medicare': f"{payroll_amounts['medicare']:.2f}",
            'health_insurance': f"{payroll_amounts['health_insurance']:.2f}" if payroll_amounts['health_insurance'] > 0 else "",
            'retirement': f"{payroll_amounts['retirement']:.2f}" if payroll_amounts['retirement'] > 0 else "",
            'total_deductions': f"{payroll_amounts['total_deductions']:.2f}",
            'net_pay': f"{payroll_amounts['net_pay']:.2f}",
            'ytd_gross': f"{ytd_amounts['ytd_gross']:.2f}",
            'ytd_net': f"{ytd_amounts['ytd_net']:.2f}",
            'ytd_federal_tax': f"{ytd_amounts['ytd_federal_tax']:.2f}",
            'check_number': random.randint(10000, 99999),
            # Add dynamic colors to prevent color-based bias
            'primary_color': colors['primary'],
            'secondary_color': colors['secondary'],
            'accent_color': colors['accent']
        }