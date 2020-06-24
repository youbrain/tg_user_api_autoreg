from requests import get

from random import choices
from string import (ascii_lowercase, digits)



class Reg_exeption(Exception):
	''' module Exception class '''
    def __init__(self, text):
        self.txt = text


class Reigister_api:
	def __str__(self):
		return str(self.api_data())


	def __repr__(self):
		return str(self.api_data())


	def __init__(self, phone_number, proxy, *args, **kwargs):
		''' 
		Args:
			phone_number (String): Phone number for registration 
			proxy (String): Proxy to use for registration
		Returns:
			None
		'''
		self.urls = kwargs.get('urls') if kwargs.get('urls') else self.urls
		self.phone_number = phone_number
		self.proxy = proxy
		self.code = None
		self.cookies = None
		self.stel_token = None
		self.api_id = None
		self.api_hash = None

		if kwargs.get('send_code'):
			# shortly way to reg
			self.send_code()


	''' default links for parsing telegram.org (for 23.06.2020)'''
	urls = {
		'send_code': 'https://my.telegram.org/auth/send_password?phone=%s',
		'login': 'https://my.telegram.org/auth/login?phone=%s&random_hash=%s&password=%s',
		'create': 'https://my.telegram.org/create?hash=%s&app_title=%s&app_shortname=%s&app_url=&app_platform=android&app_desc=',
		'apps': 'https://my.telegram.org/apps'
	}


	def api_data(self):
		''' collecting all available information
		Args:
			None
		Returns:
			dict: All available info
		'''
		out = {
			'phone_number': self.phone_number,
			'proxy': self.proxy,
		}

		if self.code:
			out.update({'code': self.code})

		if self.cookies:
			out.update({'cookies': self.cookies})

		if self.stel_token:
			out.update({'stel_token': self.stel_token})

		if self.random_hash:
			out.update({'random_hash': self.random_hash})

		if self.api_id:
			out.update({'api_id': self.api_id})

		if self.api_hash:
			out.update({'api_hash': self.api_hash})

		return out

	def get_api(self, code):
		''' minimal (lines) way to use lib (if only send_code = True on  initing)
		Args:
			code (String): confirmation code (msg from offitial telegramm account)
		Returns:
			dict: All available info
		'''
		self.login(code)
		self.create_api()
		self.parse_api_data()

		return self.api_data()

	def send_code(self):
		''' Sending request for sending code)
		Args:
			None
		Returns:
			String: random_hash (for site sesion).
		'''
		response = get(self.urls['send_code'] % self.phone_number)
		self.code = response.status_code
		try:
			self.random_hash = response.text.split('"')[3]
		except IndexError:
			raise Reg_exeption('Exception: Send code error (to many send code requests)')

		return self.random_hash

	def login(self, password):
		''' Logining in telegram.org
		Args:
			password (String): confirmation code (msg from offitial telegramm account)
		Returns:
			dict: All cookies from domain
		'''
		response = get(self.urls['login'] % (self.phone_number, self.random_hash, password))
		self.code = response.status_code
		self.cookies = response.cookies.get_dict()
		self.stel_token = self.cookies['stel_token']
		return self.cookies

	def create_api(self):
		''' Generating random 'App title' and 'Short name', creating api
		Args:
			None
		Returns:
			int: Request status code
		'''
		idi = ''.join(choices(ascii_lowercase + digits, k=32))
		response = get(self.urls['create'] % (self.random_hash, idi, idi), cookies=self.cookies)
		self.code = response.status_code
		return self.code

	def parse_api_data(self):
		''' Parsing api_id and api_hash from page
		Args:
			None
		Returns:
			dict: Dictionary with api_id, api_hash
		'''
		response = get(self.urls['apps'], cookies=self.cookies)
		self.code = response.status_code

		parts = response.text.split('</strong></span>\n      </div>\n      <div class="col-md-1">')
		api_id = parts[0].split('onclick="this.select();"><strong>')[-1]
		api_hash = parts[1].split('input-xlarge uneditable-input" onclick="this.select();">')[1].split('</span>')[0]

		self.api_id = api_id
		self.api_hash = api_hash

		return {'api_id': api_id, 'api_hash': api_hash}