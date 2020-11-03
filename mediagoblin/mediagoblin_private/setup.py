# mediagoblin-private, a MediaGoblin plugin
# Copyright (C) 2016 Jerome Lebleu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

__version__ = '0.2.0'

with open('README.rst') as fobj:
    long_description = fobj.read()

setup(
    name='mediagoblin_private',
    version=__version__,
    description='Restrict the access of anonymous users',
    long_description=long_description,
    url='https://code.maroufle.fr/jerome/mediagoblin-private',
    author='Jerome Lebleu',
    author_email='jerome.lebleu@mailoo.org',
    packages=['mediagoblin_private'],
    include_package_data=True,
    license='AGPLv3',
)
