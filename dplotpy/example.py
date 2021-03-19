import dplotpy as dp
import numpy as np

# Generate some data
x = np.linspace(0, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)
y_sin2 = np.sin(x+np.pi)

# Put the data into curves
sin_curve = dp.curve(x, y_sin, title='Sine Wave')
cos_curve = dp.curve(x, y_cos, title='Cosine Wave')
sin2_curve = dp.curve(x, y_sin2, title='Sine Wave 2')
sin2_curve.label = 'Sine Wave 2'

# Example 1
sin_plot = dp.plot(sin_curve, title='Example 1', subtitle='Sine Wave', xlabel='Degrees [rad]', ylabel='Amplitude [units]')
sin_plot.save('Example1')
sin_plot.show()

# Example 2
cos_plot = dp.plot()
cos_plot.add_curve(cos_curve)
cos_plot.title = 'Example 2'
cos_plot.subtitle = 'Example Subtitle'
cos_plot.xlabel = 'Degrees [rad]'
cos_plot.ylabel = 'Amplitude [units]'
cos_plot.legend = False
cos_plot.save('Example2')
cos_plot.show()

# Example 3
all_plot = dp.plot(sin_curve)
all_plot.add_curve(cos_curve)
all_plot.add_curve(sin2_curve)
all_plot.title = 'Example 3'
all_plot.subtitle = 'Example Subtitle'
all_plot.xlabel = 'Degrees [rad]'
all_plot.ylabel = 'Amplitude [units]'
all_plot.save('Example3')
all_plot.show()