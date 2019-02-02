import json
import cv2
import argparse
import random
import os

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--json', type=str, help='name of json file')
    argparser.add_argument('--img_dir', type=str, help='img dir')
    argparser.add_argument('--out_dir', type=str, help='out dir')
    argparser.add_argument('--n_imgs', type=int, help='no. of imgs to be visualised')
    return argparser.parse_args()


def save_imgs(args):
    with open(args.json) as f:
        d = json.load(f)
    n_ann = len(d['annotations'])
    rand_inds = [random.randrange(0, n_ann) for i in range(args.n_imgs)]
    anns = [d['annotations'][i] for i in rand_inds]
    for ann in anns:
        image_id = int(ann['image_id'])
        assert d['images'][image_id]['id'] == image_id
        img_name = d['images'][image_id]['file_name']
        img_path = os.path.join(args.img_dir, img_name)
        img = cv2.imread(img_path)
        bbox = ann['bbox']
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
        out_path = os.path.join(args.out_dir, img_name)
        cv2.imwrite(out_path, img)

if __name__=='__main__':
    args = parse_args()
    save_imgs(args)
