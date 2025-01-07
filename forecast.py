import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to run the forecast
def run_forecast():
    initial_investment = float(initial_investment_entry.get())
    colocation_expense = float(colocation_expense_entry.get())
    marketing_expense = float(marketing_expense_entry.get())
    months = int(months_entry.get())
    price_per_gb = float(price_per_gb_entry.get())
    avg_gb_per_user = float(avg_gb_per_user_entry.get())
    initial_users = int(initial_users_entry.get())
    initial_companies = int(initial_companies_entry.get())
    min_employees_per_company = int(min_employees_entry.get())
    max_employees_per_company = int(max_employees_entry.get())
    acquisition_rate = float(acquisition_rate_entry.get())
    mean_company_size = float(mean_company_size_entry.get())
    cost_per_gb = float(cost_per_gb_entry.get())
    initial_storage = float(initial_storage_entry.get())

    expenses = {
        "colocation": colocation_expense,
        "marketing": marketing_expense
    }

    company_growth = [initial_companies]
    user_growth = [initial_users]

    for month in range(1, months):
        new_companies = company_growth[-1] * acquisition_rate * np.exp(-company_growth[-1] / 10)
        company_growth.append(company_growth[-1] + new_companies)
        
        weights = np.exp(-np.arange(min_employees_per_company, max_employees_per_company + 1) / mean_company_size)
        new_users = new_companies * np.random.choice(np.arange(min_employees_per_company, max_employees_per_company + 1), p=weights/weights.sum())
        user_growth.append(user_growth[-1] + new_users)

    monthly_storage_usage = [users * avg_gb_per_user for users in user_growth]
    monthly_revenue = [usage * price_per_gb for usage in monthly_storage_usage]

    total_monthly_expense = sum(expenses.values())
    one_time_extra_usage_cost = 0
    extra_usage_applied = False
    for usage in monthly_storage_usage:
        if usage > initial_storage and not extra_usage_applied:
            extra_usage = usage - initial_storage
            one_time_extra_usage_cost += extra_usage * cost_per_gb
            extra_usage_applied = True

    monthly_net_profit = [revenue - total_monthly_expense for revenue in monthly_revenue]
    cumulative_profit = np.cumsum(monthly_net_profit) - initial_investment
    cumulative_profit = [profit - one_time_extra_usage_cost if i == 0 else profit for i, profit in enumerate(cumulative_profit)]

    total_net_profit = cumulative_profit[-1]
    ROI = (total_net_profit / initial_investment) * 100

    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, "\nCompany and User Growth Metrics:\n")
    for month, (companies, users) in enumerate(zip(company_growth, user_growth)):
        results_text.insert(tk.END, f"Month {month + 1}: {companies:.0f} companies, {users:.0f} users\n")
    results_text.insert(tk.END, "-----------------------------------\n")
    results_text.insert(tk.END, f"Price per GB: ${price_per_gb:.2f}\n")
    results_text.insert(tk.END, f"Average GB per user: {avg_gb_per_user} GB\n")
    results_text.insert(tk.END, f"Total Net Profit after {months} months: ${total_net_profit:.2f}\n")
    results_text.insert(tk.END, f"ROI after {months} months: {ROI:.2f}%\n")

    break_even_month = next((i for i, profit in enumerate(cumulative_profit) if profit >= 0), None)
    if break_even_month is not None:
        results_text.insert(tk.END, f"Break-even at month {break_even_month + 1}: {company_growth[break_even_month]:.0f} companies, {user_growth[break_even_month]:.0f} users\n")
    else:
        results_text.insert(tk.END, "No break-even point within the given timeframe.\n")

    results_text.see(tk.END)  # Auto scroll to the bottom

    # Clear the previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Create the plot
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(range(1, months + 1), cumulative_profit, label="Cumulative Profit")
    ax.plot(range(1, months + 1), user_growth, label="Number of Users", linestyle="--")
    ax.plot(range(1, months + 1), company_growth, label="Number of Companies", linestyle=":")
    ax.plot(range(1, months + 1), monthly_storage_usage, label="Total GB Usage", linestyle="-.")
    ax.axhline(0, color='red', linestyle='--', label="Break-even")
    ax.set_title("Cumulative Profit, User Growth, Company Growth, and Total GB Usage Over Time")
    ax.set_xlabel("Months")
    ax.set_ylabel("Cumulative Profit (USD) / Users / Companies / GB")
    ax.legend()
    ax.grid()

    # Display the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create the main window
