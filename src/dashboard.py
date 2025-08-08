from flask import Flask, render_template, jsonify
import json
import sqlite3
from license_manager import LicenseManager
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)
license_manager = LicenseManager('config.json')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/license-usage')
def api_license_usage():
    if license_manager.authenticate():
        licenses = license_manager.get_license_usage()
        return jsonify(licenses)
    return jsonify([])

@app.route('/api/recommendations')
def api_recommendations():
    recommendations = license_manager.get_optimization_recommendations()
    return jsonify(recommendations)

@app.route('/api/usage-chart')
def api_usage_chart():
    conn = sqlite3.connect('data/license_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT date, sku_name, assigned_licenses, total_licenses
        FROM license_usage
        WHERE date >= date('now', '-30 days')
        ORDER BY date
    ''')
    
    data = cursor.fetchall()
    conn.close()
    
    # Create plotly chart
    fig = go.Figure()
    
    # Group by SKU
    skus = {}
    for row in data:
        date, sku_name, assigned, total = row
        if sku_name not in skus:
            skus[sku_name] = {'dates': [], 'assigned': [], 'total': []}
        skus[sku_name]['dates'].append(date)
        skus[sku_name]['assigned'].append(assigned)
        skus[sku_name]['total'].append(total)
    
    for sku_name, sku_data in skus.items():
        fig.add_trace(go.Scatter(
            x=sku_data['dates'],
            y=sku_data['assigned'],
            mode='lines+markers',
            name=f'{sku_name} (Assigned)',
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title='License Usage Trends',
        xaxis_title='Date',
        yaxis_title='Number of Licenses',
        hovermode='x unified'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
