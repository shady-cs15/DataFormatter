import os
import json
import argparse
import constants
from xml.etree import ElementTree as ET
from coco_utils import CocoUtils

'sket', 1588)
('bed', 783)
('blanket', 85)
('book', 4770)
('bottle', 10310)
('cell', 571)
('cell_phone', 653)
('cloth', 3077)
('comb', 307)
('container', 5685)
('dent_floss', 547)
('detergent', 1105)
('dish', 8216)
('door', 7903)
('elec_keys', 118)
('electric_keys', 1570)
('food/snack', 3836)
('fridge', 1999)
('kettle', 1239)
('keyboard', 107)
('knife/spoon/fork', 4843)
('laptop', 7027)
('large_container', 558)
('microwave', 2369)
('milk/juice', 366)
('monitor', 316)
('mop', 403)
('mug/cup', 11050)
('oven/stove', 3196)
('pan', 3156)
('perfume', 550)
('person', 4651)
('pills', 394)
('pitcher', 1208)
('shoe', 694)
('shoes', 3248)
('soap_liquid', 8375)
('tap', 7826)
('tea_bag', 359)
('thermostat', 332)
('tooth_brush', 1795)
('tooth_paste', 1746)
('towel', 4480)
('trash_can', 2075)
('tv', 5600)
('tv_remote', 2813)
('vacuum', 519)
('washer/dryer', 3362)'''

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--set', dest='set', default='train', type=str, help='train or val')
    args = parser.parse_args()
    return args
'''

annotation_root_dir = constants.annotation_root_dir
jpg_dir = constants.jpg_dir
output_path = constants.output_path


def _get_class_id_from_name(name):
    name_map = { 'cell': 'cell_phone',
                 'large_container': 'container',
                 'shoe': 'shoes',
                 'blanket':, 'towel',
                 'elec_keys': 'electric_keys', }

    names = ['__background__', 'basket', 'bed', 'towel', 'book', 'bottle',
             'cell_phone', 'cloth', 'comb', 'container', 'dent_floss', 'detergent',
             'dish', 'door', 'electric_keys', 'food/snack', 'fridge', 'kettle',
             'keyboard', 'knife/spoon/fork', 'laptop', 'microwave', 'milk/juice', 
             'monitor', 'mop', 'mug/cup', 'oven/stove', 'pan', 'perfume', 'person',
             'pills', 'pitcher', 'shoes', 'soap_liquid', 'tap', 'tea_bag', 'thermostat',
             'tooth_brush', 'tooth_paste', 'trash_can', 'tv', 'tv_remote', 'vacuum', 
             'washer/dryer']
    
    print(len(names))
    if name in name_map:
        name = name_map[name]
    assert name in names
    for i, cls_name in enumerate(names):
        if name == cls_name:
            return i


def _read_ann_file(ann_file, height, width):
    anns = {}
    with open(ann_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.split()
            assert len(data)==8
            f_id = int(data[5])
            if f_id not in anns:
                anns[f_id] = [data[7], data[1: 5], height, width]
            else:
                anns[f_id].append[data[7], data[1: 5], height, width]
    return anns


def load_annotations():
    annotations = {}
    for i in range(1, 21):
        vid_id = 'P_'+'0'*(2-len(str(i)))+str(i)
        vid_path = os.path.join(vid_root_dir, vid_id+'.MP4')
        ann_path = os.path.join(annotation_root_dir, 'object_annot_'+vid_id+'.txt')
        cap = cv2.VideoCapture(vid_path)
        ret, frame = cap.read()
        print frame.shape
        _, h, w = frame.shape
        vid_ann = _read_ann_file(ann_path, h, w)
        import pdb; pdb.set_trace();


def floating_fn():
    xmltree = ET.parse(xml)
    size = xmltree.find('size')
    height = int(size.find('height').text)
    width = int(size.find('width').text)
    objects = xmltree.findall('object')
    data = []
    for obj in objects:
        cls_code = obj.find('name').text
        cls_id = _get_class_id_from_code(cls_code)
        bndbox = obj.find('bndbox')
        xmin = float(bndbox.find('xmin').text)
        xmax = float(bndbox.find('xmax').text)
        ymin = float(bndbox.find('ymin').text)
        ymax = float(bndbox.find('ymax').text)
        x = xmin; y = ymin;
        w = xmax - xmin; h = ymax - ymin;
        box = [x, y, w, h]
        data.append([cls_id, box, height, width])
    return data


def _get_image_name(sub_root, vid, xml, train=True):
    if train:
        prefix = 'train_'
        image_name = prefix + sub_root + '_' + vid + '_'
    else:
        prefix = 'val_'
        image_name = prefix + vid + '_'
    image_name += xml.split('.')[0]+'.jpg'
    return image_name


# define custom load annotation function
def load_train_annotations():
    annotations = {}
    annotation_subroots = sorted(os.listdir(annotation_root_dir))
    for annotation_subroot in annotation_subroots:
        print;
        annotation_subroot_dir = os.path.join(annotation_root_dir, annotation_subroot)
        vids = sorted(os.listdir(annotation_subroot_dir))
        for i, vid in enumerate(vids):
            #print '\033[F{0} | done: {1:.2f}%'.format(annotation_subroot, (i+1)*100./len(vids))
            vid_dir = os.path.join(annotation_subroot_dir, vid)
            xmls = sorted(os.listdir(vid_dir))
            for xml in xmls:
                xmlpath = os.path.join(vid_dir, xml)
                data = _read_xml(xmlpath)
                annotations[_get_image_name(annotation_subroot, vid, xml)] = data
    return annotations


def load_val_annotations():
    annotations = {}
    annotation_subroot = annotation_root_dir
    annotation_subroot_dir = os.path.join(annotation_root_dir, annotation_subroot)
    vids = sorted(os.listdir(annotation_subroot_dir))
    print;
    for i, vid in enumerate(vids):
        print '\033[F{0} | done: {1:.2f}%'.format(annotation_subroot, (i+1)*100./len(vids))
        vid_dir = os.path.join(annotation_subroot_dir, vid)
        xmls = sorted(os.listdir(vid_dir))
        for xml in xmls:
            xmlpath = os.path.join(vid_dir, xml)
            data = _read_xml(xmlpath)
            annotations[_get_image_name(None, vid, xml, False)] = data
    return annotations


# custom get id map function
def get_id_map():
    classes = ['__background__',  # always index 0
           'airplane', 'antelope', 'bear', 'bicycle',
           'bird', 'bus', 'car', 'cattle',
           'dog', 'domestic_cat', 'elephant', 'fox',
           'giant_panda', 'hamster', 'horse', 'lion',
           'lizard', 'monkey', 'motorcycle', 'rabbit',
           'red_panda', 'sheep', 'snake', 'squirrel',
           'tiger', 'train', 'turtle', 'watercraft',
           'whale', 'zebra']
    id_map = {}
    for i in range(1, len(classes)): #ignore background
        id_map[i] = classes[i]
    return id_map


def main():

    load_annotations()
    
    
    id_map = get_id_map()
    ccutils = CocoUtils(jpg_dir, annotations, id_map)
    coco_annotations = ccutils.get_coco_annotations()

    with open(output_path, 'w') as fp:
        json.dump(coco_annotations, fp)


if __name__ == '__main__':
    main()
