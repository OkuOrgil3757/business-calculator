# Business Calculator

A web-based business analytics tool for calculating break-even points, profit margins, and pricing strategies.

## Features

- **Break-even Analysis**: Calculate the minimum price needed to cover all costs
- **Profit Margin Calculator**: Determine selling prices for target profit margins (20%, 30%, 40%, 50%, 60%)
- **Cost Management**: Track both variable and fixed costs separately
- **Pricing Guide**: See recommended prices for different profit margin targets
- **Save & Compare**: Store calculations for future reference

## Cost Categories

### Variable Costs (per unit)
- Product / Material cost
- Transportation / Shipping
- Tax / Fees
- Other variable costs

### Fixed Costs (total)
- Staff salaries
- Marketing / Advertising
- Rent / Lease
- Utilities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/business-calculator.git
cd business-calculator
```

2. Install dependencies:
```bash
pip install flask
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to: `http://127.0.0.1:8080`

## Project Structure

```
business_calculator/
├── app.py              # Flask web application
├── calculator.py       # Core calculation logic
├── storage.py          # JSON data persistence
├── data/
│   └── calculations.json   # Saved calculations
└── README.md
```

## Usage

1. Enter your product/service name and number of units
2. Fill in variable costs (per unit)
3. Fill in fixed costs (total amounts)
4. Set your target profit margin
5. Click "Calculate" to see analysis
6. Save calculations for future reference

## Technologies

- Python 3
- Flask (Web Framework)
- HTML/CSS (Frontend)
- JSON (Data Storage)
