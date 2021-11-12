import os
import cv2
import numpy as np
from tqdm import tqdm
from utils.utils import get_mask
from utils.image_folder import make_dataset

texture_dir = 'D:/Datasets/TextureDataset/6_Textures/'
input_dir = 'C:/Users/daniel/Desktop/chl2_texture/validation/digital/'
output_dir = 'C:/Users/daniel/Desktop/chl2_texture/validation/'

sources = ['printed', 'screen']

random_crop = False
random_flip = True
exten = '.jpg'

for s in [0, 1]:

    # Output Folder
    output_dir2 = output_dir + sources[s] + '/'

    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)

    # Define texture image names
    if s == 0:
        Textures_pA = make_dataset(texture_dir + 'printedA/');
        Textures_pB = make_dataset(texture_dir + 'printedB/');
        Textures = Textures_pA + Textures_pB
    else:
        Textures = make_dataset(texture_dir + 'screen/');

    Nt = len(Textures);

    # Find image names
    Files = make_dataset(input_dir)
    Nf = len(Files);

    # Loop control variables
    ind_text = np.random.randint(low=0, high=Nt-1, size=Nf)

    # Main loop
    for f in tqdm(range(Nf), desc='Texturing {}'.format(sources[s])):
        # Get texture index and image ID
        n = ind_text[f]
        ID = Files[f].split('/')[-1]
        ID = ID[:-4]

        # File names
        file1 = Textures[n]
        file2 = Files[f]
        file3 = output_dir2 + ID + exten

        # Read texture
        texture = cv2.imread(file1)
        H1, W1, _  = texture.shape

        # Read image
        im2 = cv2.imread(file2);
        H2, W2, _  = im2.shape

        if random_crop:
            # Random Crop
            x = np.random.randint(low=0, high=int((W1/3)))
            y = np.random.randint(low=0, high=int((H1/3)))
            Wx = W1 - x
            Wy = int((H1-y)*W2/H2)
            max_W = min([Wx, Wy])
            W3 = np.random.randint(low=int(0.67*max_W) , high=max_W)
            H3 = int(W3*H2/W2)
            rect = [x, y, W3-1, H3-1]
        else:
            # Max area crop
            W3 = int(W2*H1/H2);
            H3 = int(H2*W1/W2);
            if H3 < H1:
                y = np.random.randint(low=0, high=H1-H3)
                rect = [0, y, W1-1, H3-1];
                x, y, W3, H3 = rect
            elif W3 < W1:
                x = np.random.randint(low=0, high=W1-W3)
                rect = [x, 0, W3-1, H1-1];
            else:
                print('Problem on {:d}'.format(f))
                rect = [0, 0, W1-1, H1-1]

        # Crop texture image
        x, y, W3, H3 = rect
        texture = texture[y:y+H3 , x:x+W3]

        # Resize texture
        texture = cv2.resize(texture, (W2,H2), interpolation=cv2.INTER_NEAREST)

        # Random flip
        if random_flip:
            if np.random.rand() < 0.5:
                texture = cv2.flip(texture , 0)
            if np.random.rand() < 0.5:
                texture = cv2.flip(texture , 1)

        # Translate texture
        im3 = im2.astype(np.int32) + texture.astype(np.int32) - 128

        # Find segmentation mask
        mask = get_mask(im2)

        # Remove mask
        im3[mask>0] = 0

        # Save image
        cv2.imwrite(file3, im3)
