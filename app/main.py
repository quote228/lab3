"""Main module for mortgage calculator GUI."""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from calculator import MortgageCalculator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MortgageApp:
    """GUI application for mortgage calculator."""

    def __init__(self, window):
        """Initialize the application.
        
        Args:
            window: Tkinter root window
        """
        self.window = window
        self.window.title("Калькулятор ипотеки")
        self.window.geometry("500x600")
        
        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets."""
        ttk.Label(self.window, text="Сумма кредита:").pack(pady=5)
        self.principal_entry = ttk.Entry(self.window)
        self.principal_entry.pack(pady=5)
        
        ttk.Label(self.window, text="Годовая ставка (%):").pack(pady=5)
        self.rate_entry = ttk.Entry(self.window)
        self.rate_entry.pack(pady=5)
        
        ttk.Label(self.window, text="Срок (лет):").pack(pady=5)
        self.years_entry = ttk.Entry(self.window)
        self.years_entry.pack(pady=5)
        
        ttk.Button(self.window, text="Рассчитать", command=self.calculate).pack(pady=10)
        
        self.result_frame = ttk.LabelFrame(self.window, text="Результаты")
        self.result_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.results_text = tk.Text(self.result_frame, height=15, width=60)
        self.results_text.pack(pady=10, padx=10, fill="both", expand=True)

    def calculate(self):
        """Calculate mortgage and display results."""
        try:
            principal = float(self.principal_entry.get())
            rate = float(self.rate_entry.get())
            years = int(self.years_entry.get())
            
            calculator = MortgageCalculator(principal, rate, years)
            
            monthly = calculator.calculate_monthly_payment()
            total = calculator.calculate_total_payment()
            overpayment = calculator.calculate_overpayment()
            schedule = calculator.generate_payment_schedule()
            
            result = f"Ежемесячный платеж: {monthly:.2f} руб.\n"
            result += f"Общая сумма выплат: {total:.2f} руб.\n"
            result += f"Переплата: {overpayment:.2f} руб.\n\n"
            result += "График платежей (первые 12 месяцев):\n"
            result += "Месяц | Платеж | Основной долг | Проценты | Остаток\n"
            result += "-" * 50 + "\n"
            
            for payment in schedule[:12]:
                result += (f"{payment['month']:5} | {payment['payment']:7.2f} | "
                          f"{payment['principal']:13.2f} | {payment['interest']:8.2f} | "
                          f"{payment['balance']:8.2f}\n")
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, result)
            
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Пожалуйста, проверьте введенные данные:\n{str(e)}")
        except Exception as e:  # pylint: disable=broad-except
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MortgageApp(root)
    root.mainloop()