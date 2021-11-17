import argparse
from translateTexture import translate_texture

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_dir',  default='/home/ubuntu/Datasets/Cedulas/Mexico/',
                         help='Path to dataset directory with train test and validation partitions')
parser.add_argument('--extension', default='.jpg',
                         help='Output image extension/format')
args = parser.parse_args()


TT = translate_texture(black_border=True, random_crop=False, random_flip=True)

dataset_dir = args.input_dir
# must have train/digital/ , test/digital and validation/digital

for sets in ['test', 'train', 'validation']:
    print('\nProcessing {} ...'.format(sets))
    for souece in ['printed', 'screen']:
        # Configure TT
        TT.set_source(souece)

        # Set in/out folders
        input_dir = dataset_dir + sets + '/digital/'
        output_dir = dataset_dir + sets + '/'

        # Translate folder
        TT.texture_folder(input_dir, output_dir, exten=args.extension)
