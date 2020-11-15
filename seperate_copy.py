import os
from tkinter import filedialog
import shutil
import numpy as np
from imutils import paths

# Root = filedialog.askdirectory()
Root = os.getcwd()
file_list = os.listdir(os.path.join(Root,'Q'))

xml_list = []
img_list = list(paths.list_images(os.path.join(Root,'Q')))

for file in file_list:
    if file.endswith(".xml"):
        xml_list.append(file)

xml_list.sort()
img_list.sort()

arr_xml = np.array(xml_list)
arr_bmp = np.array(img_list)

type_list = [xml_list, img_list]

linspace_ = np.linspace(1,len(xml_list), 4)
linspace_ = list(map(int, linspace_))
linspace_.pop(0)
print(linspace_)

init_num = 0
count = 1

for lens in linspace_:
    os.makedirs(os.path.join(Root, 'Q_{}'.format(count)), exist_ok=True)
    for i in range(init_num,lens):
        shutil.copy(os.path.join(Root, 'Q', xml_list[i]), os.path.join(Root, 'Q_{}'.format(count), xml_list[i]))
        # shutil.copy(os.path.join(Root, 'U', img_list[i]), os.path.join(Root, 'U_{}'.format(count), img_list[i]))
        shutil.copy(img_list[i], os.path.join(Root, 'Q_{}'.format(count), os.path.basename(img_list[i])))
    init_num = lens
    count += 1






