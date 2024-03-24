import cv2
import numpy as np
from numpy import ndarray
import math


class Contour(object):
    """轮廓查找与检测"""

    contour_info = {}  # 维护轮廓的有关信息：ID-信息（ID相同的轮廓信息会相互覆盖）

    @staticmethod
    def find(
        binary_img,
        mode=cv2.RETR_EXTERNAL,
        approx=cv2.CHAIN_APPROX_NONE,
        return_hierarchy=False,
    ):
        """
        contours：list结构，列表中每个元素代表一个边沿信息。每个元素是(x,1,2)的三维向量，x表示该条边沿里共有多少个像素点，第三维的那个“2”表示每个点的横、纵坐标；
            如果输入选择cv2.CHAIN_APPROX_SIMPLE，则contours中一个list元素所包含的x点之间应该用直线连接起来，这个可以用cv2.drawContours()函数观察一下效果。
        hierarchy：(x,4)的二维ndarray。x和contours里的x是一样的意思。
            如果输入选择cv2.RETR_TREE，则以树形结构组织输出，hierarchy的四列分别对应下一个轮廓编号、上一个轮廓编号、父轮廓编号、子轮廓编号，该值为负数表示没有对应项。
        """
        contours, hierarchy = cv2.findContours(binary_img, mode, approx)
        if return_hierarchy:
            return contours, hierarchy
        else:
            return contours

    @staticmethod
    def area(contour):
        """获得轮廓的面积"""
        return cv2.contourArea(contour)

    @staticmethod
    def arc_lenth(contour, close=True):
        """当轮应该是闭合的时候，close设为true"""
        return cv2.arcLength(contour, close)

    @classmethod
    def rect(cls, contour, mode=0, box_point=True):
        """获得轮廓的外接矩形"""
        if mode == 0:
            rect = cv2.minAreaRect(contour)
            (cx, cy), (width, height), rotation_angle = rect
        elif mode == 1:
            return
        if box_point:
            return rect, cls.box_point(rect)
        else:
            return (cx, cy), (width, height), rotation_angle

    @staticmethod
    def box_point(rect):
        """获取矩形的四个顶点坐标"""
        box = cv2.boxPoints(rect)
        box_int = np.int0(box)  # 浮点转整形，用于draw
        return box, box_int

    @classmethod
    def approximate(cls, contour, eps, cnt_lenth=None, close=True):
        """
        获得轮廓的近似:
            eps表示以轮廓周长cnt_lenth为参考的近似程度，越大相似程度越低
            cnt_lenth为None时将根据传入的轮廓自动计算
            close参数指定曲线是否是闭合的
        该函数可用于在拟合外接矩形前对轮廓进行一些处理，特别是去掉一些
        """
        if cnt_lenth is None:
            cnt_lenth = cls.arc_lenth(contour)
        epsilon = eps * cnt_lenth
        return cv2.approxPolyDP(contour, epsilon, close)

    @staticmethod
    def isContourConvex(approx):
        """判断轮廓是否凸包"""
        return cv2.isContourConvex(approx)

    @staticmethod
    def draw(frame, cnts_box: list, color=(0, 0, 255), thickness=2, index=-1):
        """
        cnt_box可以是轮廓外接矩形的四个顶点，也可以是轮廓
        单个轮廓也应该是list类型，即[cnt]
        """
        cv2.drawContours(frame, cnts_box, index, color, thickness)

    @classmethod
    def NFC_F(
        cls,
        frame_cnts,
        area_limit: tuple,
        ratio_max: float,
        mid_xy: tuple,
        mid_z: float = None,
        image_size=(640, 480),
    ):
        """
        Nearest fit contour finder
        给定面积的范围、最大的长宽比例（指轮廓的最小外接矩形）、参考中位值（用于确定最近的轮廓），从所有轮廓中选择最合适的那个。
        frame_cnts可以是图像或轮廓，若是前者，则自动使用默认参数完成图像的轮廓查找。
        """
        nearest_dis = mid_xy[0] + mid_xy[1]
        if mid_z is not None:
            mid_z_sqrt = math.sqrt(mid_z)
        nearest_cnt = None
        if isinstance(frame_cnts, ndarray):
            frame_cnts = cls.find(frame_cnts)
        if area_limit[0] + area_limit[1] < 2:  # 百分比面积
            area = image_size[0] * image_size[1]
            area_limit[0] = area * area_limit[0]
            area_limit[1] = area * area_limit[1]
        for (
            cnt
        ) in (
            frame_cnts
        ):  # 首先是轮廓面积初筛，然后是拟合矩形的面积再次筛选，然后是长宽比筛选
            cnt_Area = cls.area(cnt)  # 计算面积
            if (
                area_limit[0] < cnt_Area < area_limit[1]
            ):  # 实际的物块距离是可知的，相机又是确定的，因此，物块的面积必然在一个较小的范围内
                # print(cnt_Area,'\r\n')  # 调试打印面积信息
                # 求最小外接矩形并获取其参数
                r_rect = cls.rect(
                    cnt, mode=0, box_point=False
                )  # 获取最小外接矩形(它返回一个Box2D结构，其中包含以下细节 -(中心(x,y)，(宽度，高度)，旋转角度))
                (cx, cy), (width, height), rotation_angle = (
                    r_rect  # https://blog.csdn.net/weixin_43229348/article/details/125986969
                )
                rect_area = width * height
                # 判断矩形面积是否合理，同时边长是否符合长宽比
                if (area_limit[0] < rect_area < area_limit[1]) and (
                    1 / ratio_max < width / height < ratio_max
                ):
                    x_bias = (
                        mid_xy[0] - cx
                    )  # 偏差为正时，即cx在偏左的地方，机械臂y轴左移
                    y_bias = (
                        mid_xy[1] - cy
                    )  # 偏差为正时，即cy在偏上的地方，机械臂x轴前移
                    if mid_z is not None:
                        z_bias = math.sqrt(rect_area) - mid_z_sqrt
                    else:
                        z_bias = 0
                    new_dis = (
                        abs(x_bias) + abs(y_bias) + abs(z_bias)
                    )  # 与欧氏距离本质相同
                    # 最终筛选出最接近中心的那个方块
                    if new_dis < nearest_dis:
                        nearest_dis = new_dis
                        # 顺带记录最近的方块的信息
                        nearest_cnt = cnt
                        nearest_rect = r_rect
                        nearest_center = (cx, cy)
                        nearest_w_h = [width, height]
                        nearest_rotation = rotation_angle
                        if mid_z is not None:
                            nearest_bias = [x_bias, y_bias, z_bias]
                        else:
                            nearest_bias = [x_bias, y_bias, 0]

        # 找到最近了轮廓后获取该轮廓的详细信息
        if nearest_cnt is not None:
            nearest_w_h = sorted(nearest_w_h)  # 始终是w<h
            _, nearest_box_int = cls.box_point(
                nearest_rect
            )  # 使用cv2.boxPoints()可获取该矩形的四个顶点坐标
            # print("area:{}".format(cnt_Area))  # 打印最近轮廓的面积
            return (
                nearest_center,
                nearest_bias,
                nearest_rotation,
                nearest_box_int,
                nearest_w_h,
                nearest_cnt,
            )
        return None, None, None, None, None, None

    # 获得轮廓信息
    @classmethod
    def get_info(cls, contour, infomode):
        """
        contour可以是id（int型,前提是保证已经存储了有关信息，若没有则将报错）或轮廓本身。
        infomode可以选择为：less:;'base':;'norm':;more;most;
        """
        if isinstance(contour, int):
            pass
