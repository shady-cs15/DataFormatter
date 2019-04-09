import os
import json
import argparse
import constants
from xml.etree import ElementTree as ET
from coco_utils import CocoUtils
import cv2


annotation_root_dir = constants.adl_annotation_root_dir
jpg_dir = constants.adl_jpg_dir
output_path = constants.adl_output_path
vid_root_dir = constants.adl_vid_dir

def _get_class_id_from_name(name):
    name_map = { 'cell': 'cell_phone',
                 'large_container': 'container',
                 'shoe': 'shoes',
                 'blanket': 'towel',
                 'elec_keys': 'electric_keys', }

    names = ['__background__', 'basket', 'bed', 'towel', 'book', 'bottle',
             'cell_phone', 'cloth', 'comb', 'container', 'dent_floss', 'detergent',
             'dish', 'door', 'electric_keys', 'food/snack', 'fridge', 'kettle',
             'keyboard', 'knife/spoon/fork', 'laptop', 'microwave', 'milk/juice', 
             'monitor', 'mop', 'mug/cup', 'oven/stove', 'pan', 'perfume', 'person',
             'pills', 'pitcher', 'shoes', 'soap_liquid', 'tap', 'tea_bag', 'thermostat',
             'tooth_brush', 'tooth_paste', 'trash_can', 'tv', 'tv_remote', 'vacuum', 
             'washer/dryer']
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
            cls_id = _get_class_id_from_name(data[7])
            box = data[1: 5]
            for i in range(4): 
                box[i] = int(box[i])
            #convert to x, y, w, h form
            assert box[2]>box[0] and box[3] > box[1]
            box[2] = box[2] - box[0]
            box[3] = box[3] - box[1]
            if f_id not in anns:
                anns[f_id] = [[cls_id, box, height, width]]
            else:
                anns[f_id].append([cls_id, box, height, width])
    return anns

def _get_fname(vid, fid):
    fname = str(fid)
    fname = '0'*(6-len(fname)) + fname + '.jpg'
    return vid+'_'+fname

def load_annotations():
    annotations = {}
    for i in range(1, 21):
        vid_id = 'P_'+'0'*(2-len(str(i)))+str(i)
        vid_path = os.path.join(vid_root_dir, vid_id+'.MP4')
        ann_path = os.path.join(annotation_root_dir, 'object_annot_'+vid_id+'.txt')
        cap = cv2.VideoCapture(vid_path)
        ret, frame = cap.read()
        h, w, _ = frame.shape
        vid_ann = _read_ann_file(ann_path, h/2, w/2)
        for f_id in vid_ann:
            annotations[_get_fname(vid_id, f_id)] = vid_ann[f_id] 
    return annotations

# custom get id map function
def get_id_map():
    classes = ['__background__', 'basket', 'bed', 'towel', 'book', 'bottle',
             'cell_phone', 'cloth', 'comb', 'container', 'dent_floss', 'detergent',
             'dish', 'door', 'electric_keys', 'food/snack', 'fridge', 'kettle',
             'keyboard', 'knife/spoon/fork', 'laptop', 'microwave', 'milk/juice', 
             'monitor', 'mop', 'mug/cup', 'oven/stove', 'pan', 'perfume', 'person',
             'pills', 'pitcher', 'shoes', 'soap_liquid', 'tap', 'tea_bag', 'thermostat',
             'tooth_brush', 'tooth_paste', 'trash_can', 'tv', 'tv_remote', 'vacuum', 
             'washer/dryer']
    id_map = {}
    for i in range(1, len(classes)): #ignore background
        id_map[i] = classes[i]
    return id_map


def main():

    annotations = load_annotations()
    id_map = get_id_map()

    ccutils = CocoUtils(jpg_dir, annotations, id_map)
    coco_annotations = ccutils.get_coco_annotations()

    with open(output_path, 'w') as fp:
        json.dump(coco_annotations, fp)


if __name__ == '__main__':
    main()
