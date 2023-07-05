from PIL import Image
import glob
import os

path_in = r"E:\GitHub\Python_Testing\Convert_pics\Input\\"
path_out = r"E:\GitHub\Python_Testing\Convert_pics\Out"

list_pngs = glob.glob(path_in + "*.jpg")
print(*list_pngs,sep="\n")

for image in glob.glob(path_in + "*.png"):
    img = Image.open(image)
    filename = os.path.basename(image)
    filename_ext = os.path.splitext(filename)
    img.save(os.path.join(path_out, filename_ext[0] + ".png"),'png')

print("finished")