from setuptools import setup, find_packages

setup(
    name='myf_face_recognition',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'keras-facenet',
        'opencv-python',
        'mtcnn',
        'ultralytics'
    ],
    entry_points={
        'console_scripts': [
            'myf_face_recognition=myf_face_recognition.__main__:main'
        ]
    },
    author='Virendrakumar Bind',
    author_email='finalyearprojectetc@gmail.com',
    description='An easy-to-use yet powerful Python library for face recognition tasks.',
    license='MIT',
    keywords='face-recognition',
    url='https://github.com/VirNotFound/myf_face_recognition_updated',
)
