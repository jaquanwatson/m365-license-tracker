import msal
import requests
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List
import logging

class LicenseManager:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.token = None
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for license tracking"""
        conn = sqlite3.connect('data/license_history.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS license_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                sku_id TEXT,
                sku_name TEXT,
                total_licenses INTEGER,
                assigned_licenses INTEGER,
                available_licenses INTEGER,
                cost_per_license REAL,
                total_cost REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                user_id TEXT,
                user_principal_name TEXT,
                display_name TEXT,
                licenses TEXT,
                last_activity TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def authenticate(self) -> bool:
        """Authenticate with Microsoft Graph"""
        try:
            app = msal.ConfidentialClientApplication(
                self.config['azure']['client_id'],
                authority=f"https://login.microsoftonline.com/{self.config['azure']['tenant_id']}",
                client_credential=self.config['azure']['client_secret']
            )
            
            result = app.acquire_token_for_client(
                scopes=["https://graph.microsoft.com/.default"]
            )
            
            if "access_token" in result:
                self.token = result["access_token"]
                return True
            else:
                logging.error(f"Authentication failed: {result}")
                return False
                
        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return False
    
    def get_license_usage(self) -> List[Dict]:
        """Get current license usage from Microsoft Graph"""
        if not self.token:
            return []
        
        headers = {'Authorization': f'Bearer {self.token}'}
        licenses = []
        
        try:
            url = "https://graph.microsoft.com/v1.0/subscribedSkus"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                skus = response.json().get('value', [])
                
                for sku in skus:
                    sku_name = sku.get('skuPartNumber', 'Unknown')
                    total = sku.get('prepaidUnits', {}).get('enabled', 0)
                    consumed = sku.get('consumedUnits', 0)
                    available = total - consumed
                    
                    # Get cost from config
                    cost_per_license = self.get_license_cost(sku_name)
                    
                    licenses.append({
                        'sku_id': sku.get('skuId'),
                        'sku_name': sku_name,
                        'total_licenses': total,
                        'assigned_licenses': consumed,
                        'available_licenses': available,
                        'utilization_percent': (consumed / total * 100) if total > 0 else 0,
                        'cost_per_license': cost_per_license,
                        'total_cost': total * cost_per_license,
                        'waste_cost': available * cost_per_license
                    })
                    
        except Exception as e:
            logging.error(f"Error getting license usage: {e}")
        
        return licenses
    
    def get_license_cost(self, sku_name: str) -> float:
        """Get license cost from configuration"""
        cost_mapping = {
            'O365_BUSINESS_ESSENTIALS': self.config['costs']['business_basic'],
            'O365_BUSINESS_PREMIUM': self.config['costs']['business_standard'],
            'SPB': self.config['costs']['business_premium'],
            'ENTERPRISEPACK': self.config['costs']['e3'],
            'ENTERPRISEPREMIUM': self.config['costs']['e5']
        }
        return cost_mapping.get(sku_name, 0.0)
    
    def get_user_licenses(self) -> List[Dict]:
        """Get detailed user license assignments"""
        if not self.token:
            return []
        
        headers = {'Authorization': f'Bearer {self.token}'}
        users = []
        
        try:
            url = "https://graph.microsoft.com/v1.0/users"
            params = {
                '$select': 'id,userPrincipalName,displayName,assignedLicenses,signInActivity',
                '$top': 999
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                user_data = response.json().get('value', [])
                
                for user in user_data:
                    if user.get('assignedLicenses'):
                        last_activity = user.get('signInActivity', {}).get('lastSignInDateTime')
                        
                        users.append({
                            'user_id': user.get('id'),
                            'user_principal_name': user.get('userPrincipalName'),
                            'display_name': user.get('displayName'),
                            'licenses': [lic.get('skuId') for lic in user.get('assignedLicenses', [])],
                            'last_activity': last_activity
                        })
                        
        except Exception as e:
            logging.error(f"Error getting user licenses: {e}")
        
        return users
    
    def save_usage_data(self, licenses: List[Dict], users: List[Dict]):
        """Save usage data to database"""
        conn = sqlite3.connect('data/license_history.db')
        cursor = conn.cursor()
        current_date = datetime.now().isoformat()
        
        # Save license usage
        for license_data in licenses:
            cursor.execute('''
                INSERT INTO license_usage 
                (date, sku_id, sku_name, total_licenses, assigned_licenses, 
                 available_licenses, cost_per_license, total_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                current_date,
                license_data['sku_id'],
                license_data['sku_name'],
                license_data['total_licenses'],
                license_data['assigned_licenses'],
                license_data['available_licenses'],
                license_data['cost_per_license'],
                license_data['total_cost']
            ))
        
        # Save user licenses
        for user in users:
            cursor.execute('''
                INSERT INTO user_licenses 
                (date, user_id, user_principal_name, display_name, licenses, last_activity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                current_date,
                user['user_id'],
                user['user_principal_name'],
                user['display_name'],
                json.dumps(user['licenses']),
                user['last_activity']
            ))
        
        conn.commit()
        conn.close()
    
    def get_optimization_recommendations(self) -> List[Dict]:
        """Generate cost optimization recommendations"""
        recommendations = []
        licenses = self.get_license_usage()
        
        for license_data in licenses:
            utilization = license_data['utilization_percent']
            available = license_data['available_licenses']
            waste_cost = license_data['waste_cost']
            
            if utilization < 80 and available > 5:
                recommendations.append({
                    'type': 'reduce_licenses',
                    'sku_name': license_data['sku_name'],
                    'current_total': license_data['total_licenses'],
                    'recommended_total': license_data['assigned_licenses'] + 2,
                    'potential_savings': waste_cost * 0.8,
                    'description': f"Consider reducing {license_data['sku_name']} licenses by {available - 2} to save ${waste_cost * 0.8:.2f}/month"
                })
        
        return recommendations
