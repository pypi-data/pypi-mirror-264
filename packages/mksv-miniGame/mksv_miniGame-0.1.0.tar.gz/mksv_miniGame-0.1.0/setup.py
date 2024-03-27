from setuptools import setup

setup(
    name='mksv_miniGame',
    version='0.1.0',
    author='Linkun Wan, Vanessa Viglucci, Sara Gizabi, Marcus Du',
    author_email='lw2861@nyu.edu, vcv227@nyu.edu, sg7029@nyu.edu, mrd9556@nyu.edu',
    description='Some mini-games using Pygame',
    long_description=open('README.md').read(),
    install_requires=[
        "pygame>=2.5.2",
    ],
    entry_points={
        'console_scripts': [
            'mksv_miniGame = src.minigame:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
