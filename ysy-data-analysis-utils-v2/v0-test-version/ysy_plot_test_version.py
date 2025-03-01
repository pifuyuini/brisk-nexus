"""
ysy_plot_utils.py

Copyright (c) 2025 pifuyuini

Author: pifuyuini
Email: <my_email>
Version: 1.1.0
Date: 2025-01-04

Description:
    This module provides a set of utility functions and settings for creating high-quality, customizable plots 
    using Matplotlib. The module includes functions to configure Matplotlib aesthetics, apply predefined color 
    palettes, and generate different types of plots (e.g., curve and scatter). It is designed to streamline the 
    process of creating publication-ready visualizations.

    Key Features:
    - `ysy_settings`: Configures global Matplotlib settings for consistent styling.
    - `science_settings`: Provides compact scientific plot settings optimized for academic publications.
    - `firefly`: Supplies a customizable color palette for visualizations.
    - `plot`: A high-level function for creating plots with customizable styles, labels, and legends.

License:
    This file is licensed under the MIT License. You may use, modify, and distribute it under the terms of the license.
    For more details, see the LICENSE file in the project root.

Usage:
    Example usage of the module:
    >>> from ysy_plot_utils import ysy_settings, plot
    >>> import matplotlib.pyplot as plt

    >>> # Configure Matplotlib with custom settings
    >>> settings = ysy_settings(dpi=150, color=True, marker=True)
    >>> plt.rcParams.update(settings)

    >>> # Generate a sample plot
    >>> x = [0, 1, 2, 3]
    >>> y = [0, 1, 4, 9]
    >>> plot(x, y, legend_name='Sample Data', plot_title='Test Plot', x_label='Time', y_label='Value')
    >>> plt.show()
"""

__version__ = "1.1.0"



# Import necessary package
import matplotlib.pyplot as plt
from cycler import cycler



# Settings


