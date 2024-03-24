import cv2
from numpy import ndarray
from typing import Optional


class Geometry(object):
    """
    OpenCV提供了两个转换函数**cv.warpAffine**和**cv.warpPerspective**，使用它们进行各种转换。
        **cv.warpAffine**采用2x3转换矩阵，而**cv.warpPerspective**采用3x3转换矩阵。
    该类目前仅实现了常用的放缩和旋转操作，而其它诸如平移、仿射、透视变换则没有。
    """

    @staticmethod
    def Resize(
        frame: ndarray, new_shape: Optional[tuple], fx=None, fy=None, precise=False
    ):
        """
        缩小首选的插值方法是：cv.INTER_AREA;放大的方法有：cv.INTER_CUBIC（慢）和cv.INTER_LINEAR。
        为此，该函数进行了一些判断，以选择较好的方式，并提供precise参数来选择在放大时是否使用较慢但更细致的方法。
        将new_shape设为none后，fx和fy将生效，可以按倍数调整。
        """
        if new_shape is None:
            new_shape = (frame.shape[0] * fx, frame.shape[1] * fy)
        if new_shape[0] > frame.shape[0] or new_shape[1] > frame.shape[1]:
            if precise:
                interpolation = cv2.INTER_CUBIC
            else:
                interpolation = cv2.INTER_LINEAR
        else:
            interpolation = cv2.INTER_AREA

        res = cv2.resize(frame.copy(), new_shape, interpolation=interpolation)
        return res

    @staticmethod
    def Rotation(frame: ndarray, angle, center=None, scale=1):
        """center为none默认图像中心为旋转中心（旋转是逆时针的）；scale为旋转后图像的放缩倍数"""
        rows_cols = frame.shape
        if center is None:
            center = ((rows_cols[1] - 1) / 2.0, (rows_cols[0] - 1) / 2.0)
        M = cv2.getRotationMatrix2D(
            center, angle, scale
        )  # 得到变换矩阵：cols-1 和 rows-1 是坐标限制
        dst = cv2.warpAffine(frame, M, (rows_cols[1], rows_cols[0]))
        return dst