root = tk.Tk()
root.title("Forecast Application")

# Configure grid weights for responsiveness
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=3)
root.grid_rowconfigure(15, weight=1)

# Create and place the input fields with default values
ttk.Label(root, text="Initial Investment:").grid(row=0, column=0, sticky="ew")
initial_investment_entry = ttk.Entry(root)
initial_investment_entry.insert(0, "2770")
initial_investment_entry.grid(row=0, column=1, sticky="ew")

ttk.Label(root, text="Colocation Expense:").grid(row=1, column=0, sticky="ew")
colocation_expense_entry = ttk.Entry(root)
colocation_expense_entry.insert(0, "100")
colocation_expense_entry.grid(row=1, column=1, sticky="ew")

ttk.Label(root, text="Marketing Expense:").grid(row=2, column=0, sticky="ew")
marketing_expense_entry = ttk.Entry(root)
marketing_expense_entry.insert(0, "50")
marketing_expense_entry.grid(row=2, column=1, sticky="ew")

ttk.Label(root, text="Months:").grid(row=3, column=0, sticky="ew")
months_entry = ttk.Entry(root)
months_entry.insert(0, "36")
months_entry.grid(row=3, column=1, sticky="ew")

ttk.Label(root, text="Price per GB:").grid(row=4, column=0, sticky="ew")
price_per_gb_entry = ttk.Entry(root)
price_per_gb_entry.insert(0, "0.12")
price_per_gb_entry.grid(row=4, column=1, sticky="ew")

ttk.Label(root, text="Average GB per User:").grid(row=5, column=0, sticky="ew")
avg_gb_per_user_entry = ttk.Entry(root)
avg_gb_per_user_entry.insert(0, "5")
avg_gb_per_user_entry.grid(row=5, column=1, sticky="ew")

ttk.Label(root, text="Initial Users:").grid(row=6, column=0, sticky="ew")
initial_users_entry = ttk.Entry(root)
initial_users_entry.insert(0, "0")
initial_users_entry.grid(row=6, column=1, sticky="ew")

ttk.Label(root, text="Initial Companies:").grid(row=7, column=0, sticky="ew")
initial_companies_entry = ttk.Entry(root)
initial_companies_entry.insert(0, "1")
initial_companies_entry.grid(row=7, column=1, sticky="ew")

ttk.Label(root, text="Min Employees per Company:").grid(row=8, column=0, sticky="ew")
min_employees_entry = ttk.Entry(root)
min_employees_entry.insert(0, "5")
min_employees_entry.grid(row=8, column=1, sticky="ew")

ttk.Label(root, text="Max Employees per Company:").grid(row=9, column=0, sticky="ew")
max_employees_entry = ttk.Entry(root)
max_employees_entry.insert(0, "200")
max_employees_entry.grid(row=9, column=1, sticky="ew")

ttk.Label(root, text="Mean Company Size:").grid(row=10, column=0, sticky="ew")
mean_company_size_entry = ttk.Entry(root)
mean_company_size_entry.insert(0, "25")
mean_company_size_entry.grid(row=10, column=1, sticky="ew")

ttk.Label(root, text="Acquisition Rate:").grid(row=11, column=0, sticky="ew")
acquisition_rate_entry = ttk.Entry(root)
acquisition_rate_entry.insert(0, "0.6")
acquisition_rate_entry.grid(row=11, column=1, sticky="ew")

ttk.Label(root, text="Initial Storage (GB):").grid(row=12, column=0, sticky="ew")
initial_storage_entry = ttk.Entry(root)
initial_storage_entry.insert(0, "8000")
initial_storage_entry.grid(row=12, column=1, sticky="ew")

ttk.Label(root, text="Cost per GB extra:").grid(row=13, column=0, sticky="ew")
cost_per_gb_entry = ttk.Entry(root)
cost_per_gb_entry.insert(0, "0.08")
cost_per_gb_entry.grid(row=13, column=1, sticky="ew")

# Create and place the run button
run_button = ttk.Button(root, text="Run Forecast", command=run_forecast)
run_button.grid(row=14, column=0, columnspan=2, sticky="ew")

# Create and place the results text box
results_text = tk.Text(root, height=15, width=50)
results_text.grid(row=15, column=0, columnspan=2, sticky="nsew")

# Create and place the plot frame
plot_frame = ttk.Frame(root)
plot_frame.grid(row=0, column=2, rowspan=16, sticky="nsew")

# Run the main loop
root.mainloop()
