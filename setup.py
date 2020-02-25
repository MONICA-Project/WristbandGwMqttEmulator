from setuptools import setup, find_packages

setup(name='wristbands-emulator', version='1.0', packages=find_packages(),
      install_requires=['paho-mqtt', 'numpy', 'pytz', 'apscheduler', 'pymap3d'])
