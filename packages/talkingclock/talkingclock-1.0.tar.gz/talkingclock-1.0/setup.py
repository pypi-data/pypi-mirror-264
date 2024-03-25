from setuptools import setup, find_packages

setup(
    name='talkingclock',
    version='1.0',
    author='Sakchart Ngamluan',
    author_email='kcommerce@gmail.com',
    description='A Python utility library for talking clock',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kcommerce/py-talkingclock',
    license='MIT',
    packages=find_packages(where="src"),
    include_package_data=True,
    package_dir={"":"src"}, 
    package_data={
        'talkingclock': ["*.txt","*.ics","mp3/*.mp3"],
    },
    install_requires=[
        'playsound','icalendar'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
