from setuptools import setup


"""
set App Name
"""
name = "FastCNN2"
version = '1.24.0327.0004'

author = "Iuty"
author_email = "dfdfggg@126.com"

"""
set entry_points
"""
entry_points={
        'console_scripts': [
            "gongda = FastCNN.entry.gongda:main",
            "sfcnn = FastCNN.entry.server:main",
            "vfcnn = FastCNN.entry.trainvisiable:main",
            "tfcnn = FastCNN.entry.train:main",
            "tfcnn2 = FastCNN.entry.train2:main",
            "sfcnn2 = FastCNN.entry.server2:main",
            "tfcnnyv5 = FastCNN.entry.trainyolov5:main",
            "sfcam = FastCNN.entry.camera:main",
        ]
    }

"""
set dependents
"""

install_requires = [
        "flask",
        "flask_restful",
        "flask_cors",
        "efficientnet-pytorch",
        "scikit-build",
        "opencv-python",
        "pandas",
        "requests",
        "pyyaml",
        "tqdm",
        "seaborn",
        "IutyLib",
        "tensorflow==2.0",
        "urllib3==1.26.7"
        ]

"""
set pip install packages 
"""
packages = [
        "FastCNN.entry",
        "FastCNN.prx",
        "FastCNN.datasets",
        "FastCNN.api",
        "FastCNN.nn",
        "FastCNN.utils",
        "FastCNN.utils.loggers",
        "FastCNN.utils.loggers.wandb",
        "FastCNN.models",
        ]

setup(
    name=name,
    version= version,
    author = author,
    author_email = author_email,
    packages=packages,
    entry_points=entry_points,
    install_requires = install_requires
)