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
	headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}


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
			print("URL Error:", e.reason)
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
	def http_error_302(self, req, resp, code, msg, hdrs):
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
	os_table = {}
	state_table = {
		"未决": [2,3,6,18,16,4],
		"开发未关闭":[5, 14],
		"测试未关闭":[13],
		"非Bug":[8, 17, 21],
		"delay":[]
	}
	report_table = {
		"本周解决":23,
		"本周新增":13,
		"上周解决": 24,
		"上周新增": 14
	}

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
				for item in dic['root']:
					MIGBUG.os_table[item['value']] = item['id']
				print("OS num: %d" % len(MIGBUG.os_table))
			except:
				print("Load page error: " + page)
		except urllib.error.URLError as e:
			print(e.code, ':', e.reason)

	def get_os_id(self, os_name):
		return MIGBUG.os_table[os_name]

	def get_user_list(self):
		pass

	@staticmethod
	def make_query_param(start=0, limit=30, sort="bugId", dir="DESC", datePrecision=1, reportType=None,
						 os=[], type="queryResult", state=[], header=None):
		param = {}
		param["queryBean.start"] = start
		param["queryBean.limit"] = limit
		param["queryBean.sort"] = sort
		param["queryBean.dir"] = dir
		param["queryBean.datePrecision"] = datePrecision
		if reportType:
			param["queryBean.reportType"] = reportType
		str = ""
		for i in os:
			str = "%s%d," % (str, i)
		param["queryBean.operateSystemJoin"] = str
		str = ""
		for st in state:
			str = "%s&%s" % (str, urllib.parse.urlencode({"queryBean.stateArr":st}))

		param["type"] = type
		param["header"] = '[{"header": "BUGID","dataIndex":"bugId","width":80},' \
						  '{"header":"状态","dataIndex":"state","width":100},' \
						  '{"header":"简述","dataIndex":"summary","width":350},' \
						  '{"header":"操作系统","dataIndex":"operateSystem","width":100},' \
						  '{"header":"严重性","dataIndex":"severity","width":90},' \
						  '{"header":"优先级","dataIndex":"priority","width":50},' \
						  '{"header":"重复性","dataIndex":"repeatable","width":85},' \
						  '{"header":"提交者","dataIndex":"submiter","width":80},' \
						  '{"header":"Bug负责人","dataIndex":"charge","width":80},' \
						  '{"header":"提交时间","dataIndex":"submitDate","width":80},' \
						  '{"header":"开发组长","dataIndex":"developLeader","width":100}]'
		return (urllib.parse.urlencode(param) + str).encode("utf-8")

	def query_bug(self, os=[], state="all", dev_type="all", report_type = None):
		get_url = 'http://migbug.ruijie.net/bug_switch/servlet/query'
		os_list = []
		for os_name in os:
			os_list.append(self.get_os_id(os_name))
		st_list = MIGBUG.state_table[state]
		if report_type:
			report_type = MIGBUG.report_table[report_type]

		postdata = MIGBUG.make_query_param(os = os_list, state=st_list, reportType = report_type)
		headers = {'User-Agent': RJ_Service.user_agent, 'Connection': 'keep-alive',
				   'Referer': 'http://migbug.ruijie.net/bug_switch/servlet/query', 'X-Requested-With': 'XMLHttpRequest'}
		get_request = urllib.request.Request(get_url, postdata, headers=headers)
		try:
			response = self.opener.open(get_request)
			page = response.read().decode()
			try:
				dic = json.loads(page)
				print("success:", dic['success'])
				print("TotalCount", dic['totalCount'])
				for bug in dic["root"]:
					print("ID:", bug["bugId"], " 负责人", bug["charge"], "提交人",
						  bug["submiter"], "摘要: ", bug["summary"])
			except:
				print("Load page error: " + page)
		except urllib.error.URLError as e:
			print(e.code, ':', e.reason)


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
		print(bug.get_os_id("11.1PJ13"))
		print(bug.get_os_id("11.1PJ13-B9"))
		print(bug.make_query_param(os=[1,2,3], state=[1,2,3,4]))
		bug.query_bug(os=["11.1PJ13-B9"], state="未决")

	if ngcf.login():
		print("NGCF login success")

