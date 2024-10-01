# error_analysis.py

import pandas as pd
import numpy as np

# Define lookup tables for resistors, voltages, and currents
resistor_table = pd.DataFrame({
    "Resistance Range": ["0-1", "1.1-10", "10.1-100", "100.1-1000", "1000.1-10000", "10000.1-100000"],
    "Base Multiplier": [0.000085, 0.000085, 0.000085, 0.00075, 0.000075, 0.000075],
    "Constant": [0.000200 * 0.001, 0.000020 * 0.001, 0.000020 * 0.1, 0.000006 * 1, 0.000006 * 10, 0.000010 * 100]
})

voltage_table = pd.DataFrame({
    "Voltage Range": ["0-.1",".1-1", "1.1-10", "10.1-100", "100.1-1000"],
    "Base Multiplier": [0.00003, 0.000025, 0.000025, 0.00004, 0.00004],
    "Constant": [0.00035 * .1, 0.000006 * 1, 0.000005 * 10, 0.000006 * 100, 0.000006 * 1000]
})

current_table = pd.DataFrame({
    "Current Range": ["0-0.00001", "0.000011-0.0001", "0.00011-0.001", "0.0011-0.01", "0.011-0.1", "0.11-1", "1.1-3", "3.1-10"],
    "Base Multiplier": [0.00045, 0.00045, 0.00045, 0.0002, 0.0002, 0.0004, 0.0005, 0.0022],
    "Constant": [0.00005 * 0.00001, 0.00005 * 0.0001, 0.00005 * 0.001, 0.00005 * 0.01, 0.00005 * 0.1, 0.00005 * 1, 0.00004 * 3, 0.00025 * 10]
})

# Helper function to check if a value is within a given range
def in_range(range_str, value):
    lower, upper = map(float, range_str.split('-'))
    return lower <= value <= upper

# Finds the average value
def calculate_average(values):
    return np.mean(values)

# Finds the Standard Deviation
def calculate_standard_deviation(values):
    return np.std(values, ddof=1)

# Calculate random error
def calculate_random_error(standard_deviation, n):
    return standard_deviation / np.sqrt(n)

# Calculate systematic error based on lookup tables for resistor, voltage, and current
def calculate_systematic_error(values, error_type):
    average = calculate_average(values)

    if error_type == 'resistor':
        error_row = resistor_table[resistor_table['Resistance Range'].apply(lambda x: in_range(x, average))]
    elif error_type == 'voltage':
        error_row = voltage_table[voltage_table['Voltage Range'].apply(lambda x: in_range(x, average))]
    elif error_type == 'current':
        error_row = current_table[current_table['Current Range'].apply(lambda x: in_range(x, average))]
    else:
        return 0  # No error if type is unrecognized

    if not error_row.empty:
        base_multiplier = error_row['Base Multiplier'].values[0]
        constant = error_row['Constant'].values[0]
        return (average * base_multiplier) + constant
    return 0

# Calculates total error as the sum of random and systematic errors
def calculate_total_error(random_error, systematic_error):
    return np.sqrt(random_error**2 + systematic_error**2)

# Calculate partial derivative of systematic error with respect to the average value
def calculate_partial_derivative(values, error_type, h=1e-6):
    average = calculate_average(values)
    
    # Perturb the average by a small amount h
    perturbed_values = values.copy()
    perturbed_values.append(average + h)
    
    # Calculate the systematic error for both original and perturbed datasets
    original_error = calculate_systematic_error(values, error_type)
    perturbed_error = calculate_systematic_error(perturbed_values, error_type)
    
    # Use numerical differentiation to approximate the partial derivative
    partial_derivative = (perturbed_error - original_error) / h
    return partial_derivative

# Main function to perform error analysis
def perform_error_analysis(values, error_type):
    avg_value = calculate_average(values)
    std_dev = calculate_standard_deviation(values)
    random_error = calculate_random_error(std_dev, len(values))
    systematic_error = calculate_systematic_error(values, error_type)
    total_error = calculate_total_error(random_error, systematic_error)
    
    # Calculate partial derivative of systematic error with respect to the input type
    partial_derivative = calculate_partial_derivative(values, error_type)

    return {
        'average': avg_value,
        'std_dev': std_dev,
        'random_error': random_error,
        'systematic_error': systematic_error,
        'total_error': total_error,
        'partial_derivative': partial_derivative
    }
