#!/usr/bin/env python3
"""
Business Calculator - Web Application
Calculate break-even, profit margins, and business analytics.
"""

from flask import Flask, render_template_string, request, redirect, url_for
from calculator import BusinessCalculator
from storage import load_calculations, save_calculations, generate_id
import json

app = Flask(__name__)

@app.template_filter('money')
def money_filter(value):
    """Format number with commas and 2 decimal places."""
    return "{:,.2f}".format(value)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Business Calculator</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0c0c1e 0%, #1a1a3e 50%, #0d2137 100%);
            background-attachment: fixed;
            color: #eee;
        }

        .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; }

        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 8px;
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 35px;
            font-size: 1.1em;
        }

        .card {
            background: rgba(30, 30, 60, 0.9);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.08);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 22px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .card-header h2 {
            color: #00d4ff;
            font-size: 1.4em;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
        }

        .form-group label {
            display: block;
            color: #999;
            font-size: 0.82em;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-group input, .form-group select {
            width: 100%;
            padding: 12px 14px;
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            background: rgba(20, 20, 50, 0.6);
            color: #fff;
            font-size: 1em;
            transition: all 0.3s;
        }

        .form-group input:focus {
            outline: none;
            border-color: #00d4ff;
            background: rgba(20, 20, 50, 0.9);
        }

        .section-title {
            color: #7b2ff7;
            font-size: 0.95em;
            margin: 22px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(123, 47, 247, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn {
            padding: 12px 28px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.95em;
            font-weight: 600;
            transition: all 0.3s;
        }

        .btn-primary {
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 212, 255, 0.4);
        }

        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: #fff;
            margin-left: 10px;
        }

        .btn-danger {
            background: #dc3545;
            color: white;
        }

        /* Results Section */
        .results-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }

        .result-box {
            background: rgba(20, 20, 50, 0.8);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .result-box .label {
            color: #888;
            font-size: 0.75em;
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }

        .result-box .value {
            font-size: 1.6em;
            font-weight: bold;
        }

        .result-box.cyan .value { color: #00d4ff; }
        .result-box.green .value { color: #00ff88; }
        .result-box.orange .value { color: #ffaa00; }
        .result-box.red .value { color: #ff4466; }
        .result-box.purple .value { color: #7b2ff7; }

        /* Breakdown */
        .breakdown {
            margin-top: 20px;
        }

        .breakdown-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .breakdown-row .item { color: #aaa; }
        .breakdown-row .amount { font-weight: 500; }
        .breakdown-row.total {
            border-top: 2px solid #7b2ff7;
            padding-top: 15px;
            margin-top: 10px;
        }
        .breakdown-row.total .item,
        .breakdown-row.total .amount {
            color: #7b2ff7;
            font-size: 1.1em;
            font-weight: 600;
        }

        /* Pricing Guide */
        .pricing-guide {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(123, 47, 247, 0.1));
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }

        .pricing-guide h3 {
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1.1em;
        }

        .pricing-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .pricing-row:last-child { border: none; }
        .pricing-row .margin { color: #888; }
        .pricing-row .price { color: #00ff88; font-weight: 600; }

        /* History Table */
        .history-table {
            width: 100%;
            border-collapse: collapse;
        }

        .history-table th {
            text-align: left;
            padding: 12px;
            color: #888;
            font-size: 0.8em;
            text-transform: uppercase;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .history-table td {
            padding: 15px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .history-table tr:hover {
            background: rgba(0, 212, 255, 0.05);
        }

        .history-table .name { color: #00d4ff; font-weight: 500; }
        .history-table .profit-positive { color: #00ff88; }
        .history-table .profit-negative { color: #ff4466; }

        .btn-small {
            padding: 6px 12px;
            font-size: 0.8em;
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        /* Scenario Analysis Table */
        .scenario-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        .scenario-table th {
            text-align: right;
            padding: 10px 12px;
            color: #888;
            font-size: 0.78em;
            text-transform: uppercase;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .scenario-table th:first-child { text-align: left; }

        .scenario-table td {
            text-align: right;
            padding: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 0.95em;
        }

        .scenario-table td:first-child { text-align: left; }

        .scenario-table tr:hover {
            background: rgba(0, 212, 255, 0.05);
        }

        .scenario-table .base-row {
            background: rgba(0, 212, 255, 0.1);
            font-weight: 600;
        }

        .scenario-table .base-row td {
            border-bottom: 2px solid rgba(0, 212, 255, 0.3);
        }

        .scenario-table .scenario-profit-positive { color: #00ff88; }
        .scenario-table .scenario-profit-negative { color: #ff4466; }

        @media (max-width: 768px) {
            .form-grid { grid-template-columns: 1fr 1fr; }
            .results-grid { grid-template-columns: 1fr 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Business Calculator</h1>
        <p class="subtitle">Break-even analysis, profit margins & cost management</p>

        <form method="POST" action="/calculate" class="card">
            <div class="card-header">
                <h2>New Calculation</h2>
            </div>

            <div class="form-grid">
                <div class="form-group">
                    <label>Product / Service Name</label>
                    <input type="text" name="name" placeholder="e.g. Product A" value="{{ form_data.name or '' }}" required>
                </div>
                <div class="form-group">
                    <label>Number of Units</label>
                    <input type="number" name="units" value="{{ form_data.units or 100 }}" min="1" required>
                </div>
                <div class="form-group">
                    <label>Selling Price per Unit ($)</label>
                    <input type="number" name="selling_price" value="{{ form_data.selling_price or 0 }}" step="0.01" placeholder="Leave 0 to auto-calculate">
                </div>
            </div>

            <div class="section-title">Variable Costs (per unit)</div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Product / Material Cost ($)</label>
                    <input type="number" name="product_cost" value="{{ form_data.product_cost or 0 }}" step="0.01">
                </div>
                <div class="form-group">
                    <label>Transportation / Shipping ($)</label>
                    <input type="number" name="transportation" value="{{ form_data.transportation or 0 }}" step="0.01">
                </div>
                <div class="form-group">
                    <label>Tax / Fees per Unit ($)</label>
                    <input type="number" name="tax" value="{{ form_data.tax or 0 }}" step="0.01">
                </div>
                <div class="form-group">
                    <label>Other Cost Name</label>
                    <input type="text" name="other_cost_name" placeholder="e.g. Packaging, Insurance" value="{{ form_data.other_cost_name or '' }}">
                </div>
                <div class="form-group">
                    <label>{{ form_data.other_cost_name or 'Other' }} Cost ($)</label>
                    <input type="number" name="other_costs" value="{{ form_data.other_costs or 0 }}" step="0.01">
                </div>
            </div>

            <div class="section-title">Fixed Costs (total)</div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Staff Salaries ($)</label>
                    <input type="number" name="staff_salary" value="{{ form_data.staff_salary or 0 }}" step="0.01">
                </div>
                <div class="form-group">
                    <label>Marketing / Advertising ($)</label>
                    <input type="number" name="marketing" value="{{ form_data.marketing or 0 }}" step="0.01">
                </div>
                <div class="form-group">
                    <label>Rent / Lease ($)</label>
                    <input type="number" name="rent" value="{{ form_data.rent or 0 }}" step="0.01">
                </div>
                <div class="form-group">
                    <label>Utilities ($)</label>
                    <input type="number" name="utilities" value="{{ form_data.utilities or 0 }}" step="0.01">
                </div>
            </div>

            <div class="section-title">Target</div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Target Profit Margin (%)</label>
                    <input type="number" name="target_margin" value="{{ form_data.target_margin if form_data.target_margin is not none else 30 }}" min="0" max="99">
                </div>
            </div>

            <div style="margin-top: 25px;">
                <button type="submit" class="btn btn-primary">Calculate</button>
                <button type="reset" class="btn btn-secondary">Clear</button>
            </div>
        </form>

        {% if calculations %}
        <div class="card">
            <div class="card-header">
                <h2>Saved Calculations</h2>
                <span style="color: #888;">{{ calculations|length }} record(s)</span>
            </div>
            <table class="history-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Units</th>
                        <th>Cost/Unit</th>
                        <th>Sell Price</th>
                        <th>Margin</th>
                        <th>Total Profit</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for calc in calculations %}
                    <tr>
                        <td class="name">{{ calc.name }}</td>
                        <td>{{ calc.units }}</td>
                        <td>${{ calc.cost_per_unit|money }}</td>
                        <td>${{ calc.selling_price|money }}</td>
                        <td>{{ "%.1f"|format(calc.profit_margin) }}%</td>
                        <td class="{{ 'profit-positive' if calc.gross_profit >= 0 else 'profit-negative' }}">
                            ${{ calc.gross_profit|money }}
                        </td>
                        <td>
                            <form method="POST" action="/delete/{{ loop.index0 }}" style="display:inline;">
                                <button type="submit" class="btn btn-danger btn-small">Delete</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}

        {% if result %}
        <div class="card">
            <div class="card-header">
                <h2>{{ result.name }} - Analysis</h2>
                <span style="color: #888;">{{ result.units }} units</span>
            </div>

            <div class="results-grid">
                <div class="result-box red">
                    <div class="label">Total Costs</div>
                    <div class="value">${{ result.total_costs|money }}</div>
                </div>
                <div class="result-box orange">
                    <div class="label">Break-even Price</div>
                    <div class="value">${{ result.breakeven_price|money }}</div>
                </div>
                <div class="result-box cyan">
                    <div class="label">Revenue</div>
                    <div class="value">${{ result.total_revenue|money }}</div>
                </div>
                <div class="result-box green">
                    <div class="label">Profit</div>
                    <div class="value">${{ result.gross_profit|money }}</div>
                </div>
            </div>

            <div class="results-grid">
                <div class="result-box purple">
                    <div class="label">Profit Margin</div>
                    <div class="value">{{ "%.1f"|format(result.profit_margin) }}%</div>
                </div>
                <div class="result-box cyan">
                    <div class="label">Cost per Unit</div>
                    <div class="value">${{ result.cost_per_unit|money }}</div>
                </div>
                <div class="result-box green">
                    <div class="label">Selling Price</div>
                    <div class="value">${{ result.selling_price|money }}</div>
                </div>
                <div class="result-box orange">
                    <div class="label">Profit per Unit</div>
                    <div class="value">${{ (result.selling_price - result.cost_per_unit)|money }}</div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div class="breakdown">
                    <h3 style="color: #7b2ff7; margin-bottom: 15px;">Variable Costs (per unit)</h3>
                    <div class="breakdown-row">
                        <span class="item">Product / Material</span>
                        <span class="amount">${{ result.product_cost|money }}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="item">Transportation / Shipping</span>
                        <span class="amount">${{ result.transportation|money }}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="item">Tax / Fees</span>
                        <span class="amount">${{ result.tax|money }}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="item">{{ result.other_cost_name or 'Other Variable' }}</span>
                        <span class="amount">${{ result.other_costs|money }}</span>
                    </div>
                    <div class="breakdown-row total">
                        <span class="item">Total Variable (x{{ result.units }})</span>
                        <span class="amount">${{ ((result.product_cost + result.transportation + result.tax + result.other_costs) * result.units)|money }}</span>
                    </div>
                </div>

                <div class="breakdown">
                    <h3 style="color: #7b2ff7; margin-bottom: 15px;">Fixed Costs (total)</h3>
                    <div class="breakdown-row">
                        <span class="item">Staff Salaries</span>
                        <span class="amount">${{ result.staff_salary|money }}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="item">Marketing / Advertising</span>
                        <span class="amount">${{ result.marketing|money }}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="item">Rent / Lease</span>
                        <span class="amount">${{ result.rent|money }}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="item">Utilities</span>
                        <span class="amount">${{ result.utilities|money }}</span>
                    </div>
                    <div class="breakdown-row total">
                        <span class="item">Total Fixed</span>
                        <span class="amount">${{ (result.staff_salary + result.marketing + result.rent + result.utilities)|money }}</span>
                    </div>
                </div>
            </div>

            <div class="pricing-guide">
                <h3>Pricing Guide - What to charge for different margins</h3>
                <div class="pricing-row">
                    <span class="margin">Break-even (0% profit)</span>
                    <span class="price">${{ result.breakeven_price|money }} per unit</span>
                </div>
                <div class="pricing-row">
                    <span class="margin">20% profit margin</span>
                    <span class="price">${{ (result.cost_per_unit / 0.8)|money }} per unit</span>
                </div>
                <div class="pricing-row">
                    <span class="margin">30% profit margin</span>
                    <span class="price">${{ (result.cost_per_unit / 0.7)|money }} per unit</span>
                </div>
                <div class="pricing-row">
                    <span class="margin">40% profit margin</span>
                    <span class="price">${{ (result.cost_per_unit / 0.6)|money }} per unit</span>
                </div>
                <div class="pricing-row">
                    <span class="margin">50% profit margin</span>
                    <span class="price">${{ (result.cost_per_unit / 0.5)|money }} per unit</span>
                </div>
                <div class="pricing-row">
                    <span class="margin">60% profit margin</span>
                    <span class="price">${{ (result.cost_per_unit / 0.4)|money }} per unit</span>
                </div>
            </div>

            {% if scenarios %}
            <div style="margin-top: 25px;">
                <h3 style="color: #00d4ff; margin-bottom: 12px;">Volume Scenario Analysis</h3>
                <p style="color: #666; font-size: 0.85em; margin-bottom: 15px;">How metrics change at different production volumes (fixed costs stay constant)</p>
                <table class="scenario-table">
                    <thead>
                        <tr>
                            <th>Volume %</th>
                            <th>Units</th>
                            <th>Total Costs</th>
                            <th>Cost/Unit</th>
                            <th>Revenue</th>
                            <th>Profit</th>
                            <th>Margin</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in scenarios %}
                        <tr class="{{ 'base-row' if s.is_base else '' }}">
                            <td>{{ s.pct }}%{{ ' (current)' if s.is_base else '' }}</td>
                            <td>{{ "{:,}"|format(s.units) }}</td>
                            <td>${{ s.total_costs|money }}</td>
                            <td>${{ s.cost_per_unit|money }}</td>
                            <td>${{ s.revenue|money }}</td>
                            <td class="{{ 'scenario-profit-positive' if s.profit >= 0 else 'scenario-profit-negative' }}">${{ s.profit|money }}</td>
                            <td class="{{ 'scenario-profit-positive' if s.margin >= 0 else 'scenario-profit-negative' }}">{{ "%.1f"|format(s.margin) }}%</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}

            <div style="margin-top: 20px;">
                <form method="POST" action="/save" style="display: inline;">
                    <input type="hidden" name="result_data" value='{{ result_json }}'>
                    <button type="submit" class="btn btn-primary">Save Calculation</button>
                </form>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    calculations = load_calculations()
    return render_template_string(HTML_TEMPLATE, calculations=calculations, result=None, result_json='', form_data={}, scenarios=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Store form data to keep values after calculation
    form_data = {
        "name": request.form.get('name', ''),
        "units": int(request.form.get('units', 1) or 1),
        "product_cost": float(request.form.get('product_cost', 0) or 0),
        "transportation": float(request.form.get('transportation', 0) or 0),
        "tax": float(request.form.get('tax', 0) or 0),
        "other_cost_name": request.form.get('other_cost_name', ''),
        "other_costs": float(request.form.get('other_costs', 0) or 0),
        "staff_salary": float(request.form.get('staff_salary', 0) or 0),
        "marketing": float(request.form.get('marketing', 0) or 0),
        "rent": float(request.form.get('rent', 0) or 0),
        "utilities": float(request.form.get('utilities', 0) or 0),
        "selling_price": float(request.form.get('selling_price', 0) or 0),
        "target_margin": float(request.form.get('target_margin', 30) or 30),
    }

    data = {
        "id": generate_id(),
        **form_data
    }

    calc = BusinessCalculator(data)

    # Auto-calculate selling price if not provided
    original_selling_price = form_data['selling_price']
    if data['selling_price'] == 0:
        data['selling_price'] = calc.price_for_margin(data['target_margin'])
        calc = BusinessCalculator(data)

    # Keep original selling price in form (0 if auto-calculated)
    form_data['selling_price'] = original_selling_price

    result = calc.to_dict()
    result['id'] = data['id']
    result['other_cost_name'] = form_data['other_cost_name']

    scenarios = calc.scenario_analysis()

    calculations = load_calculations()
    return render_template_string(HTML_TEMPLATE, calculations=calculations, result=result, result_json=json.dumps(result), form_data=form_data, scenarios=scenarios)

@app.route('/save', methods=['POST'])
def save():
    result_data = json.loads(request.form['result_data'])
    calculations = load_calculations()
    calculations.append(result_data)
    save_calculations(calculations)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    calculations = load_calculations()
    if 0 <= index < len(calculations):
        calculations.pop(index)
        save_calculations(calculations)
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Business Calculator")
    print("="*50)
    print("\n  Open: http://127.0.0.1:8080\n")
    app.run(host='127.0.0.1', debug=False, port=8080)
