# sacredfig

SacredFig is a Python library that provides opinionated styles for scientific figures in matplotlib.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install SacredFig.

```bash
pip install sacredfig
```

## Usage

```python
import matplotlib.pyplot as plt

import seaborn as sns
sns.reset_orig()
iris = sns.load_dataset("iris")

import sacredfig
from sacredfig import cm2in

plt.style.use(sacredfig.style)

fig, ax = plt.subplots(figsize=(6 * cm2in, 6 * cm2in), dpi=150)
ax.grid(False, which='major', axis='x')

ax.boxplot([iris.sepal_length.values, iris.sepal_width.values],
           labels=['Sepal length', 'Sepal width'])

ax.set_box_aspect(1)
ax.set(xlabel="Attribute", ylabel="Empirical distribution", ylim=(0, 10));
```