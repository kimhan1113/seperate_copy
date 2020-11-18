import os
from xml.etree.ElementTree import parse
from pascal_voc_writer import Writer
from tqdm import tqdm
from imutils import paths
import shutil
import argparse
import re

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(dest = 'dir',
                        nargs='+',
                        help = 'file or directory path(s) to execute preprocessing',
                        )
    args = parser.parse_args()
    save_path = args.dir[0] + '_refine'
    return args, save_path

def remove_dup_char(dir_name, save):

    Root = os.getcwd()
    xml_path = (os.path.join(Root, dir_name))
    xml_list = [xml for xml in os.listdir(xml_path) if xml.endswith('.xml')]

    # new_dir_name = dir_name + new_name
    save_path = os.path.join(Root, save)
    os.makedirs(save_path, exist_ok=True)

    for xml in tqdm(xml_list):

        tree = parse(os.path.join(xml_path, xml))
        root = tree.getroot()

        objects = root.findall("object")
        object_list = []

        size = root.find("size")
        width = size.find("width").text
        height = size.find("height").text
        file_name = root.find("filename").text

        for _object in objects:

            name = _object.find("name")
            name = str(name.text)

            # Check '&' Character
            if '&' in name:
                concat_char = []
                for ch in name:
                    if ch == '&':
                        char = ch + "amp;"
                        concat_char.append(char)
                    else:
                        concat_char.append(ch)

                name = ''.join(concat_char)

            bndbox = _object.find("bndbox")

            xmin = float(bndbox.find("xmin").text)
            ymin = float(bndbox.find("ymin").text)
            xmax = float(bndbox.find("xmax").text)
            ymax = float(bndbox.find("ymax").text)

            object_list.append([name, xmin, ymin, xmax, ymax])

            # if '&' in name:
            #     pass
            # else:
            #     object_list.append([name, xmin, ymin, xmax, ymax])

        non_double_list = []

        for i in range(len(object_list)):

            if object_list[i] not in non_double_list:
                non_double_list.append(object_list[i])
            else:
                continue

        writer = Writer(os.path.join(xml_path, file_name), width, height)
        for list in non_double_list:
            writer.addObject(list[0], list[1], list[2], list[3], list[4])
        writer.save(os.path.join(save_path, xml))

def copy_img(dir_name, save):

    img_list = list(paths.list_images(dir_name))
    Root = os.getcwd()
    for img in tqdm(img_list):
        shutil.copy(img, os.path.join(Root, save, os.path.basename(img)))

if __name__ == '__main__':

    args, save_path = parse_args()
    dir_name = args.dir[0]
    remove_dup_char(dir_name, save_path)
    copy_img(dir_name, save_path)

    print('\nPreprocessing Completed')