"""Unit tests for mortgage calculator."""
import unittest
import sys
import os
from app.calculator import MortgageCalculator

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestMortgageCalculator(unittest.TestCase):
    """Test cases for MortgageCalculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calculator = MortgageCalculator(1000000, 7.5, 10)
    
    def test_monthly_payment_normal_case(self):
        """Test monthly payment calculation in normal conditions."""
        monthly = self.calculator.calculate_monthly_payment()
        self.assertAlmostEqual(monthly, 11870.18, places=1)
        self.assertIsInstance(monthly, float)
    
    def test_monthly_payment_zero_interest(self):
        """Test payment calculation with zero interest rate."""
        calculator = MortgageCalculator(120000, 0, 10)
        monthly = calculator.calculate_monthly_payment()
        self.assertEqual(monthly, 1000.0)
    
    def test_monthly_payment_high_interest(self):
        """Test calculation with high interest rate."""
        calculator = MortgageCalculator(500000, 15, 5)
        monthly = calculator.calculate_monthly_payment()
        self.assertGreater(monthly, 11800)
        self.assertLess(monthly, 13000)
    
    def test_total_payment(self):
        """Test total payment calculation."""
        total = self.calculator.calculate_total_payment()
        self.assertAlmostEqual(total, 1424421.6, places=0)
        self.assertGreater(total, 1000000)
    
    def test_overpayment(self):
        """Test overpayment calculation."""
        overpayment = self.calculator.calculate_overpayment()
        self.assertAlmostEqual(overpayment, 424421.6, places=0)
        self.assertGreater(overpayment, 0)
    
    def test_payment_schedule_length(self):
        """Test payment schedule length."""
        schedule = self.calculator.generate_payment_schedule()
        self.assertEqual(len(schedule), 120)
    
    def test_payment_schedule_structure(self):
        """Test payment schedule structure."""
        schedule = self.calculator.generate_payment_schedule()
        first_payment = schedule[0]
        
        self.assertIn('month', first_payment)
        self.assertIn('payment', first_payment)
        self.assertIn('principal', first_payment)
        self.assertIn('interest', first_payment)
        self.assertIn('balance', first_payment)
        
        self.assertIsInstance(first_payment['month'], int)
        self.assertIsInstance(first_payment['payment'], float)
    
    def test_payment_schedule_balance_decrease(self):
        """Test balance decrease in payment schedule."""
        schedule = self.calculator.generate_payment_schedule()
        
        for i in range(1, len(schedule)):
            self.assertLessEqual(schedule[i]['balance'], schedule[i-1]['balance'])
    
    def test_initial_balance_equals_principal(self):
        """Test initial balance after first payment."""
        schedule = self.calculator.generate_payment_schedule()
        first_payment = schedule[0]
        self.assertLess(first_payment['balance'], 1000000)
    
    def test_final_balance_near_zero(self):
        """Test final balance is near zero."""
        schedule = self.calculator.generate_payment_schedule()
        final_balance = schedule[-1]['balance']
        self.assertLessEqual(final_balance, 1.0)
    
    def test_invalid_principal_raises_error(self):
        """Test invalid principal raises error."""
        with self.assertRaises(ValueError):
            MortgageCalculator("invalid", 7.5, 10)
    
    def test_negative_principal_raises_error(self):
        """Test negative principal raises error."""
        with self.assertRaises(ValueError):
            MortgageCalculator(-100000, 7.5, 10)
    
    def test_negative_interest_raises_error(self):
        """Test negative interest rate raises error."""
        with self.assertRaises(ValueError):
            MortgageCalculator(100000, -5, 10)
    
    def test_invalid_years_raises_error(self):
        """Test invalid years raises error."""
        with self.assertRaises(ValueError):
            MortgageCalculator(100000, 7.5, "10")
    
    def test_zero_years_raises_error(self):
        """Test zero years raises error."""
        with self.assertRaises(ValueError):
            MortgageCalculator(100000, 7.5, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)