# textures
Translate a digital image into a printed version or a screen capture.

It is based on manually captured images of solid colors under different conditions of printer setups, illumination, paper qualities, capturing devices, and projected screens. The original images were processed to isolate the underlaying color with texture. After that the mean color was subtracted from the image, leaving only the texture underneath.

This repository contains functions that transfer those manually-captured textures to any new image, using basic image processing techniques. The resulting image will thus possess the appearance of a printed or screen captured version of itself.

Finally, if the image was segmented with black borders around it, those borders are not textured so they remain solid black.

#### Examples
Let's apply different textures to Lena
![alt text](./assets/full_images.png?raw=true)

Textures can be better appreciated while zoomed in
![alt text](./assets/zoomed_images.png?raw=true)

#### Requirements and Configuration
1) This requires an environment with python>3.5, opencv>4.0, numpy, tqdm, json, matplotlib and jupyter notebook

2) Download the textures from [google drive](https://drive.google.com/file/d/1wLyl2vb3RLFWliGA2LwngwZeHmRex3SB/view?usp=sharing) and unzip them in a known location

3) Copy cfg_example.json under the name cfg.json, and change the field "path_to_textures" so that it points to the location where you saved the downloaded textures

4) Enjoy!

#### How to use
The main program is **translateTexture.py**, which contains the **translate_texture** class and can also be used to translate entire folders via console.

The **translate_texture** object can be used to translate single images, as well as entire folders. The jupyter notebook **example_one_image.ipynb** gives an explanation on how to use it.

If you want to translate an entire dataset with train, test and validation partitions, then you must use the jupyter notebook **Translate Dataset.ipynb**, which iterates over the **translate_texture** class to translate all the folders in the dataset.

#### Future improvements
1) Use threading for parallel processing
2) More data augmentations over the textures
