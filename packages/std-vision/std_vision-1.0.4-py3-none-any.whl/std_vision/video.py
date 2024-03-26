import cv2
import numpy as np
from numpy import ndarray
import math, os
from typing import Optional, Union, List, Dict
import time
from threading import Thread
import queue
from matplotlib import pyplot as plt
import atexit

from .ros_tools import ROSDevice, RosTools


class Types(object):
    """定义一些名称便于使用(所有其它子类中的类型也均统一放到这里)"""

    COLOR_BGR2GRAY = cv2.COLOR_BGR2GRAY
    COLOR_BGR2HSV = cv2.COLOR_BGR2HSV
    COLOR_BGR2RGB = cv2.COLOR_BGR2RGB
    COLOR_BGR2LAB = cv2.COLOR_BGR2LAB
    COLOR_BGR2YCrCb = cv2.COLOR_BGR2YCrCb

    THRESH_BINARY = cv2.THRESH_BINARY  # 超过阈值时取maxval，否则取0（常用）
    THRESH_BINARY_INV = cv2.THRESH_BINARY_INV  # 与cv2.THRESH_BINARY相反
    THRESH_TRUNC = cv2.THRESH_TRUNC  # 超过阈值时取阈值，否则不变（阈值处截断）
    THRESH_TOZERO = cv2.THRESH_TOZERO  # 超过阈值时不变，否则取0（低于阈值取0）
    THRESH_TOZERO_INV = (
        cv2.THRESH_TOZERO_INV
    )  # 超过阈值时取0，否则不变（与cv2.THRESH_TOZERO相反）
    THRESH_ADAPTIVE_MEAN_C = (
        cv2.ADAPTIVE_THRESH_MEAN_C
    )  # 为局部邻域块的平均值，该算法是先求出块中的均值。
    THRESH_ADAPTIVE_GAUSSIAN_C = (
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    )  # 为局部邻域块的高斯加权和。该算法是在区域中(x, y)周围的像素根据高斯函数按照他们离中心点的距离进行加权计算。

    WINDOW_NORMAL = cv2.WINDOW_NORMAL  # 用户能够调节窗口大小（常用）
    WINDOW_AUTOSIZE = cv2.WINDOW_AUTOSIZE  # 根据图像大小显示窗口，大小固定
    WINDOW_FREERATIO = cv2.WINDOW_FREERATIO  # 调整图像，不考虑其比例
    WINDOW_KEEPRATIO = cv2.WINDOW_KEEPRATIO  # 调整图像，保持图像比例

    CAP_TIME_LAST = cv2.CAP_PROP_POS_MSEC
    CAP_NOW_FRAME = cv2.CAP_PROP_POS_FRAMES
    CAP_FRAME_WIDTH = cv2.CAP_PROP_FRAME_WIDTH
    CAP_FRAME_HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
    CAP_FPS = cv2.CAP_PROP_FPS
    CAP_PROP_FOURCC = cv2.CAP_PROP_FOURCC  # 视频格式，一般为MJPG和YUYV

    CONTOUR_RETR_EXTERNAL = cv2.RETR_EXTERNAL  # 只检测外轮廓（常用）
    CONTOUR_RETR_LIST = cv2.RETR_LIST  # 检测的轮廓不建立等级关系
    CONTOUR_RETR_CCOMP = (
        cv2.RETR_CCOMP
    )  # 建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层
    CONTOUR_RETR_TREE = cv2.RETR_TREE  # 建立一个等级树结构的轮廓
    CONTOUR_APPROX_NONE = (
        cv2.CHAIN_APPROX_NONE
    )  # 存储所有的轮廓点，相邻的两个点的像素位置差不超过1
    CONTOUR_APPROX_SIMPLE = (
        cv2.CHAIN_APPROX_SIMPLE
    )  # 压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标

    DRAW_FONT_SIMPLEX = (
        cv2.FONT_HERSHEY_SIMPLEX
    )  # 各字体效果：https://cloud.tencent.com/developer/article/1821937
    DRAW_FONT_PLAIN = cv2.FONT_HERSHEY_PLAIN
    DRAW_FONT_DUPLEX = cv2.FONT_HERSHEY_DUPLEX
    DRAW_FONT_COMPLEX = cv2.FONT_HERSHEY_COMPLEX
    DRAW_FONT_TRIPLEX = cv2.FONT_HERSHEY_TRIPLEX
    DRAW_FONT_COMPLEX_SMALL = cv2.FONT_HERSHEY_COMPLEX_SMALL
    DRAW_FONT_SCRIPT_SIMPLEX = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    DRAW_FONT_SCRIPT_COMPLEX = cv2.FONT_HERSHEY_SCRIPT_COMPLEX


class FilesDevice(object):
    """用于将一个文件夹下的所有图片模拟为一个视频设备"""

    def __init__(self, files_device: str) -> None:
        if os.path.isdir(files_device):
            self.file_names = os.listdir(files_device)
            self.folder_path = files_device
        elif os.path.isfile(files_device):
            self.file_names = [files_device.split("/")[-1]]
        self.img_reader = self.__read_image_from_path()

    def __read_image_from_path(self):
        # 遍历该目录下的所有图片文件 #TODO:遍历顺序指定;支持多级目录
        for filename in os.listdir(self.folder_path):
            try:
                yield cv2.imread(self.folder_path + "/" + filename)
            except:
                print(
                    f"文件：{filename}无法被作为图像读取，已自动跳过，读取下一个文件"
                )

    def read(self):
        try:
            self.__image = next(self.img_reader)
        except:
            return False, self.__image
        else:
            return True, self.__image

    def grab(self):
        try:
            next(self.img_reader)
        except:
            return False
        else:
            return True

    def release(self):
        self.img_reader = None


