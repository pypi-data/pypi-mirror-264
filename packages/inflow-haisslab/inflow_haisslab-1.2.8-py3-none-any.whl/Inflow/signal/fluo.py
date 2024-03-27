# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import zscore

def non_zero_raw_fluorescence(array):
    return (array - array.min() ) + 2

def delta_over_F(array, F0_index = 0, F0_span = 1):
    """Performs deltaF over F0 ( with eq : DF0 = F - F0 / F0 )    
    """
    
    if array.min() <= 0:
        array = non_zero_raw_fluorescence(array.copy())
    
    F0_frame = array[F0_index:F0_index+F0_span].mean(axis = 0)
    
    F0_frames = np.repeat( F0_frame[np.newaxis], repeats = array.shape[0], axis = 0)
    return (array - F0_frames) / F0_frames 
    
# def delta_over_F(array, F0_index = 0, sigma = None, optimize = "speed"):
#     from scipy.ndimage import gaussian_filter1d
#     #NOT A SINGLE OR AVERAGE OF MULTIPLE FRAMES BUT A TEMPORAL GAUSSIAN AROUND FRAME 
    
#     if array.min() <= 0:
#         array = non_zero_raw_fluorescence(array.copy())
    
#     if sigma is not None :    
#         F0_frame = gaussian_filter1d(array, sigma , axis = 0)[F0_index] #time as first index. Other dimensions after that
#     else :
#         F0_frame = array[F0_index]
    
#     if optimize == "speed":
#         F0_frame = np.repeat( F0_frame[np.newaxis], array.shape[0], axis = 0)
#         return (array - F0_frame) / F0_frame 
#     elif optimize == "ram":
#         return_array = array.copy()
#         for i in range(return_array.shape[0]):
#             return_array[i] = (return_array[i] - F0_frame) / F0_frame
#         return return_array
#     else :
#         raise ValueError("optimize argument must either be 'speed' or 'ram'")
    
delta_over_f = delta_over_F

    