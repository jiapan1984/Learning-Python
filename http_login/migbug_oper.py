import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import json

user_agent = r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'
headers = {'User-Agent':user_agent, 'Connection':'keep-alive','Referer':'http://migbug.ruijie.net/bug_switch/servlet/query','X-Requested-With':'XMLHttpRequest'}

cookie_filename = 'mibbug.ruijie.net'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
# print(cookie)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

def get_os_list(opener):
	get_url = 'http://migbug.ruijie.net/bug_switch/servlet/operateSystem'
	postdata = b'type=queryAll'
	get_request = urllib.request.Request(get_url,postdata, headers=headers)
	try:
		response = opener.open(get_request)
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


def get_bug_list(opener, os = 0):
	get_url = 'http://migbug.ruijie.net/bug_switch/servlet/query'
	postdata = b'queryBean.start=0&queryBean.limit=30&queryBean.sort=bugId&queryBean.dir=DESC&queryBean.datePrecision=1&queryBean.operateSystemJoin=1557%2C&queryBean.stateArr=2&queryBean.stateArr=3&queryBean.stateArr=6&queryBean.stateArr=18&queryBean.stateArr=16&queryBean.stateArr=4&type=queryResult&header=%5B%7B%22header%22%3A%22BUGID%22%2C%22dataIndex%22%3A%22bugId%22%2C%22width%22%3A80%7D%2C%7B%22header%22%3A%22%E7%8A%B6%E6%80%81%22%2C%22dataIndex%22%3A%22state%22%2C%22width%22%3A100%7D%2C%7B%22header%22%3A%22%E7%AE%80%E8%BF%B0%22%2C%22dataIndex%22%3A%22summary%22%2C%22width%22%3A350%7D%2C%7B%22header%22%3A%22%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%22%2C%22dataIndex%22%3A%22operateSystem%22%2C%22width%22%3A100%7D%2C%7B%22header%22%3A%22%E4%B8%A5%E9%87%8D%E6%80%A7%22%2C%22dataIndex%22%3A%22severity%22%2C%22width%22%3A90%7D%2C%7B%22header%22%3A%22%E4%BC%98%E5%85%88%E7%BA%A7%22%2C%22dataIndex%22%3A%22priority%22%2C%22width%22%3A50%7D%2C%7B%22header%22%3A%22%E9%87%8D%E5%A4%8D%E6%80%A7%22%2C%22dataIndex%22%3A%22repeatable%22%2C%22width%22%3A85%7D%2C%7B%22header%22%3A%22%E6%8F%90%E4%BA%A4%E8%80%85%22%2C%22dataIndex%22%3A%22submiter%22%2C%22width%22%3A80%7D%2C%7B%22header%22%3A%22Bug%E8%B4%9F%E8%B4%A3%E4%BA%BA%22%2C%22dataIndex%22%3A%22charge%22%2C%22width%22%3A80%7D%2C%7B%22header%22%3A%22%E6%8F%90%E4%BA%A4%E6%97%B6%E9%97%B4%22%2C%22dataIndex%22%3A%22submitDate%22%2C%22width%22%3A80%7D%2C%7B%22header%22%3A%22%E5%BC%80%E5%8F%91%E7%BB%84%E9%95%BF%22%2C%22dataIndex%22%3A%22developLeader%22%2C%22width%22%3A100%7D%5D'
	get_request = urllib.request.Request(get_url,postdata, headers=headers)
	try:
		response = opener.open(get_request)
		page = response.read().decode()
		try:
			dic = json.loads(page)
			print(dic['success'])
			print(dic['totalCount'])
			print(type(dic['root']))
		except:
			print("Load page error: " + page)
	except urllib.error.URLError as e:
		print(e.code, ':', e.reason)

if __name__ == '__main__':
	get_bug_list(opener)