from astropy.io import fits
from astropy.wcs import WCS

import numpy as np

import os
import pickle


def ellipse_coords(x, y, a, b, theta, num_points=100, b_is_ellipticity=False):

    # Generate angles for sampling
    angles = np.linspace(0, 2*np.pi, num_points)
    
    # If b is supplied as an ellipticity (and not as the semiminor axis directly, calculate semiminor axis)
    if b_is_ellipticity:
        b = a * (1 - b)

    # Parametric equation for the ellipse
    x_coords = x + a * np.cos(angles) * np.cos(theta) - b * np.sin(angles) * np.sin(theta)
    y_coords = y + a * np.cos(angles) * np.sin(theta) + b * np.sin(angles) * np.cos(theta)

    # Return the sampled coordinates as a NumPy array
    return x_coords, y_coords


def line_endpoints(x0, y0, L, theta):
    # Convert the angle from degrees to radians
    theta_radians = np.deg2rad(theta)

    # Calculate the endpoint coordinates
    xs = np.array([x0 + L * np.cos(theta_radians), x0 - L * np.cos(theta_radians)])
    ys = np.array([y0 + L * np.sin(theta_radians), y0 - L * np.sin(theta_radians)])

    return xs, ys


def line_corners(x0, y0, w, L, theta):
    theta = np.deg2rad(90 - theta)
    # Rotation matrix
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], 
                                [np.sin(theta),  np.cos(theta)]])
    
    # Half dimensions
    hw, hL = w / 2, L / 2
    
    # Define corners relative to center before rotation
    corners = np.array([(-hw, -hL), (hw, -hL), (hw, hL), (-hw, hL), (-hw, -hL)])
    
    # Rotate and translate corners
    rotated_corners = np.dot(corners, rotation_matrix) + np.array([x0, y0])
    
    return np.transpose(rotated_corners)


def centre_coords(input_wcs, ra, dec):
    cent_x, cent_y = input_wcs.wcs_world2pix(ra, dec, 0)

    return cent_x, cent_y



def match_wcs_axes(wcs1, wcs2):
    """ Match the axes in WCS axes (mostly for image alignment with cubes and images).
        This method assumes that the ra/dec axes are always at indices 0 and 1.

    Args:
        wcs1 (astropy.wcs): WCS A
        wcs2 (astropy.wcs): WCS B

    Returns:
        _type_: Both WCS objects.
    """
    
    naxis1, naxis2 = wcs1.wcs.naxis, wcs2.wcs.naxis

    if naxis1 == naxis2:
        return wcs1, wcs2
    
    to_reduce, target = np.argmax([naxis1, naxis2]), np.min([naxis1, naxis2])

    wcs_objs = [wcs1, wcs2]

    while wcs_objs[to_reduce].wcs.naxis > target:
        wcs_objs[to_reduce] = wcs_objs[to_reduce].dropaxis(-1)

    return wcs_objs


def bounds_from_moment_map(data, padding=0):
    
    non_nans = np.transpose(np.argwhere(~np.isnan(data)))
    ymin, ymax = np.min(non_nans[0]) - padding, np.max(non_nans[0]) + padding
    xmin, xmax = np.min(non_nans[1]) - padding, np.max(non_nans[1]) + padding

    return int(xmin), int(xmax), int(ymin), int(ymax)


def pad_limits(limits, padding):
    xmin, xmax, ymin, ymax = limits
    return [int(xmin - padding), int(xmax + padding), int(ymin - padding), int(ymax + padding)]


def beam_area(bmaj, bmin):
    """ Get the area of the beam based on a standard elliptical Gaussian beam with major and 
        minor axes bmaj and bmin.

    Args:
        bmaj (float): Major axis of beam
        bmin (float): Minor axis of beam

    Returns:
        float: The beam area.
    """
    return np.pi * bmaj * bmin / (4 * np.log(2))


def RMS(a, sigclip=False):
    # todo: add sigma clipping
    a = np.asarray(a)
    return np.sqrt(np.nanmean(a * a))


def estimate_rms(cube, channel_min, channel_max):

    spec_empty = np.concatenate((cube[:channel_min], cube[-channel_max:]))
    
    return np.nanmean(spec_empty), RMS(spec_empty)


