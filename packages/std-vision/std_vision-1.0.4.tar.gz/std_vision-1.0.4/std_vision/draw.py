import cv2
from .video import StdVideo
from .contour import Contour


class Draw(object):
    """
    绘制各种图像：几种基本图形内容、准星、鼠标绘图等
    注意：默认所绘制内容直接覆盖原图(带有cover参数的可以通过设置为false不破坏原图，没有的请自行先copy)
    """

    @staticmethod
    def basic_draw(
        frame,
        pos1_c,
        pos2_r=(None,),
        color=(0, 0, 0),
        thickness=1,
        line_type=cv2.LINE_8,
        elipse_angles=(0, 0, 0),
        font=cv2.FONT_HERSHEY_PLAIN,
        shape_convert=False,
        close=True,
        cover=True,
        tips="",
    ):
        """
        根据传入的参数特点，自动确定绘制何种内容（直线和矩形的区分部分是靠shape_convert为false或true）
        支持绘制的内容有：圆和椭圆、文本、多段直线和多边形、单段直线和矩形
        """
        if not cover:
            frame = frame.copy()
        if (
            not isinstance(pos2_r, tuple) or shape_convert == "circle"
        ):  # 例：cv2.circle(src, (250, 250), 150, (0, 0, 255), 4, cv2.LINE_8, 0)  # 圆
            cv2.circle(frame, pos1_c, pos2_r, color, thickness, line_type, 0)  # 圆
        elif (
            elipse_angles != (0, 0, 0) or shape_convert == "elipse"
        ):  # 例：cv2.ellipse(src, (250, 250), (150, 50), 360, 0, 360, (255, 234, 0), 3, cv2.LINE_8, 0)  # 椭圆
            cv2.ellipse(
                frame, pos1_c, pos2_r, *elipse_angles, color, thickness, line_type, 0
            )  # 椭圆
        elif isinstance(pos1_c, str):
            cv2.putText(
                frame, pos1_c, pos2_r, font, thickness, color, 2, cv2.LINE_8
            )  # 文字
        elif len(pos1_c[0]) > 1:  # 绘制(多段)直线
            len_ = len(pos1_c)
            if len_ == 2:  # 绘制一条直线
                cv2.line(
                    frame, pos1_c[0], pos1_c[1], color, thickness, line_type, 0
                )  # 直线
            else:
                for index, point in enumerate(pos1_c):
                    cv2.line(
                        frame,
                        point,
                        pos1_c[(index + 1) % len_],
                        color,
                        thickness,
                        line_type,
                        0,
                    )
                    if not close and index == len_ - 2:
                        break  # 不封闭直接退出
        elif (
            shape_convert
        ):  # 例：cv2.line(src, (10, 10), (400, 400), (255, 0, 0), 1, cv2.LINE_8, 0)
            cv2.line(frame, pos1_c, pos2_r, color, thickness, line_type, 0)  # 直线
        else:
            cv2.rectangle(
                frame, pos1_c, pos2_r, color, thickness, line_type, 0
            )  # 正方形
        if not cover:
            return frame

    @staticmethod
    def front_sight(frame, x, y, corlors=((0, 0, 255), (0, 0, 255)), corver=True):
        """绘制瞄准准星"""
        x, y = int(x), int(y)
        start, end = 10, 40
        if not corver:
            frame = frame.copy()
        frame = cv2.circle(frame, (x, y), 17, corlors[0], 2)
        frame = cv2.line(
            frame, (x, y + start), (x, y + end), corlors[1], 2, cv2.LINE_8, 0
        )
        frame = cv2.line(
            frame, (x + start, y), (x + end, y), corlors[1], 2, cv2.LINE_8, 0
        )
        frame = cv2.line(
            frame, (x, y - start), (x, y - end), corlors[1], 2, cv2.LINE_8, 0
        )
        frame = cv2.line(
            frame, (x - start, y), (x - end, y), corlors[1], 2, cv2.LINE_8, 0
        )
        if not corver:
            return frame

    @staticmethod
    def border():  # TODO
        """为图像添加边框"""
        pass

    @classmethod
    def mouse_draw(cls, window_name=None, frame=None, color=(0, 0, 0), thickness=2):
        """
        鼠标在给定的窗口上绘图。显然window_name和frame之间具有一定的关联性，但是frame是每帧不断变化的，因此这种关联是不固定的。
        为此需要每次进行更新，这是通过bind_to的绑定属性来实现联系的。
        实际上，对一幅图进行描绘的时候图片应该是固定的，或者说变化的频率是不快的，否则上一幅图片还没绘制好就刷新了要重画。
        只不过，考虑到有时候我们需要在对图片进行标记的时候需要一幅一幅地连续处理，因此这样的操作还是有用的。
        """

        def bind_to(window_name, frame):
            """所有的绑定函数都有相同的参数：第一个是窗口名，第二个是frame"""
            if not hasattr(bind_to, window_name):  # 同一个窗口仅执行一次回调函数设置
                drawing = False
                bind_to.__dict__[window_name] = frame
                if (
                    window_name not in StdVideo.windows_set
                ):  # 为保证setMouseCallback不出错，先创建一个空窗口
                    cv2.namedWindow(window_name)

                def call_back(event, x, y, flags, param):
                    nonlocal drawing
                    if event == cv2.EVENT_LBUTTONDOWN:
                        drawing = True
                        cv2.circle(
                            bind_to.__dict__[window_name], (x, y), thickness, color, -1
                        )
                    elif event == cv2.EVENT_MOUSEMOVE:
                        if drawing == True:
                            cv2.circle(
                                bind_to.__dict__[window_name],
                                (x, y),
                                thickness,
                                color,
                                -1,
                            )
                    elif event == cv2.EVENT_LBUTTONUP:
                        drawing = False

                cv2.setMouseCallback(window_name, call_back)
            else:
                bind_to.__dict__[window_name] = frame

        # 立刻执行绑定
        if None not in (window_name, frame):
            bind_to(window_name, frame)
        # 返回绑定函数
        else:
            return bind_to

    @staticmethod
    def draw_contour(frame, cnt_box, color=(0, 0, 255), thickness=2):
        return Contour.draw(frame, cnt_box, color, thickness)
