import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys

def general_func(x, *params):
    return sum(p * x**i for i, p in enumerate(params))

def estimate_errors(y, trend_y):
    return np.abs(y - trend_y)  # Error based on deviation from trendline

def plot_data_with_errors(file_path, degree=2):
    # Load data from the file
    file_extension = file_path.split('.')[-1]
    
    if file_extension == 'csv':
        df = pd.read_csv(file_path)
    elif file_extension in ['xls', 'xlsx']:  # Excel files
        df = pd.read_excel(file_path)
    elif file_extension == 'ods':  # ODS files
        df = pd.read_excel(file_path, engine='odf')
    else:
        print("Unsupported file format.")
        sys.exit(1)
    
    # Ensure required columns exist
    required_columns = ['f', 'ppc']
    if not all(col in df.columns for col in required_columns):
        print(f"The file must contain columns: {required_columns}")
        sys.exit(1)
    
    x = df['ppc'].values
    y = df['f'].values
    
    # Fit a general function
    popt, _ = curve_fit(lambda x, *p: general_func(x, *p), x, y, p0=[1] * (degree + 1))
    trend_y = general_func(x, *popt)
    
    # Estimate errors based on deviation from the trendline
    error = estimate_errors(y, trend_y)
    
    # Plot data with error bars
    plt.figure(figsize=(8, 6))
    plt.errorbar(x, y,xerr = 0.01, yerr=error, fmt='o', label='Data with Errors', capsize=5, elinewidth=1, markeredgewidth=1)
    plt.plot(x, trend_y, '--r', label=f'Trend Line (Polynomial Degree {degree})')
    plt.plot(x, y, '-b', alpha=0.5, label='Joining Line')
    
    # Modify legend to include error range
    legend_labels = [f'Data with Errors (±{np.mean(error):.2f})', f'Trend Line (Polynomial Degree {degree})', 'Joining Line']
    plt.legend(legend_labels, loc= "upper left")
    
    plt.ylabel('frequency(kHz)')
    plt.xlabel('Phase per unit cell(degree)')
    plt.title('Data Plot with Trend Line and Error Bars')
    plt.grid(True)
    
    plt.ylim(0, 70)
    plt.xlim(0, 210)

    # plt.savefig(f"<File Path>", bbox_inches='tight', pad_inches=0.1)  # This will save the image in the current working directory
    # plt.close()
    plt.show()


plot_data_with_errors("<File Path>", degree=3)
