# textures
Translate a digital image into a printed version or a screen capture.

It is based on manually captured images of solid colors under different conditions of printer setups, illumination, paper qualities, capturing devices, and projected screens. The original images were processed to isolate the underlaying color with texture. After that the mean color was subtracted from the image, leaving only the texture underneath.

Ten-thousand textures were captured in total, with great variability. Therefore, there are smooth textures from high quality glossy paper and HD displays, but also there are rough textures with lots of details regarding inks, paper surfaces and pixel aliasing.

This repository contains functions that transfer those manually-captured textures to any new image, using basic image processing techniques. The resulting image will thus possess the appearance of a printed or screen captured version of itself.

Finally, if the image was segmented with black borders around it, there is a flag to respect those borders so they remain solid black.

#### Examples
Let's apply different textures to Lena
![alt text](./assets/full_images.png?raw=true)

Textures can be better appreciated while zoomed in
![alt text](./assets/zoomed_images.png?raw=true)

#### Requirements and Configuration
1) This requires an environment with python>3.5, opencv>4.0, numpy, tqdm, json, matplotlib and jupyter notebook.

2) Download the textures from [this link](https://www.dropbox.com/s/t9ha0hgx0rsficc/textures-ID-Card.zip?dl=0) and unzip them in a known location. You must request the password to the authors:
  - Daniel Benalcazar: dbenalcazar@ug.uchile.cl
  - Juan Tapia: juan.tapia-farias@h-da.de

3) Copy cfg_example.json under the name cfg.json, and change the field "path_to_textures" so that it points to the location where you saved the downloaded textures.

4) Enjoy!

#### How to use
The main program is **translateTexture.py**, which contains the **translate_texture** class and can also be used to translate entire folders via console.

The **translate_texture** object can be used to translate single images, as well as entire folders. The jupyter notebook **example_one_image.ipynb** gives an explanation on how to use it.

If you want to translate an entire dataset with train, test and validation partitions, then you must use the jupyter notebook **Translate Dataset.ipynb**, which iterates over the **translate_texture** class to translate all the folders in the dataset.

#### Future improvements
1) Use threading for parallel processing
2) More data augmentations over the textures
3) Increase the amount of manually captured textures

### Cite Us
(comming soon)
