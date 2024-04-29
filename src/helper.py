import numpy as np
from scipy.ndimage.morphology import binary_dilation
from scipy.ndimage import generate_binary_structure
from scipy.signal import convolve2d

def sum_of_neighbors(array, row, col):
    # Define the neighborhood indices around the target element (row, col)
    array_copy = array.copy()
    for i in range(len(array_copy)):
        for j in range(len(array_copy[i])):
            if array_copy[i][j] is None:
                array_copy[i][j] = 0

    neighborhood = array_copy[max(0, row - 1):min(array_copy.shape[0], row + 2),
                         max(0, col - 1):min(array_copy.shape[1], col + 2)]
    
    # Sum all elements in the neighborhood and subtract the value of the target element
    neighbors_sum = np.sum(neighborhood) - array_copy[row, col]
    return neighbors_sum


def print_colored_array(array):
    color_map = {
        0: '\033[91m',  # Red color for 0
        1: '\033[92m',  # Green color for 1
        2: '\033[93m',  # Yellow color for 2
        3: '\033[94m',  # Blue color for 3
        4: '\033[95m',  # Magenta color for 4
        5: '\033[96m',  # Cyan color for 5
        6: '\033[97m',  # White color for 6
        # Add more colors for additional values if needed
    }
    reset_color = '\033[0m'  # Reset color to default
    
    for row in array:
        for value in row:                
            if value in color_map:
                colored_value = color_map[value] + str(value) + reset_color
            else:
                colored_value = str(value)
            print(f'{colored_value:4}', end='')  # Adjust the spacing as needed
        print()  # Move to the next line after printing each row

def bool_to_int(bool_ar):
    # Convert boolean array to integer array
    int_ar = bool_ar.astype(int)
    return int_ar

def neighbors(x, y, shape):
    return mask(x, y, shape) ^ binary_dilation(mask(x, y, shape), structure=generate_binary_structure(2, 2))

def mask(x, y, shape):
    mask = np.zeros(shape, dtype=bool)
    mask[y, x] = True
    return mask

def get_true_neighbor_count(arr):
    ftr = np.array([[1,1,1],[1,0,1],[1,1,1]])
    # print("Arr: ", arr)
    return convolve2d(arr, ftr, mode='same')