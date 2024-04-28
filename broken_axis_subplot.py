import matplotlib.pyplot as plt
from brokenaxes import brokenaxes
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import re

def read_numbers_from_file(filename):
    numbers = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                try:
                    number = float(line.strip())
                    numbers.append(number)
                except ValueError:
                    print(f"Ignored non-numeric line: {line.strip()}")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return numbers

def write_numbers_to_file(numbers, filename):
    try:
        with open(filename, 'w') as file:
            for number in numbers:
                file.write(f"{number}\n")
        print(f"Numbers have been written to '{filename}' successfully.")
    except Exception as e:
        print(f"Error writing to '{filename}': {e}")

def plot_numbers(p1, p2, p3, p4):
    plt.figure(figsize=(10, 6))

    plt.plot(p1, marker='o', linestyle='-', color = '#403990', label='Pi_p')
    plt.plot(p2, marker='s', linestyle='-', color = '#f46f43', label='Pi_p_u')
    plt.plot(p3, marker='h', linestyle='-', color = '#80a6e2', label='loss')
    plt.plot(p4, marker='*', linestyle='-', color = 'red', label='loss')

    plt.show()

def same_sizer(*p):
    longest_lst = max(p, key=len)

    for lst in p:
        if len(lst) < len(longest_lst):
            lst.extend([lst[-1]] * (len(longest_lst) - len(lst)))

def sliding_window_mean(nums_in, window_size = 5, step_length = 3):
    if len(nums_in) < window_size:
        return f"Not enough numbers for a window of size {window_size}."
    means = []
    nums = nums_in + [nums_in[-1]]*(window_size-1)
    for i in range(0, len(nums)-(window_size-1), step_length):
        window = nums[i:i+window_size]
        mean = sum(window) / window_size
        means.append(mean)
        
    return means

def extract_float(s):
    match = re.search(r'(\d+\.\d+)', s)
    if match:
        return float(match.group(1))
    else:
        return None
    
def sci_format(x, pos):
    if x == 0:
        return "0"
    coeff, exp = f"{x:.1e}".split('e')
    coeff = coeff.rstrip('0').rstrip('.')
    return f"{coeff}e{int(exp)}"



fig = plt.figure(figsize=(24, 5))

sps = GridSpec(1,4, wspace=0.5)
onwhat = 'Pi_p_u_temp'
percentage_list = ["0.25_en", "0.2_en", "0.15_en", "0.1_en"]

handles_list = []
labels_list = []

formatter = FuncFormatter(sci_format)