class StdVideo(object):
    """
    从视频图像获取到处理后图像信息的输出一条龙的CV类，底层主要基于OpenCV实现，在其上进行了进一步封装以求更加方便使用。
    主要用于直接从视频设备获取图像并进行后续处理；同时也对ROS以及直接传入原始图像提供一定支持。
    推荐：import StdVideo as sv
    """

    windows_set = (
        set()
    )  # 维护不同的windows窗口(尽管窗口可以和frame建立一种对应关系，但是frame是一直变化的，从而维护这种联系意义不大，故采用集合变量)
    cap_dict = {}  # 维护不同的视频流(索引号-cap实例)
    video_info = {}  # 维护不同的视频流的信息（索引号-视频信息）
    actual_fps = {}
    __fps_cal = {}  # 维护不同窗口的实际帧率信息（窗口名-帧率）
    pub_topics = {}  # 维护不同的图片发布话题（话题名-消息类型）
    cap_buffer: Dict[Union[int, str], Union[queue.Queue, ndarray]] = {}  # 图片队列

    @classmethod
    def Find(cls, max_num=5):
        """帮助搜寻所有可以使用的设备号"""
        device_avilable = []
        for i in range(max_num):
            try:
                cls.Cap(i)
            except:
                pass
            else:
                device_avilable.append(i)
                # TODO:退出刚才cap的内容
        print(f"在搜寻区间[0,{max_num-1}]中，可用的设备号共有：", device_avilable)

    @classmethod
    def Cap(
        cls,
        device: Union[int, str, tuple] = 0,
        wh_set: tuple = None,
        fps_set: int = None,
        format=None,
        api=cv2.CAP_V4L2,
        buffer=0,
    ):
        """
        打开一个设备视频流或根据传入路径读取视频文件。
        要捕获视频，你需要的参数可以是设备device索引或视频文件的名称(唯一身份ID)。设备索引就是指定哪个摄像头的数字。通常仅有一个摄像头会被连接。
        可以简单地传0(或-1)。多个设备时，一般会按照上电顺序确定索引。可以传max或none，此时将自动寻找当前序号最大的设备进行开启。
        format为None则不更改相机视频输出格式，另外可以改成‘MJPG’和‘YUYV’，从而指定格式。
        api默认为Linux下最好的cv2.CAP_V4L2，若是Windows，请更换为默认。
        当device是tuple类型时，是对ROS话题订阅的支持，(topic_name,data_class,queue_size)。
        """
        print("视频流开启中......")
        if device in ["max", None]:
            device = max(cls.Find(max_num=5))
        if cls.cap_dict.get(device) is not None:
            raise Exception("请不要重复获取同一设备的视频流")
        else:
            if isinstance(device, tuple):  # ROS话题订阅
                cls.cap_dict[device[0]] = ROSDevice(*device)
                return cap  # 直接返回，虚拟设备不进行后续检查与配置
            else:
                cap = cv2.VideoCapture(
                    device, api
                )  # Linux下cv2.CAP_V4L2是最佳的视频接口（理论上默认安装了已经）
        if not cap.grab():  # 由于isopened函数始终返回none，因此改用grab()来判断是否开启
            raise Exception(f"Unable to open device: {device}")

        # 设置视频宽和高
        if wh_set is not None:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, wh_set[0])  # 设置图像宽度
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, wh_set[1])  # 设置图像高度
        # 设置视频帧率
        if fps_set is not None:
            cap.set(cv2.CAP_PROP_FPS, fps_set)  # 设置帧率
        # 设置图像格式
        if format is not None:
            cap.set(6, cv2.VideoWriter.fourcc(*format))
        cls.cap_dict[device] = cap
        # 记录视频主要参数：尺寸、帧率
        fps = cap.get(cv2.CAP_PROP_FPS)
        cls.video_info[device] = {
            "width": cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            "height": cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            "fps": fps,
        }
        if (
            buffer > 0
        ):  # 创建图片缓冲，即开启一个线程，以相机的帧率为频率进行图像的读取存储。
            cls.cap_buffer[device] = queue.Queue(maxsize=buffer)

            def buffer_read():
                period_half = 1 / fps / 2
                while True:
                    # 从-1到0，先进先出，即0位始终为最旧，-1为最新
                    cls.cap_buffer[device].put(cap.read())
                    time.sleep(period_half)

            Thread(target=buffer_read, daemon=True).start()
        # 注册程序退出时对cap和所有windows的关闭函数
        atexit.register(cap.release)
        atexit.register(cv2.destroyAllWindows)
        print("视频流成功开启！")
        return cap

    @classmethod
    def Release(cls, device=0):
        cls.cap_dict[device].release()

    @classmethod
    def Read(
        cls,
        device: Union[int, ndarray, str] = 0,
        resize_xyc: Optional[tuple] = None,
        color_convert=None,
        return_raw=False,
    ):
        """
        从视频流中获取一帧图像(也可直接传入图像),返回处理后的图像和原图像（可选）。
        纯cap视频流没有缓冲区，因此read始终读取的是最新的一帧。
        resize_xyc可以是两个元素也可以三个元素且第三个元素为0，表示将图像转为灰度图，第三个元素大于0则表示按照该阈值对图像进行常用的二值化操作。
            前两个元素可以均为none，此时仅最后一个元素将生效。
            考虑简洁性，不支持单独仅某个方向的resize，请根据图像实际大小自行将不需调整的方向设置为原始大小。
        """
        frame = None
        if not isinstance(device, ndarray):  # int或str
            # 检查并保证cap被创建
            if cls.cap_dict.get(device) is None:
                try:
                    cls.Cap(device)  # 若未检测到视频流，则创建，从而起始不用先cap后read
                except:  # 读取失败认为可能是获取图片文件
                    try:
                        frame = cv2.imread(device)
                    except:
                        pass
            # 读取图像
            if frame is None:
                if cls.cap_buffer.get(device) is None:
                    ret, frame = cls.cap_dict[
                        device
                    ].read()  # ret为true为正常读取到贞，false表示读取到视频的结尾。对于开启相机的正常情况下始终为true
                else:  # 尝试从buffer中获取
                    if isinstance(cls.cap_buffer[device], ndarray):
                        frame = cls.cap_buffer[device]
                    else:
                        frame = cls.cap_buffer[device].get(timeout=0.2)
                        cls.cap_buffer[device].task_done()
                # 判断是否读取到非空图像
                if frame is None:
                    exit("Unable to read image from target device")
                elif not ret:
                    exit("The video has been read over")
        else:
            frame = device  # frame直接传入图像
        frame_cp = frame.copy()  # 复制防止改动原图
        if resize_xyc is not None:
            lis2 = resize_xyc[:2]
            if None not in lis2:
                frame_cp = cls.Geometry.Resize(frame_cp, lis2)
            if len(resize_xyc) == 3:
                if resize_xyc[2] == 0:
                    frame_cp = cv2.cvtColor(frame_cp, Types.COLOR_BGR2GRAY)
                else:
                    frame_cp = cls.Threshold.gray_global(frame_cp, resize_xyc[2], 255)
        if color_convert is not None:
            frame_cp = cv2.cvtColor(frame_cp, color_convert)
        # print(cls.cap_dict[device].get(cv2.CAP_PROP_POS_FRAMES))
        if return_raw:
            return frame_cp, frame
        else:
            return frame_cp

    @classmethod
    def Jump(cls, device, target_frame=-1, inc=False, not_pass=0):
        """
        跳到某一帧。默认为最新帧即不跳帧。相比于Read更快。
        inc为true时target_frame表示目标帧为当前帧增量。
        not_pass为0时目标帧实际会pass掉，下次read的是目标帧的下一帧。
        """
        if inc:
            target_frame = (
                cls.cap_dict[device].get(cv2.CAP_PROP_POS_FRAMES) + target_frame
            )
        while (
            cls.cap_dict[device].get(cv2.CAP_PROP_POS_FRAMES) < target_frame - not_pass
        ):  # 当前帧，基于以0开始的被捕获或解码的帧索引
            cls.cap_dict[device].grab()

    @classmethod
    def Info(cls, device, info_name):
        """除了基本信息的全局字典外，提供获取其它参数的函数"""
        if info_name == Types.CAP_PROP_FOURCC:
            fourcc = int(cls.cap_dict[device].get(cv2.CAP_PROP_FOURCC))
            fourcc_str = (
                chr(fourcc & 0xFF)
                + chr((fourcc >> 8) & 0xFF)
                + chr((fourcc >> 16) & 0xFF)
                + chr((fourcc >> 24) & 0xFF)
            )
            return fourcc_str
        else:
            return cls.cap_dict[device].get(info_name)

    @classmethod
    def Show(
        cls,
        window_name: str,
        frames=None,
        window_size=(640, 480),
        window_mode=cv2.WINDOW_NORMAL,
        wait_time=1,
        rows=1,
        cols=None,
        EXIT_KEY: Union[str, int] = 27,
        show_fps=False,
        cal_fps=False,
        func_bound=(),
        auto3D=True,
        use_plt=False,
        disable=False,
    ):
        """
        显示图像(融合了窗口配置、图片拼接与显示、帧率提示、按键检测、绑定函数等功能)；图像为None时将自动完成读取（仅默认情况下成功），因此实现了一行代码读取和显示图像
        可以实现多幅图像的拼接显示（多幅图像放到tuple中），将按照给定的rows,cols参数进行排列显示
        auto3D=True时自动将单通道图像转换为3通道，从而可以与3通道图像一同显示
        disable=True时该函数将失效，图片不再进行展示
        EXIT_KEY默认为27，表示按下ESC键退出程序，可以改成其它键值或字符
        show_fps和cal_fps与帧率有关，前者为True时将计算并在图像左下角实时显示帧率，而前者为False后者为True时将计算帧率并保存在类变量中，可供取用
        默认创建窗口只在该函数中才最终生效，设定window_mode为none才认为"窗口已经之前设定好了"，不新设定窗口，不过仍然可以调整窗口大小
        func_bound可以是一个或者多个函数对象，用来绑定一些窗口功能，如鼠标位置打印等，绑定函数的参数固定为window_name,frames（即窗口名和图像），示例见print_mouse_color方法
        use_plt=True将使用matplotlib.pyplot进行图片展示，不推荐
        """
        if not disable:
            # 甚至集成到了如果frames为none，则直接自动read
            if frames is None:
                frames = cls.Read()
            # 拼接图片(图片数量为1则返回原图)
            if not use_plt:
                frames = cls.Combine(frames, rows, cols, auto3D)
            try:
                cv2.getWindowProperty(
                    window_name, 0
                )  # 使用这种方式进行判断窗口是否存在，耗时在微妙级，不影响性能
            except:
                cls.windows_set.discard(
                    window_name
                )  # 如果不存在，则执行一次窗口集合移除操作，便于重新进行配置，消除窗口关闭后大小改变的bug
            # 初次使用定义窗口（或窗口摧毁后重新定义）
            if window_name not in cls.windows_set:  # 仅在该函数中配置全局窗口set
                if window_mode is not None:
                    cls.windows_set.add(window_name)
                    try:
                        cv2.destroyWindow(
                            window_name
                        )  # 为避免之前临时创建了window这里要尝试清除一下否则后面的设定不会生效
                    except:
                        pass
                    cv2.namedWindow(window_name, window_mode)
                if window_size is not None and window_mode != cv2.WINDOW_AUTOSIZE:
                    cv2.resizeWindow(window_name, *window_size)
                cls.__fps_cal[window_name] = [
                    0,
                    0,
                ]  # 第一个负责计数控制，第二个负责记录时间；可用于计算每个窗口的图像实际显示帧率（第一帧忽略，然后从第一帧show结束(相当于第二帧开始)到到下一帧show前）
            # 执行绑定的函数（主要是一些窗口回调函数）
            if callable(func_bound):
                func_bound(window_name, frames)
            elif len(func_bound) > 0:
                for func in func_bound:
                    func(window_name, frames)
            # 性能计算：结束
            if (cal_fps or show_fps) and cls.__fps_cal[window_name][0] == 1:
                cls.__fps_cal[window_name][0] = 0
                now_time = time.time()
                cls.actual_fps[window_name] = 1 / (
                    now_time - cls.__fps_cal[window_name][1]
                )
                if show_fps:  # 在图像左下角显示fps
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(
                        frames,
                        f"FPS:{cls.actual_fps[window_name]:.2f}",
                        (5, frames.shape[0] - 5),
                        font,
                        1,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA,
                    )  # 图片、文字、坐标（文字左下角）、类型、大小、颜色、厚度、线条类型
            # 图片显示与按键退出
            if not use_plt:
                cv2.imshow(window_name, frames)
            else:
                cls.plt_imgs_show(frames)  # 使用爬plt进行图片显示
            k = (
                cv2.waitKey(wait_time) & 0xFF
            )  # 如果使用的是64位计算机，则必须&0XFF或&0xff
            if isinstance(EXIT_KEY, str):
                if k == ord(EXIT_KEY):
                    if wait_time > 0:
                        raise Exception(f"{EXIT_KEY}键按下，程序结束")
                    else:
                        cv2.destroyWindow(window_name)
            elif k == EXIT_KEY:
                if wait_time > 0:
                    raise Exception(f"ESC键按下，程序结束")
                else:
                    cv2.destroyWindow(window_name)
            # 性能计算：开始
            if (cal_fps or show_fps) and cls.__fps_cal[window_name][0] == 0:
                cls.__fps_cal[window_name][1] = time.time()
                cls.__fps_cal[window_name][0] = 1

    @classmethod
    def Combine(
        cls,
        frames: Union[ndarray, List[ndarray], tuple],
        rows=1,
        cols=None,
        auto3D=True,
    ):
        """
        指定行数或列数拼为基准来接图片；均指定则以列数为准；
        可设置auto3D为false,则将不会自动检测维度并进行调整显示；（默认自动检测，因为单次检测耗时不多在微妙级）
        """
        # 根据列数或行数将多幅图像拼接
        if not isinstance(frames, ndarray):
            num = len(frames)
            if auto3D:  # 二维图自动转为3D图
                for frame in frames:
                    if frame.ndim == 2:
                        frame = cls.To3D(frame)
        else:
            num = 1
        if num > 1:
            row_frames = []
            if cols is not None:  # 按列排序
                h_num = num // cols  # 求商,得到共有多少行
                res_v = num % cols  # 求余，得到最后一行剩下几个空位
                i = 0
                for i in range(h_num):
                    row_frames.append(np.hstack(frames[i * cols : (i + 1) * cols]))
                if h_num > 0:
                    i += 1
                if res_v > 0:
                    black = frames[0] * 0
                    row_frames.append(
                        np.hstack(frames[i * cols :] + [black for _ in range(res_v)])
                    )
                # 得到最终拼接好的图像
                frames = np.vstack(row_frames)
            # 默认按行排序
            else:
                rem = num % rows  # 求出余数reminder
                if rem > 0:
                    res = rows - rem  # 需要补充的数量
                    cols = int(num / rows) + 1  # 每行列数
                    black = frames[0] * 0
                    frames.append([black for _ in range(res)])  # 用黑色图补充缺少的图片
                else:
                    cols = int(num / rows)
                # 行拼接
                for i in range(rows):
                    row_frames.append(np.hstack(frames[i * cols : (i + 1) * cols]))
                # 列拼接
                frames = np.vstack(row_frames)
        return frames

    @classmethod
    def Save(cls, frame: ndarray, name="Image", path="../Images/", cover: int = 0):
        """保存图像(该函数通过启动线程的方式进行图像与视频保存，对主进程影响较小)"""
        if cover > 0:  # 不覆盖，修改下name
            if not hasattr(cls.Save, name):
                cls.Save.__dict__[name] = 0
            name += f"_{cls.Save.name[0]}"
            cls.Save.__dict__[name] += 1
            if cls.Save.__dict__[name] >= cover:
                cls.Save.__dict__[name] = 0
        # 开启线程进行图片写入（实测是线程安全的，不论是否覆盖）
        Thread(target=cv2.imwrite, args=(path + name, frame), daemon=True).start()

    @staticmethod
    def To3D(frame: ndarray) -> ndarray:
        """将灰度或二值图变成3D图，从而可以跟color图一起通过imshow展示"""
        return np.dstack(
            (frame, frame, frame)
        )  # 为了实现并排显示，需要将二值图变成3d图

    @staticmethod
    def Cover(base: ndarray, coveror: ndarray, position=(0, 0), mask=None, quit=True):
        """
        将coveror覆盖到base上,position为左上角（因为OpenCV图像的左上角是图像原点）
        若coveror右下角超出了base，quit为真多余的部分将被忽略，否则将自动调整图像大小刚好覆盖base。
        mask为none，则直接覆盖，否则根据mask提取出coveror的特定区域进行对应的覆盖。mask可参考如下方式获得：
            coverorgray = cv2.cv2tColor(coveror,cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(coverorgray, 10, 255, cv2.THRESH_BINARY)
        """
        # 我想把logo放在左上角，所以我创建了ROI
        row_end = position[1] + coveror.shape[0]
        col_end = position[0] + coveror.shape[1]
        if row_end > base.shape[0] or col_end > base.shape[1]:
            if quit:  # 裁剪
                coveror = coveror[
                    : base.shape[0] - position[1], : base.shape[1] - position[0]
                ]
            else:  # 放缩
                coveror = cv2.resize(
                    coveror, (base.shape[0] - position[1], base.shape[1] - position[0])
                )
        # 提取出base的roi位置的局部图
        roi = base[position[1] : row_end, position[0] : col_end]
        if mask is None:
            mask = cv2.add(coveror, 255)  # 加了255必然全变成了最大值，即认为全部为mask
        # 根据logo的掩码创建其相反掩码
        mask_inv = cv2.bitwise_not(mask)
        # 现在将ROI中logo的区域涂黑
        base_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        # 仅从logo图像中提取logo区域
        coveror_fg = cv2.bitwise_and(coveror, coveror, mask=mask)
        # 将logo放入ROI并修改主图像
        dst = cv2.add(base_bg, coveror_fg)
        base[position[1] : row_end, position[0] : col_end] = dst
        return base

    @classmethod
    def plt_imgs_show(
        cls,
        frames,
        row_col=None,
        new_thread=False,
        daemon=True,
        convert_color=True,
        dpi=100,
    ):
        """
        通过plt展示多图是方便的，但是也就因此无法使用OpenCV的一些额外的功能，如窗口回调、waitkey等等;
        若row_col为none，则将采用尽可能的正方形方式对图像进行恰当的显示；
        convert_color为true则对图像进行bgr到rgb的转换，若已经转换了，请设为false；
        new_thread为true时让图片显示可以在另外的线程中运行，从而不会阻塞当前线程。此时daemon表明
        """
        if new_thread:
            Thread(
                target=cls.plt_imgs_show,
                daemon=daemon,
                args=(frames, row_col, False, convert_color),
            ).start()
            return
        if row_col is None:
            if isinstance(frames, ndarray):
                row_col = (1, 1)
                frames = [frames]
                show_title = False
            else:
                show_title = True
                len_ = len(frames)
                len_sqr = math.sqrt(len_)
                len_sqr_int = int(len_sqr)
                if len_sqr_int * (len_sqr_int + 1) < len_:
                    row_col = (len_sqr_int + 1, len_sqr_int + 1)
                else:
                    row_col = (len_sqr_int + 1, len_sqr_int)
        plt.figure(dpi=dpi)  # 调整图像dpi，dpi过低会无法显示一些图像细节信息
        for index, frame in enumerate(frames, 1):
            if convert_color:
                frame = cv2.cvtColor(frame, Types.COLOR_BGR2RGB)
            plt.subplot(*row_col, index), plt.imshow(frame, "gray"), plt.axis("off")
            plt.subplots_adjust(
                top=1, bottom=0, right=1, left=0, hspace=0, wspace=0
            )  # 减小白色边框
            if show_title:
                plt.title(f"{index}")
        plt.show()

    @classmethod
    def print_mouse_position(cls, window_name, click=False, enable=True):
        """click为true则点击后才打印当前坐标信息，否则时刻刷新打印"""
        if enable and not hasattr(cls.print_mouse_position, window_name):
            cls.print_mouse_position.__dict__[window_name] = True

            def call_back(
                event, x, y, flags, param
            ):  # 创建鼠标回调函数具有特定的格式，该格式在所有地方都相同。
                if click and event == cv2.EVENT_LBUTTONDOWN:
                    print(x, y)
                else:
                    print(x, y)  # 始终打印

            cv2.setMouseCallback(window_name, call_back)

    @classmethod
    def print_mouse_color(cls, window_name=None, frame=None, print_pos=True):
        """ """

        def bind_to(window_name, frame):
            """所有的绑定函数都有相同的参数：第一个是窗口名，第二个是frame"""
            if not hasattr(bind_to, window_name):  # 同一个窗口仅执行一次回调函数设置
                bind_to.__dict__[window_name] = frame
                if (
                    window_name not in StdVideo.windows_set
                ):  # 为保证setMouseCallback不出错，先创建一个空窗口
                    cv2.namedWindow(window_name)
                    # TODO: 问题：call_back返回的是窗口的位置，而不是图片的位置，因此，如果窗口大小和这里的图片大小不一致就会对应不上

                def call_back(event, x, y, flags, param):
                    if event == cv2.EVENT_LBUTTONDOWN:
                        # 根据维度判断颜色是灰度还是rgb
                        if bind_to.__dict__[window_name].ndim == 2:
                            if print_pos:
                                print(
                                    "({},{})点灰度值为：{}".format(
                                        x, y, bind_to.__dict__[window_name].item(y, x)
                                    )
                                )
                            else:
                                print(
                                    "该点灰度值为：{}".format(
                                        x, y, bind_to.__dict__[window_name].item(y, x)
                                    )
                                )  # item方法比直接取值更好
                        else:
                            print(
                                "({},{})点BGR值为：{}".format(
                                    x, y, bind_to.__dict__[window_name][y, x]
                                )
                            )
                            # 关于numpy的一些注意：Numpy是用于快速数组计算的优化库。因此，简单地访问每个像素值并对其进行修改将非常缓慢，因此不建议使用
                            # 对于单个像素访问，Numpy数组方法array.item()和array.itemset())被认为更好，但是它们始终返回标量
                            # 如果要访问所有B，G，R值，则需要分别调用所有的array.item()。距离：img.itemset((10,10,2),100)
                            # 这里对性能无要求，因此直接取值更方便

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
    def color_filter(
        frame: ndarray, ColorL: list, ColorH: list, convert=cv2.COLOR_BGR2HSV
    ):
        """根据HSV选择合适的颜色阈值对彩色图像（默认为BGR格式）进行处理"""
        frame_cp = frame.copy()
        cvt = cv2.cvtColor(frame_cp, convert)
        lower_thresh = np.array(ColorL)
        upper_thresh = np.array(ColorH)
        mask = cv2.inRange(cvt, lower_thresh, upper_thresh)
        res = cv2.bitwise_and(frame_cp, frame_cp, mask=mask)
        return res, mask

    @staticmethod
    def color_exchange(frame: ndarray, order=(1, 0, 2)):
        """order=(1,0,2)意为，原来图像的通道1变为通道0，通道0变为通道1，通道2不变，依次类推"""
        bgr = (frame[:, :, 0], frame[:, :, 1], frame[:, :, 2])
        lis = [0, 0, 0]
        for index, ele in enumerate(order):
            lis[index] = bgr[ele]
        return cv2.merge(lis)

    @classmethod
    def color_thresh_determine(cls,frame_dev_topic=None,default=0,mode='HSV',save_path=None,show_raw=False):
        """  # TODO:增加腐蚀膨胀操作的滑条
            确定最佳HSV阈值的函数：frame可以为图像（ndarray）、设备号（int）或ros话题名（str）
            frame为none则尝试默认参数进行图片获取：先尝试设备0，再尝试获取ros消息，都不行则报错退出:
                技巧：可以通过保持frame为none而修改default为其它不存在的设备号来自动触发对ros默认图像话题的连接。
            mode默认为hsv，另外还可以使用YUV（YCrCb）、LAB。
        """
        # 鲁棒的连接处理
        flag=0
        if frame_dev_topic is None: frame_dev_topic = default;flag = 1
        # frame_dev_topic本身就是图片
        if isinstance(frame_dev_topic, ndarray):
            def get_img(): return frame_dev_topic
        # 尝试device
        elif isinstance(frame_dev_topic, int):
            try:
                if cls.cap_dict.get(frame_dev_topic) is None:  # 还没有cap过
                    cls.Cap(frame_dev_topic)  # 重新还行cap
            except:
                if flag == 1:  # 表明报错是因为default的值有问题
                    frame_dev_topic = "camera/color/image_raw"
                    print('连接错误：未找到视觉设备，尝试连接ROS')  # 尝试连接ROS
                else: cls.Cap(frame_dev_topic)  # 重新尝试连接
            else:
                print(f'成功连接设备号：{frame_dev_topic}')
                def get_img():
                    return cls.Read(frame_dev_topic)
        # 尝试topic
        elif isinstance(frame_dev_topic, str):
            assert ROSDevice.ready, "Try as ROS topic name, but ROS is not ready."
            import subprocess
            import rospy
            from sensor_msgs.msg import Image
            try:
                p = subprocess.getoutput("pgrep rosmaster")
                if p == '': raise Exception('连接错误：rosmaster未开启，使用ROS模式请先启动roscore')
                else:
                    NODE_NAME = 'color_thresh_determine'
                    if rospy.get_name() == '/unnamed':
                        rospy.init_node(NODE_NAME)
                        print(f"Initializing {NODE_NAME} node.")
                    else:
                        NODE_NAME = rospy.get_name()
                        print(f"Node {NODE_NAME} already initialized.")
                    rospy.wait_for_message("/camera/color/image_raw",Image,timeout=1)
            except:
                if flag: raise Exception('连接错误：未查询到图片消息，获取消息失败\r\n两种方式均失败，请明确采用的方式及参数后重试')
                else: raise Exception(f'给定话题{frame_dev_topic}无法获取图片消息')
            else:
                print(f'成功连接ROS话题:{frame_dev_topic}')
                def get_img():
                    img = rospy.wait_for_message(frame_dev_topic, Image)
                    return RosTools.imgmsg_to_cv2(img)

        # 创建窗口和滑条
        def callback(*arg):
            pass  # 创建空回调函数（比起直接置0更易拓展）
        WINDOW_NAME = 'Color pick(Press ESC to exit)'
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        if mode in ['HSV','hsv']:
            cv2.createTrackbar('LH', WINDOW_NAME, 0, 179, callback)
            cv2.createTrackbar('LS', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('LV', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('HH', WINDOW_NAME, 0, 179, callback)
            cv2.createTrackbar('HS', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('HV', WINDOW_NAME, 0, 255, callback)
        elif mode in ['YUV','YCrCb']:
            cv2.createTrackbar('LY ', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('LCr', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('LCb', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('HY ', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('HCr', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('HCb', WINDOW_NAME, 0, 255, callback)
        elif mode in ['LAB','Lab','lab']:
            cv2.createTrackbar('LL', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('LA', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('LB', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('HL', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('HA', WINDOW_NAME, 0, 255, callback)
            cv2.createTrackbar('HB', WINDOW_NAME, 0, 255, callback)
        # 主循环
        while True:
            if mode in ['HSV','hsv']:
                LH = cv2.getTrackbarPos('LH', WINDOW_NAME)
                LS = cv2.getTrackbarPos('LS', WINDOW_NAME)
                LV = cv2.getTrackbarPos('LV', WINDOW_NAME)
                HH = cv2.getTrackbarPos('HH', WINDOW_NAME)
                HS = cv2.getTrackbarPos('HS', WINDOW_NAME)
                HV = cv2.getTrackbarPos('HV', WINDOW_NAME)
                ColorL = [LH, LS, LV]
                ColorH = [HH, HS, HV]
                img = get_img()
                res, mask = StdVideo.color_filter(img,ColorL,ColorH,convert=Types.COLOR_BGR2HSV)
            elif mode in ['YUV','YCrCb']:
                LY = cv2.getTrackbarPos('LY ', WINDOW_NAME)
                LCr = cv2.getTrackbarPos('LCr', WINDOW_NAME)
                LCb = cv2.getTrackbarPos('LCb', WINDOW_NAME)
                HY = cv2.getTrackbarPos('HY ', WINDOW_NAME)
                HCr = cv2.getTrackbarPos('HCr', WINDOW_NAME)
                HCb = cv2.getTrackbarPos('HCb', WINDOW_NAME)
                ColorL = [LY, LCr, LCb]
                ColorH = [HY, HCr, HCb]
                img = get_img()
                res, mask = StdVideo.color_filter(img,ColorL,ColorH,convert=Types.COLOR_BGR2YCrCb)
            elif mode in ['Lab','LAB']:
                LL = cv2.getTrackbarPos('LL', WINDOW_NAME)
                LA = cv2.getTrackbarPos('LA', WINDOW_NAME)
                LB = cv2.getTrackbarPos('LB', WINDOW_NAME)
                HL = cv2.getTrackbarPos('HL', WINDOW_NAME)
                HA = cv2.getTrackbarPos('HA', WINDOW_NAME)
                HB = cv2.getTrackbarPos('HB', WINDOW_NAME)
                ColorL = [LL, LA, LB]
                ColorH = [HL, HA, HB]
                img = get_img()
                res, mask = StdVideo.color_filter(img,ColorL,ColorH,convert=Types.COLOR_BGR2LAB)
            else: exit('错误：请输入正确的mode参数值')
            # 显示
            mask = np.dstack((mask,mask,mask))  # 为了实现并排显示，需要将二值图变成3d图
            try:
                StdVideo.Show(WINDOW_NAME,(mask,res),window_size=(1280,720),window_mode=None)
                if show_raw: StdVideo.Show('raw_img(按ESC键退出)',img,window_size=(640,480))
            except Exception as e:
                print(e)
                print(f'最终确定的阈值为："{mode}_L":{ColorL}, "{mode}_H":{ColorH}')
                if save_path is not None:
                    cls.save_parameters(ColorL+ColorH,save_path)
                break
        cv2.destroyWindow(WINDOW_NAME)
        return ColorL,ColorH  # 返回确定阈值

    @classmethod
    def color_replace(
        cls, frame: ndarray, color: Union[int, tuple, list], area: Union[tuple, list]
    ):
        """
        将图像中的某些区域替换为
            area = ([])  # TODO
        """
        if frame.ndim == 2:
            pass
        else:
            # # 裁切图像，避免由于物块大小不均匀造成的下层物块在上层轮廓侧边的漏出误识别
            # bi_cp = StdVideo.create_empty_frame(ImageSize[:2],0)
            # bi_cp[:,281:359] = binary_img[:,281:359]
            # binary_img = bi_cp
            if not isinstance(color, int):
                color = color[0]
            cls.create_empty_frame()
            pass

    @classmethod
    def gradient(cls, frame, mode: str, ksize=5, convert=cv2.COLOR_BGR2GRAY):
        """
        mode:
            sobelx,sobely,sobel
            scharrx,scharry,scharr
            laplace
        ksize: scharr系列始终为3，其它默认为5
        """
        if convert is not None:
            frame = cv2.cvtColor(frame, convert)
        if mode in ["sobelx", "scharrx"]:
            if mode == "scharr":
                ksize = -1
            g_frame = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=ksize)
        elif mode in ["sobely", "scharry"]:
            if mode == "scharr":
                ksize = -1
            g_frame = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=ksize)
        elif mode == "sobelxy":
            g_frame = cv2.Sobel(frame, cv2.CV_64F, 1, 1, ksize=ksize)
        elif mode == "sobel":
            g_frame = cls.Math.plus(
                [cv2.Sobel(frame, cv2.CV_64F, 0, 1), cv2.Sobel(frame, cv2.CV_64F, 1, 0)]
            )
        elif mode == "scharr":
            g_frame = cls.Math.plus(
                [
                    cv2.Scharr(frame, cv2.CV_64F, 0, 1),
                    cv2.Scharr(frame, cv2.CV_64F, 1, 0),
                ]
            )
        elif mode == "laplace":
            g_frame = cv2.Laplacian(frame, cv2.CV_64F)
        else:
            raise Exception("梯度mode错误")
        return np.uint8(np.absolute(g_frame))

    @classmethod
    def canny_determine(cls):
        """通过滑动条动态更改canny函数的参数"""

        # 创建空回调函数（比起直接置0更易拓展）
        def callback(*arg):
            pass

        if not hasattr(cls.canny_determine, "first"):
            cls.canny_determine.__dict__["first"] = False
            cv2.createTrackbar("min_val", "EdgesDetect", 0, 255, callback)
            cv2.createTrackbar("max_val", "EdgesDetect", 0, 254, callback)
            cv2.createTrackbar("sobel_size", "EdgesDetect", 3, 7, callback)
            cv2.createTrackbar("precise", "EdgesDetect", 0, 1, callback)
        min_val = cv2.getTrackbarPos("min_val", "EdgesDetect")
        max_val = cv2.getTrackbarPos("max_val", "EdgesDetect")
        sobel_size = cv2.getTrackbarPos("sobel_size", "EdgesDetect")
        precise = cv2.getTrackbarPos("precise", "EdgesDetect")

        if sobel_size < 5:
            sobel_size = 3
        if 5 <= sobel_size < 7:
            sobel_size = 5
        else:
            sobel_size = 7
        if precise >= 1:
            precise = True
        else:
            precise = False

        return min_val, max_val, sobel_size, precise

    @staticmethod
    def edge_detect(
        frame, min_val, max_val, sobel_size, precise, convert=cv2.COLOR_BGR2GRAY
    ):  # 第三个参数越大边缘越多，第四个参数为True能有效减少杂散边缘
        """
        采用经典最佳的canny算法:
            强度梯度大于 maxVal 的任何边缘必定是边缘，而小于 minVal 的那些边缘必定是非边缘，因此
            将其丢弃。介于这两个阈值之间的对象根据其连通性被分类为边缘或非边缘。如果将它们连接
            到“边缘”像素，则将它们视为边缘的一部分。否则，它们也将被丢弃。
        """
        # 将新的颜色图进行灰度化
        if convert is not None:
            frame = cv2.cvtColor(frame, convert)
        # 对灰度化图进行canny边缘检测（canny自带了5x5高斯滤波器消除图像中的噪声）
        edges_img = cv2.Canny(frame, min_val, max_val, None, sobel_size, precise)
        return edges_img

    @staticmethod
    def create_empty_frame(size: Union[tuple, list], color: Union[tuple, list, int]):
        """
        创建纯色空图：
            size可以为2元或3元
            color可以为灰度值或bgr值
            上述两者应对应好
        """
        if isinstance(color, int):
            channels = 1  # 利用np的维度判断函数对数据的维度进行判断
        else:
            channels = len(color)  # 根据颜色数量
            if channels == 2:
                exit("颜色维度不能为2，只能为1（灰度or二值图）和3（彩色图）")
            if channels == 1:
                color = color[0]

        if channels == 3:
            src = np.zeros(
                [size[1], size[0], 3], dtype=np.uint8
            )  # dtype在调试时非常重要，因为OpenCV-Python代码中的大量错误是由无效的数据类型引起的
            for i in range(3):
                src[:, :, i] += color[i]
        else:
            src = np.zeros([size[1], size[0]], dtype=np.uint8) + color

        return src

    @staticmethod
    def save_parameters(params, path: str):
        """保存参数"""
        import json

        FILE_NAME = path
        with open(FILE_NAME, "w") as f_obj:
            json.dump(params, f_obj)
        print("参数已存储到指定文件中")

    @staticmethod
    def load_parameters(path: str):
        """载入保存的参数"""
        import json

        FILE_NAME = path
        with open(FILE_NAME) as f_obj:
            return json.load(f_obj)

    class Color(object):
        pass

    class Filter(object):
        """
        与一维信号一样，还可以使用各种低通滤波器（LPF），高通滤波器（HPF）等对图像进行滤波。
        LPF有助于消除噪声，使图像模糊等。HPF滤波器有助于在图像中找到边缘。
        """

        pass  # TODO
