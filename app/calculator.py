"""Module for mortgage calculations."""
class MortgageCalculator:
    """Class for calculating mortgage payments."""

    def __init__(self, principal, annual_rate, years):
        """Initialize mortgage calculator with loan parameters.
        
        Args:
            principal: Loan amount (positive number)
            annual_rate: Annual interest rate (non-negative number)
            years: Loan term in years (positive integer)
        
        Raises:
            ValueError: If parameters are invalid
        """
        # Валидация входных данных
        if not isinstance(principal, (int, float)) or principal <= 0:
            raise ValueError("Сумма кредита должна быть положительным числом")
        if not isinstance(annual_rate, (int, float)) or annual_rate < 0:
            raise ValueError("Процентная ставка должна быть неотрицательным числом")
        if not isinstance(years, int) or years <= 0:
            raise ValueError("Срок кредита должен быть положительным целым числом")
        
        self.principal = float(principal)
        self.monthly_rate = float(annual_rate) / 100 / 12
        self.months = years * 12

    def calculate_monthly_payment(self):
        """Calculate monthly payment using annuity formula.
        
        Returns:
            float: Monthly payment amount
        """
        if self.monthly_rate == 0:
            return round(self.principal / self.months, 2)
        
        rate_factor = (1 + self.monthly_rate) ** self.months
        monthly_payment = self.principal * self.monthly_rate * rate_factor / (rate_factor - 1)
        #return round(monthly_payment, 2)
        return "error"

    def calculate_total_payment(self):
        """Calculate total payment over loan term.
        
        Returns:
            float: Total payment amount
        """
        monthly = self.calculate_monthly_payment()
        return round(monthly * self.months, 2)

    def calculate_overpayment(self):
        """Calculate overpayment amount.
        
        Returns:
            float: Overpayment amount
        """
        total = self.calculate_total_payment()
        return round(total - self.principal, 2)

    def generate_payment_schedule(self):
        """Generate payment schedule.
        
        Returns:
            list: List of payment dictionaries
        """
        schedule = []
        balance = self.principal
        monthly_payment = self.calculate_monthly_payment()
        
        for month in range(1, self.months + 1):
            interest_payment = balance * self.monthly_rate
            principal_payment = monthly_payment - interest_payment
            
            # Корректировка последнего платежа для избежания погрешности
            if month == self.months:
                principal_payment = balance
                monthly_payment = principal_payment + interest_payment
                balance = 0
            else:
                balance -= principal_payment
            
            schedule.append({
                'month': month,
                'payment': round(monthly_payment, 2),
                'principal': round(principal_payment, 2),
                'interest': round(interest_payment, 2),
                'balance': round(max(balance, 0), 2)
            })
        
        return schedule