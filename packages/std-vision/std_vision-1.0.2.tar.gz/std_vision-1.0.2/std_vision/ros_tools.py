import rospy
import os


class RosTools(object):
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
