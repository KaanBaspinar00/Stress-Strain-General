import os
import seaborn as sns
import matplotlib.pyplot as plt
# Specify the directory where you want to save the PNG files


# List all files in the current directory
# Write directory of csv files.

files = os.listdir("C:/Users/baspi/OneDrive/Masaüstü/29062024 (1)/29062024/DATA99")

# Filter for CSV files (find csv files and append them in a list called csv_files)
csv_files = [file for file in files if file.endswith('.csv')]
import pandas as pd
from scipy.signal import find_peaks, savgol_filter
import numpy as np

from scipy.fftpack import fft, ifft
import plotly.graph_objects as go

# Load the file
#file_ = csv_files[11]
for file_ in csv_files:
    try:
        full_path = os.path.join(r"C:/Users/baspi/OneDrive/Masaüstü/29062024 (1)/29062024/DATA99", file_)
        file_ = "C:/Users/baspi/OneDrive/Masaüstü/29062024 (1)/29062024/DATA99/" + file_
        # Read the data
        data = pd.read_csv(file_, encoding='latin1', delimiter=';', skiprows=1)
        data = data.iloc[:, :3]

        # Rename columns
        data.columns = ['time_sec', 'extension_mm', 'force_N']

        # Convert commas to dots and convert to float
        data['time_sec'] = data['time_sec'].str.replace(',', '.').astype(float)
        data['extension_mm'] = data['extension_mm'].str.replace(',', '.').astype(float)
        data['force_N'] = data['force_N'].str.replace(',', '.').astype(float)
        data['force_N'] = data['force_N'] - data['force_N'][0]

        # Apply FFT and Inverse FFT for Noise Reduction
        fft_signal = fft(data['force_N'].values)
        frequencies = np.fft.fftfreq(len(data['time_sec'].values),
                                     data['time_sec'].values[1] - data['time_sec'].values[0])

        # Filter out high frequency noise
        threshold = 20
        fft_signal[np.abs(frequencies) > threshold] = 0
        filtered_signal = ifft(fft_signal)

        # Smoothing the force data using a Savitzky-Golay filter
        force_smooth = savgol_filter(np.real(filtered_signal), window_length=31, polyorder=7)

        # Find peaks (local maxima) and troughs (local minima)
        peaks, _ = find_peaks(force_smooth, height=0, prominence=0.7)
        troughs, _ = find_peaks(-force_smooth, height=-250, prominence=0.7)

        # Filter troughs where the extension is greater than 1 mm
        troughs = troughs[data['extension_mm'].iloc[troughs] <= 1]
        peaks = peaks[data['extension_mm'].iloc[peaks] <= 1]

        # Determine the first significant point
        if peaks.size and troughs.size:
            first_significant_point = min(peaks[0], troughs[0])
        elif peaks.size:
            first_significant_point = peaks[0]
        elif troughs.size:
            first_significant_point = troughs[0]
        else:
            first_significant_point = 0  # fallback in case no peaks or troughs are identified

        x_values = [0, data['extension_mm'].iloc[first_significant_point]]
        y_values = [0, force_smooth[first_significant_point]]

        # Linear fit
        fit_coefficients = np.polyfit(x_values, y_values, 1)
        fit_line = np.poly1d(fit_coefficients)

        # Plotting using Plotly
        fig = go.Figure()

        # Main data trace
        fig.add_trace(go.Scatter(
            x=data['extension_mm'],
            y=force_smooth,
            mode='lines',
            name='Smoothed Data',
            line=dict(color='orange')
        ))

        # Adding markers for the peaks and troughs
        fig.add_trace(go.Scatter(
            x=data['extension_mm'].iloc[peaks],
            y=force_smooth[peaks],
            mode='markers',
            name='Local Maxima',
            marker=dict(color='red', size=8)
        ))

        fig.add_trace(go.Scatter(
            x=data['extension_mm'].iloc[troughs],
            y=force_smooth[troughs],
            mode='markers',
            name='Local Minima',
            marker=dict(color='blue', size=8)
        ))

        # Annotations listed on the side - create secondary axis to show these as a static text box
        annotations_text = "Annotations:<br>"
        for t, x, y in zip(data['time_sec'].iloc[peaks], data['extension_mm'].iloc[peaks], force_smooth[peaks]):
            annotations_text += f'Peak at {x:.2f} mm, {y:.2f} N ({t:.1f} s)<br>'
        for t, x, y in zip(data['time_sec'].iloc[troughs], data['extension_mm'].iloc[troughs], force_smooth[troughs]):
            annotations_text += f'Trough at {x:.2f} mm, {y:.2f} N ({t:.1f} s)<br>'

        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='text',
            text=[annotations_text],
            textposition="top right"
        ))

        # Customize layout based on file name condition
        yaxis_range = [0, 500] if "FCSC" in file_ else [0, 500]
        xaxis_range = [0, 2.2] if "FCSC" in file_ else [0, 2.2]
        # Adjust layout to make space for annotations on the side
        fig.update_layout(
            title='Signal Processing: Noise Reduction, Smoothing, and Peak/Trough Identification',
            xaxis_title='Extension (mm)',
            yaxis_title='Force (N)',
            showlegend=False,
            xaxis=dict(range=xaxis_range),
            yaxis=dict(range=yaxis_range),
            # template='plotly_white',
            # xaxis=dict(domain=[0, 0.85]),  # Adjust domain to make space for annotations
            annotations=[dict(
                xref="paper", yref="paper",
                x=0.75, y=0.5, align="left",
                text=annotations_text,
                showarrow=False,
                xanchor="left",
                bordercolor="black",
                borderwidth=1
            )],
            template='plotly_white'
        )

        # Show plot
        #fig.show()

        # Plotting using Seaborn and Matplotlib
        # Plotting the main data
        # Create a figure and axis with the correct size
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot using Seaborn on the correct axis
        sns.lineplot(x=data['extension_mm'], y=force_smooth, ax=ax, label='Smoothed Data', color='orange')

        # Adding markers for the peaks and troughs
        ax.scatter(data['extension_mm'].iloc[peaks], force_smooth[peaks], color='red', label='Local Maxima', s=50)
        ax.scatter(data['extension_mm'].iloc[troughs], force_smooth[troughs], color='blue', label='Local Minima', s=50)

        ax.set_title(f"{file_.replace('.csv', '').split('/')[-1]}")
        ax.set_xlabel('Extension (mm)')
        ax.set_ylabel('Force (N)')
        ax.set_xlim([0, 2.2])
        ax.set_ylim([0, 500])

        # Generate annotation text
        annotation_text = "Annotations:\n"
        for idx in peaks:
            annotation_text += f"Peak at {data['extension_mm'].iloc[idx]:.2f} mm, {force_smooth[idx]:.2f} N ({data['time_sec'].iloc[idx]:.1f} s)\n"
        for idx in troughs:
            annotation_text += f"Trough at {data['extension_mm'].iloc[idx]:.2f} mm, {force_smooth[idx]:.2f} N ({data['time_sec'].iloc[idx]:.1f} s)\n"

        # Placing text box inside the plot
        ax.text(1.5, 300, annotation_text, fontsize=8, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='wheat', edgecolor='black'))

        # Adjust plot layout to make space for the table
        #plt.subplots_adjust(right = 0.4)  # May need to adjust depending on the table size

        ax.legend()
        ax.grid(True)

        #plt.show()
        # Save the plot to a file
        save_directory = f"C:/Users/baspi/OneDrive/Masaüstü/Plots/{file_.replace('.csv', '.png').split('/')[-1]}"
        plt.savefig(save_directory)
        print(f"Plot saved to {save_directory}")
        plt.close()

    except Exception as e:
        print(f"An error occurred: {e}")
