# gui.py

import customtkinter as ctk
from tkinter import messagebox
from Error_analysis import perform_error_analysis  # Import the error analysis functions
import pandas as pd
from sympy import symbols, diff, sympify  # For handling user-defined function input and differentiation

# List to store all the calculated results
results_list = []

# Store the results from error analysis for further use in partial derivative calculation
last_results = {}

# Function to handle the error analysis when a button is pressed
def calculate_error(error_type):
    global last_results
    try:
        # Get the experimental values from the input
        values_input = values_entry.get()
        values = list(map(float, values_input.split(',')))

        # Perform the error analysis using the provided values and error type
        results = perform_error_analysis(values, error_type)

        # Store the results for future reference
        last_results = {'values': values, 'error_type': error_type, 'results': results}

        # Append results to the results_list
        results_list.append({
            'Type': error_type,
            'Average': results['average'],
            'Standard Deviation': results['std_dev'],
            'Random Error': results['random_error'],
            'Systematic Error': results['systematic_error'],
            'Total Error': results['total_error']
        })

        # Display the results in a popup
        messagebox.showinfo("Error Analysis Results", f"Average Value: {results['average']:.4f}\n"
                                                     f"Standard Deviation: {results['std_dev']:.4f}\n"
                                                     f"Random Error: {results['random_error']:.4f}\n"
                                                     f"Systematic Error: {results['systematic_error']:.4f}\n"
                                                     f"Total Error: {results['total_error']:.4f}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

# Function to calculate user-defined function partial derivatives
def calculate_function_partial_derivatives():
    try:
        func_input = function_entry.get()
        variable_input = variable_entry.get()

        # Parse the function into a sympy expression
        func_expr = sympify(func_input)

        # Define the variable symbol for differentiation
        var = symbols(variable_input)

        # Calculate the partial derivative with respect to the variable
        derivative = diff(func_expr, var)

        # Get variable substitutions if provided
        substitution_input = substitution_entry.get().strip()
        if substitution_input:
            substitutions_dict = {}
            for substitution_pair in substitution_input.split(','):
                var_name, var_value = substitution_pair.split('=')
                substitutions_dict[symbols(var_name.strip())] = symbols(var_value.strip())
            derivative = derivative.subs(substitutions_dict)

        # Display the resulting derivative in a popup
        messagebox.showinfo("Partial Derivative Result", f"Partial Derivative: {derivative}")

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input or calculation error: {str(e)}")

# Function to reset the input fields
def reset_calculation():
    values_entry.delete(0, 'end')
    function_entry.delete(0, 'end')
    variable_entry.delete(0, 'end')
    substitution_entry.delete(0, 'end')

# Function to save results to a CSV file
def save_results():
    if results_list:
        df = pd.DataFrame(results_list)
        df.fillna('', inplace=True)  # Fill any missing values with empty strings
        df.to_csv('error_analysis_results.csv', index=False)
        messagebox.showinfo("Saved", "Results have been saved to error_analysis_results.csv")
    else:
        messagebox.showerror("No Data", "No calculations have been performed yet.")

# GUI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize the main window
root = ctk.CTk()
root.geometry("500x800")
root.title("Error Analysis and Partial Derivative Calculator")

# Input for experimental values
values_label = ctk.CTkLabel(root, text="Enter Experimental Values (comma-separated):", font=("Helvetica", 14))
values_label.pack(pady=10)

values_entry = ctk.CTkEntry(root, width=400)
values_entry.pack(pady=10)

# Buttons for selecting calculation type
ctk.CTkLabel(root, text="Select Calculation Type:", font=("Helvetica", 14)).pack(pady=10)

resistor_button = ctk.CTkButton(root, text="Resistors", command=lambda: calculate_error('resistor'), width=200, height=40)
resistor_button.pack(pady=10)

voltage_button = ctk.CTkButton(root, text="Voltages", command=lambda: calculate_error('voltage'), width=200, height=40)
voltage_button.pack(pady=10)

current_button = ctk.CTkButton(root, text="Currents", command=lambda: calculate_error('current'), width=200, height=40)
current_button.pack(pady=10)

# Section for user-defined function partial derivatives
ctk.CTkLabel(root, text="Find Partial Derivatives of a Function:", font=("Helvetica", 14)).pack(pady=20)

function_label = ctk.CTkLabel(root, text="Enter Function (e.g., 'x^2 + y^3'):", font=("Helvetica", 14))
function_label.pack(pady=10)
function_entry = ctk.CTkEntry(root, width=400)
function_entry.pack(pady=10)

variable_label = ctk.CTkLabel(root, text="Differentiate with respect to (e.g., 'x'):", font=("Helvetica", 14))
variable_label.pack(pady=10)
variable_entry = ctk.CTkEntry(root, width=200)
variable_entry.pack(pady=10)

substitution_label = ctk.CTkLabel(root, text="Variable Substitutions (Optional, e.g., 'z=x, w=y'):", font=("Helvetica", 14))
substitution_label.pack(pady=10)
substitution_entry = ctk.CTkEntry(root, width=400)
substitution_entry.pack(pady=10)

function_partial_derivative_button = ctk.CTkButton(root, text="Calculate Function Partial Derivative", command=calculate_function_partial_derivatives, width=200, height=40)
function_partial_derivative_button.pack(pady=10)

# Reset and Done buttons
calculate_again_button = ctk.CTkButton(root, text="Calculate Again", command=reset_calculation, width=200, height=40)
calculate_again_button.pack(pady=10)

done_button = ctk.CTkButton(root, text="Done", command=save_results, width=200, height=40, fg_color="green")
done_button.pack(pady=20)

root.mainloop()
