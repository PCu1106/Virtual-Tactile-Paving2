from yolov5.utils.general import cv2
import numpy as np

def is_in_poly(p, poly): #https://www.796t.com/article.php?id=190303
    """

    :param p: [x, y]
    :param poly: [[], [], [], [], ...]
    :return:
    """
    px, py = p
    flag = False
    i = 0
    length = len(poly)
    j = length - 1
    while i < length:
        x1, y1 = poly[i]
        x2, y2 = poly[j]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):
            flag = True
            break
        if y1 < py <= y2 or y2 < py <= y1:
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:
                flag = True
                break
            elif x > px:
                # convert the flag
                flag = not flag
        j = i
        i += 1

    return flag

def draw_tactile_paving(im0, tactile_paving):
    if tactile_paving:
        start=0
        while start < len(tactile_paving)-1:
            cv2.line(im0, tactile_paving[start], tactile_paving[start+1], (255, 0, 0), 2)
            start+=1
        cv2.line(im0, tactile_paving[start], tactile_paving[0], (255, 0, 0), 2)
        
def draw_alert_zone(im0, alert_zone):
    if alert_zone:
        start=0
        while start < len(alert_zone)-1:
            cv2.line(im0, alert_zone[start], alert_zone[start+1], (0, 0, 255), 2)
            start+=1
        cv2.line(im0, alert_zone[start], alert_zone[0], (0, 0, 255), 2)

def get_target_id(target_id, outputs, alert_zone):
    ids = [output[4] for output in outputs[0]]
    if target_id in ids:
        bbox = outputs[0][ids.index(target_id)][0:4]
        representational_point = ((bbox[0] + (bbox[2] - bbox[0]) / 2), bbox[3])
        if is_in_poly(representational_point, alert_zone):
            return target_id
    else:
        for output in outputs[0]:
            bbox = output[0:4]
            representational_point = ((bbox[0] + (bbox[2] - bbox[0]) / 2), bbox[3])
            if is_in_poly(representational_point, alert_zone):
                return output[4]
    return None