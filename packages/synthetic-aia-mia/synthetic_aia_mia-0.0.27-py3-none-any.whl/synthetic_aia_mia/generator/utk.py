from pygan._mxnet.gan_image_generator import GANImageGenerator
from pathlib import Path
import pickle
import numpy as np
import os
from PIL import Image

def _pathmaker(i):
    path = Path("dataset_for_pygan")
    os.makedirs(path, exist_ok=True)
    return Path(path, f"{str(i)}")

def gan(dataset):
    """Generate image using pygan.

    :param dataset: Image dataset used to train the gan.
    :type dataset: fetch_data.utk.StorageDataset
    :return: A dataset with generated images.
    :rtype : fetch_data.utk.StorageDataset
    """

    #Saving 50x50 images from the train dataset
    for i in range(len(dataset)):
        x = dataset[i][0]
        x = x*255
        x = np.moveaxis(x,0,2).astype(int)
        image = Image.fromarray(x.astype('uint8'), 'RGB')
        image.save(_pathmaker(i), "bmp")
        

    gan_image_generator = GANImageGenerator(
        # `list` of path to your directories.
        dir_list=["dataset_for_pygan"],
        # `int` of image width.
        width=50,
        # `int` of image height.
        height=50,
        # `int` of image channel.
        channel=3,
        # `int` of batch size.
        batch_size=40,
        # `float` of learning rate.
        learning_rate=1e-06,
    )

    gan_image_generator.learn(
        # `int` of the number of training iterations.
        iter_n=100000,
        # `int` of the number of learning of the discriminative model.
        k_step=10,
    )

    
    path = Path("synthetic_data")
    
    arr = gan_image_generator.GAN.generative_model.draw()
    
    #arr shape is:
    #batch
    #channel
    #height
    #width

    #save generate images 
    for i in range(np.shape(arr))[0]:
        Path(path,str(i))
        image = Image.fromarray(arr[i].astype('uint8'), 'RGB')
        image.save(_pathmaker(i), "bmp")
        




