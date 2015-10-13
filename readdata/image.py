import os
from skimage.feature import hog
from PIL import Image

def num_gen(size, num):
    str_num = str(num)
    return ('0'*(size - len(str_num))) + str_num


def copy_file_to(file, dest):
    os.system('cp '+file+' '+dest)


def convert_to_pgm(img_path, destine_folder, name):
    os.system("convert "+img_path+" "+destine_folder+"/"+name+".pgm")


def read_all_images(path, dest):
    images = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    size, count = len(str(len(images))), 1

    hog_vect = []

    for img in images:
        print(count)
        convert_to_pgm(img, dest, num_gen(size, count))
        path_img = os.path.join(dest, num_gen(size, count)+'.pgm')

        i = Image.open(path_img)
        hg = hog(i, orientations=8, pixels_per_cell=(32, 32), cells_per_block=(2, 2))

        hog_vect.append(hg)
        count += 1

    return hog_vect
