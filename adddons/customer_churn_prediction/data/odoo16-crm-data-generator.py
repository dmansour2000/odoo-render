import csv
import random
from datetime import datetime, timedelta
import uuid
from faker import Faker
import argparse

faker = Faker()

# Configuration
COMPANIES = 150  # Number of companies to generate
CONTACTS_PER_COMPANY_MIN = 1
CONTACTS_PER_COMPANY_MAX = 5
OPPORTUNITIES_MIN = 300  # Minimum number of opportunities
OPPORTUNITIES_MAX = 500  # Maximum number of opportunities

# CRM Stages
STAGES = [
    {'name': 'New', 'probability': 10},
    {'name': 'Qualification', 'probability': 30},
    {'name': 'Proposition', 'probability': 50},
    {'name': 'Negotiation', 'probability': 70},
    {'name': 'Won', 'probability': 100},
    {'name': 'Lost', 'probability': 0}
]

# CRM Teams
TEAMS = [
    'Direct Sales',
    'Indirect Sales',
    'Website Sales',
    'Point of Sale'
]

# Sales People (empty for now, to be populated with actual Odoo users)
SALES_PEOPLE = [
    {'name': 'Mark Johnson', 'email': 'mark.johnson@example.com'},
    {'name': 'Sarah Chen', 'email': 'sarah.chen@example.com'},
    {'name': 'David Rodriguez', 'email': 'david.rodriguez@example.com'},
    {'name': 'Emily Smith', 'email': 'emily.smith@example.com'}
]

# Product Categories
PRODUCT_CATEGORIES = [
    'Software Services',
    'Hardware Products',
    'Consulting Services',
    'Training',
    'Support Contracts'
]

# Products with price ranges
PRODUCTS = [
    {'name': 'Odoo Implementation', 'category': 'Software Services', 'min_price': 5000, 'max_price': 50000},
    {'name': 'Server Setup', 'category': 'Hardware Products', 'min_price': 2000, 'max_price': 15000},
    {'name': 'Business Process Consulting', 'category': 'Consulting Services', 'min_price': 3000, 'max_price': 25000},
    {'name': 'User Training', 'category': 'Training', 'min_price': 1000, 'max_price': 10000},
    {'name': 'Premium Support Plan', 'category': 'Support Contracts', 'min_price': 2500, 'max_price': 20000},
    {'name': 'Custom Development', 'category': 'Software Services', 'min_price': 8000, 'max_price': 60000},
    {'name': 'Network Infrastructure', 'category': 'Hardware Products', 'min_price': 5000, 'max_price': 40000},
    {'name': 'ERP Migration', 'category': 'Software Services', 'min_price': 10000, 'max_price': 100000},
    {'name': 'Database Optimization', 'category': 'Consulting Services', 'min_price': 2000, 'max_price': 15000},
    {'name': 'Admin Training', 'category': 'Training', 'min_price': 1500, 'max_price': 12000}
]

# Tags
TAGS = [
    'High Priority',
    'Hot Lead',
    'Existing Customer',
    'Strategic Account',
    'SMB',
    'Enterprise',
    'Public Sector',
    'Healthcare',
    'Education',
    'Manufacturing',
    'Retail'
]

# Countries and states
COUNTRIES = [
    {'name': 'United States', 'code': 'US', 'states': [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]},
    {'name': 'Canada', 'code': 'CA', 'states': [
        'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'ON', 'PE', 'QC', 'SK'
    ]},
    {'name': 'United Kingdom', 'code': 'UK', 'states': []},
    {'name': 'France', 'code': 'FR', 'states': []},
    {'name': 'Germany', 'code': 'DE', 'states': []},
    {'name': 'Spain', 'code': 'ES', 'states': []},
    {'name': 'Italy', 'code': 'IT', 'states': []},
    {'name': 'Netherlands', 'code': 'NL', 'states': []},
    {'name': 'Belgium', 'code': 'BE', 'states': []},
    {'name': 'Australia', 'code': 'AU', 'states': [
        'ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA'
    ]}
]

