'''
Created by auto_sdk on 2021.10.12
'''
from dingtalk.api.base import RestApi
class OapiAppstoreOrdersSpecialCanalUpdateOrderRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.ding_order_id = None
		self.status = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.appstore.orders.special_canal.update_order'
