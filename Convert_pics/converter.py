from PIL import Image
import glob
import os

path_in = r"E:\GitHub\Python_Testing\Convert_pics\Originals\\"
path_out = r"E:\GitHub\Python_Testing\Convert_pics\Out\\"

list_pngs = glob.glob(path_in + "*.png")
print(list_pngs)
counter = 0
for image in glob.glob(path_in + "pu*.jpg"):
    counter = counter + 1
    img = Image.open(image)
    filename = os.path.basename(image)
    img.save(os.path.join(path_out, filename),'png')