for percentage, sp in zip(percentage_list, sps):
    p1 = read_numbers_from_file('GA-EN\\' + percentage + '\\' + onwhat + '_1e.txt')
    p2 = read_numbers_from_file('GA-FR\\' + percentage + '\\' + onwhat + '_1e.txt')
    p3 = read_numbers_from_file('GA-JA\\' + percentage + '\\' + onwhat + '_1e.txt')
    p4 = read_numbers_from_file('GA-ZH\\' + percentage + '\\' + onwhat + '_1e.txt')
    same_sizer(p1, p2, p3, p4)
    p1 = p1[16:]
    p2 = p2[16:]
    p3 = p3[16:]
    p4 = p4[16:]

    if (percentage == "0.25_en"):
        ylims = ((0.002, 0.008), (0.04, 0.1))
        xminorLocator0 = MultipleLocator(1)
        xminorLocator1 = MultipleLocator(1)
        yminorLocator0 = MultipleLocator(0.0125)
        yminorLocator1 = MultipleLocator(0.0005)
    elif (percentage == "0.2_en"):
        ylims = ((0.001, 0.006), (0.01, 0.02))
        p1 = p1[::2]
        p2 = p2[::2]
        p3 = p3[::2]
        p4 = p4[::2]
        xminorLocator0 = MultipleLocator(0.5)
        xminorLocator1 = MultipleLocator(0.5)
        yminorLocator0 = MultipleLocator(0.0025)
        yminorLocator1 = MultipleLocator(0.0005)
    elif (percentage == "0.15_en"):
        ylims = ((0.0002, 0.0015), (0.004, 0.01))
        p1 = p1[::3]
        p2 = p2[::3]
        p3 = p3[::3]
        p4 = p4[::3]
        xminorLocator0 = MultipleLocator(2/3)
        xminorLocator1 = MultipleLocator(2/3)
        yminorLocator0 = MultipleLocator(0.00125)
        yminorLocator1 = MultipleLocator(0.0001)
    else:
        ylims = ((0, 0.00015), (0.0004, 0.0012))
        p1 = p1[::2]
        p2 = p2[::2]
        p3 = p3[::2]
        p4 = p4[::2]
        xminorLocator0 = MultipleLocator(0.5)
        xminorLocator1 = MultipleLocator(0.5)
        yminorLocator0 = MultipleLocator(0.00125)
        yminorLocator1 = MultipleLocator(0.00001)

    bax = brokenaxes(ylims=ylims, height_ratios=[1, 3], subplot_spec=sp, d=0.005, despine=False)
    bax.plot(np.arange(0, len(p1), 1), p1, 
             marker='s', markerfacecolor='white', markersize=12, markeredgewidth=2,
             linewidth=4, color = '#403990', label=r'GA-EN')
    bax.plot(np.arange(0, len(p2), 1), p2, 
             marker='^', markerfacecolor='white', markersize=12, markeredgewidth=2,
             linewidth=4, color = '#80a6e2', label=r'GA-FR')
    bax.plot(np.arange(0, len(p3), 1), p3, 
             marker='o', markerfacecolor='white', markersize=12, markeredgewidth=2,
             linewidth=4, color = '#fbdd85', label=r'GA-JA')
    bax.plot(np.arange(0, len(p4), 1), p4, 
             marker='D', markerfacecolor='white', markersize=12, markeredgewidth=2,
             linewidth=4, color = '#f46f43', label=r'GA-ZH')

    bax.axs[0].set_xlim(0, len(p1)-1/2)
    bax.axs[1].set_xlim(0, len(p1)-1/2)

    handles, labels = bax.axs[0].get_legend_handles_labels()
    handles_list.extend(handles)
    labels_list.extend(labels)

    original_ticks = bax.axs[1].get_xticks()

    bax.axs[1].yaxis.set_major_formatter(formatter)
    bax.axs[0].yaxis.set_major_formatter(formatter)
    # set upper plot x tickers
    bax.axs[0].tick_params(axis='x', which='minor', direction='out', length=3, width=2,colors='k')
    bax.axs[0].tick_params(axis='x', which='major', direction='out', length=6, width=2,colors='k')
    # set lower plot x tickers
    bax.axs[1].tick_params(axis='x', which='minor', direction='out', length=3, width=2,colors='k')
    bax.axs[1].tick_params(axis='x', which='major', direction='out', length=6, width=2,colors='k')
    # set upper plot y tickers
    bax.axs[0].tick_params(axis='y', which='minor', direction='out', length=3, width=2,colors='k')
    bax.axs[0].tick_params(axis='y', which='major', direction='out', length=6, width=2,colors='k')
    # set lower plot y tickers
    bax.axs[1].tick_params(axis='y', which='minor', direction='out', length=3, width=2,colors='k')
    bax.axs[1].tick_params(axis='y', which='major', direction='out', length=6, width=2,colors='k')

    if (percentage == "0.25_en"):
        bax.axs[1].set_yticks(np.arange(0.002, 0.009, 0.002))
        bax.axs[0].set_yticks(np.arange(0.04, 0.12, 0.05))
        bax.axs[0]
        bax.set_ylabel('Prior', labelpad=60)
    elif (percentage == "0.2_en"):
        bax.axs[1].set_yticks(np.arange(0.001, 0.007, 0.002))
        bax.axs[0].set_yticks(np.arange(0.01, 0.03, 0.01))
        bax.set_ylabel('Prior', labelpad=60)
        bax.axs[1].set_xticklabels((original_ticks * 2).astype(int))
    elif (percentage == "0.15_en"):
        bax.axs[1].set_yticks(np.arange(0.0002, 0.0016, 0.0005))
        bax.axs[0].set_yticks(np.arange(0.004, 0.012, 0.005))
        bax.set_ylabel('Prior', labelpad=75)
        bax.axs[1].set_xticklabels((original_ticks * 3).astype(int))
    else:
        bax.axs[1].set_yticks(np.arange(0, 0.00014, 0.00004))
        bax.axs[0].set_yticks(np.arange(0.0004, 0.0014, 0.0005))
        bax.set_ylabel('Prior', labelpad=80)
        bax.axs[1].set_xticklabels((original_ticks * 2).astype(int))

    # bax.axs[0].xaxis.set_minor_locator(xminorLocator0)
    bax.axs[1].xaxis.set_minor_locator(xminorLocator1)
    bax.axs[0].yaxis.set_minor_locator(yminorLocator0)
    bax.axs[1].yaxis.set_minor_locator(yminorLocator1)
    
    bax.set_xlabel('Epoch', labelpad=30)
    bax.set_title(extract_float(percentage), fontsize=19)

    for axis in ['top','bottom','left','right']:
        bax.axs[0].spines[axis].set_linewidth(2)
        bax.axs[1].spines[axis].set_linewidth(2)
    
    # bax.grid(which='both')

fig.legend(handles_list[:4], labels_list[:4], loc='upper center', ncol=4, bbox_to_anchor=(0.5, 1.1))

plt.tight_layout()
plt.rcParams.update({'font.size': 20})
plt.savefig(f'..\\GA_XX_prior_epoch.pdf', bbox_inches='tight', format='pdf')
