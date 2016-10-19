#!/usr/bin/env python3.4
#
"""
__author__ = 'jiapan'
__email__ = 'jiapan@ruijie.com.cn'

"""
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import os
import json

class RJ_Service:
	user_agent = r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'
	headers = {'User-Agent':user_agent, 'Connection':'keep-alive'}

class RJ_SSO(RJ_Service):
	cookie_name = "sso.ruijie.net"
	url = 'https://sso.ruijie.net:8443/cas/login'
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.is_login = False
		if not os.path.exists(username):
			os.mkdir(username, 0o777)
		self.cookie_file = username + os.sep + self.cookie_name

	def get_cookie_file(self):
		return self.cookie_file

	def get_cookie_path(self):
		return self.username + os.sep

	def login(self):
		if self.is_login:
			return True
		upstr = "username=%s&password=%s" % (self.username, self.password)
		postdata = upstr.encode('utf-8') + b"&lt=e1s1&_eventId=submit&submit=%E7%99%BB%E5%BD%95"
		cookie = http.cookiejar.MozillaCookieJar(self.cookie_file)
		handler = urllib.request.HTTPCookieProcessor(cookie)
		opener = urllib.request.build_opener(handler)
		req = urllib.request.Request(self.url, headers=self.headers)
		try:
			response = opener.open(req)
			page = response.read().decode()
			# 没有考虑网络不通的情况.
		except urllib.error.URLError as e:
			print("URL Error:" , e.reason)
			return False

		req = urllib.request.Request(self.url, postdata, self.headers)
		try:
			response = opener.open(req)
		except urllib.error.URLError as e:
			print("URL Error:", e.reason)
			return False

		for item in cookie:
			# 判断是否登陆成功，cookie中包含castgc才算成功.
			if item.name == "CASTGC":
				self.is_login = True
				cookie.save(ignore_discard=True, ignore_expires=True)
				return True
		return False

	def logout(self):
		pass


class RedirectHandler(urllib.request.HTTPRedirectHandler):
	def http_error_302(self, req, resp, code,msg,hdrs):
		self.location = hdrs['Location']

class RJ_DevService(RJ_Service):
	service = ""
	cookie_name = ""

	def __init__(self, sso):
		self.sso = sso
		self.is_login = False
		self.opener = None

	def get_cookie_file(self):
		return self.sso.get_cookie_path() + self.cookie_name

	def login(self):
		cookie_filename = self.sso.get_cookie_file()
		cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
		cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
		cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
		get_url = 'https://sso.ruijie.net:8443/cas/login?%s' % urllib.parse.urlencode({"service": self.service})
		red_handler = RedirectHandler()
		opener = urllib.request.build_opener(cookie_handler, red_handler)
		get_request = urllib.request.Request(get_url, headers=self.headers)
		try:
			response = opener.open(get_request)
			page = response.read()
		except urllib.error.URLError as e:
			print(e.code, ':', e.reason)
			print(red_handler.location)

		cookie_filename = self.get_cookie_file()
		cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
		cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
		self.opener = urllib.request.build_opener(cookie_handler)
		get_request = urllib.request.Request(red_handler.location, headers=self.headers)
		try:
			response = self.opener.open(get_request)
		except error.URLError as e:
			print(e.code, ':', e.reason)
		cookie.save(ignore_discard=True, ignore_expires=True)
		return True


class MIGBUG(RJ_DevService):
	service = "http://migbug.ruijie.net/bug_switch/servlet/main"
	cookie_name = "migbug.ruijie.net"

	def get_os_list(self):
		get_url = 'http://migbug.ruijie.net/bug_switch/servlet/operateSystem'
		headers = {'User-Agent': self.user_agent, 'Connection': 'keep-alive',
				   'Referer': 'http://migbug.ruijie.net/bug_switch/servlet/query', 'X-Requested-With': 'XMLHttpRequest'}

		postdata = b'type=queryAll'
		get_request = urllib.request.Request(get_url, postdata, headers=headers)
		try:
			response = self.opener.open(get_request)
			page = response.read().decode()
			try:
				dic = json.loads(page)
				print(dic['success'])
				print(type(dic['root']))
				for list in dic['root']:
					print(list['id'], list['value'])
			except:
				print("Load page error: " + page)
		except urllib.error.URLError as e:
			print(e.code, ':', e.reason)


	def get_user_list(self):
		pass

	def get_bug(self, os="all", state="all", dev_type="all"):
		pass

class NGCF(RJ_DevService):
	service = "http://ngcf.ruijie.net:8080/ngcf/svn2Index.jsp"
	cookie_name = "ngcf.ruijie.net"

	def get_daily_build_info(self, os, date=None):
		pass

if __name__ == "__main__":
	user = input("user:")
	pwd = input("password:")
	sso = RJ_SSO(user, pwd)
	bug = MIGBUG(sso)
	ngcf = NGCF(sso)
	if sso.login():
		print("SSO Login success")
	if bug.login():
		print("Bug login success")
		bug.get_os_list()
	if ngcf.login():
		print("NGCF login success")
