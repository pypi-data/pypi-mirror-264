import cv2
import numpy as np
from numpy import ndarray


class Morphology(object):
    """图像形态学：腐蚀、膨胀、开运算、闭运算"""

    def kernel(size, shape=cv2.MORPH_RECT):
        """获得各种形状的核：cv2.MORPH_RECT（矩形）、cv2.MORPH_CROSS（十字形）、cv2.MORPH_ELLIPSE（(椭)圆形）"""
        return cv2.getStructuringElement(shape, size)

    def erode(frame: ndarray, kernel=(3, 3), iterations=1):
        """腐蚀（侵蚀）"""
        if isinstance(kernel, tuple):
            kernel = np.ones(kernel, np.uint8)
        return cv2.erode(frame, kernel, iterations=iterations)

    def dilate(frame: ndarray, kernel=(3, 3), iterations=1):
        """膨胀（扩张）"""
        if isinstance(kernel, tuple):
            kernel = np.ones(kernel, np.uint8)
        return cv2.dilate(frame, kernel, iterations=iterations)

    def open(frame, kernel=(3, 3)):
        """
        一个白色封闭圆环，open先腐蚀后膨胀，从而，这个圆环中薄弱的地方被切断，实现了“open”
        它对于消除噪音很有用
        """
        if isinstance(kernel, tuple):
            kernel = np.ones(kernel, np.uint8)
        return cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

    def close(frame, kernel=(3, 3)):
        """
        一个白色断裂圆环，close先膨胀后腐蚀，从而，这个圆环中切断的地方被连接，实现了“close”
        在关闭前景对象内部的小孔或对象上的小黑点时很有用
        """
        if isinstance(kernel, tuple):
            kernel = np.ones(kernel, np.uint8)
        return cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

    def gradient(frame, kernel=(3, 3)):
        """
        结果看起来像是图像的轮廓
        """
        if isinstance(kernel, tuple):
            kernel = np.ones(kernel, np.uint8)
        return cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)

    def top_hat(frame, kernel=(3, 3)):
        """
        输入图像和图像开运算之差。可以得到只有图像中的噪声的图像。仿佛是将噪声的帽子顶了出来。
        """
        if isinstance(kernel, tuple):
            kernel = np.ones(kernel, np.uint8)
        return cv2.morphologyEx(frame, cv2.MORPH_TOPHAT, kernel)

    def black_hat(frame, kernel=(3, 3)):
        """
        输入图像和图像闭运算之差。可以得到只有图像中的空洞（此时变成白色）的图像。仿佛是给黑洞带个帽子。
        """
        if isinstance(kernel, tuple):
            kernel = np.ones(kernel, np.uint8)
        return cv2.morphologyEx(frame, cv2.MORPH_BLACKHAT, kernel)
