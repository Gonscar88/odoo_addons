# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Smile (<http://www.smile.fr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, registry
from openerp.tools.func import wraps


def with_impex_cursor(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with api.Environment.manage():
            with registry(self._cr.dbname).cursor() as new_cr:
                # autocommit: each insert/update request will be performed atomically.
                # Thus everyone (with another cursor) can access to a running impex record
                new_cr.autocommit(True)
                self = self.with_env(self.env(cr=new_cr)).with_context(original_cr=self._cr)
                return method(self, *args, **kwargs)
    return wrapper