"""
Other Document Generator (receipts, invoices, etc.)
"""

import os
import glob
import random
from datetime import datetime, timedelta
import sys

# Add parent directory to path for base_generator import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from base_generator import BaseDocumentGenerator


class OtherGenerator(BaseDocumentGenerator):
    """Generator for other document types (receipts, invoices, etc.) with round-robin template selection."""
    
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
    
    def generate_items(self, num_items=None):
        """Generate a list of items for receipt/invoice."""
        if num_items is None:
            num_items = random.randint(1, 8)
        
        items = []
        categories = [
            'Electronics', 'Clothing', 'Food & Beverage', 'Home & Garden',
            'Books', 'Sports & Outdoors', 'Health & Beauty', 'Automotive',
            'Office Supplies', 'Toys & Games'
        ]
        
        for _ in range(num_items):
            category = random.choice(categories)
            
            # Generate item based on category
            if category == 'Electronics':
                item_names = ['Smartphone Case', 'USB Cable', 'Wireless Charger', 'Bluetooth Speaker', 'Power Bank']
            elif category == 'Clothing':
                item_names = ['T-Shirt', 'Jeans', 'Sneakers', 'Jacket', 'Cap', 'Sweater']
            elif category == 'Food & Beverage':
                item_names = ['Coffee', 'Sandwich', 'Snacks', 'Energy Drink', 'Fruit Bowl', 'Muffin']
            elif category == 'Home & Garden':
                item_names = ['Plant Pot', 'Garden Tool', 'Light Bulb', 'Storage Box', 'Cleaning Supply']
            elif category == 'Books':
                item_names = ['Novel', 'Cookbook', 'Magazine', 'Technical Manual', 'Notebook']
            elif category == 'Sports & Outdoors':
                item_names = ['Water Bottle', 'Fitness Tracker', 'Yoga Mat', 'Sports Gloves', 'Backpack']
            elif category == 'Health & Beauty':
                item_names = ['Shampoo', 'Moisturizer', 'Vitamins', 'Toothbrush', 'Face Mask']
            elif category == 'Automotive':
                item_names = ['Car Charger', 'Air Freshener', 'Floor Mats', 'Windshield Wiper', 'Motor Oil']
            elif category == 'Office Supplies':
                item_names = ['Pen Set', 'Notebook', 'Paper Clips', 'Stapler', 'Folder', 'Calculator']
            else:  # Toys & Games
                item_names = ['Board Game', 'Puzzle', 'Action Figure', 'Card Game', 'Building Blocks']
            
            item_name = random.choice(item_names)
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(2.99, 99.99), 2)
            total_price = round(quantity * unit_price, 2)
            
            items.append({
                'name': item_name,
                'quantity': quantity,
                'unit_price': f"{unit_price:.2f}",
                'total_price': f"{total_price:.2f}"
            })
        
        return items
    
    def calculate_totals(self, items):
        """Calculate subtotal, tax, and total for the receipt."""
        subtotal = sum(float(item['total_price']) for item in items)
        
        # Random tax rate between 5% and 10%
        tax_rate = random.uniform(0.05, 0.10)
        tax_amount = subtotal * tax_rate
        
        # Occasionally add discount
        discount_amount = 0
        if random.random() < 0.3:  # 30% chance of discount
            discount_rate = random.uniform(0.05, 0.20)
            discount_amount = subtotal * discount_rate
        
        total = subtotal - discount_amount + tax_amount
        
        return {
            'subtotal': f"{subtotal:.2f}",
            'discount': f"{discount_amount:.2f}" if discount_amount > 0 else None,
            'tax_rate': f"{tax_rate * 100:.1f}%",
            'tax_amount': f"{tax_amount:.2f}",
            'total': f"{total:.2f}"
        }
    
    def generate_fake_data(self):
        """Generate fake data for various document types."""
        # Determine document type based on template name
        template_path = self.get_html_template_path()
        template_name = os.path.basename(template_path).lower()
        
        if 'receipt' in template_name:
            return self.generate_receipt_data()
        elif 'invoice' in template_name:
            return self.generate_invoice_data()
        else:
            # Default to receipt
            return self.generate_receipt_data()
    
    def generate_receipt_data(self):
        """Generate fake data specifically for receipts."""
        # Store information
        store_name = random.choice([
            'QuickMart', 'SuperSave', 'MegaStore', 'CityShop', 'FreshMarket',
            'TechZone', 'StyleHub', 'HomeBase', 'GreenLeaf', 'ValuePlus'
        ])
        
        store_address = self.fake.address().replace('\n', '<br>')
        store_phone = self.fake.phone_number()
        
        # Receipt information
        receipt_number = random.randint(100000, 999999)
        transaction_date = self.fake.date_time_between(start_date='-30d', end_date='now')
        cashier_id = random.randint(100, 999)
        register_number = random.randint(1, 10)
        
        # Items
        items = self.generate_items()
        totals = self.calculate_totals(items)
        
        # Payment method
        payment_methods = ['Cash', 'Credit Card', 'Debit Card', 'Mobile Payment']
        payment_method = random.choice(payment_methods)
        
        if payment_method in ['Credit Card', 'Debit Card']:
            card_number = f"****-****-****-{random.randint(1000, 9999)}"
        else:
            card_number = None
        
        return {
            'store_name': store_name,
            'store_address': store_address,
            'store_phone': store_phone,
            'receipt_number': receipt_number,
            'transaction_date': transaction_date.strftime('%m/%d/%Y %I:%M %p'),
            'cashier_id': cashier_id,
            'register_number': register_number,
            'items': items,
            'subtotal': totals['subtotal'],
            'discount': totals['discount'],
            'tax_rate': totals['tax_rate'],
            'tax_amount': totals['tax_amount'],
            'total': totals['total'],
            'payment_method': payment_method,
            'card_number': card_number,
            'change_given': f"{random.uniform(0, 20):.2f}" if payment_method == 'Cash' else None
        }
    
    def generate_invoice_data(self):
        """Generate fake data specifically for invoices."""
        # Company information
        company_name = self.fake.company()
        company_address = self.fake.address().replace('\n', '<br>')
        company_phone = self.fake.phone_number()
        company_email = self.fake.company_email()
        
        # Client information
        client_name = random.choice([self.fake.name(), self.fake.company()])
        client_address = self.fake.address().replace('\n', '<br>')
        
        # Invoice details
        invoice_number = f"INV-{random.randint(1000, 9999)}"
        invoice_date = self.fake.date_between(start_date='-60d', end_date='today')
        due_date = invoice_date + timedelta(days=random.randint(15, 45))
        
        # Items/Services
        items = self.generate_items(random.randint(1, 5))
        # For invoices, modify item names to be more service-oriented
        service_names = [
            'Consulting Services', 'Website Development', 'Graphic Design', 
            'Content Writing', 'SEO Optimization', 'Data Analysis',
            'Software Development', 'Project Management', 'Training Session'
        ]
        for item in items:
            if random.random() < 0.7:  # 70% chance to use service name
                item['name'] = random.choice(service_names)
                item['quantity'] = 1  # Services usually billed as single units
                item['unit_price'] = f"{random.uniform(50, 500):.2f}"
                item['total_price'] = item['unit_price']
        
        totals = self.calculate_totals(items)
        
        return {
            'company_name': company_name,
            'company_address': company_address,
            'company_phone': company_phone,
            'company_email': company_email,
            'client_name': client_name,
            'client_address': client_address,
            'invoice_number': invoice_number,
            'invoice_date': invoice_date.strftime('%m/%d/%Y'),
            'due_date': due_date.strftime('%m/%d/%Y'),
            'items': items,
            'subtotal': totals['subtotal'],
            'discount': totals['discount'],
            'tax_rate': totals['tax_rate'],
            'tax_amount': totals['tax_amount'],
            'total': totals['total'],
            'payment_terms': random.choice(['Net 30', 'Net 15', 'Due on Receipt', 'Net 45'])
        }