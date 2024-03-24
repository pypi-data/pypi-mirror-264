import cv2
import numpy as np
from numpy import ndarray


class Threshold(object):
    """用于图像二值化"""

    @staticmethod
    def color_range(
        frame: ndarray, ColorL: list, ColorH: list, convert=cv2.COLOR_BGR2HSV
    ):
        """根据颜色空间范围选择合适的颜色阈值对彩色图像（默认为BGR格式）进行处理"""
        frame_cp = frame.copy()
        cvt = cv2.cvtColor(frame_cp, convert)
        lower_thresh = np.array(ColorL)
        upper_thresh = np.array(ColorH)
        mask = cv2.inRange(cvt, lower_thresh, upper_thresh)
        res = cv2.bitwise_and(frame_cp, frame_cp, mask=mask)
        return res, mask

    @staticmethod
    def gray_global(
        frame,
        threshold_value,
        threshold_max,
        mode=cv2.THRESH_BINARY,
        convert_color=True,
        return_thresh=False,
    ):
        """灰度图像全局二值化"""
        if convert_color:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh, new_img = cv2.threshold(frame, threshold_value, threshold_max, mode)
        if return_thresh:
            return thresh, new_img
        else:
            return new_img

    @staticmethod
    def gray_adaptive(
        frame,
        maxValue,
        method=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=3,
        C=0,
        convert_color=True,
    ):
        """
        src：需要进行二值化的一张灰度图像
        maxValue：满足条件的像素点需要设置的灰度值（将要设置的灰度值）
        method：自适应阈值算法。可选ADAPTIVE_THRESH_MEAN_C 或 ADAPTIVE_THRESH_GAUSSIAN_C
        thresholdType：opencv提供的二值化方法，只能THRESH_BINARY或者THRESH_BINARY_INV
        blockSize：要分成的区域大小，上面的N值，一般取奇数
        C：常数，每个区域计算出的阈值的基础上在减去这个常数作为这个区域的最终阈值，可以为负数
        """
        if convert_color:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(
            frame, maxValue, method, thresholdType, blockSize, C
        )

    @staticmethod
    def gray_otsu(
        frame,
        threshold_value,
        threshold_max,
        mode=cv2.THRESH_BINARY,
        convert_color=True,
        return_thresh=False,
    ):
        """大津法自适应阈值（参数与灰度全局二值化相同）"""
        if convert_color:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh, new_img = cv2.threshold(
            frame, threshold_value, threshold_max, mode + cv2.THRESH_OTSU
        )
        if return_thresh:
            return thresh, new_img
        else:
            return new_img
