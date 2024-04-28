import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np

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

def plot_numbers(ax, pi_p, pi_p_u, loss, dot_pi_p, dot_pi_p_u, language):
    xminorLocator   = MultipleLocator(0.5)
    if language == 'FR_EN':
        yminorLocator = MultipleLocator(0.05)
    else:
        yminorLocator = MultipleLocator(0.025)

    ax.tick_params(axis='x', which='minor', direction='out', length=3, width=2,colors='k')
    ax.tick_params(axis='x', which='major', direction='out', length=6, width=2,colors='k')
    ax.tick_params(axis='y', which='minor', direction='out', length=3, width=2,colors='k')
    ax.tick_params(axis='y', which='major', direction='out', length=6, width=2,colors='k')

    ax.axhline(y=dot_pi_p, color='blue', linewidth=4, linestyle='--', label='dot_pi_p')
    ax.axhline(y=dot_pi_p_u, color='red', linewidth=4, linestyle='--', label='dot_pi_p_u')

    ax.plot(pi_p, marker='o', markerfacecolor='white', markersize=12, markeredgewidth=2, 
            linestyle='-', linewidth=4, color='#403990', label='Pi_p')
    ax.plot(pi_p_u, marker='s', markerfacecolor='white', markersize=12, markeredgewidth=2, 
            linestyle='-', linewidth=4, color='#f46f43', label='Pi_p_u')
    
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.yaxis.set_minor_locator(yminorLocator)

    original_ticks = ax.get_xticks()
    ax.set_xticklabels((original_ticks * 2).astype(int) + 4)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.set_ylim(0, max(max(pi_p), max(pi_p_u), dot_pi_p, dot_pi_p_u)*1.1)
    ax.set_xlim(0)
    ax.set_yticklabels([''] + ax.get_yticklabels()[1:])

    ax.set_xlabel('Epoch')
    ax.set_ylabel('Prior')
    ax.set_title(language.replace('_', '-'), fontsize=18)

    ax.grid(which='both', linewidth=1.5)



lang_list = ['fr_en', 'ja_en', 'zh_en']
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for ax, language in zip(axs, lang_list):
    pi_p = read_numbers_from_file(f'{language}\\Pi_p_epoch_temp.txt')
    pi_p_u = read_numbers_from_file(f'{language}\\Pi_p_u_epoch_temp.txt')
    loss = read_numbers_from_file(f'{language}\\loss_epoch.txt')

    if (language == 'ja_en'):
        window_size = 10
        step_length = 2
        start_point = 121
        dot_pi_p = 2*39770/(100860+139304)
        dot_pi_p_u = 0.7*2*39770/(100860+139304 - 0.3*2*39770 )
    elif (language == 'fr_en'):
        window_size = 5
        step_length = 1
        start_point = 100
        dot_pi_p = 2*123952/(221327+278411)
        dot_pi_p_u = 0.7*2*123952/(221327+278411 - 0.3*2*123952 )
    else:
        window_size = 5
        step_length = 1
        start_point = 80
        dot_pi_p = 2*33183/(84996+118996)
        dot_pi_p_u = 0.7*2*33183/(84996+118996 - 0.3*2*33183 )

    mean_pi_p = sliding_window_mean(pi_p[start_point::2], window_size=window_size, step_length=step_length)
    mean_pi_p_u = sliding_window_mean(pi_p_u[start_point::2], window_size=window_size, step_length=step_length)
    mean_loss = sliding_window_mean(loss[start_point::2], window_size=window_size, step_length=step_length)
    
    plot_numbers(ax, pi_p=mean_pi_p, pi_p_u=mean_pi_p_u, loss=mean_loss, dot_pi_p=dot_pi_p, dot_pi_p_u=dot_pi_p_u, language=language.upper())

plt.rcParams.update({'font.size': 20})
plt.tight_layout()
fig.legend([r'$\pi_p$', r'$\pi_p^u$', r'true prior $\pi_p$', r'true prior $\pi_p^u$'], loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4)

plt.savefig('..\\dbp2.0_prior_epoch.pdf', format='pdf', bbox_inches='tight')
plt.show()