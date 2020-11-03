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

import logging
import re

from werkzeug.exceptions import Unauthorized

from mediagoblin import meddleware
from mediagoblin.tools import pluginapi
from mediagoblin.tools.translate import pass_to_ugettext as _

_log = logging.getLogger(__name__)


class LoginRestrictionMeddleware(meddleware.BaseMeddleware):
    _setup_plugin_called = 0

    # Plugin configuration
    deny_access = True
    path_exceptions = set()
    path_regex_exceptions = set()

    def process_request(self, request, controller):
        """Restrict the access as needed if the user is not logged in"""
        # Skip restriction if the user is logged in or if the requested
        # path starts with /auth/
        if ((request.user or
             request.path.startswith('/auth/'))):
            return

        deny = self.deny_access

        # Check if requested route has another restriction
        # than the default one
        if request.path in self.path_exceptions:
            deny = not deny
        else:
            for regex in self.path_regex_exceptions:
                if regex.match(request.path):
                    deny = not deny
                    break

        # Raise if the user is not authorized
        if deny:
            raise Unauthorized(
                _('You must be logged in to access this page.'))

    @classmethod
    def setup_plugin(cls):
        """Set up this meddleware as a plugin during 'setup' hook"""
        global _log

        if cls._setup_plugin_called:
            _log.info('private plugin was already set up.')
            return

        _log.info('Setting up private plugin...')

        # Retrieve and set plugin configuration
        config = pluginapi.get_config('mediagoblin_private')
        if config:
            cls.deny_access = config['deny_access']
            for path in config['path_exceptions']:
                # Normalize route path with ending slash
                if path[-1] != '/':
                    path += '/'
                cls.path_exceptions.add(path)
            for regex in config['path_regex_exceptions']:
                cls.path_regex_exceptions.add(re.compile(regex))

        _log.info('Done setting up private plugin!')
        cls._setup_plugin_called += 1

        # Append ourselves to the list of enabled Meddlewares
        meddleware.ENABLED_MEDDLEWARE.append(
            '{0}:{1}'.format(cls.__module__, cls.__name__))


hooks = {
    'setup': LoginRestrictionMeddleware.setup_plugin
}
