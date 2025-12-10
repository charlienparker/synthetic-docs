"""
W-2 Tax Form Document Generator
"""

import os
import glob
import random
from datetime import datetime
import sys

from ..base_generator import BaseDocumentGenerator


class W2Generator(BaseDocumentGenerator):
    """Generator for W-2 tax forms with round-robin template selection."""
    
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
    
    def generate_fake_data(self):
        """Generate fake data for W-2 form."""
        # Generate realistic wage amounts
        annual_wages = random.randint(30000, 150000)
        federal_tax_rate = random.uniform(0.18, 0.28)
        state_tax_rate = random.uniform(0.03, 0.08)
        
        federal_withholding = annual_wages * federal_tax_rate
        state_withholding = annual_wages * state_tax_rate
        social_security_wages = min(annual_wages, 160200)  # 2023 SS wage base
        social_security_tax = social_security_wages * 0.062
        medicare_tax = annual_wages * 0.0145
        
        # Generate employer info
        employer_name = self.fake.company()
        employer_address = self.fake.address().replace('\n', '<br>')
        
        # Generate employee info
        employee_first_name = self.fake.first_name()
        employee_last_name = self.fake.last_name()
        employee_address = self.fake.address().replace('\n', '<br>')
        
        # Generate random tax year from modern era (2000-current year)
        current_year = datetime.now().year
        tax_year = random.randint(2000, current_year)
        
        return {
            'tax_year': tax_year,
            'employee_ssn': self.fake.ssn(),
            'employee_first_name': employee_first_name,
            'employee_last_name': employee_last_name,
            'employee_address': employee_address,
            'employer_ein': f"{random.randint(10,99)}-{random.randint(1000000,9999999)}",
            'employer_name': employer_name,
            'employer_address': employer_address,
            'employer_state_id': f"{random.randint(100000,999999)}",
            'control_number': f"{random.randint(10000,99999)}",
            'wages': f"{annual_wages:,.2f}",
            'federal_tax_withheld': f"{federal_withholding:,.2f}",
            'social_security_wages': f"{social_security_wages:,.2f}",
            'social_security_tax': f"{social_security_tax:,.2f}",
            'medicare_wages': f"{annual_wages:,.2f}",
            'medicare_tax': f"{medicare_tax:,.2f}",
            'social_security_tips': "0.00",
            'allocated_tips': "0.00",
            'dependent_care_benefits': f"{random.randint(0, 5000):,.2f}" if random.random() > 0.7 else "0.00",
            'nonqualified_plans': f"{random.randint(0, 10000):,.2f}" if random.random() > 0.8 else "0.00",
            'state_wages': f"{annual_wages:,.2f}",
            'state_tax_withheld': f"{state_withholding:,.2f}",
            'state': self.fake.state_abbr(),
            'local_wages': f"{annual_wages:,.2f}" if random.random() > 0.5 else "",
            'local_tax': f"{annual_wages * random.uniform(0.01, 0.03):,.2f}" if random.random() > 0.5 else "",
            'locality_name': self.fake.city() if random.random() > 0.5 else ""
        }