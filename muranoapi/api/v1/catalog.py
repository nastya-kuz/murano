#    Copyright (c) 2014 Mirantis, Inc.
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo.config import cfg
from webob import exc

from muranoapi.db.catalog import api as db_api
from muranoapi.openstack.common import exception
from muranoapi.openstack.common.gettextutils import _  # noqa
from muranoapi.openstack.common import log as logging
from muranoapi.openstack.common import wsgi


LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def _check_content_type(req, content_type):
    try:
        req.get_content_type((content_type,))
    except exception.InvalidContentType:
        msg = _("Content-Type must be '{0}'").format(content_type)
        LOG.debug(msg)
        raise exc.HTTPBadRequest(explanation=msg)


class Controller(object):
    """
        WSGI controller for application catalog resource in Murano v1 API
    """

    def update(self, req, body, package_id):
        """
        List of allowed changes:
            { "op": "add", "path": "/tags", "value": [ "foo", "bar" ] }
            { "op": "add", "path": "/categories", "value": [ "foo", "bar" ] }
            { "op": "remove", "path": "/tags" }
            { "op": "replace", "path": "/tags", "value": ["foo", "bar"] }
            { "op": "replace", "path": "/is_public", "value": true }
            { "op": "replace", "path": "/description",
                                "value":"New description" }
            { "op": "replace", "path": "/name", "value": "New name" }
        """
        _check_content_type(req, 'application/murano-packages-json-patch')
        if not isinstance(body, list):
            msg = _('Request body must be a JSON array of operation objects.')
            LOG.error(msg)
            raise exc.HTTPBadRequest(explanation=msg)
        package = db_api.package_update(package_id, body, req.context)

        return package.to_dict()

    def get(self, req, package_id):
        package = db_api.package_get(package_id, req.context)
        return package.to_dict()


def create_resource():
    return wsgi.Resource(Controller())