from typing import Optional
from ros_tools import RosTools
import numpy as np


if RosTools.ready:
    import rospy
    from sensor_msgs.msg import CameraInfo, Image


class UnitConvert(object):
    """该类主要实现像素单位和米之间的对应转换"""

    camrera_info_dict = {}  # 维护设备号（或ROS话题名）-相机信息（对单位转换有用的信息）
    default_topic_name = "/camera/color/camera_info"
    unit_coefficient = {}  # 维护设备号（或ROS话题名）-m_per_pixel转换关系

    @classmethod
    def get_camera_info(cls, path="", topic=""):
        """
        自动获取相机有关信息，其中path为用相机排到的某幅图片的位置。
        注意图片必须是相机原生拍摄或使用系统相机软件拍摄得到的，而
        不能是用OpenCV读取后保存的，因为这种情况下图片其它信息丢失了。
        """
        if topic != "":  # 从ROS话题获取消息
            if topic == "":
                topic = cls.default_topic_name
            info = rospy.wait_for_message(topic, CameraInfo)
            cls.camrera_info_dict[topic] = [info.K[0], info.K[4]]
            print("成功获取相机信息:fx={},fy={}.".format(info.K[0], info.K[4]))
        elif path != "":
            with open(path, "rb") as f:
                import exifread

                tags = exifread.process_file(f)
            try:
                FL = tags.get("EXIF FocalLength").values[0]
                DZR = tags.get("EXIF DigitalZoomRatio")
                if DZR is None:
                    DZR = 1
                else:
                    DZR = DZR.values[0]
                cls.camrera_info_dict[topic] = [FL, DZR]
            except:
                raise Exception(
                    "错误：无法提取指定相机的有关信息，您的相机可能不具备相关信息的输出，请查阅手册自行获取"
                )

        return cls.camrera_info_dict[topic]

    @classmethod
    def set_camera_info(cls, device, f_sensor: Optional[list] = None, fx=None, fy=None):
        """
        若无法自动获取相机信息，请自行查阅资料并获取如下有关信息，通过该函数进行设置：
            相机的镜头焦距+感光芯片尺寸，或者，fx或fy。
            两种方式二选一，如果都选，则默认使用第一种。
        """
        if f_sensor is not None:
            cls.camrera_info_dict[device] = f_sensor
        else:
            cls.camrera_info_dict[device] = [fx, fy]

    @classmethod
    def calculate_m_pixel_coefficient(cls, device, x_or_y="x") -> float:
        """得到在distance为1m时的像素-米对应关系，该关系与distance成正比"""
        if isinstance(device, str):
            if device == "":
                device = cls.default_topic_name
            if x_or_y == "x":
                fx = cls.camrera_info_dict[device].K[
                    0
                ]  # k为相机内参矩阵，python中实际表示为一个tuple：(fx,0,cx,0,fy,cy,0,0,1)
                m_per_pixel_dis1m = 1 / fx
            else:
                fy = cls.camrera_info_dict[device].K[4]  # 一般以fx为准
                m_per_pixel_dis1m = 1 / fy
        else:
            pixels_length = 1
            distance = 1
            f, dzr = cls.camrera_info_dict[device]
            m_per_pixel_dis1m = (
                pixels_length * distance / f / 5.62 * 0.8 / 1000 / dzr * 0.925
            )
        cls.unit_coefficient[device] = m_per_pixel_dis1m
        return m_per_pixel_dis1m

    @classmethod
    def convert_pixel_bias_to_meter(cls, device, pixel_bias, distance):
        """转换像素数-meter"""
        return cls.unit_coefficient[device] * distance * pixel_bias

    @classmethod
    def convert_meter_bias_to_pixels(cls, device, meter_bias, distance):
        """转换meter-像素数"""
        return 1 / (cls.unit_coefficient[device] * distance) * meter_bias


def ToCV2(frame) -> np.ndarray:
    """将ROS图像或realsense彩色图像转为OpenCV格式"""
    frame_type = type(frame)
    if frame_type is Image:
        return RosTools.imgmsg_to_cv2(frame)
    else:
        import pyrealsense2 as rs

        if frame_type is rs.pyrealsense2.BufData:
            return np.asanyarray(frame)
        elif frame_type is rs.pyrealsense2.video_frame:
            return np.asanyarray(frame.get_data())
