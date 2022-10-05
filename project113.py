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
    '''
    Give the vertices of tactile_paving clockwise, then draw it on the output image.
    '''
    if tactile_paving:
        start=0
        while start < len(tactile_paving)-1:
            cv2.line(im0, tactile_paving[start], tactile_paving[start+1], (255, 0, 0), 2)
            start+=1
        cv2.line(im0, tactile_paving[start], tactile_paving[0], (255, 0, 0), 2)
        
def draw_alert_zone(im0, alert_zone):
    '''
    Give the vertices of alert_zone clockwise, then draw it on the output image.
    '''
    if alert_zone:
        start=0
        while start < len(alert_zone)-1:
            cv2.line(im0, alert_zone[start], alert_zone[start+1], (0, 0, 255), 2)
            start+=1
        cv2.line(im0, alert_zone[start], alert_zone[0], (0, 0, 255), 2)

def get_target_id(target_id, outputs, alert_zone):
    '''
    Function of the method we determine the target id.
    We choose a random person in the alert_zone as the target at first.
    If the person is still in the alert_zone in following frames, the target_id keep the same.
    If the person isn't in the alert_zone for a frame, the target change to another random person.

    If there is no person in alert_zone, target_id will be None.
    '''
    ids = [output[4] for output in outputs[0]]
    if target_id in ids:
        bbox = outputs[0][ids.index(target_id)][0:4]
        representational_point = ((bbox[0] + (bbox[2] - bbox[0]) / 2), bbox[3])
        if is_in_poly(representational_point, alert_zone):
            return target_id
    else:
        for output in outputs[0]:
            if output[5] == 0: #only person can be the target
                bbox = output[0:4]
                representational_point = ((bbox[0] + (bbox[2] - bbox[0]) / 2), bbox[3])
                if is_in_poly(representational_point, alert_zone):
                    return output[4]
    return None