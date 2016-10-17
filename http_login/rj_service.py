class RJ_Service:
	service = ""
	cookie_name = "sso.ruijie.net"
	user_agent = r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'
	header = {'User-Agent':user_agent, 'Connection':'keep-alive'}
	def __init__(self, user, password):
		self.user = user
		self.password = password


class MIGBUG(RJ_Service):
	service = "http://migbug.ruijie.net/bug_switch/servlet/main"
	cookie_name = "migbug.ruijie.net"

class NGCF(RJ_Service):
	service = "http://ngcf.ruijie.net:8080/ngcf/svn2Index.jsp"
	cookie_name = "ngcf.ruijie.net"