# DEXPLORIZE DATA EXPLORATION PYTHON LIBRARY

Dexplorize is a Python library tailored to simplify and enhance the journey of data analysis tasks. Whether you're diving into datasets, conducting statistical analyses, or visualizing data, dexplorize (Data Exploration) equips you with a comprehensive toolkit to expedite the process and extract valuable insights efficiently.

# FEATURES

UNIVARIATE ANALYSIS
- Entropy Based Binning
- Equal Width Based Binning
- Equal Frequency Based Binning
- Binary Encoding
- Imputation Values

BIVARIATE ANALYSIS
1. [NUMERICAL AND NUMERICAL]
- Scatter Plot
- Linear Correlation

2. [CATEGORICAL AND CATEGORICAL]
- Combination Chart
- Stacked Column Chart

3. [CATEGORICAL AND NUMERICAL]
- Line Chart w/ Error Bars


# NEW FEATURES
- Pie Chart (Univariate Categorical)
- Statistical Measure (Univariate Numerical)
- Histogram (Univariate Numerical)

# FIXED FEATURES
- Target Encoding (concatenated dataframe)
- Line Chart (undefined variable)
- Linear Correlation (unfefinef axis)
- Stacked Column (undefined axis)

# INSTALLATION
You can install DataExploration with pip and required libraries.

::
    
    pip install dexplorize
    pip install matplotlib
    pip install numpy
    pip install pandas
    ...

# USAGE
Univariate Function (Data Preprocessing and Visualization)
- entropy_based(data, target, bins)
- equal_width(data, bins)
- ewidth_bin(data, bins)
- ewidth_plot(data)
- equal_freq(data, bins)
- efreq_bin(data, bins)
- efreq_plot(data)
- binary_encoding(data, values)
- target_encoding(data, values)
- impute_values(data)
- pie_chart(data)
- stat_measure(data)
- hist_bar(data, bins)

Bivariate Function (Data Visualization)
- scatter_plot(data, attr1, attr2)
- linear_corr(data, attr1, attr2)
- stacked_column(data, val1, val2)
- line_chart(data, attr1, attr2)

# IMPORT LIBRARY
::
    
    from DataExploration.univariate import *
    from DataExploration.bivariate import *
    
    from DataExploration import univariate
    from DataExploration import bivariate
    ...

# INFORMATION
Data Exploration is about describing the data by means of statistical and visualization techniques. We explore data in order to bring important aspects of that data into focus for further analysis.