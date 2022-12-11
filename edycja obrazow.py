
import os
from PIL import Image, ImageEnhance


def linia():
    print()
    print(60*"#")


zrodlo = "D://testowy"

files_count = 0


for name in os.listdir(zrodlo):
    if ".jpg" in name:
        files_count += 1
        file_adress = os.path.join(zrodlo, name)

        print(name)

        with Image.open(file_adress) as new_file:
            enhance = ImageEnhance.Contrast(new_file)
            new_file= enhance.enhance(1.3)
            enhance = ImageEnhance.Sharpness(new_file)
            new_file = enhance.enhance(5)

            #greyscale= new_file.convert('L')
            # greyscale.save(file_output)
            
            new_file.save(zrodlo + "//edited//" + name)

linia()
print(f'Znaleziono {files_count} plików...')
linia()
