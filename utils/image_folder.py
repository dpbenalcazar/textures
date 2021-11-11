import numpy as np
import os

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
    '.tif', '.TIF', '.tiff', '.TIFF', '.npy'
]


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def make_dataset(path_files, root_dir='', max_n=float("inf"), shuffle=False):
    if path_files.find('.txt') != -1:
        # Read image names from text files
        paths, size = make_dataset_txt(path_files)
    else:
        # Read the image names inside a folder
        paths, size = make_dataset_dir(path_files)

    # Shuffle images
    if shuffle:
        np.random.shuffle(paths)
    else:
        paths = sorted(paths)

    # Limit the number of images
    if size > max_n:
        paths = paths[:max_n]

    return paths

def make_dataset_txt(path_files, root_dir=''):
    # reading txt file
    image_paths = []

    with open(path_files) as f:
        paths = f.readlines()

    for path in paths:
        # path = path.strip()
        path = root_dir + path.strip()
        image_paths.append(path)

    return image_paths, len(image_paths)


def make_dataset_dir(dir):
    image_paths = []

    assert os.path.isdir(dir), '%s is not a valid directory' % dir

    for root, _, fnames in os.walk(dir):
        for fname in sorted(fnames):
            if is_image_file(fname):
                path = os.path.join(root, fname)
                image_paths.append(path)

    return image_paths, len(image_paths)



def default_loader(path):
    return Image.open(path).convert('RGB')
