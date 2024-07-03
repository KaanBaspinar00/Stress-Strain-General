# Stress-Strain-General

# 1st Stage 
## (Noise Reduction - Smoothing - Maxima & Minima Detection)

1. Imports and Dependencies

* Pandas: For data manipulation and reading CSV files.

* SciPy: find_peaks for identifying peaks, savgol_filter for smoothing the signal, and fft/ifft for Fourier Transform and Inverse Fourier Transform respectively.

* NumPy: For numerical operations like creating linear fits.

* Plotly: For interactive plotting.

**Begin your Colab notebook by ensuring all dependencies are installed:**

```
!pip install pandas scipy numpy plotly
```

2. Data Loading
* Reading the CSV file: Ensure the delimiter and encoding are correctly specified to match the data file structure. Handling non-standard encodings like 'latin1' and delimiters like ';' is crucial for correctly parsing the data.
3. Data Preprocessing
* Comma to Dot Conversion: Replace commas with dots in numeric columns to handle European decimal formats. Convert these strings to floats for subsequent numerical operations.
* Baseline Adjustment: Subtract the first value of the force_N column from itself to set a baseline, adjusting the force data to start from zero.
4. FFT for Noise Reduction
* FFT Application: Convert the time-domain force data into the frequency domain to identify and filter out high-frequency noise.
* Thresholding: Frequencies beyond a certain threshold (20 Hz in your case) are set to zero to disregard high-frequency components.
* Inverse FFT: Convert the data back to the time domain after filtering.
5. Data Smoothing
* Savitzky-Golay Filter: Apply this filter to smooth the signal. Parameters such as window_length and polyorder affect the smoothness and fidelity of the smoothing: 
* **window_length should be an odd number** defining the size of the window used.
* polyorder defines the polynomial's order used to fit the samples. Higher orders can fit wider varieties of curves but can lead to overfitting.
6. Peak and Trough Detection
* find_peaks: This function is used twice, once to find peaks and once with inverted data to find troughs. The prominence parameter helps in defining the minimal vertical distance between a peak and its neighboring lower points.
7. Linear Fit Calculation
* Polyfit and Poly1d: Calculate the linear fit using two points: the origin and the first significant peak or trough. This part of the script generates a simple linear model (y = mx + c) for the initial part of the data.
8. Plotting with Plotly
* Interactive Visualization: Use Plotly to create interactive plots that can be zoomed, panned, and hovered to display values. This helps in detailed inspection of the smoothed data, peaks, and troughs.
* Annotations and Layout: Customize the plot with annotations for peaks and troughs and adjust the layout to ensure all information is visible without clutter.
9. Error Handling
Try-Except Block: Ensures that the script can continue processing other files even if one file causes an error. The error message is printed to help in debugging.



# 2nd Stage

## (Shifting - Linear Fit)

### Added Identification of Main Trough and Main Peak:
* Main Trough Identification: After detecting all troughs, this part of the code identifies the 'main trough' which is significantly separated from the next one by more than 0.17 mm in extension. If no trough meets this condition, it defaults to the last trough in the list.
* Main Peak Identification: Following the identification of the main trough, the code looks for the nearest peak that occurs after this trough. This is considered the 'main peak'. The logic ensures that the peak must occur after the trough in the dataset.
### Calculating Linear Fit Between Main Trough and Main Peak:
* Data Range Selection: Selects the segment of data between the main trough and main peak to perform a linear regression. This helps to analyze this specific section of the force-extension curve.
* np.polyfit and np.poly1d: These functions calculate and create the linear model. The x-values (extensions) and y-values (forces) between the main trough and main peak are used here. The linear model helps in understanding the behavior of the material between these two points.
### Data Shifting:
* Calculating Offsets: Offsets for both the extension and force are calculated using the values at the main trough. These offsets are used to shift the curve so that the main trough aligns at the origin (0,0) in the plot.
* Shifted Data Creation: Applies the calculated offsets to all points in the dataset. This transformation helps in isolating and examining the behavior of the data around the main trough and peak without the influence of absolute values.
### Plotting Enhancements:
* Plotting Shifted Data: In addition to plotting the original data, shifted data is also plotted for comparison. This helps in visualizing how the data transformation (shifting) affects the analysis.
* Markers for Peaks and Troughs in Shifted Data: Adds markers to the shifted data points that are peaks and troughs. Using different symbols ('cross') for these points in the shifted plot differentiates them visually from the original data points.
* Linear Fit Line in Shifted Data: A dashed green line is added to represent the linear fit between the main trough and main peak in the shifted plot. This line helps visualize the linear relationship in the selected data range.
* Slope Annotation: Displays the slope of the linear fit directly on the plot. This annotation provides immediate insight into the rate of change between force and extension, which is crucial for material property analysis.
### Error Handling and Feedback:
* Conditional Messaging: Additional print statements provide feedback about the absence of a main peak or trough, which is helpful for debugging and understanding the dataset's characteristics.



# 3rd Stage:

### Calculation of the Area Under the Curve
The script calculates the area under the curve between the main trough and main peak using the trapezoidal rule. This is achieved with the trapz function from scipy.integrate. This area represents physical quantities such as work done or energy in various applications, making it a significant analytical measurement.



```
area = trapz(shifted_force[main_trough:main_peak+1], shifted_extension[main_trough:main_peak+1])
```

* shifted_force and shifted_extension: These arrays are derived from the force and extension data, shifted so that the analysis starts from the main trough.
* trapz function: Integrates using the trapezoidal rule, which effectively sums up trapezoidal areas under the curve.

### Visualization Enhancements

Adding the Area Plot
A plot fill is added to visually represent the area under the curve between the main trough and main peak. This is not only helpful for visual assessment but also emphasizes the specific section under analysis.



```
area_trace = go.Scatter(
    x=shifted_extension[main_trough:main_peak+1],
    y=shifted_force[main_trough:main_peak+1],
    fill='tozeroy',
    name='Area Under Curve',
    mode='lines',
    line=dict(color='rgba(0, 100, 80, 0.2)'),
)
fig.add_trace(area_trace)
```

* fill='tozeroy': Indicates that the area under the curve should be filled, connecting the line graph to the zero line on the y-axis.
* Color and Transparency: The fill uses a semi-transparent green color, allowing underlying gridlines or other plot elements to be visible through the fill, ensuring clarity and readability of the plot.



