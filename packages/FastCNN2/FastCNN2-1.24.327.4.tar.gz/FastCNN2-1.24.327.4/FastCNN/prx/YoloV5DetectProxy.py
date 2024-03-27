# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.

Usage - sources:
    $ python path/to/detect.py --weights yolov5s.pt --source 0              # webcam
                                                             img.jpg        # image
                                                             vid.mp4        # video
                                                             path/          # directory
                                                             path/*.jpg     # glob
                                                             'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                             'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python path/to/detect.py --weights yolov5s.pt                 # PyTorch
                                         yolov5s.torchscript        # TorchScript
                                         yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                         yolov5s.xml                # OpenVINO
                                         yolov5s.engine             # TensorRT
                                         yolov5s.mlmodel            # CoreML (macOS-only)
                                         yolov5s_saved_model        # TensorFlow SavedModel
                                         yolov5s.pb                 # TensorFlow GraphDef
                                         yolov5s.tflite             # TensorFlow Lite
                                         yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
"""

import argparse
import os
import sys

import time
import threading

import numpy as np
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from FastCNN.models.common import DetectMultiBackend
from FastCNN.utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from FastCNN.utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from FastCNN.utils.plots import Annotator, colors, save_one_box
from FastCNN.utils.torch_utils import select_device, time_sync

from FastCNN.prx.PathProxy import PathProxy3 as PathProxy
from IutyLib.commonutil.config import JConfig


@torch.no_grad()
def run(
        weights=ROOT / 'yolov5s.pt',  # model.pt path(s)
        source=ROOT / 'data/images',  # file/dir/URL/glob, 0 for webcam
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        fcnn=False
):
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    rtn = {'results':[]}
    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
    bs = 1  # batch_size
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    dt, seen = [0.0, 0.0, 0.0], 0
    for path, im, im0s, vid_cap, s in dataset:
        rtn['imgpath'] = path
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
        pred = model(im, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3
        
        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                
                for *xyxy, conf, cls in reversed(det):
                    
                    rtn['results'].append([i.item() for i in [cls,conf,*xyxy]])
        rtn["spends"] = dt[0]+dt[1]+dt[2]
                
    return rtn


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projectid', type=str, default=projectid, help='the id of project')
    parser.add_argument('--modelid', type=str, default=modelid, help='the id of model')
    
    parser.add_argument('--fcnn', action='store_false', help='not a fcnn project')
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt

def predictSingle(projectid,modelid,imgpath):
    saver = PathProxy.getValidCKPT(projectid,modelid)[:-1]
    
    return run(weights=saver,  # model.pt path(s)
        source=imgpath,  # file/dir/URL/glob, 0 for webcam
        data=None,  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        fcnn = True
    )

def main(opt):
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))

class ResourcePool:
    def __init__(self,items):
        self.cs = items
        self.lock = threading.Lock()
        pass
    
    def enPool(self,c):
        self.lock.acquire()
        self.cs.append(c)
            
        self.lock.release()
        pass
    
    def dePool(self):
        rtn = None
        self.lock.acquire()
        if len(self.cs):
            rtn = self.cs.pop(0)
            
        self.lock.release()
        return rtn
    
    def dePoolAsync(self):
        item = self.dePool()
        
        while(item == None):
            time.sleep(0.001)
            item = self.dePool()
        return item
    
    def getItems(self):
        return self.cs
    pass

class ObjValidObj:
    _model = None
    _labels = None
    _pre = None
    _projid = ""
    _modelid = ""
    _busy = False
    
    def __init__(self,projectid,modelid,model):
        self._projid = projectid
        self._modelid = modelid
        self._model = model
        
        pass

class SelectModel:
    def __init__(self):
        
        #self._model = None
        #self._pool = ResourcePool([None,None,None,None])
        self._pool = []
        pass
    
    def size(self):
        rtn = 0
        if self._model:
            rtn = sum([np.prod(list(p.size())) for p in self._model.parameters()]) *4/1000/1000
        return rtn
    
    def loadModel0(self,projectid,modelid):
        saver = PathProxy.getValidCKPT(projectid,modelid)[:-1]
        
        device = select_device("")
        #self._model = DetectMultiBackend(saver, device=device, dnn=False, data=False, fp16=False)
        p = []
        
        try:
            for item in self._pool.getItems():
                md = DetectMultiBackend(saver, device=device, dnn=False, data=False, fp16=False)
                p.append(md)
            
            self._pool = ResourcePool(p)
        except Exception as err:
            print(err)
    
    def loadModel(self,projectid,modelid,clr = True):
        saver = PathProxy.getValidCKPT(projectid,modelid)[:-1]
        imgsz=(640, 640)
        device = select_device("")
        #self._model = DetectMultiBackend(saver, device=device, dnn=False, data=False, fp16=False)
        try:
            md = DetectMultiBackend(saver, device=device, dnn=False, data=False, fp16=False)
            o = ObjValidObj(projectid,modelid,md)
            o._model.warmup(imgsz=(1 , 3, *imgsz))
            if clr:
                self._pool.clear()
            self._pool.append(o)
        except Exception as err:
            print(err)
    
    def loadModels(self,projmdls,count=5):
        self._pool.clear()
        
        for i in range(count):
            for projectid,modelid in projmdls:
                self.loadModel(projectid,modelid,False)
        
        pass
    
    def getModel(self):
        if len(self._pool) > 0:
            model = self._pool[0]
            model._busy = True
        return model
    
    def getModelByID(self,projectid,modelid):
        mdl = None
        for m in self._pool:
            if m._projid == projectid and m._modelid == modelid and (not m._busy):
                mdl = m
                mdl._busy = True
                break
        return mdl
    
    def predictByID(self,projectid,modelid,imgpath):
        mdl = self.getModelByID(projectid,modelid)
        if mdl != None:
            return self.predictSingle(imgpath,mdl)
        else:
            raise Exception("No model setted projectid:{}-modelid:{}".format(projectid,modelid))
    
    def predictSingle(self,imgpath,modelobj = None):
        device = select_device("")
        
        imgsz=(640, 640)
        conf_thres=0.25
        iou_thres=0.45
        max_det=1000
        
        classes=None  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False  # class-agnostic NMS
        augment=False  # augmented inference
        visualize=False # visualize features
        
        line_thickness=3  # bounding box thickness (pixels)
        hide_labels=False  # hide labels
        hide_conf=False  # hide confidences
        t0 = time_sync()
        
        if modelobj == None:
            modelobj = self.getModel()
        
        if not modelobj:
            return None
        model = modelobj._model
        #modelobj._busy = True
        
        stride, names, pt = model.stride, model.names, model.pt
        imgsz = check_img_size(imgsz, s=stride)  # check image size

        rtn = {'results':""}
        dataset = LoadImages(imgpath, img_size=imgsz, stride=stride, auto=pt)
        
        bs = 1  # batch_size
        vid_path, vid_writer = [None] * bs, [None] * bs
        t0 = time_sync()
        # Run inference
        #model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
        dt, seen = [0.0, 0.0, 0.0], 0
        t1 = time_sync()
        ot1 = t1-t0
        for path, im, im0s, vid_cap, s in dataset:
            
            rtn['imgpath'] = path
            t1 = time_sync()
            im = torch.from_numpy(im).to(device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
            t2 = time_sync()
            dt[0] += t2 - t1

            # Inference
            #visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)
            t3 = time_sync()
            dt[1] += t3 - t2

            # NMS
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
            dt[2] += time_sync() - t3
            
            # Second-stage classifier (optional)
            # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
                sizex,sizey = im0.shape[:2]

                p = Path(p)  # to Path
                
                
                s += '%gx%g ' % im.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                
                #annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                #print(det)
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    
                    for *xyxy, conf, cls in reversed(det):
                        
                        #xyxy[0] /= sizex
                        #xyxy[1] /= sizey
                        #xyxy[2] /= sizex
                        #xyxy[3] /= sizey
                        
                        #xyxy[2] -= xyxy[0]
                        #xyxy[3] -= xyxy[1]
                        
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                        xywh[0] -= xywh[2]/2
                        xywh[1] -= xywh[3]/2
                        for ritem in [cls,conf]:
                            if len(rtn['results']) > 0:
                                rtn['results'] += ","
                            
                            rtn['results'] += str(round(ritem.item(),2))
                        for cor in xywh:
                            if len(rtn['results']) > 0:
                                rtn['results'] += ","
                            
                            rtn['results'] += str(round(cor,2))
            print((ot1),dt[0],dt[1],dt[2])
            rtn["spend"] = round((t1-t0)+dt[0]+dt[1]+dt[2],3)
            
        modelobj._busy = False
        return rtn

_model = SelectModel()

if __name__ == "__main__":
    #opt = parse_opt()
    #main(opt)
    _model.loadModel("New_Project2","20220602_031608")
    for i in range(5):
        print(_model.predictSingle(r"D:\PSolution\yolov5\data\images\Error1_1_6312802_084623.bmp"))
    
