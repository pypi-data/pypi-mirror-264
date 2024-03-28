from setuptools import setup

setup(
    name='mksv_miniGame',
    version='0.1.7',
    author='Linkun Wan, Vanessa Viglucci, Sara Gizabi, Marcus Du',
    author_email='lw2861@nyu.edu, vcv227@nyu.edu, sg7029@nyu.edu, mrd9556@nyu.edu',
    description='Some mini-games using Pygame',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_data={
        'minigame': ['*.png'], 
    },
    install_requires=[
        "pygame>=2.5.2",
    ],
    entry_points={
        'console_scripts': [
            'mksv_miniGame = minigame.__main__:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
