import cv2
import os

class CocoUtils(object):
    def __init__(self, jpg_dir, annotations, id_map):
        self.jpg_dir = jpg_dir
        self.annotations = annotations
        self.id_map = id_map
        self.out_annotations = []
        self.out_imageinfo = []
        self.out_classes = []


    def _load_annotations(self):
        jpgs = sorted(os.listdir(self.jpg_dir))
        bbox_id = 0; print;
        for image_id, jpg in enumerate(jpgs):
            image_name = jpg
            print '\033[Fdone: {0:.2f} %'.format((image_id+1)*100./len(jpgs))
            
            cur_imageinfo = {'license': None, 'coco_url': None,\
                                'flickr_url': None, 'date_captured': None}
            cur_imageinfo['file_name'] = jpg
            cur_imageinfo['id'] = int(image_id)
            self.out_imageinfo.append(cur_imageinfo)
            
            # if annotation file doesn't exist for a given image
            if image_name not in self.annotations:
                self.annotations[image_name] = {}

            # if file exists but no bounding box
            if len(self.annotations[image_name]) == 0:
                cur_annotation = {'segmentation': None, 'iscrowd': 0}
                cur_annotation['image_id'] = int(image_id)
                cur_annotation['area'] = 0
                cur_annotation['bbox'] = []
                cur_annotation['category_id'] = -1
                cur_annotation['id'] = -1
                self.out_annotations.append(cur_annotation)
                
            for cls_id, box, imh, imw in self.annotations[image_name]:
                x, y, w, h = box
                box = [float(x), float(y), float(w), float(h)]
                if 'height' not in cur_imageinfo:
                    cur_imageinfo['height'] = imh
                if 'width' not in cur_imageinfo:
                    cur_imageinfo['width'] = imw
                cur_annotation = {'segmentation': None, 'iscrowd': 0}
                cur_annotation['image_id'] = int(image_id)
                cur_annotation['area'] = float(h*w)
                cur_annotation['bbox'] = box
                cur_annotation['category_id'] = int(cls_id)
                cur_annotation['id'] = int(bbox_id)
                self.out_annotations.append(cur_annotation)
                bbox_id +=1
        
    
    def _load_categories(self):
        out_classes = []

        for cls_id in self.id_map:
            cur_cls = {}
            cur_cls['id'] = int(cls_id)
            cur_cls['name'] = self.id_map[cls_id]
            cur_cls['supercategory'] = self.id_map[cls_id]
            out_classes.append(cur_cls)

        self.out_classes = out_classes


    def get_coco_annotations(self):
        self._load_annotations()
        self._load_categories()
        out = {}
        out['info'] = {}
        out['licenses'] = []
        out['images'] = self.out_imageinfo
        out['annotations'] = self.out_annotations
        out['categories'] = self.out_classes
        return out
