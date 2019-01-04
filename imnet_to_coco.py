import os
import json
from xml.etree import ElementTree as ET
from coco_utils import CocoUtils

# define annotation root dir
annotation_root_dir = '/usr1/schakra1/datasets/IMAGENET_VID/Annotations/train'
jpg_dir = '/usr1/schakra1/packages/Detectron.pytorch/data/imnet_vid/images/train'
output_path = '/usr1/schakra1/packages/Detectron.pytorch/data/imnet_vid/annotations/train.json'


def _get_class_id_from_code(code):
    codes = ['__background__',  # always index 0
               'n02691156', 'n02419796', 'n02131653', 'n02834778',
               'n01503061', 'n02924116', 'n02958343', 'n02402425',
               'n02084071', 'n02121808', 'n02503517', 'n02118333',
               'n02510455', 'n02342885', 'n02374451', 'n02129165',
               'n01674464', 'n02484322', 'n03790512', 'n02324045',
               'n02509815', 'n02411705', 'n01726692', 'n02355227',
               'n02129604', 'n04468005', 'n01662784', 'n04530566',
               'n02062744', 'n02391049']
    for i, cls_code in enumerate(codes):
        if code == cls_code:
            return i


def _read_xml(xml):
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
    else:
        prefix = 'val_'
    image_name = prefix + sub_root + '_' + vid + '_'
    image_name += xml.split('.')[0]+'.jpg'
    return image_name


# define custom load annotation function
def load_annotations():
    annotations = {}
    annotation_subroots = sorted(os.listdir(annotation_root_dir))
    for annotation_subroot in annotation_subroots:
        print;
        annotation_subroot_dir = os.path.join(annotation_root_dir, annotation_subroot)
        vids = sorted(os.listdir(annotation_subroot_dir))
        for i, vid in enumerate(vids):
            print '\033[F{0} | done: {1:.2f}%'.format(annotation_subroot, (i+1)*100./len(vids))
            vid_dir = os.path.join(annotation_subroot_dir, vid)
            xmls = sorted(os.listdir(vid_dir))
            for xml in xmls:
                xmlpath = os.path.join(vid_dir, xml)
                data = _read_xml(xmlpath)
                annotations[_get_image_name(annotation_subroot, vid, xml)] = data
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
    for i in range(len(classes)):
        id_map[i] = classes[i]
    return id_map

annotations = load_annotations()
#with open('annotations.json') as fp:
#    annotations = json.load(fp)

import pdb; pdb.set_trace();    
id_map = get_id_map()
ccutils = CocoUtils(jpg_dir, annotations, id_map)
coco_annotations = ccutils.get_coco_annotations()

import pdb; pdb.set_trace();
with open(output_path, 'w') as fp:
    json.dump(coco_annotations, fp)
