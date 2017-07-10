----ApiTest.py是单线程循环调用用户画像线上接口
----HttpTest.py是多线程实现，可以在url列表中继续添加全部线上接口，一并监控。



目前由于亮亮查询数据量大的会超时的问题引起的接口：
'http://api.data.social-touch.com:8091/cdapi/req?appid=11&passwd=918672562&appkey=172139920&tagIds=55,1&propertyCondition={"query_type":"and","queryconditionArr":[]}&page=1&pageSize=12&sortFlag=true&sortPropertyName=active_val&sortType=desc&method=getFansListByPropertiesAndTagIds'
超时问题，会在下下礼拜解决，因此临时替换了查询顺序先查询tagid为55的小数据量。
	请求的脚本位置在repository/test下。
	解决后直接跑monitor下ApiTest.py脚本，这个脚本配置的目前一天只执行两次，到时改为15分钟请求一次即可。


如需监控全部接口，换为跑monitor下HttpTest.py脚本