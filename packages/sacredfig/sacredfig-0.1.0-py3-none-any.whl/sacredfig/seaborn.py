from sacredfig.main import restyle_axis
import seaborn as sns

STRIPPLOT_KWARGS = {'linewidth': 0.1, 'size': 3, 'alpha': 0.2, 'color': 'k',
                     'facecolors': 'none', 'edgecolors': 'r', 'marker': '$\circ$'}

def boxplot(*args, **kwargs):
    if kwargs is None: kwargs = dict()  
    if args is None: args = dict()

    bp = sns.boxplot(*args, **kwargs)

    if 'ax' in kwargs:
        restyle_axis(
            kwargs['ax'],
            artistprops=dict(ec = 'k', fc='w', lw=0.5),
            lineprops=dict(color='k', lw=0.5))

def stripplot(*args, **kwargs):
    if kwargs is None: kwargs = dict()  
    if args is None: args = dict()

    kwargs.update(STRIPPLOT_KWARGS)

    return sns.stripplot(*args, **kwargs)


boxplot.__doc__= sns.boxplot.__doc__
stripplot.__doc__= sns.stripplot.__doc__