# Company Types
COMPANY_TYPES = ['Individual', 'Company']
COMPANY_INDUSTRIES = [
    'Agriculture', 'Apparel', 'Banking', 'Biotechnology', 'Chemicals',
    'Communications', 'Construction', 'Consulting', 'Education', 'Electronics',
    'Energy', 'Engineering', 'Entertainment', 'Environmental', 'Finance',
    'Food & Beverage', 'Government', 'Healthcare', 'Hospitality', 'Insurance',
    'Machinery', 'Manufacturing', 'Media', 'Not For Profit', 'Recreation',
    'Retail', 'Shipping', 'Technology', 'Telecommunications', 'Transportation',
    'Utilities'
]

def random_date(start, end):
    """Generate a random date between start and end dates"""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_companies(num_companies):
    """Generate company data"""
    companies = []
    
    for i in range(num_companies):
        country_data = random.choice(COUNTRIES)
        country_name = country_data['name']
        country_code = country_data['code']
        
        state_code = ''
        if country_data['states']:
            state_code = random.choice(country_data['states'])
        
        company_type = random.choice(COMPANY_TYPES)
        if company_type == 'Individual':
            name = faker.name()
        else:
            name = faker.company()
        
        company = {
            'id': i + 1,
            'name': name,
            'is_company': company_type == 'Company',
            'type': company_type,
            'industry': random.choice(COMPANY_INDUSTRIES) if company_type == 'Company' else '',
            'street': faker.street_address(),
            'street2': faker.secondary_address() if random.random() < 0.3 else '',
            'city': faker.city(),
            'state_code': state_code,
            'zip': faker.zipcode(),
            'country_code': country_code,
            'country_name': country_name,
            'email': faker.company_email() if company_type == 'Company' else faker.email(),
            'phone': faker.phone_number(),
            'mobile': faker.phone_number() if random.random() < 0.7 else '',
            'website': faker.url() if company_type == 'Company' and random.random() < 0.7 else '',
            'customer_rank': random.randint(0, 10),
            'supplier_rank': random.randint(0, 5) if random.random() < 0.3 else 0,
            'tags': random.sample(TAGS, random.randint(0, 3)) if random.random() < 0.7 else [],
            'external_id': f'company_{i+1}'
        }
        companies.append(company)
    
    return companies

def generate_contacts(companies):
    """Generate contact data based on companies"""
    contacts = []
    contact_id = 1
    
    for company in companies:
        # Skip contacts for type 'Individual' as they are already the contact
        if company['type'] == 'Individual':
            continue
        
        num_contacts = random.randint(CONTACTS_PER_COMPANY_MIN, CONTACTS_PER_COMPANY_MAX)
        
        for j in range(num_contacts):
            function = faker.job()
            
            # First contact is usually higher in hierarchy
            if j == 0:
                functions = ['CEO', 'President', 'Director', 'Owner', 'Manager']
                function = random.choice(functions)
                
            contact = {
                'id': contact_id,
                'name': faker.name(),
                'company_id': company['id'],
                'company_name': company['name'],
                'function': function,
                'email': faker.email(),
                'phone': faker.phone_number(),
                'mobile': faker.phone_number() if random.random() < 0.8 else '',
                'notes': faker.text(max_nb_chars=200) if random.random() < 0.3 else '',
                'external_id': f'contact_{contact_id}'
            }
            
            contacts.append(contact)
            contact_id += 1
    
    return contacts