# Personal
def ysy_settings(dpi=300, color=True, font=True, jupyter=False, marker=False):
    '''
    Configures Matplotlib plot settings to ensure consistent and high-quality visualizations.

    This function creates a dictionary of configuration settings for Matplotlib. It allows customization of 
    figure appearance, gridlines, fonts, colors, markers, and other plot elements. You can toggle specific 
    settings based on your requirements, making it ideal for publication-ready plots or tailored visualizations.

    Args:
        dpi (int, optional): Dots per inch (DPI) for figure resolution. Defaults to 300.
        color (bool, optional): Enables a predefined color cycle for plots. Defaults to True.
        font (bool, optional): Configures font family and style. Defaults to True.
        jupyter (bool, optional): Adapts settings for Jupyter Notebook display, with smaller sizes and simpler fonts. Defaults to False.
        marker (bool, optional): Adds a custom marker style cycle to the plots. Defaults to False.

    Returns:
        dict: A dictionary containing Matplotlib configuration settings. This can be directly applied using `matplotlib.rcParams.update()`.

    Configuration Overview:
        - **Figure**: Default figure size and DPI.
        - **Axes**: Title and label font sizes, grid visibility and style.
        - **Ticks**: Major and minor tick sizes and widths, as well as label font sizes.
        - **Grid**: Customizable gridlines, including color, style, and transparency.
        - **Legend**: Frame visibility, shadow, font size, and fancy box styling.
        - **Font**: Default font family and support for mathematical text rendering.
        - **Lines**: Default line width and optional marker styles.

    Examples:
        >>> import matplotlib.pyplot as plt
        >>> from ysy_plot_utils import ysy_settings
        >>> config = ysy_settings(dpi=150, color=True, font=False, marker=True)
        >>> plt.rcParams.update(config)
        >>> plt.plot([0, 1, 2], [0, 1, 4])
        >>> plt.show()

    '''
    # Global
    config = {
        # Default 
        # figure
        'figure.figsize':(12.5, 9), 
        # label
        'axes.labelsize':27,
        'axes.titlesize': 30,
        # x
        'xtick.major.size': 9,
        'xtick.major.width': 1.5,
        'xtick.minor.size': 4.5,
        'xtick.minor.width': 1.5,
        # y
        'ytick.major.size': 9,
        'ytick.major.width': 1.5,
        'ytick.minor.size': 4.5,
        'ytick.minor.width': 1.5,
        # xy label
        'xtick.labelsize': 25,
        'ytick.labelsize': 25,
        # grid
        'axes.grid' : True,
        'axes.axisbelow' : True,
        'grid.linestyle': '--',
        'grid.color': 'k',
        'grid.alpha': 0.5,
        'grid.linewidth': 0.5,
        # legend
        'legend.frameon': True,
        'legend.framealpha': 1.0,
        'legend.fancybox': True,
        'legend.numpoints': 1,
        'legend.shadow': True,
        'legend.fontsize': 25,
        'legend.title_fontsize': 25,
        # font
        'font.family': 'Times New Roman',
        'axes.formatter.use_mathtext': True,
        'mathtext.fontset': 'cm',
        'text.usetex': False,
        # line
        'lines.linewidth': 3.,
        }
    # Additional
    # dpi
    if dpi != None:
        add_dpi = {'figure.dpi': dpi}
        config.update(add_dpi)
    # color
    if color:
        add_color = {'axes.prop_cycle': cycler('color', firefly(requirement='cycle'))}
        config.update(add_color)
    # font
    if font:
        add_font = {
            'font.serif': ['cmr10', 'Computer Modern Serif', 'DejaVu Serif'],
            'font.family': 'serif'
        }
        config.update(add_font)
    # marker
    if marker:
        add_marker = {
            'axes.prop_cycle': (cycler('marker', ['o', 's', '^', 'v', '<', '>', 'd']) + 
                    cycler('color', ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e']) + 
                    cycler('ls', [' ', ' ', ' ', ' ', ' ', ' ', ' '])),
            'lines.markersize': 3,
        }
        config.update(add_marker)
    # Jupyter Notebook
    if jupyter:
        add_jupyter = {
            'figure.figsize': (8, 6),
            'xtick.major.size': 6,
            'xtick.major.width': 1,
            'xtick.minor.size': 3,
            'xtick.minor.width': 1,
            'ytick.major.size': 6,
            'ytick.major.width': 1,
            'ytick.minor.size': 3,
            'ytick.minor.width': 1,
            'xtick.labelsize': 16,
            'ytick.labelsize': 16,
            'legend.fontsize': 16,
            'legend.title_fontsize': 16,
            'axes.titlesize': 16,
            'axes.labelsize': 16,
            'axes.linewidth': 1,
            'grid.linewidth': 1,
            'lines.linewidth': 2.,
            'font.family': 'sans-serif',
            'mathtext.fontset': 'dejavusans',
            'text.usetex': False,
        }
        config.update(add_jupyter)
    return config


# Science
def science_settings(dpi=300, frame_on=False):
    '''
    Configures Matplotlib settings optimized for scientific plots.

    This function provides a set of Matplotlib configuration options tailored for creating high-quality 
    scientific visualizations. It ensures consistent styling with a focus on precision and clarity, suitable 
    for academic publications or professional presentations.

    Args:
        dpi (int, optional): Dots per inch (DPI) for figure resolution. Defaults to 300.
        frame_on (bool, optional): Toggles the display of a legend frame. Defaults to False.

    Returns:
        dict: A dictionary of Matplotlib configuration settings. This can be applied using `matplotlib.rcParams.update()`.

    Configuration Details:
        - **Color Cycle**: A predefined set of colors for plots.
        - **Figure**: Default size optimized for compact scientific plots (3.5 x 2.625 inches).
        - **Ticks**: Major and minor tick sizes, widths, and visibility for both x and y axes.
        - **Axes**: Thin axis lines for a cleaner look.
        - **Gridlines**: Lightweight gridlines with consistent width.
        - **Legend**: Optionally includes a frame with adjustable transparency.
        - **Savefig**: Tight bounding box and minimal padding for saving figures.
        - **Font**: Serif font family and support for mathematical text rendering.

    Examples:
        >>> import matplotlib.pyplot as plt
        >>> from ysy_plot_utils import science_settings
        >>> config = science_settings(dpi=150, frame_on=True)
        >>> plt.rcParams.update(config)
        >>> plt.plot([0, 1, 2], [0, 1, 4], label='Example Line')
        >>> plt.legend()
        >>> plt.savefig('example_plot.png')
        >>> plt.show()

    Notes:
        - This configuration emphasizes compact and precise plots with minimal clutter.
        - The `dpi` parameter allows for high-resolution outputs suitable for publications.
        - The `frame_on` parameter provides flexibility to include or exclude a legend frame.

    '''
    config = {
    'axes.prop_cycle': cycler('color', ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e']),
    'figure.figsize': (3.5, 2.625),
    'xtick.direction': 'in',
    'xtick.major.size': 3,
    'xtick.major.width': 0.5,
    'xtick.minor.size': 1.5,
    'xtick.minor.width': 0.5,
    'xtick.minor.visible': True,
    'xtick.top': True,
    'ytick.direction': 'in',
    'ytick.major.size': 3,
    'ytick.major.width': 0.5,
    'ytick.minor.size': 1.5,
    'ytick.minor.width': 0.5,
    'ytick.minor.visible': True,
    'ytick.right': True,
    'axes.linewidth': 0.5,
    'grid.linewidth': 0.5,
    'lines.linewidth': 1.0,
    'legend.frameon': False,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'font.family': 'serif',
    'mathtext.fontset': 'dejavuserif',
    }
    # Additional
    # dpi
    if dpi != None:
        add_dpi = {'figure.dpi': dpi}
        config.update(add_dpi)
    # legend frame
    if frame_on:
        add_legend_frame = {
            'legend.frameon': True,
            'legend.framealpha': 1.0,
        }
        config.update(add_legend_frame)
    return config


# Color
def firefly(requirement=None):
    '''
    Provides a predefined set of colors inspired by the firefly theme.

    This function returns color codes in hexadecimal format based on the specified `requirement`. It is 
    designed to offer a palette for styling plots and visualizations. The function can return the full 
    color palette, a subset for cycling, or a specific color code.

    Args:
        requirement (str, optional): Specifies the type of color output. Defaults to `None`.
            - `None`: Returns the full list of firefly colors.
            - `'cycle'`: Returns a subset of the palette suitable for color cycling in plots.
            - Specific color name (`'fgrayblue'`, `'fgraygreen'`, `'fred'`, `'fbluegreen'`, `'fblack'`, `'fsilver'`): Returns the corresponding hex color code.

    Returns:
        list or str: 
            - A list of hex color codes if `requirement` is `None` or `'cycle'`.
            - A single hex color code if a specific color name is provided.

    Full Palette (Default):
        1. `#475d7b` (Gray Blue)
        2. `#97c6c0` (Gray Green)
        3. `#e26e1b` (Deep Orange Yellow)
        4. `#4df8e8` (Blue Green)
        5. `#3e324a` (Purple Black)
        6. `#e6e4e0` (Silver White)

    Color Cycle (Subset for `requirement='cycle'`):
        - `#475d7b`, `#97c6c0`, `#e26e1b`, `#4df8e8`

    Color Names (For specific `requirement` values):
        - `'fgrayblue'`: `#475d7b`
        - `'fgraygreen'`: `#97c6c0`
        - `'fred'`: `#e26e1b`
        - `'fbluegreen'`: `#4df8e8`
        - `'fblack'`: `#3e324a`
        - `'fsilver'`: `#e6e4e0`

    Examples:
        >>> firefly()
        ['#475d7b', '#97c6c0', '#e26e1b', '#4df8e8', '#3e324a', '#e6e4e0']

        >>> firefly('cycle')
        ['#475d7b', '#97c6c0', '#e26e1b', '#4df8e8']

        >>> firefly('fred')
        '#e26e1b'

    Notes:
        - The function is flexible and can be used to style Matplotlib plots with custom color palettes.
        - Ensure the `requirement` string matches one of the predefined keys for specific color retrieval.

    '''
    if requirement == None:
        colors = ['#475d7b', '#97c6c0', '#e26e1b', '#4df8e8', '#3e324a', '#e6e4e0']
        return colors
    elif requirement == 'cycle':
        colors = ['#475d7b', '#97c6c0', '#e26e1b', '#4df8e8']
        return colors
    else:
        color_dictionary = {
            'fgrayblue': '#475d7b', 
            'fgraygreen': '#97c6c0', 
            'fred': '#e26e1b', 
            'fbluegreen': '#4df8e8', 
            'fblack': '#3e324a', 
            'fsilver': '#e6e4e0', 
        }
        return color_dictionary[requirement]



# Standardized Plot
def plot(x, y, legend_name, plot_title='', x_label='X', y_label='Y', plot_type='curve', legend_title=''):
    '''
    A utility function to plot data using Matplotlib.

    This function generates a customizable plot (curve or scatter) for single or multiple datasets. 
    It provides options for setting plot titles, axis labels, legend names, and legend titles.

    Args:
        x (list or array-like): The x-axis data.
        y (list, array-like, or tuple of lists/arrays): The y-axis data. If `y` is a tuple, multiple datasets are plotted.
        legend_name (str or list of str): The legend label(s) for the dataset(s). Must match the length of `y` if `y` is a tuple.
        plot_title (str, optional): The title of the plot. Defaults to an empty string.
        x_label (str, optional): The label for the x-axis. Defaults to 'X'.
        y_label (str, optional): The label for the y-axis. Defaults to 'Y'.
        plot_type (str, optional): The type of plot to generate. Options are:
            - `'curve'` (default): Plots lines using `plt.plot`.
            - `'scatter'`: Plots points using `plt.scatter`.
        legend_title (str, optional): The title of the legend box. Defaults to an empty string.

    Returns:
        None: The function does not return a value but displays the generated plot.

    Examples:
        Plotting a single dataset as a curve:
        >>> x = [1, 2, 3, 4]
        >>> y = [10, 20, 30, 40]
        >>> plot(x, y, legend_name='Dataset 1', plot_title='Sample Plot', x_label='Time', y_label='Value')

        Plotting multiple datasets as scatter plots:
        >>> x = [1, 2, 3, 4]
        >>> y = ([10, 20, 30, 40], [15, 25, 35, 45])
        >>> legend_names = ['Dataset 1', 'Dataset 2']
        >>> plot(x, y, legend_name=legend_names, plot_type='scatter', legend_title='Groups')

    Notes:
        - The function automatically handles multiple datasets if `y` is a tuple.
        - Ensure that the length of `legend_name` matches the number of datasets in `y` when `y` is a tuple.
        - The plot is immediately displayed using `plt.show()`.

    '''
    plt.figure()
    if isinstance(y, tuple):
        for i in range(len(y)):
            if plot_type == 'curve':
                plt.plot(x, y[i], label=legend_name[i])
            if plot_type == 'scatter':
                plt.scatter(x, y[i], label=legend_name[i])
    else:
        if plot_type == 'curve':
            plt.plot(x, y, label=legend_name)
        if plot_type == 'scatter':
            plt.scatter(x, y, label=legend_name)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(plot_title)
    plt.legend(title=legend_title)
    plt.show()
    return None
