# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#  This file is part of the cogniva parsing tool.                            #
#                                                                            #
#  cogniva is free software: you can redistribute it and/or modify           #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  cogniva is distributed in the hope that it will be useful,                #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with cogniva. If not, see <http://www.gnu.org/licenses/>.           #
#                                                                            #
##############################################################################

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='cogniva',
      version='1.0',
      description="cogniva is a python script best suitied for reporting environment modules usage in HPC contexts",
      url='https://github.com/epfl-scitas/cogniva',
      author='EPFL SCITAS',
      author_email='scitas@epfl.ch',
      scripts=['bin/cogniva'],
      packages=['cogniva'],
      license='GPLv3',
      zip_safe=False)