def normalize(a, clip_low = None, clip_high=None, stretch=None):
    a_norm = np.copy(a)

    if clip_low is not None:
        a_norm[a_norm < clip_low] = clip_low

    a_norm -= np.nanmin(a_norm)

    if clip_high is not None:
        a_norm[a_norm > clip_high] = clip_high

    a_norm /= np.nanmax(a_norm)

    if stretch == "square":
        a_norm = a_norm * a_norm
    if stretch == "log":
        a_norm = np.log10(a_norm)
    if stretch == "asin":
        a_norm = np.arcsin(a_norm)
    if stretch == "asinh":
        a_norm = np.arcsinh(a_norm)

    return a_norm


def imstat(a):
    """ Simple tool to return statistics for a given array.

    Args:
        a (ndarray): Input array to get statistics.

    Returns:
        _type_: _description_
    """
    return {
        "MEDIAN": np.nanmedian(a),
        "STD": np.nanstd(a),
        "MAX": np.nanmax(a),
        "MIN": np.nanmin(a)
    }

def im_bounds(stats, sigma=1):
    if type(sigma) in (int, float):
        sigma = (sigma, sigma)


    low = stats["MEDIAN"] - sigma[0] * stats["STD"]
    high = stats["MEDIAN"] + sigma[1] * stats["STD"]

    return low, high


def normalized_rgb_image(image, sigma=1, stretch=None):
    """ Generate a properly formatted RGB image from a 3xmxn input.

    Args:
        image (ndarray): 3 x m x n input image.
        sigma (int, float, or array optional): Sigma levels to adjust stretches and clips. Defaults to 1.
            int: sigma for all 3 RGB images 
            tuple: All 3 images clipped to (sigma[0], sigma[1])
            Array of len(3): R,G,B images clipped to sigma[0], sigma[1], sigma[2], respectively.
        stretch (str, optional): Type of stretch to apply. Defaults to None.

    Returns:
        ndarray: The properly transposed, stretched and clipped RGB image.
    """
    r,g,b = image

    # If the sigma length is 3, assume it's of the format [sigma_r, sigma_g, sigma_br]
    if type(sigma) not in (int, float) and len(sigma) == 3:
        sigma_r, sigma_g, sigma_b = sigma
    else:
        sigma_r = sigma_g = sigma_b = sigma
    
    bounds_r = im_bounds(imstat(r), sigma=sigma_r)
    bounds_g = im_bounds(imstat(g), sigma=sigma_g)
    bounds_b = im_bounds(imstat(b), sigma=sigma_b)

    r = normalize(r, clip_low=bounds_r[0], clip_high=bounds_r[1], stretch=stretch)
    g = normalize(g, clip_low=bounds_g[0], clip_high=bounds_g[1], stretch=stretch)
    b = normalize(b, clip_low=bounds_b[0], clip_high=bounds_b[1], stretch=stretch)

    return np.asarray([r,g,b]).transpose(1,2,0)


def recommended_figsize(a, width=8):

    height = np.round(width * a.shape[0] / a.shape[1], 1)

    return (width, height)


def check_and_make_dir(directory):
    path = os.path.dirname(directory)
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return directory



def check_kwarg(key, default, kwargs: dict):
    if key in kwargs.keys(): 
        return kwargs[key]
    else: 
        return default
    

def create_channel_ranges(n):
    """ Create an array of None values of length n (to initialize channel ranges for spectral analysis) """
    return [None for _ in range(n)]


def H2_Mass(SCO, D_L=100., z_gal=0.01, freq=220., a_CO=3.2, R_21=0.8):
    """ Calculate the H2 mass from a CO(2-1) emission map

    Args:
        SCO (float): The integrated CO(2-1) flux (in Jy km/s)
        D_L (float, optional): The luminosity distance (in MPC). Defaults to 100.
        z_gal (float, optional): The redshift of the galaxy. Defaults to 0.01.
        freq (float, optional): The observing frequency (in GHz). Defaults to 220.
        a_CO (float, optional): The CO conversion factor (in solar masses per square pc). Defaults to 3.2.
        R_21 (float, optional): The CO(2-1)/(1-0) ratio. Defaults to 0.8 (from Leroy et al, 2009).
    """
    LCO = 3.25e7 * SCO * (D_L ** 2)
    LCO /= (freq ** 2)
    LCO /= ((1 + z_gal) ** 3)

    MH2 = 1.34 * (a_CO / R_21) * LCO

    return MH2


def save_pickle(out_object, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(out_object, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    with open(filename, 'rb') as handle:
        out_object = pickle.load(handle)
    return out_object
