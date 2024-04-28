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

def same_sizer(*p):
    longest_lst = max(p, key=len)

    for lst in p:
        if len(lst) < len(longest_lst):
            lst.extend([lst[-1]] * (len(longest_lst) - len(lst)))

def subtract_first_to_zero(lst):
    lst = [int(x) for x in lst]
    first_element = lst[0]
    return [x - first_element for x in lst]

def calculate_differences(list):
    differences = []
    
    for i in range(len(list) - 1):
        diff = abs(list[i+1] - list[i])
        differences.append(diff)
    
    return differences

def calculate_mean_and_variance(lines):
    # Convert lists to NumPy arrays
    lines = [np.array(line) for line in lines]
    
    # Calculate mean line
    mean_line = np.mean(lines, axis=0)
    
    # Calculate variance line
    variance_line = np.var(lines, axis=0)
    
    return mean_line, variance_line

def plot_numbers(ax, loss_25, loss_2, loss_15, loss_1, language, color):
    xminorLocator   = MultipleLocator(5)
    yminorLocator = MultipleLocator(0.05)

    losses = [loss_25, loss_2, loss_15, loss_1]
    mean_line, variance_line = calculate_mean_and_variance(losses)

    ax.tick_params(axis='x', which='minor', direction='out', length=3, width=2,colors='k')
    ax.tick_params(axis='x', which='major', direction='out', length=6, width=2,colors='k')
    ax.tick_params(axis='y', which='minor', direction='out', length=3, width=2,colors='k')
    ax.tick_params(axis='y', which='major', direction='out', length=6, width=2,colors='k')

    ax.plot(mean_line, linestyle='-', linewidth=2, color=color, label=f'0.25')
    ax.fill_between(np.arange(len(mean_line)), mean_line-np.sqrt(variance_line), mean_line, color=color, alpha=0.2)
    ax.fill_between(np.arange(len(mean_line)), mean_line+np.sqrt(variance_line), mean_line, color=color, alpha=0.2)
    
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.yaxis.set_minor_locator(yminorLocator)

#     original_ticks = ax.get_xticks()
#     ax.set_xticklabels(subtract_first_to_zero(original_ticks * 2))

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.set_ylim(0, max(mean_line+variance_line)*1.1)
    ax.set_xlim(0)
    ax.set_yticklabels([''] + ax.get_yticklabels()[1:])

    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title(language, fontsize=18)



language_list = ['GA-EN', 'GA-FR', 'GA-JA', 'GA-ZH']
color_list = ['red', 'green', 'blue', 'orange']
fig, axs = plt.subplots(1, 4, figsize=(20, 5))

for ax, language, color in zip(axs, language_list, color_list):
    loss_25 = read_numbers_from_file(f'{language}\\0.25_en\\loss_1e.txt')
    loss_2 = read_numbers_from_file(f'{language}\\0.2_en\\loss_1e.txt')
    loss_15 = read_numbers_from_file(f'{language}\\0.15_en\\loss_1e.txt')
    loss_1 = read_numbers_from_file(f'{language}\\0.1_en\\loss_1e.txt')

    same_sizer(loss_25, loss_2, loss_15, loss_1)
    
    plot_numbers(ax, loss_25=loss_25, loss_2=loss_2, loss_15=loss_15, loss_1=loss_1, 
                 language=language, color=color)

plt.rcParams.update({'font.size': 20})
plt.tight_layout()
fig.legend(['mean', 'variance'], loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4)

plt.savefig('..\\GA_XX_prior_epoch_loss.pdf', format='pdf', bbox_inches='tight')
plt.show()