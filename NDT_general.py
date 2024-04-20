import numpy as np


# ------------------------------------------------------------------------------
# Generally useful functions
def fn_hanning_band_pass(no_pts, start_rise_fract, end_rise_fract, start_fall_fract, end_fall_fract):
    """Returns a vector containing a Hanning band-pass function.

    The vector will be no_pts long, it will usually start at zero, rise
    smoothly to one, remain at one, then return smoothly to zero. The points
    where the transitions start and end are determined by the arguments
    start_rise_fract, end_rise_fract, start_fall_fract, and end_fall_fract.
    All of these are expressed as fractions of the total length of the vector,
    where 0 is the first point and 1 is the last point.
    """
    return fn_hanning_hi_pass(no_pts, start_rise_fract, end_rise_fract) * fn_hanning_lo_pass(no_pts, start_fall_fract,
                                                                                             end_fall_fract)


def fn_hanning_hi_pass(no_pts, start_rise_fract, end_rise_fract):
    """Returns a vector containing a Hanning high-pass function.

    The vector will be no_pts long, it will usually start at zero, rise
    smoothly to one, and remain at one. The points where the transition starts
    and ends are determined by the arguments start_rise_fract and end_rise_fract.
    Both of these are expressed as fractions of the total length of the vector,
    where 0 is the first point and 1 is the last point.
    """
    x = np.linspace(0, 1, no_pts)
    window = 0.5 * (1 - np.cos(np.pi * (x - start_rise_fract) / (end_rise_fract - start_rise_fract))) * (
                x > start_rise_fract)
    window[x > end_rise_fract] = 1
    return window


def fn_hanning_lo_pass(no_pts, start_fall_fract, end_fall_fract):
    """Returns a vector containing a Hanning low-pass function.

    The vector will be no_pts long, it will usually start at one, fall
    smoothly to zero, and remain at zero. The points where the transition starts
    and ends are determined by the arguments start_fall_fract and end_fall_fract.
    Both of these are expressed as fractions of the total length of the vector,
    where 0 is the first point and 1 is the last point.
    """
    x = np.linspace(0, 1, no_pts)
    window = 0.5 * (1 + np.cos(np.pi * (x - start_fall_fract) / (end_fall_fract - start_fall_fract))) * (
                x < end_fall_fract);
    window[x < start_fall_fract] = 1
    return window


def fn_hanning(no_pts, peak_pos_fract, half_width_fract):
    """Returns a vector containing a Hanning function.

    The vector will be no_pts long, it will usually start at zero, rise smoothly
    to one and then return smoothly to zero. The position and width of the peak
    are determined by the arguments peak_pos_fract and half_width_fract.
    Both of these are expressed as fractions of the total length of the vector,
    where 0 is the first point and 1 is the last point.
    """
    x = np.linspace(0, 1, no_pts)
    window = 0.5 * (1 + np.cos((x - peak_pos_fract) / half_width_fract * np.pi)) * \
             ((x >= (peak_pos_fract - half_width_fract)) & (x <= (peak_pos_fract + half_width_fract)))
    return window


def fn_sinc(x):
    """Evaluates the sinc function, sin(pi * x) / (pi * x)

    Input x should be an Numpy array. The function will return correct values
    without warnings even as abs(x) -> 0.
    """
    eps = np.finfo(np.float64).eps
    i = np.abs(x) < eps
    x[i] = 1
    y = np.sin(np.pi * x) / (np.pi * x)
    y[i] = 1
    return y