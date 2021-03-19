import matplotlib.cbook as cbook
import matplotlib.image as image
import cv2
import os
import numpy as np
import urllib.request
import os.path

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

def filename_to_image(filename):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    if os.path.isfile(filename):
      image = cv2.imread(filename)
    else:
      assert filename.startswith("http")
      url = filename
      request = urllib.request.Request(url, headers=headers)
      resp = urllib.request.urlopen(request).read()
      image_array = np.asarray(bytearray(resp), dtype="uint8")
      # raise Exception(len(image_array))
      image = cv2.imdecode(image_array, cv2.IMREAD_COLOR) 
      
    # return the image
    return image

def scale_image(filename_with_path, scaling_factor=1, mirror=False):
    with cbook.get_sample_data(filename_with_path) as file:
      original_image = image.imread(file)
    new_shape = (int(original_image.shape[1] / scaling_factor), 
                 int(original_image.shape[0] / scaling_factor))
    resized_image = cv2.resize(original_image, dsize=new_shape)
    if mirror:
      resized_image = resized_image[:,::-1,:]
    return resized_image

def mirror_image(img):
    return img[:,::-1,:]

def prepare_image(filename_with_path, mirror=False):
    if filename_with_path.startswith('~'):
        filename_with_path = os.path.expanduser(filename_with_path)
    with cbook.get_sample_data(filename_with_path) as file:
        prepared_image = image.imread(file)
    if mirror:
        prepared_image = mirror_image(img=prepared_image)
    return prepared_image

def show_image(ax, prepared_image, origin, zorder=0, scaling_factor=1, where_position=""):
    extent=[origin[0], origin[0] + prepared_image.shape[1] * scaling_factor, 
            origin[1], origin[1] + prepared_image.shape[0] * scaling_factor]
    if 'R' in where_position:
        extent[0] -= prepared_image.shape[0]*scaling_factor
        extent[1] -= prepared_image.shape[0]*scaling_factor

    result = ax.imshow(prepared_image, extent=extent, zorder=zorder)
    return result