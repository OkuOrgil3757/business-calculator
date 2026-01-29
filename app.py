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

        @media (max-width: 768px) {
            .form-grid { grid-template-columns: 1fr 1fr; }
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
                    <input type="text" name="name" placeholder="e.g. Product A" required>
                </div>
                <div class="form-group">
                    <label>Number of Units</label>
                    <input type="number" name="units" value="100" min="1" required>
                </div>
                <div class="form-group">
                    <label>Selling Price per Unit ($)</label>
                    <input type="number" name="selling_price" value="0" step="0.01">
                </div>
            </div>

            <div class="section-title">Variable Costs (per unit)</div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Product / Material Cost ($)</label>
                    <input type="number" name="product_cost" value="0" step="0.01">
                </div>
                <div class="form-group">
                    <label>Transportation / Shipping ($)</label>
                    <input type="number" name="transportation" value="0" step="0.01">
                </div>
                <div class="form-group">
                    <label>Tax / Fees per Unit ($)</label>
                    <input type="number" name="tax" value="0" step="0.01">
                </div>
                <div class="form-group">
                    <label>Other Variable Costs ($)</label>
                    <input type="number" name="other_costs" value="0" step="0.01">
                </div>
            </div>

            <div class="section-title">Fixed Costs (total)</div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Staff Salaries ($)</label>
                    <input type="number" name="staff_salary" value="0" step="0.01">
                </div>
                <div class="form-group">
                    <label>Marketing / Advertising ($)</label>
                    <input type="number" name="marketing" value="0" step="0.01">
                </div>
                <div class="form-group">
                    <label>Rent / Lease ($)</label>
                    <input type="number" name="rent" value="0" step="0.01">
                </div>
                <div class="form-group">
                    <label>Utilities ($)</label>
                    <input type="number" name="utilities" value="0" step="0.01">
                </div>
            </div>

            <div class="section-title">Target</div>
            <div class="form-grid">
                <div class="form-group">
                    <label>Target Profit Margin (%)</label>
                    <input type="number" name="target_margin" value="30" min="0" max="99">
                </div>
            </div>

            <div style="margin-top: 25px;">
                <button type="submit" class="btn btn-primary">Calculate</button>
                <button type="reset" class="btn btn-secondary">Clear</button>
            </div>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    calculations = load_calculations()
    return render_template_string(HTML_TEMPLATE, calculations=calculations, result=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = {
        "id": generate_id(),
        "name": request.form['name'],
        "units": int(request.form.get('units', 1) or 1),
        "product_cost": float(request.form.get('product_cost', 0) or 0),
        "transportation": float(request.form.get('transportation', 0) or 0),
        "tax": float(request.form.get('tax', 0) or 0),
        "other_costs": float(request.form.get('other_costs', 0) or 0),
        "staff_salary": float(request.form.get('staff_salary', 0) or 0),
        "marketing": float(request.form.get('marketing', 0) or 0),
        "rent": float(request.form.get('rent', 0) or 0),
        "utilities": float(request.form.get('utilities', 0) or 0),
        "selling_price": float(request.form.get('selling_price', 0) or 0),
        "target_margin": float(request.form.get('target_margin', 30) or 30),
    }

    calc = BusinessCalculator(data)
    result = calc.to_dict()
    result['id'] = data['id']

    calculations = load_calculations()
    return render_template_string(HTML_TEMPLATE, calculations=calculations, result=result)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Business Calculator")
    print("="*50)
    print("\n  Open: http://127.0.0.1:8080\n")
    app.run(host='127.0.0.1', debug=False, port=8080)
