from threading import Thread
from typing import Dict, Union
import os
from threading import Event
import cv2

try:  # 尝试使用ROS
    import rospy
    from cv_bridge import CvBridge
    from sensor_msgs.msg import Image
except Exception as e:
    ROS_OK = False
else:
    ROS_OK = True


class RosTools(object):
    """该类主要实现ROS相关的工具函数"""
    topic_names:Dict[str, Dict[str, Union[rospy.Publisher, Image, Thread, bool, float]]] = {}
    ready = ROS_OK
    @classmethod
    def ros_spin_once(cls, sleep_time=0.5):
        """该函数改版自rospy.spin，实现了python中ros的单次spin的spinonce函数"""
        if not hasattr(cls.ros_spin_once, "first"):
            cls.ros_spin_once.__dict__["first"] = False
            if not rospy.core.is_initialized():
                raise rospy.exceptions.ROSInitException(
                    "client code must call rospy.init_node() first"
                )
            rospy.core.logdebug(
                "node[%s, %s] entering spin(), pid[%s]",
                rospy.core.get_caller_id(),
                rospy.core.get_node_uri(),
                os.getpid(),
            )
        try:
            if not rospy.core.is_shutdown():
                rospy.rostime.wallsleep(sleep_time)
            else:
                exit("\r\nROS Core Shut Down")
        except KeyboardInterrupt:
            rospy.core.logdebug("keyboard interrupt, shutting down")
            rospy.core.signal_shutdown("keyboard interrupt")

    @classmethod
    def cv2_to_imgmsg(cls, cv_image, desired_encoding="passthrough"):
        """
        将cv2的图片转换为ros的图片消息:
        cv_image: cv2的图片
        desired_encoding: 想要的编码格式
            默认为"passthrough", 即不做任何转换;
            其他常用的编码格式有"bgr8", "rgb8", "mono8", "mono16"等
        """
        bridge = CvBridge()
        return bridge.cv2_to_imgmsg(cv_image, desired_encoding)

    @classmethod
    def imgmsg_to_cv2(cls, img_msg, desired_encoding="bgr8"):
        """
        将ros的图片消息转换为cv2的图片:
        img_msg: ros的图片消息
        desired_encoding: 想要的编码格式
            默认为"passthrough", 即不做任何转换;
            其他常用的编码格式有"bgr8", "rgb8", "mono8", "mono16"等
        """
        bridge = CvBridge()
        return bridge.imgmsg_to_cv2(img_msg, desired_encoding)
    
    @classmethod
    def to_topic(cls, topic_name, msg, freq=30, duration=1, wait=True):
        """
        将消息发布到指定的话题上:
        topic_name: 话题名
        msg: 消息
        freq: 发布频率
        duration: 持续时间，单位为秒，若为0则一直发布
        wait: duration>0时是否阻塞直到持续时间结束
        """
        def _publish(topic_name, msg, freq):
            rate = rospy.Rate(freq)
            start_time = rospy.Time.now()
            duration = cls.topic_names[topic_name]['duration']
            while not rospy.is_shutdown():
                if duration != 0 and rospy.Time.now() - start_time > rospy.Duration(duration):
                    break
                if cls.topic_names[topic_name].get('shutdown', False):
                    cls.topic_names[topic_name]['shutdown'] = False
                    break
                cls.topic_names[topic_name]['pub'].publish(msg)
                rate.sleep()
        if topic_name not in cls.topic_names:
            cls.topic_names[topic_name] = {}
            cls.topic_names[topic_name]['pub'] = rospy.Publisher(topic_name, type(msg), queue_size=1)
            cls.topic_names[topic_name]['thread'] = Thread(target=_publish, args=(topic_name, msg, freq, duration))
            cls.topic_names[topic_name]['duration'] = duration
        if not isinstance(msg, Image):
            msg = cls.cv2_to_imgmsg(msg)
        # 持续时间不为0则先杀掉之前的线程然后重启一个线程
        new_thread = False
        if duration != 0 or cls.topic_names[topic_name]['duration'] != 0:
            new_thread = True
            if cls.topic_names[topic_name]['thread'].is_alive():
                cls.topic_names[topic_name]['shutdown'] = True
                cls.topic_names[topic_name]['thread'].join()
                assert cls.topic_names[topic_name]['shutdown'] == False
        cls.topic_names[topic_name]['duration'] = duration
        cls.topic_names[topic_name]['msg'] = msg
        if new_thread:
            cls.topic_names[topic_name]['thread'] = Thread(target=_publish, args=(topic_name, msg, freq, duration))
        if duration != 0 and wait:
            cls.topic_names[topic_name]['thread'].join()


class ROSDevice(object):
    """用于将ROS图像订阅模拟为一个视频设备"""
    ready = ROS_OK
    def __init__(self, name, data_class=Image, queue_size=1) -> None:
        rospy.wait_for_message(name, Image, timeout=1)
        self.ros_device = name
        self.image = None
        self.img_suber = rospy.Subscriber(
            name, Image, queue_size=queue_size, callback=self.img_call_back
        )
        self.__new = Event()

    def read(self):
        if self.__new.wait(timeout=1):  # 图像流帧率不低于1Hz
            self.__new.clear()
            return True, self.image
        else:
            return False, self.image

    def release(self):
        self.img_suber.unregister()

    def img_call_back(self, img_msg):
        image = CvBridge().imgmsg_to_cv2(img_msg)
        self.image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.__new.set()