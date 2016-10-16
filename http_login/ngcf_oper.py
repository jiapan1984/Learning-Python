import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import json

user_agent = r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'
headers = {'User-Agent':user_agent, 'Connection':'keep-alive','Referer':'http://ngcf.ruijie.net:8080/ngcf/queryDailyBuild.do?type=skipEverydayQuery','X-Requested-With':'XMLHttpRequest'}

cookie_filename = 'ngcf.ruijie.net'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
# print(cookie)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

get_url = 'http://ngcf.ruijie.net:8080/ngcf/queryDailyBuild.do'
postdata = b'start=0&limit=15&type=query&tree_name=git-rgosm-build&branch_name=11_1_PJ13_B9P3&product=%E8%AF%B7%E8%BE%93%E5%85%A5&build_type=&build_date=&query_start_time=2016-09-15&query_end_time=2016-09-16&result=&error_msg=%E8%AF%B7%E8%BE%93%E5%85%A5&owner=%E8%AF%B7%E8%BE%93%E5%85%A5'

get_request = urllib.request.Request(get_url,postdata, headers=headers)
try:
	response = opener.open(get_request)
	page = response.read().decode()
	try:
		dic = json.loads(page)
		print(dic['totalCount'])
		for item in dic['list']:
			print("product: "+item['product']+', url: '+ item['outputUrl'])
	except:
		print("Load page error: " + page) 

except urllib.error.URLError as e:
	print(e.code, ':', e.reason)



