"""
Author : pciunkiewicz

Visualization code for YouTube video 001

Structured as an interactive Python file,
requires VSCode Python and Jupyter extensions
to run cells (# %%) in interactive mode
"""
# %%
import yaml
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from matplotlib.patches import FancyBboxPatch

sns.set('talk')
sns.set_style('whitegrid')


with open('benchmarks.yml', 'r') as file:
    results = yaml.safe_load(file)


# %%
def plot(df, fname, seconds=True):
    with plt.style.context('fivethirtyeight'):
        fig, ax = plt.subplots(figsize=[10, 3])
        ax = sns.barplot(
            x='value',
            y='variable',
            data=df.melt(),
            ax=ax,
            errwidth=1.5,
            errcolor='0.1',
            capsize=0.2)
        ax.set(xlabel='', ylabel='')
        if seconds:
            ax.set_xticklabels(pd.to_datetime(ax.get_xticks(), unit='s').strftime('%M:%S'), size=12)
        else:
            ax.set_xticklabels(ax.get_xticks().astype(int), size=12)
        ax.set_yticklabels(ax.get_yticklabels(), weight='bold')
        sns.despine(bottom=True)

        for patch in reversed(ax.patches):
            bb = patch.get_bbox()
            scale = ax.get_xlim()[1] / 100
            p_bbox = FancyBboxPatch(
                (bb.xmin, bb.ymin),
                abs(bb.width),
                abs(bb.height),
                boxstyle=f'round,pad=-0.40,rounding_size={scale}',
                ec='none',
                fc=patch.get_facecolor(),
                mutation_aspect=0.2 / scale)

            patch.remove()
            ax.add_patch(p_bbox)

        plt.savefig(f'{fname}.png', dpi=600, bbox_inches='tight')

# plot(pd.DataFrame(results['Simulation-Results']['Single-core']), 'sim-single-core')


# %%
plot(pd.DataFrame(results['Simulation-Results']['Single-core']), 'sim-single-core')
plot(pd.DataFrame(results['Simulation-Results']['Multi-core']), 'sim-multi-core')
plot(pd.DataFrame(results['Simulation-Results']['Animation']), 'sim-animation')

plot(pd.DataFrame(results['Deep-Learning-Results']), 'deep-learning')

plot(pd.DataFrame(results['Geekbench-Results']['Single-core']), 'geek-single-core', seconds=False)
plot(pd.DataFrame(results['Geekbench-Results']['Multi-core']), 'geek-multi-core', seconds=False)


# %%