def generate_opportunities(companies, contacts):
    """Generate CRM opportunities"""
    opportunities = []
    
    # Create a mapping of company_id to contacts for that company
    company_contacts = {}
    for contact in contacts:
        company_id = contact['company_id']
        if company_id not in company_contacts:
            company_contacts[company_id] = []
        company_contacts[company_id].append(contact)
    
    # Add individual companies as their own contact
    for company in companies:
        if company['type'] == 'Individual':
            if company['id'] not in company_contacts:
                company_contacts[company['id']] = [{
                    'id': None,
                    'name': company['name'],
                    'company_id': company['id'],
                    'company_name': company['name']
                }]
    
    num_opportunities = random.randint(OPPORTUNITIES_MIN, OPPORTUNITIES_MAX)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for i in range(num_opportunities):
        # Select a random company
        company = random.choice(companies)
        company_id = company['id']
        
        # Select a contact from this company if available
        contact = None
        if company_id in company_contacts and company_contacts[company_id]:
            contact = random.choice(company_contacts[company_id])
        
        # Select a random product
        product = random.choice(PRODUCTS)
        
        # Generate a random creation date
        create_date = random_date(start_date, end_date)
        
        # Select a random stage with weighted probabilities based on the creation date
        days_old = (end_date - create_date).days
        
        # Newer opportunities tend to be in earlier stages
        if days_old < 30:
            stage_weights = [0.5, 0.3, 0.1, 0.05, 0.03, 0.02]
        elif days_old < 90:
            stage_weights = [0.1, 0.3, 0.3, 0.15, 0.1, 0.05]
        else:
            stage_weights = [0.05, 0.1, 0.15, 0.2, 0.3, 0.2]
        
        stage = random.choices(STAGES, weights=stage_weights, k=1)[0]
        
        # Generate expected closing date based on stage and creation date
        if stage['name'] in ['Won', 'Lost']:
            expected_closing = random_date(create_date, create_date + timedelta(days=min(days_old, 180)))
        else:
            expected_closing = random_date(end_date, end_date + timedelta(days=90))
        
        # Generate a random amount within the product's price range
        amount = round(random.uniform(product['min_price'], product['max_price']), 2)
        
        # Assign a random salesperson
        salesperson = random.choice(SALES_PEOPLE)
        
        # Generate opportunity name
        opp_name = f"{product['name']} - {company['name']}"
        
        opportunity = {
            'id': i + 1,
            'name': opp_name,
            'partner_id': company['id'],
            'partner_name': company['name'],
            'contact_id': contact['id'] if contact and 'id' in contact else None,
            'contact_name': contact['name'] if contact else None,
            'stage_id': stage['name'],
            'probability': stage['probability'],
            'expected_revenue': amount,
            'planned_revenue': amount,
            'date_deadline': expected_closing.strftime('%Y-%m-%d'),
            'create_date': create_date.strftime('%Y-%m-%d'),
            'team_id': random.choice(TEAMS),
            'user_id': salesperson['name'],
            'user_email': salesperson['email'],
            'product_id': product['name'],
            'product_category': product['category'],
            'priority': random.choice(['0', '1', '2', '3']),
            'tags': random.sample(TAGS, random.randint(0, 3)) if random.random() < 0.6 else [],
            'external_id': f'opportunity_{i+1}'
        }
        
        opportunities.append(opportunity)
    
    return opportunities

def write_csv(data, filename, fieldnames=None):
    """Write data to CSV file"""
    if not fieldnames:
        fieldnames = data[0].keys() if data else []
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description='Generate realistic CRM data for Odoo 16')
    parser.add_argument('--companies', type=int, default=200, help='Number of companies to generate')
    parser.add_argument('--min-opps', type=int, default=400, help='Minimum number of opportunities')
    parser.add_argument('--max-opps', type=int, default=600, help='Maximum number of opportunities')
    parser.add_argument('--output-dir', type=str, default='.', help='Output directory for CSV files')
    args = parser.parse_args()

    # Update global variables
    global COMPANIES, OPPORTUNITIES_MIN, OPPORTUNITIES_MAX
    COMPANIES = args.companies
    OPPORTUNITIES_MIN = args.min_opps
    OPPORTUNITIES_MAX = args.max_opps
    
    print(f"Generating {COMPANIES} companies...")
    companies = generate_companies(COMPANIES)
    
    print("Generating contacts...")
    contacts = generate_contacts(companies)
    
    print(f"Generating {OPPORTUNITIES_MIN}-{OPPORTUNITIES_MAX} opportunities...")
    opportunities = generate_opportunities(companies, contacts)
    
    # Write to CSV files
    import os
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    print("Writing CSV files...")
    write_csv(companies, os.path.join(output_dir, 'res.partner.csv'))
    write_csv(contacts, os.path.join(output_dir, 'res.partner.contact.csv'))
    write_csv(opportunities, os.path.join(output_dir, 'crm.lead.csv'))
    
    print(f"Generated {len(companies)} companies, {len(contacts)} contacts, and {len(opportunities)} opportunities.")
    print(f"CSV files saved in {output_dir}")

if __name__ == "__main__":
    main()
