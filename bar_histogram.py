import numpy as np

def plot_numbers(ax, loss, language, color):
    ax.bar(np.arange(len(loss)), loss, edgecolor='black', alpha=1, color=color, linewidth=0, width=0.25)

    ax.tick_params(axis='x', which='major', direction='out', length=6, width=2,colors='k')
    ax.tick_params(axis='y', which='major', direction='out', length=6, width=2,colors='k')

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    
    ax.set_ylim(0, max(loss)*0.9)
    ax.set_xlim(0)

    ax.set_xlabel('epoch')
    ax.set_ylabel(r'$\Delta Loss$')
    language = language.replace('_', '-').upper()
    ax.set_title(f'{language}')

def plot_numbers(ax, loss, language, color):
    ax.hist(loss, edgecolor='black', alpha=1, bins=25, color=color, linewidth=2)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    
    ax.set_ylim(0)
    ax.set_xlim(0)

    ax.set_xlabel(r'$\Delta Loss$')
    language = language.replace('_', '-').upper()
    ax.set_title(f'{language}')