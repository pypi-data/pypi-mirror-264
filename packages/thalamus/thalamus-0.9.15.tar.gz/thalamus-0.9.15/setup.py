#!/usr/bin/env python
# SPDX-FileCopyrightText: 2017-2024 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2017-2024 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
# Thalamus, the GNU Health Federation Message and Authentication Server #
#                                                                       #
#             Thalamus is part of the GNU Health project                #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                           Thalamus package                            #
#                       setup.py: Setuptools file                       #
#########################################################################

from setuptools import setup, find_packages

long_desc = open("README.rst").read()

version = open("version").read().strip()

setup(name='thalamus',
      version=version,
      description='The GNU Health Federation Message'
                  ' and Authentication Server',
      keywords='health API REST',
      long_description=long_desc,
      platforms='any',
      author='GNU Solidario',
      author_email='health@gnusolidario.org',
      url='https://www.gnuhealth.org',
      download_url='http://ftp.gnu.org/gnu/health',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        ],
      install_requires=[
        "flask",
        "flask-cors"
        "flask_httpauth",
        "flask_restful",
        "flask_wtf",
        "psycopg2-binary",
        "bcrypt",
      ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      )
