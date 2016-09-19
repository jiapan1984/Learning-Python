#!/usr/bin/env python3.4
# 
"""
__author__ = 'jiapan'
__email__ = 'jiapan@ruijie.com.cn'

"""
import urllib.request, urllib.parse, urllib.error
import http.cookiejar


user_agent = r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'
headers = {'User-Agent':user_agent, 'Connection':'keep-alive'}

def login_ruijie_sso(username, password, debug=0):
	sso_url = 'https://sso.ruijie.net:8443/cas/login'
	upstr = "username=%s&password=%s" % (username, password)
	postdata = upstr.encode('utf-8') +  b"&lt=e1s1&_eventId=submit&submit=%E7%99%BB%E5%BD%95"
	cookie_filename = 'sso.ruijie.net'
	cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
	handler = urllib.request.HTTPCookieProcessor(cookie)
	opener = urllib.request.build_opener(handler)
	req = urllib.request.Request(sso_url, headers=headers)
	try:
		response = opener.open(req)
		page = response.read().decode()
	except urllib.error.URLError as e:
		print(e.code, ':', e.reason)

	req = urllib.request.Request(sso_url, postdata, headers)
	try:
		response = opener.open(req)
    	# page = response.read().decode()
	except urllib.error.URLError as e:
		print(e.code, ':', e.reason)

	cookie.save(ignore_discard=True, ignore_expires=True)
	if debug == 1:
		print(cookie)
		for item in cookie:
			print('Name=' + item.name)
			print('Value=' + item.value)



class RedirectHandler(urllib.request.HTTPRedirectHandler):
	def http_error_302(self, req, resp, code,msg,hdrs):
		self.location = hdrs['Location']


def login_ruijie_ngcf(debug=0):
	cookie_filename = 'sso.ruijie.net'
	cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
	cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
	cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
	get_url = r'https://sso.ruijie.net:8443/cas/login?service=http%3A%2F%2Fngcf.ruijie.net%3A8080%2Fngcf%2Fsvn2Index.jsp'
	red_handler = RedirectHandler()
	opener = urllib.request.build_opener(cookie_handler, red_handler)
	get_request = urllib.request.Request(get_url, headers=headers)
	try:
		response = opener.open(get_request)
		page = response.read()
	except urllib.error.URLError as e:
		print(e.code, ':', e.reason)
		if debug == 1:
			print(red_handler.location)

	# save ngcf cookie.
	cookie_filename = 'ngcf.ruijie.net'
	cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
	cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
	opener = urllib.request.build_opener(cookie_handler)
	get_request = urllib.request.Request(red_handler.location, headers=headers)
	try:
		response = opener.open(get_request)
	except error.URLError as e:
		print(e.code, ':', e.reason)

	cookie.save(ignore_discard=True, ignore_expires=True)
	

if __name__ == '__main__':
	user = input("user:")
	pwd = input("password:")
	login_ruijie_sso(user, pwd)
	login_ruijie_ngcf()
	

