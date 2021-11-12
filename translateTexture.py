import os
import cv2
import json
import argparse
import numpy as np
from tqdm import tqdm
from utils.utils import get_mask
from utils.image_folder import make_dataset

class translate_texture(object):
    def __init__(self, random_crop=False, random_flip=True):
        self.texture_dir = json.load(open('./cfg.json'))["path_to_textures"]
        self.sources = ['printed', 'screen']
        self.random_crop = random_crop
        self.random_flip = random_flip
        self.set_source()

    def set_source(self, source='printed'):
        if source == 'printed':
            Textures_pA = make_dataset(self.texture_dir + 'printedA/')
            Textures_pB = make_dataset(self.texture_dir + 'printedB/')
            self.Textures = Textures_pA + Textures_pB
            self.source = 'printed'
        else:
            self.Textures = make_dataset(self.texture_dir + 'screen/')
            self.source = 'screen'
        self.Nt = len(self.Textures)
        return

    def set_augmentation(self, random_crop=False, random_flip=True):
        self.random_crop = random_crop
        self.random_flip = random_flip
        return

    def texture_image(self, image, n=None):
        # Read texture
        if n is None: n = np.random.randint(self.Nt)
        texture = cv2.imread(self.Textures[n])

        # Get imagege shapes
        H1, W1, _  = texture.shape
        H2, W2, _  = image.shape

        if self.random_crop:
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
        if self.random_flip:
            if np.random.rand() < 0.5:
                texture = cv2.flip(texture , 0)
            if np.random.rand() < 0.5:
                texture = cv2.flip(texture , 1)

        # Translate texture
        im_out = image.astype(np.int32) + texture.astype(np.int32) - 128

        # Find segmentation mask
        mask = get_mask(image)

        # Remove mask
        im_out[mask>0] = 0
        np.clip(im_out, 0, 255, out=im_out)

        return im_out

    def texture_folder(self, input_dir, output_dir, exten='.jpg'):

        # Output Folder
        output_dir2 = output_dir + self.source + '/'
        if not os.path.exists(output_dir2):
            os.makedirs(output_dir2)

        # Find image names
        Files = make_dataset(input_dir)
        Nf = len(Files)

        # Loop control variables
        ind_text = np.random.randint(low=0, high=self.Nt-1, size=Nf)

        # Main loop
        for f in tqdm(range(Nf), desc='  Texturing {}'.format(self.source)):
            # Get texture index and image ID
            n = ind_text[f]
            ID = Files[f].split('/')[-1]
            ID = ID[:-4]

            # File names
            file_in = Files[f]
            file_out = output_dir2 + ID + exten

            # Read image
            image = cv2.imread(file_in)

            # Texture image
            im_out = self.texture_image(image, n=n)

            # Save image
            cv2.imwrite(file_out, im_out)

        # Acknowledge loop finish
        print('  Texture {} completed!\n'.format(self.source))
        return

if __name__ == '__main__':
    # Get user argumets
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir',  default='C:/Users/danki/Desktop/chl2_texture/validation/digital/',
                             help='Input path (directly to images)')
    parser.add_argument('-o', '--output_dir', default='C:/Users/danki/Desktop/chl2_texture/validation/',
                             help='Output folder where the [digital, printed, screen] classes will be placed')
    parser.add_argument('--random_crop', action='store_true',
                             help="Performs texture random crop with the same aspect ratio as the input")
    parser.add_argument('--random_flip', action='store_true',
                             help="Performs texture random flip (horizontal and vertical)")
    parser.add_argument('--extension', default='.jpg',
                             help='Output image extension/format')
    args = parser.parse_args()


    # Create texture translation object
    TT = translate_texture(random_crop=args.random_crop, random_flip=args.random_flip)

    # Translate to printed
    TT.set_source('printed')
    TT.texture_folder(input_dir=args.input_dir, output_dir=args.output_dir, exten=args.extension)

    # Translate to screen
    TT.set_source('screen')
    TT.texture_folder(input_dir=args.input_dir, output_dir=args.output_dir, exten=args.extension)

    print('Done!\n')
