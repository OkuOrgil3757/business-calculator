"""
Business Calculator - Core calculation logic.
"""


class BusinessCalculator:
    """Core business calculation engine."""

    def __init__(self, data):
        # Basic info
        self.name = data.get("name", "Untitled")
        self.units = data.get("units", 1)

        # Costs
        self.product_cost = data.get("product_cost", 0)
        self.staff_salary = data.get("staff_salary", 0)
        self.tax = data.get("tax", 0)
        self.transportation = data.get("transportation", 0)
        self.marketing = data.get("marketing", 0)
        self.rent = data.get("rent", 0)
        self.utilities = data.get("utilities", 0)
        self.other_costs = data.get("other_costs", 0)

        # Pricing
        self.selling_price = data.get("selling_price", 0)
        self.target_margin = data.get("target_margin", 0)

    @property
    def total_fixed_costs(self):
        """Calculate total fixed costs (don't change with units)."""
        return self.staff_salary + self.rent + self.utilities + self.marketing

    @property
    def total_variable_costs(self):
        """Calculate total variable costs (change with units)."""
        return (self.product_cost + self.transportation + self.tax + self.other_costs) * self.units

    @property
    def total_costs(self):
        """Calculate total costs."""
        return self.total_fixed_costs + self.total_variable_costs

    @property
    def cost_per_unit(self):
        """Calculate cost per unit."""
        if self.units <= 0:
            return 0
        return self.total_costs / self.units

    @property
    def breakeven_price(self):
        """Calculate break-even price per unit."""
        return self.cost_per_unit

    @property
    def total_revenue(self):
        """Calculate total revenue."""
        return self.selling_price * self.units

    @property
    def gross_profit(self):
        """Calculate gross profit."""
        return self.total_revenue - self.total_costs

    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.total_revenue <= 0:
            return 0
        return (self.gross_profit / self.total_revenue) * 100

    @property
    def markup_percentage(self):
        """Calculate markup percentage over cost."""
        if self.cost_per_unit <= 0:
            return 0
        return ((self.selling_price - self.cost_per_unit) / self.cost_per_unit) * 100

    def price_for_margin(self, target_margin):
        """Calculate selling price needed for a target profit margin."""
        if target_margin >= 100:
            return float('inf')
        return self.cost_per_unit / (1 - target_margin / 100)

    def price_for_markup(self, target_markup):
        """Calculate selling price needed for a target markup."""
        return self.cost_per_unit * (1 + target_markup / 100)

    def units_to_breakeven(self):
        """Calculate units needed to break even at current price."""
        profit_per_unit = self.selling_price - self.cost_per_unit
        if profit_per_unit <= 0:
            return float('inf')
        return self.total_fixed_costs / profit_per_unit

    def to_dict(self):
        """Convert to dictionary for storage."""
        return {
            "name": self.name,
            "units": self.units,
            "product_cost": self.product_cost,
            "staff_salary": self.staff_salary,
            "tax": self.tax,
            "transportation": self.transportation,
            "marketing": self.marketing,
            "rent": self.rent,
            "utilities": self.utilities,
            "other_costs": self.other_costs,
            "selling_price": self.selling_price,
            "target_margin": self.target_margin,
            "total_costs": self.total_costs,
            "cost_per_unit": self.cost_per_unit,
            "breakeven_price": self.breakeven_price,
            "total_revenue": self.total_revenue,
            "gross_profit": self.gross_profit,
            "profit_margin": self.profit_margin,
        }
