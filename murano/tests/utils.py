# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from murano import context
from murano.db import models
from murano.db import session
from murano.openstack.common.db import options


def setup_dummy_db():
    options.cfg.set_defaults(options.database_opts, sqlite_synchronous=False)
    options.set_defaults(sql_connection="sqlite://", sqlite_db='murano.db')
    models.register_models(session.get_engine())


def reset_dummy_db():
    models.unregister_models(session.get_engine())


def dummy_context(user='test_username', tenant_id='test_tenant_id',
                  password='password', roles=[], user_id=None):
    return context.RequestContext.from_dict({
        'tenant': tenant_id,
        'user': user,
        #'roles': roles,  # Commented until policy check changes land
        'is_admin': False,

    })


def save_models(*models):
    s = session.get_session()
    for m in models:
        m.save(s)
