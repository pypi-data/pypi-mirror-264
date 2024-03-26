from setuptools import setup, find_packages

setup(
    name="std_vision",
    version="1.0.4",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=["numpy", "matplotlib", "opencv-python"],
    author="OpenGHz",
    author_email="ghz23@mails.tsinghua.edu.cn",
    description="Vision tools for easily processing videos and images.",
    url="https://gitlab.com/OpenGHz/airbot_play_vision_python.git",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
