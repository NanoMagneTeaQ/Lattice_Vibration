import matplotlib.pyplot as plt
import numpy as np
import numpy.polynomial.polynomial as poly

def plot_acoustic_optical():
    # Given data
    f = np.array([2.251, 7.576, 12.64, 17.08, 21.24, 36.03, 39.78, 44.28])  # Frequency (kHz)
    p = np.array([90.4, 270.5, 450.3, 630.8, 810.9, 991.2, 1171.4, 1353.2])  # Phase (degree)
    
    # Swap x and y for plotting
    p_acoustic, f_acoustic = p[:5], f[:5]
    p_optical, f_optical = p[5:], f[5:]
    
    # Fit 3rd-degree polynomial trend lines
    coeffs_acoustic = poly.Polynomial.fit(p_acoustic, f_acoustic, 3)
    coeffs_optical = poly.Polynomial.fit(p_optical, f_optical, 2)
    
    # Compute fitted values
    f_acoustic_fit = coeffs_acoustic(p_acoustic)
    f_optical_fit = coeffs_optical(p_optical)
    
    # Compute errors (discrepancy from trend line)
    yerr_acoustic = np.abs(f_acoustic - f_acoustic_fit)
    yerr_optical = np.abs(f_optical - f_optical_fit)
    
    # Find band gap
    band_gap = f_optical[0] - f_acoustic[-1]
    
    # Plot the data
    plt.figure(figsize=(8, 6))
    plt.errorbar(p_acoustic, f_acoustic, yerr=yerr_acoustic, fmt='bo', capsize=5, label='Acoustic Band')
    plt.errorbar(p_optical, f_optical, yerr=yerr_optical, fmt='r*', markersize = 14, capsize=5, label='Optical Band')
    
    # Plot trend lines
    p_range_acoustic = np.linspace(min(p_acoustic), max(p_acoustic), 100)
    p_range_optical = np.linspace(min(p_optical), max(p_optical), 100)
    plt.plot(p_range_acoustic, coeffs_acoustic(p_range_acoustic), 'b-', label='Acoustic Trend')
    plt.plot(p_range_optical, coeffs_optical(p_range_optical), 'r--', label='Optical Trend')
    
    # Add vertical lines for band gap
    plt.axhline(f_acoustic[-1], color='blue', linestyle='-.', label=f'Max Acoustic = {max(f_acoustic)}kHz')
    plt.axhline(f_optical[0], color='red', linestyle='-.', label=f'Min Optical = {min(f_optical)}kHz')
    plt.text((p_acoustic[-1] + p_optical[0]) / 2, np.mean(f), f'Band Gap: {band_gap:.2f} kHz',
             verticalalignment='bottom', horizontalalignment='center', fontsize=14, color='purple')
    
    # Labels and legend
    plt.xlabel('Phase (degree)')
    plt.ylabel('Frequency (kHz)')
    plt.title('Lattice Vibration: Acoustic and Optical Bands')

    plt.xlim(None,1650)
    plt.ylim(None,55)
    plt.legend()
    plt.grid()

    # plt.savefig(f"<File Path>", bbox_inches='tight', pad_inches=0.1)  # This will save the image in the current working directory
    # plt.close()
    plt.show()


plot_acoustic_optical()
