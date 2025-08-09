# Microsoft 365 License Tracker

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Microsoft Graph](https://img.shields.io/badge/Microsoft%20Graph-API-green)](https://docs.microsoft.com/en-us/graph/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Comprehensive Microsoft 365 license usage tracker with cost optimization analytics and automated reporting dashboard.

## Overview

Track, analyze, and optimize your Microsoft 365 license usage with real-time dashboards, cost analysis, and automated reporting. Perfect for IT administrators managing large M365 deployments.

## Features

- **Real-time Dashboard**: Interactive web dashboard with usage analytics
- **Cost Optimization**: Identify unused licenses and potential savings
- **Automated Reporting**: Scheduled reports via email and Teams
- **Multi-tenant Support**: Manage multiple M365 tenants
- **Usage Analytics**: Detailed user activity and license utilization
- **Compliance Tracking**: Monitor license compliance and assignments

##  Demo

[View Live Demo](https://jaquanwatson.github.io/license-tracker-demo.html)

![License Tracker Dashboard](https://via.placeholder.com/800x400/0066cc/ffffff?text=M365+License+Dashboard)

## Installation

### Prerequisites

- Python 3.8 or higher
- Microsoft Graph API permissions:
  - `User.Read.All`
  - `Organization.Read.All`
  - `Directory.Read.All`

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jaquanwatson/m365-license-tracker.git
   cd m365-license-tracker
Install dependencies

bash

pip install -r requirements.txt
Configure authentication

bash

cp config.example.json config.json
# Edit config.json with your Azure app details
Run the application

bash

python app.py
Access dashboard
Open http://localhost:5000 in your browser

Configuration
json

{
  "azure": {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "tenant_id": "your-tenant-id"
  },
  "reporting": {
    "email_enabled": true,
    "email_recipients": ["admin@company.com"],
    "report_frequency": "weekly"
  },
  "thresholds": {
    "unused_days": 30,
    "cost_alert_threshold": 1000
  }
}
## Dashboard Features
License Overview
Total licenses by type
Active vs. unused licenses
Monthly cost breakdown
Usage trends over time
Cost Analysis
Unused license identification
Potential savings calculations
Cost per department/user
Budget vs. actual spending
User Analytics
Individual user license assignments
Last activity tracking
License utilization rates
Compliance status
API Endpoints
python

# Get license summary
GET /api/licenses/summary

# Get user details
GET /api/users/{user_id}/licenses

# Get cost analysis
GET /api/costs/analysis

# Generate report
POST /api/reports/generate

# Sample Reports
Weekly License Report
code

Microsoft 365 License Report - Week of Jan 8, 2025
================================================

Summary:
- Total Licenses: 1,247
- Active Users: 1,089 (87%)
- Unused Licenses: 158
- Monthly Cost: $18,705
- Potential Savings: $2,370/month

Top Unused License Types:
1. Power BI Pro: 45 licenses ($450/month)
2. Project Plan 3: 32 licenses ($960/month)
3. Visio Plan 2: 28 licenses ($420/month)

Recommendations:
- Remove 45 unused Power BI Pro licenses
- Consider downgrading 15 E5 to E3 licenses
- Review Project Plan 3 assignments

## Security & Compliance
Secure Authentication: Uses Azure AD app registration
Least Privilege: Minimal required permissions
Data Privacy: No sensitive data stored locally
Audit Logging: All actions logged for compliance
Encryption: All API communications encrypted
## Deployment Options
Docker Deployment
bash

docker build -t m365-license-tracker .
docker run -p 5000:5000 m365-license-tracker
Azure Container Instances
bash

az container create \
  --resource-group myResourceGroup \
  --name license-tracker \
  --image m365-license-tracker:latest \
  --ports 5000
## Contributing
Contributions are welcome! Please read our Contributing Guide for details.

Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
Email: jqwatson96@gmail.com

LinkedIn: jaquanwatson

Issues: GitHub Issues

Acknowledgments

Microsoft Graph API team

Python Flask community

Chart.js for visualization components

⭐ Found this useful? Give it a star! ⭐