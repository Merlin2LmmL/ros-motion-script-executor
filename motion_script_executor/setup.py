from setuptools import find_packages, setup

package_name = 'motion_script_executor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Merlin Ortner',
    maintainer_email='ortnermerlin@gmail.com',
    description='Executes sequential robot motion commands from a predefined instruction list or external JSON file using ROS2 publishers.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'motion_script_executor = motion_script_executor.motion_script_executor:main'
        ],
    },
)
