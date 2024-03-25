# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''Interface for the cloud. Needed for ansar CLI.

Defined here so that dependency is from cloud to ansar-connect, rather
than linking ansar-connect to the cloud. Cloud codebase not dragged into
this library.
'''

import ansar.connect as ar
from ansar.connect.product import *

__all__ = [
	'FOH_PORT',
	'AccountSignup',
	'AccountLogin',
	'AccountRead',
	'AccountUpdate',
	'AccountDelete',
	'AccessRead',
	'AccessUpdate',
	'AccessExport',
	'AccountOpened',
	'DirectoryAccessExported',
	'DirectoryAccessPage',
	'DirectoryPage',
	'AccountPage',
	'LoginPage',
	'LoginDeleted',
	'AccountDeleted',
	'DirectoryDeleted',
	'DirectoryAccessDeleted',
]

FOH_PORT=5022

# Forms to present to the cloud foh.
# Open an existing session with an account/developer
class AccountSignup(object):
	def __init__(self, login_email=None, password=None,
			family_name=None, given_name=None, nick_name=None, honorific=None,
			organization_name=None, organization_location=None):
		self.login_email = login_email
		self.password = password
		self.family_name = family_name
		self.given_name = given_name
		self.nick_name = nick_name
		self.honorific = honorific
		self.organization_name = organization_name
		self.organization_location = organization_location

class AccountLogin(object):
	def __init__(self, login_email=None, password=None):
		self.login_email = login_email
		self.password = password

class AccountRead(object):
	def __init__(self, login_token=None):
		self.login_token = login_token

class AccountUpdate(object):
	def __init__(self, login_token=None, organization_name=None, organization_location=None):
		self.login_token = login_token
		self.organization_name = organization_name
		self.organization_location = organization_location

class AccountDelete(object):
	def __init__(self, login_token=None):
		self.login_token = login_token

class AccessRead(object):
	def __init__(self, login_token=None, access_id=None):
		self.login_token = login_token
		self.access_id = access_id

class AccessUpdate(object):
	def __init__(self, login_token=None, access_id=None):
		self.login_token = login_token
		self.access_id = access_id

class AccessExport(object):
	def __init__(self, login_token=None, access_id=None, access_name=None):
		self.login_token = login_token
		self.access_id = access_id
		self.access_name = access_name

SHARED_SCHEMA = {
	"login_token": ar.UUID(),
	"login_email": ar.Unicode(),
	"password": ar.Unicode(),
	"family_name": ar.Unicode(),
	"given_name": ar.Unicode(),
	"nick_name": ar.Unicode(),
	"honorific": ar.Unicode(),
	"organization_name": ar.Unicode(),
	"organization_location": ar.Unicode(),
	"account_id": ar.UUID(),
	"directory_product": ar.Unicode(),
	"directory_instance": InstanceOfProduct,
	"access_id": ar.UUID(),
	"exported_access": ar.VectorOf(ar.Unicode()),
	"control_tag": ar.VectorOf(ar.Unicode()),
	"directory_id": ar.UUID(),
	"account_id": ar.UUID(),
	"technical_contact": ar.VectorOf(ar.Any()),
	"financial_contact": ar.VectorOf(ar.Any()),
	"administrative_contact": ar.VectorOf(ar.Any()),
	"login_id": ar.UUID(),
	"assigned_directory": ar.SetOf(ar.UUID()),
	"access_token": ar.UUID(),
	"access_name": ar.Unicode(),
}

ar.bind(AccountSignup, object_schema=SHARED_SCHEMA)
ar.bind(AccountLogin, object_schema=SHARED_SCHEMA)
ar.bind(AccountRead, object_schema=SHARED_SCHEMA)
ar.bind(AccountUpdate, object_schema=SHARED_SCHEMA)
ar.bind(AccountDelete, object_schema=SHARED_SCHEMA)
ar.bind(AccessRead, object_schema=SHARED_SCHEMA)
ar.bind(AccessUpdate, object_schema=SHARED_SCHEMA)
ar.bind(AccessExport, object_schema=SHARED_SCHEMA)

# Forms and responses to present to cloud clients.
class AccountOpened(object):
	def __init__(self, login_token=None):
		self.login_token = login_token

# Read/update response covered by AccountPage.

class LoginDeleted(object): pass
class AccountDeleted(object): pass
class DirectoryDeleted(object): pass
class DirectoryAccessDeleted(object): pass

class DirectoryAccessExported(object):
	def __init__(self, access_id=None, access_token=None, account_id=None, directory_id=None):
		self.access_id = access_id
		self.access_token = access_token
		self.account_id = account_id
		self.directory_id = directory_id

class DirectoryAccessPage(object):
	def __init__(self, access_id=None, exported_access=None, control_tag=None):
		self.access_id = access_id			# Unique key.
		self.exported_access = exported_access
		self.control_tag = control_tag or ar.default_vector()
		# Expiry
		# Number of concurrent accesses
		# Number of total accesses.

class DirectoryPage(object):
	def __init__(self, directory_id=None, directory_product=None, directory_instance=None, control_tag=None, access_page=None):
		self.directory_id = directory_id			# Unique key.
		self.directory_product = directory_product
		self.directory_instance = directory_instance
		self.control_tag = control_tag or ar.default_vector()
		# Number of routes/relays
		# Message rate
		# Bytes rate
		self.access_page = access_page or ar.default_vector()

class AccountPage(object):
	def __init__(self, account_id=None,
			organization_name=None, organization_location=None, technical_contact=None, financial_contact=None, administrative_contact=None,
			control_tag=None,
			directory_page=None):
		self.account_id = account_id				# Unique key.
		self.organization_name = organization_name
		self.organization_location = organization_location
		self.technical_contact = technical_contact or ar.default_vector()
		self.financial_contact = financial_contact or ar.default_vector()
		self.administrative_contact = administrative_contact or ar.default_vector()
		# Payment
		# Invoices
		self.control_tag = control_tag or ar.default_vector()

		self.directory_page = directory_page or ar.default_vector()

class LoginPage(object):
	def __init__(self, login_id=None, login_email=None,
			account_id=None, assigned_directory=None,
			family_name=None, given_name=None, nick_name=None, honorific=None):
		self.login_id = login_id			# Unique key.
		self.login_email = login_email
		self.account_id = account_id		# Belong to this account.
		self.assigned_directory = assigned_directory or ar.default_set()	# Assigned use of.
		self.family_name = family_name
		self.given_name = given_name
		self.nick_name = nick_name
		self.honorific = honorific

ar.bind(AccountOpened, object_schema=SHARED_SCHEMA)
ar.bind(DirectoryAccessExported, object_schema=SHARED_SCHEMA)
ar.bind(DirectoryAccessPage, object_schema=SHARED_SCHEMA)

ACCESS_SCHEMA = {
	"access_page": ar.VectorOf(DirectoryAccessPage),
}
ACCESS_SCHEMA.update(SHARED_SCHEMA)

ar.bind(DirectoryPage, object_schema=ACCESS_SCHEMA)

DIRECTORY_SCHEMA = {
	"directory_page": ar.VectorOf(DirectoryPage),
}
DIRECTORY_SCHEMA.update(ACCESS_SCHEMA)

ar.bind(AccountPage, object_schema=DIRECTORY_SCHEMA)
ar.bind(LoginPage, object_schema=SHARED_SCHEMA)
ar.bind(LoginDeleted, object_schema=SHARED_SCHEMA)
ar.bind(AccountDeleted, object_schema=SHARED_SCHEMA)
ar.bind(DirectoryDeleted, object_schema=SHARED_SCHEMA)
ar.bind(DirectoryDeleted, object_schema=SHARED_SCHEMA)
