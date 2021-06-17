# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

from setuptools import setup

if __name__ == '__main__':

    long_description = open('README').read()

    setup(
        name='solentware-misc',
        version='1.1.1',
        description='Classes perhaps useful beyond original application',
        author='Roger Marsh',
        author_email='roger.marsh@solentware.co.uk',
        url='http://www.solentware.co.uk',
        package_dir={'solentware_misc':''},
        packages=[
            'solentware_misc',
            'solentware_misc.api', 'solentware_misc.gui',
            'solentware_misc.workarounds',
            'solentware_misc.about',
            ],
        package_data={
            'solentware_misc.about': ['LICENCE', 'CONTACT'],
            },
        long_description=long_description,
        license='BSD',
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Operating System :: OS Independent',
            'Topic :: Software Development',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta',
            ],
        )
