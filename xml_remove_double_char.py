import os
from xml.etree.ElementTree import parse
from pascal_voc_writer import Writer

Root = os.getcwd()
xml_path = (os.path.join(Root, 'U'))
xml_list = [xml for xml in os.listdir(xml_path) if xml.endswith('.xml')]
os.makedirs(os.path.join(Root, 'U_'), exist_ok=True)

for xml in xml_list:

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

        bndbox = _object.find("bndbox")

        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)

        object_list.append([name, xmin, ymin, xmax, ymax])

    non_double_name = []
    non_double_list = []

    for i in range(len(object_list)):

        if object_list[i][0] not in non_double_name:
            non_double_name.append(object_list[i][0])
            non_double_list.append(object_list[i])
        else:
            continue

    writer = Writer(os.path.join(xml_path, file_name), width, height)
    for list in non_double_list:
        # 라벨이 여러개 있을 수 있으니 리스트로 돌아가면서 추가해준다.
        writer.addObject(list[0], list[1], list[2], list[3], list[4])
    writer.save(os.path.join(Root, 'U_', xml))
