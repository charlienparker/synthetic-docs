"""
Other Document Generator - Diverse document types including driver's licenses, receipts, letters, etc.
"""

import os
import glob
import random
from datetime import datetime, timedelta
import sys

from ..base_generator import BaseDocumentGenerator


class OtherGenerator(BaseDocumentGenerator):
    """Generator for diverse document types with template-specific data generation."""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.template_index = 0
        self.templates = self._load_templates()
        self.document_types = self._get_document_types()
    
    def _load_templates(self):
        """Load all HTML templates from the templates folder."""
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        template_files = glob.glob(os.path.join(templates_dir, '*.html'))
        if not template_files:
            raise FileNotFoundError(f"No HTML templates found in {templates_dir}")
        return sorted(template_files)  # Sort for consistent ordering
    
    def _get_document_types(self):
        """Map template filenames to document types for specialized data generation."""
        document_types = {}
        for template in self.templates:
            filename = os.path.basename(template)
            if 'drivers_license' in filename:
                document_types[template] = 'drivers_license'
            elif 'receipt' in filename:
                document_types[template] = 'receipt'
            elif 'letter' in filename:
                document_types[template] = 'letter'
            elif 'book' in filename:
                document_types[template] = 'book_page'
            elif 'invoice' in filename:
                document_types[template] = 'invoice'
            elif 'medical' in filename:
                document_types[template] = 'medical'
            elif 'bank' in filename:
                document_types[template] = 'bank_statement'
            elif 'report' in filename:
                document_types[template] = 'report_card'
            else:
                document_types[template] = 'generic'
        return document_types
    
    def get_html_template_path(self):
        """Return the next template path using round-robin selection."""
        template_path = self.templates[self.template_index]
        self.template_index = (self.template_index + 1) % len(self.templates)
        return template_path
    
    def generate_fake_data(self):
        """Generate fake data based on the current template type."""
        current_template = self.templates[self.template_index - 1]  # -1 because index was incremented
        doc_type = self.document_types.get(current_template, 'generic')
        
        if doc_type == 'drivers_license':
            return self.generate_drivers_license_data()
        elif doc_type == 'receipt':
            return self.generate_receipt_data()
        elif doc_type == 'letter':
            return self.generate_letter_data()
        elif doc_type == 'book_page':
            return self.generate_book_page_data()
        elif doc_type == 'invoice':
            return self.generate_invoice_data()
        elif doc_type == 'medical':
            return self.generate_medical_data()
        elif doc_type == 'bank_statement':
            return self.generate_bank_statement_data()
        elif doc_type == 'report_card':
            return self.generate_report_card_data()
        else:
            return self.generate_generic_data()
    
    def generate_drivers_license_data(self):
        """Generate realistic driver's license data."""
        states = [
            {'name': 'California', 'abbr': 'CA', 'format': 'A1234567'},
            {'name': 'Texas', 'abbr': 'TX', 'format': '12345678'},
            {'name': 'Florida', 'abbr': 'FL', 'format': 'A123-456-78-901-0'},
            {'name': 'New York', 'abbr': 'NY', 'format': '123456789'},
            {'name': 'Pennsylvania', 'abbr': 'PA', 'format': '12 345 678'},
            {'name': 'Illinois', 'abbr': 'IL', 'format': 'A123-4567-8901'},
            {'name': 'Ohio', 'abbr': 'OH', 'format': 'AB123456'},
        ]
        
        state = random.choice(states)
        birth_date = self.fake.date_of_birth(minimum_age=16, maximum_age=80)
        issue_date = self.fake.date_between(start_date='-5y', end_date='today')
        exp_date = issue_date.replace(year=issue_date.year + random.choice([4, 5, 8]))
        
        # Generate license number based on state format
        license_format = state['format']
        license_number = ''
        for char in license_format:
            if char.isalpha():
                license_number += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            elif char.isdigit():
                license_number += str(random.randint(0, 9))
            else:
                license_number += char
        
        return {
            'state_name': state['name'],
            'state_abbr': state['abbr'],
            'license_number': license_number,
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'address': self.fake.street_address(),
            'city': self.fake.city(),
            'state': state['abbr'],
            'zip_code': self.fake.zipcode(),
            'birth_date': birth_date.strftime('%m/%d/%Y'),
            'issue_date': issue_date.strftime('%m/%d/%Y'),
            'exp_date': exp_date.strftime('%m/%d/%Y'),
            'height': f"{random.randint(4, 6)}'-{random.randint(8, 11)}\"",
            'weight': random.randint(100, 300),
            'eye_color': random.choice(['BRN', 'BLU', 'GRN', 'HZL', 'GRY', 'AMB']),
            'sex': random.choice(['M', 'F']),
            'class': random.choice(['C', 'D', 'M', 'CDL']),
            'restrictions': random.choice(['NONE', 'CORRECTIVE LENSES', 'DAYTIME ONLY', '']),
            'donor': random.choice(['Y', 'N'])
        }
    
    def generate_receipt_data(self):
        """Generate store receipt data."""
        store_types = [
            {'name': 'SuperMart', 'type': 'grocery', 'phone': '(555) 123-4567'},
            {'name': 'TechWorld', 'type': 'electronics', 'phone': '(555) 234-5678'},
            {'name': 'Fashion Plus', 'type': 'clothing', 'phone': '(555) 345-6789'},
            {'name': 'Home Depot', 'type': 'hardware', 'phone': '(555) 456-7890'},
            {'name': 'BookCorner', 'type': 'bookstore', 'phone': '(555) 567-8901'},
        ]
        
        store = random.choice(store_types)
        items = self.generate_receipt_items(store['type'])
        
        subtotal = sum(item['total'] for item in items)
        tax_rate = random.uniform(0.06, 0.12)
        tax = subtotal * tax_rate
        total = subtotal + tax
        
        return {
            'store_name': store['name'],
            'store_phone': store['phone'],
            'store_address': self.fake.address().replace('\n', '<br>'),
            'transaction_date': self.fake.date_between(start_date='-30d', end_date='today').strftime('%m/%d/%Y'),
            'transaction_time': f"{random.randint(8, 22):02d}:{random.randint(0, 59):02d}",
            'cashier_id': f"#{random.randint(100, 999)}",
            'register': random.randint(1, 8),
            'items': items,
            'subtotal': f"{subtotal:.2f}",
            'tax_rate': f"{tax_rate:.1%}",
            'tax': f"{tax:.2f}",
            'total': f"{total:.2f}",
            'payment_method': random.choice(['VISA ****1234', 'CASH', 'MASTERCARD ****5678', 'DEBIT ****9012']),
            'transaction_id': f"T{random.randint(100000, 999999)}"
        }
    
    def generate_receipt_items(self, store_type):
        """Generate items specific to store type."""
        num_items = random.randint(2, 8)
        items = []
        
        item_databases = {
            'grocery': ['Milk', 'Bread', 'Eggs', 'Bananas', 'Chicken Breast', 'Rice', 'Pasta', 'Cereal', 'Orange Juice'],
            'electronics': ['USB Cable', 'Phone Case', 'Wireless Mouse', 'Keyboard', 'Headphones', 'Power Bank', 'Screen Protector'],
            'clothing': ['T-Shirt', 'Jeans', 'Sneakers', 'Jacket', 'Dress', 'Socks', 'Belt', 'Hat'],
            'hardware': ['Screws', 'Paint', 'Light Bulb', 'Extension Cord', 'Tool Set', 'Garden Hose', 'Door Handle'],
            'bookstore': ['Novel', 'Magazine', 'Notebook', 'Pen Set', 'Bookmark', 'Calendar', 'Textbook']
        }
        
        item_list = item_databases.get(store_type, item_databases['grocery'])
        
        for _ in range(num_items):
            item_name = random.choice(item_list)
            quantity = random.randint(1, 4)
            price = round(random.uniform(1.99, 89.99), 2)
            total = round(quantity * price, 2)
            
            items.append({
                'name': item_name,
                'quantity': quantity,
                'price': f"{price:.2f}",
                'total': total
            })
        
        return items
    
    def generate_letter_data(self):
        """Generate personal letter data."""
        letter_types = ['business', 'personal', 'complaint', 'thank_you', 'invitation']
        letter_type = random.choice(letter_types)
        
        sender_name = self.fake.name()
        recipient_name = self.fake.name()
        
        subjects = {
            'business': ['Job Application', 'Meeting Request', 'Project Update', 'Contract Discussion'],
            'personal': ['Family Update', 'Vacation Plans', 'Birthday Wishes', 'General Catch-up'],
            'complaint': ['Service Issue', 'Product Problem', 'Billing Error', 'Poor Experience'],
            'thank_you': ['Interview Thank You', 'Gift Appreciation', 'Help Acknowledgment', 'Service Praise'],
            'invitation': ['Wedding Invitation', 'Party Invitation', 'Event Invite', 'Dinner Invitation']
        }
        
        return {
            'sender_name': sender_name,
            'sender_address': self.fake.address().replace('\n', '<br>'),
            'recipient_name': recipient_name,
            'recipient_address': self.fake.address().replace('\n', '<br>'),
            'date': self.fake.date_between(start_date='-60d', end_date='today').strftime('%B %d, %Y'),
            'subject': random.choice(subjects[letter_type]),
            'salutation': random.choice(['Dear', 'Hello', 'Hi']),
            'body_paragraph_1': self.fake.paragraph(nb_sentences=4),
            'body_paragraph_2': self.fake.paragraph(nb_sentences=3),
            'body_paragraph_3': self.fake.paragraph(nb_sentences=2),
            'closing': random.choice(['Sincerely', 'Best regards', 'Yours truly', 'Kind regards']),
            'letter_type': letter_type
        }
    
    def generate_book_page_data(self):
        """Generate book page content."""
        book_genres = ['fiction', 'non_fiction', 'textbook', 'manual', 'cookbook']
        genre = random.choice(book_genres)
        
        titles = {
            'fiction': ['The Silent Garden', 'Midnight Chronicles', 'The Last Journey', 'Whispers in Time'],
            'non_fiction': ['The Art of Success', 'History Unveiled', 'Science Today', 'Understanding Nature'],
            'textbook': ['Introduction to Physics', 'Advanced Mathematics', 'Biology Fundamentals', 'Chemistry Principles'],
            'manual': ['User Manual', 'Operating Instructions', 'Safety Guidelines', 'Technical Specifications'],
            'cookbook': ['Family Recipes', 'International Cuisine', 'Healthy Cooking', 'Quick Meals']
        }
        
        return {
            'book_title': random.choice(titles[genre]),
            'author': self.fake.name(),
            'chapter_number': random.randint(1, 25),
            'chapter_title': self.fake.sentence(nb_words=4).replace('.', ''),
            'page_number': random.randint(1, 500),
            'content_paragraph_1': self.fake.paragraph(nb_sentences=6),
            'content_paragraph_2': self.fake.paragraph(nb_sentences=5),
            'content_paragraph_3': self.fake.paragraph(nb_sentences=4),
            'footnote': self.fake.sentence() if random.random() < 0.3 else '',
            'genre': genre,
            'publisher': f"{self.fake.company()} Publishing",
            'isbn': self.fake.isbn13(),
            'copyright_year': random.randint(1990, 2024)
        }
    
    def generate_invoice_data(self):
        """Generate business invoice data."""
        return {
            'company_name': self.fake.company(),
            'company_address': self.fake.address().replace('\n', '<br>'),
            'company_phone': self.fake.phone_number(),
            'company_email': self.fake.company_email(),
            'client_name': self.fake.name(),
            'client_company': self.fake.company(),
            'client_address': self.fake.address().replace('\n', '<br>'),
            'invoice_number': f"INV-{random.randint(1000, 9999)}",
            'invoice_date': self.fake.date_between(start_date='-30d', end_date='today').strftime('%m/%d/%Y'),
            'due_date': (self.fake.date_between(start_date='today', end_date='+30d')).strftime('%m/%d/%Y'),
            'services': self.generate_invoice_services(),
            'subtotal': '0',  # Will be calculated
            'tax': '0',       # Will be calculated
            'total': '0'      # Will be calculated
        }
    
    def generate_invoice_services(self):
        """Generate services for invoice."""
        services = ['Web Development', 'Graphic Design', 'Consulting', 'Content Writing', 'Marketing', 'Photography']
        num_services = random.randint(1, 4)
        service_list = []
        
        for _ in range(num_services):
            service = random.choice(services)
            hours = random.randint(5, 40)
            rate = round(random.uniform(50, 150), 2)
            total = hours * rate
            
            service_list.append({
                'description': f"{service} Services",
                'hours': hours,
                'rate': f"{rate:.2f}",
                'total': f"{total:.2f}"
            })
        
        return service_list
    
    def generate_medical_data(self):
        """Generate medical document data."""
        return {
            'patient_name': self.fake.name(),
            'patient_dob': self.fake.date_of_birth(minimum_age=1, maximum_age=90).strftime('%m/%d/%Y'),
            'patient_address': self.fake.address().replace('\n', '<br>'),
            'doctor_name': f"Dr. {self.fake.name()}",
            'clinic_name': f"{self.fake.city()} Medical Center",
            'clinic_address': self.fake.address().replace('\n', '<br>'),
            'visit_date': self.fake.date_between(start_date='-30d', end_date='today').strftime('%m/%d/%Y'),
            'diagnosis': random.choice(['Annual Checkup', 'Cold Symptoms', 'Blood Pressure Check', 'Follow-up Visit']),
            'prescription': random.choice(['Ibuprofen 200mg', 'Amoxicillin 500mg', 'Vitamin D', 'None prescribed']),
            'next_visit': (self.fake.date_between(start_date='today', end_date='+90d')).strftime('%m/%d/%Y'),
            'insurance': f"{random.choice(['BlueCross', 'Aetna', 'Kaiser', 'UnitedHealth'])} #{random.randint(100000, 999999)}"
        }
    
    def generate_bank_statement_data(self):
        """Generate bank statement data."""
        return {
            'bank_name': random.choice(['First National Bank', 'Community Trust', 'Metro Bank', 'Valley Credit Union']),
            'account_holder': self.fake.name(),
            'account_number': f"****{random.randint(1000, 9999)}",
            'statement_period': f"{self.fake.date_between(start_date='-60d', end_date='-30d').strftime('%m/%d/%Y')} - {self.fake.date_between(start_date='-30d', end_date='today').strftime('%m/%d/%Y')}",
            'beginning_balance': f"{random.uniform(500, 5000):.2f}",
            'ending_balance': f"{random.uniform(300, 6000):.2f}",
            'transactions': self.generate_bank_transactions()
        }
    
    def generate_bank_transactions(self):
        """Generate bank transaction list."""
        transactions = []
        for _ in range(random.randint(5, 15)):
            transaction_types = ['DEPOSIT', 'WITHDRAWAL', 'PURCHASE', 'TRANSFER']
            transactions.append({
                'date': self.fake.date_between(start_date='-30d', end_date='today').strftime('%m/%d'),
                'description': random.choice(['ATM Withdrawal', 'Online Purchase', 'Direct Deposit', 'Check Payment', 'Transfer']),
                'type': random.choice(transaction_types),
                'amount': f"{random.uniform(10, 500):.2f}"
            })
        return transactions
    
    def generate_report_card_data(self):
        """Generate school report card data."""
        subjects = ['Mathematics', 'English', 'Science', 'History', 'Art', 'Physical Education', 'Music']
        grades = []
        
        for subject in subjects[:random.randint(4, 7)]:
            grade_letter = random.choice(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-'])
            grades.append({
                'subject': subject,
                'grade': grade_letter,
                'comments': random.choice(['Excellent work', 'Good progress', 'Needs improvement', 'Outstanding effort'])
            })
        
        return {
            'student_name': self.fake.name(),
            'grade_level': random.choice(['3rd Grade', '4th Grade', '5th Grade', '6th Grade', '7th Grade', '8th Grade']),
            'school_name': f"{self.fake.city()} Elementary School",
            'teacher_name': f"Ms./Mr. {self.fake.last_name()}",
            'semester': random.choice(['Fall 2024', 'Spring 2024', 'Fall 2023']),
            'grades': grades,
            'attendance': f"{random.randint(85, 100)}%",
            'overall_gpa': f"{random.uniform(2.0, 4.0):.2f}"
        }
    
    def generate_generic_data(self):
        """Generate generic document data."""
        return {
            'title': self.fake.sentence(nb_words=4).replace('.', ''),
            'content': self.fake.paragraph(nb_sentences=6),
            'date': self.fake.date_between(start_date='-30d', end_date='today').strftime('%m/%d/%Y'),
            'name': self.fake.name(),
            'company': self.fake.company()
        }