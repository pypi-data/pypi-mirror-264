import cv2
from numpy import ndarray
from typing import List, Union


class Math(object):
    """图像的各种算数、位运算"""

    @staticmethod
    def plus(
        imgs: List[Union[ndarray, float]], weights: Union[None, list, tuple] = None
    ):
        """饱和相加，imgs最后元素允许为标量，标量不给予权重"""
        if isinstance(imgs[-1], (int, float)):
            scalar = imgs.pop(-1)
        else:
            scalar = 0
        if weights is None:
            weights = [1 for _ in range(len(imgs))]
        img_p = cv2.addWeighted(
            imgs.pop(0), weights[0], imgs.pop(0), weights[1], scalar
        )
        for img in imgs:
            img_p = cv2.addWeighted(img_p, 1, img, weights[2], 0)
        return img_p

    @classmethod
    def bitwise(*args):
        """
        这包括按位AND OR XOR NOT操作。它们在提取图像的任何部分、定义和处理非矩形ROI等方面非常有用。
        参数按输入示例(执行顺序始终从左至右)：
            带not：bitwise('not',img1,'and','not',img2,'or',img3,'xor',img4)
            无not：bitwise(img1,'and',img2,'or',img3,'xor',img4)
        该函数虽然方便，但是却较大地影响了处理速度，择需使用。
        """

        def __bitwise_X(a, operator, b=None):
            if operator == "and":
                a = cv2.bitwise_and(
                    a, b
                )  # 注意区别cv2.bitwise_and(a,a,mask=b)的写法，在提取特定区域时，不直接写成cv2.bitwise_and(a,mask)，其意义？
            elif operator == "or":
                a = cv2.bitwise_or(a, b)
            elif operator == "xor":
                a = cv2.bitwise_xor(a, b)
            elif operator == "not":
                a = cv2.bitwise_not(a)
            else:
                exit("算符错误")
            return a

        args = list(args)
        # 先对需要求反的图像进行求反
        while "not" in args:
            next = args.index("not") + 1
            args[next] = cv2.bitwise_not(args[next])
            args.pop(next - 1)
        # 然后执行AND OR XOR操作
        i = 0
        len_ = len(args) - 1
        while i < len_:
            args[i + 2] = __bitwise_X(args[i], args[i + 1], args[i + 2])
            i += 2
        return args[-1]  # 最后一个元素保存着最后位运算完的结果
