import asyncio
import requests
import re
import json
import os
import sys
import pickle
from bs4 import BeautifulSoup


class gta():
	"""docstring for gtavapi"""
	def __init__(self, resetAuth=False):
		DEFAULT_HEADERS = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.8,nl;q=0.6',
			'Connection': 'keep-alive',
			'Host': 'socialclub.rockstargames.com',
			'Origin': 'https://socialclub.rockstargames.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		}


		
		if os.path.exists('auth.txt'):
			with open('auth.txt', 'r') as auth:
				login = auth.read().splitlines()
				self.username = login[0]
				self.password = login[1]
		else:
			print('no auth file found')
			sys.exit(0)


		self.api = requests.session()

		if os.path.exists('cookies.jar'):
			self.loadCookies()
		#else:
		#	self.signIn()

		self.api.headers = DEFAULT_HEADERS

		if resetAuth is True:
			self.renewAuthentication()

		if os.path.exists('verify.txt'):
			with open('verify.txt') as verify:
				self.verificationToken = verify.read()
		else:
			self.getVerificationToken()

		
		#print(self.getPlayerStats())
			
	def getVerificationToken(self):
		resp = self.api.get('https://socialclub.rockstargames.com/profile/signin')
		tokenRe = re.compile(r'<input name="__RequestVerificationToken" type="hidden" value="(.*)" \/>')
		matches = tokenRe.search(resp.text)
		try:
			with open('verify.txt', 'w') as auth:
				self.verificationToken = matches.group(1)
				auth.write(matches.group(1))
			
			return
		except IndexError:
			raise ValueError('No regex matches for verify token')
			return

	def saveCookies(self):
		with open('cookies.jar', 'wb') as cookie:
			pickle.dump((requests.utils.dict_from_cookiejar(self.api.cookies)), cookie)

	def loadCookies(self):
		with open('cookies.jar', 'rb') as cookie:
			self.api.cookies = requests.utils.cookiejar_from_dict(pickle.load(cookie))

	def signIn(self): #TODO: Actually Work??
		if (self.verificationToken is None):
			raise KeyError("There is no verify token")
		headers = {
			'Accept':'application/json, text/javascript, */*; q=0.01',
			'Content-Type':'application/json; charset=UTF-8',
			'RequestVerificationToken' : self.verificationToken
			}
		body = {
			'login' : self.username,
			'password' : self.password,
			'rememberme' : True
		}
		login = self.api.post('https://socialclub.rockstargames.com/profile/signincompact', data=body, headers=headers)
		if login.status_code == 403:
			raise ValueError("""Signing into SocialClub failed, probably because a CAPTCHA is requested.
				Using this machine, first sign into SocialClub manually using a browser
				and then try to run this script again.""")
		elif login.status_code != 200:
			raise ValueError("""Signing into SocialClub failed. The problem could be anything.
				Please make sure the correct headers are in the HTTP request.""")
		self.saveCookies()
		return

	def renewAuthentication(self):
		self.getVerificationToken()
		self.signIn()
		self.saveCookies()

	def get(self, url):
		return self.api.get('https://socialclub.rockstargames.com/' + url)

	def getPlayerStats(self):
		html = self.get('games/gtav/career/overviewAjax?slot=Freemode').text
		soup = BeautifulSoup(html, 'html.parser')
		player = {
			"general": {
				"rank" : int(self.soupfind(soup, "div", "class", 'rankHex').h3.text),
				"xp" : self.soupfind(soup, "div", "class", 'rankXP').div.h3.text,
				"playTime" : self.soupfind(soup, "div", "class", 'rankBar').h4.text,
				"money" : {
					"cash" : int(self.soupfind(soup, "span", "id", "cash-value").text[1:].replace(',','')),
					"bank" : int(self.soupfind(soup, "span", "id", "bank-value").text[1:].replace(',',''))
				}
			},
			"crew": self.getCrew(soup),
			"freemode" : {
				"races" : {
					"wins" : int(self.soupfind(soup, "p", 'data-name', 'Races')['data-win']),
					"losses" : int(self.soupfind(soup, "p", 'data-name', 'Races')['data-loss']),
					"time" : self.soupfind(soup, "p", 'data-name', 'Races')['data-extra']
				},
				"deathmatches": {
					"wins" : int(self.soupfind(soup, "p", 'data-name', 'Deathmatches')['data-win']),
					"losses" : int(self.soupfind(soup, "p", 'data-name', 'Deathmatches')['data-loss']),
					"time" : self.soupfind(soup, "p", 'data-name', 'Deathmatches')['data-extra']
				},
				"parachuting": {
					"wins" : int(self.soupfind(soup, "p", 'data-name', 'Parachuting')['data-win']),
					"losses" : int(self.soupfind(soup, "p", 'data-name', 'Parachuting')['data-loss']),
					"time" : self.soupfind(soup, "p", 'data-name', 'Parachuting')['data-extra']
				},
				"darts": {
					"wins" : int(self.soupfind(soup, "p", 'data-name', 'Darts')['data-win']),
					"losses" : int(self.soupfind(soup, "p", 'data-name', 'Darts')['data-loss']),
					"time" : self.soupfind(soup, "p", 'data-name', 'Darts')['data-extra']
				},
				"tennis": {
					"wins" : int(self.soupfind(soup, "p", 'data-name', 'Tennis')['data-win']),
					"losses" : int(self.soupfind(soup, "p", 'data-name', 'Tennis')['data-loss']),
					"time" : self.soupfind(soup, "p", 'data-name', 'Tennis')['data-extra']
				},
				"golf": {
					"wins" : int(self.soupfind(soup, "p", 'data-name', 'Golf')['data-win']),
					"losses" : int(self.soupfind(soup, "p", 'data-name', 'Golf')['data-loss']),
					"time" : self.soupfind(soup, "p", 'data-name', 'Golf')['data-extra']
				}
			},
			"money": {
				"total": {
					'spent' : self.soupfind(soup, 'div', 'id', 'cashSpent').p.text,
					'earned' : self.soupfind(soup, 'div', 'id', 'cashEarned').p.text
				},
				"earnedby": {
					'jobs' : self.soupfind(soup, 'div', 'data-name', 'Jobs')['data-cash'],
					'shared' : self.soupfind(soup, 'div', 'data-name', 'Shared')['data-cash'],
					'betting' : self.soupfind(soup, 'div', 'data-name', 'Betting')['data-cash'],
					'car-sales' : self.soupfind(soup, 'div', 'data-name', 'Car Sales')['data-cash'],
					'picked-up' : self.soupfind(soup, 'div', 'data-name', 'Picked Up')['data-cash'],
					'other' : self.soupfind(soup, 'div', 'data-name', 'Other')['data-cash']
				}
			},
			"stats": self.calculateStatisticsBars(self.soupfind(soup, 'ul', 'class', 'Freemode')),
			"criminalrecord": self.parseCriminalRecord(soup)
		}
		return player

	def soupfind(self, soup, tag, element, search):
		return soup.find(tag, {element : search})

	def calculateStatisticsBars(self, soup):
		result = {}
		stats = soup.find_all('li')
		for stat in stats:
			percentage = 0
			progress = stat.find_all('span')
			for prog in progress:
				subP = int((prog.text[:-1],0)[prog.text == '%'])
				percentage += subP
			result[stat.h5.text.lower().replace(" ","-")] = percentage / 5
		return result

	def parseCriminalRecord(self, soup):
		record = soup.find_all('ul', {'class': 'span4col'})
		stat = []
		for item in record:
			for li in item.find_all('li'):
				stat.append(li)
		return {
			'cops-killed' : int(stat[0].p.text.replace(',','')),
			'wanted-stars' : int(stat[1].p.text.replace(',','')),
			'time-wanted' : stat[2].p.text,
			'stolen-vehicles': int(stat[3].p.text.replace(',','')),
			'cars-exported': int(stat[4].p.text.replace(',','')),
			'store-holdups': int(stat[5].p.text.replace(',',''))
		}
	def getCrew(self, soup):
		crew = self.soupfind(soup, 'div', 'class', 'crewCard') if not None else False
		if crew is False:
			return crew
		else:
			crew = crew.div
			self.crew = crew
			return {
				'name': crew.div.h3.a.text,
				'tag' : crew.div.div.span.text.strip(),
				'emblem' : crew.img['src'],
				'colour': crew.div.div.span.span['style'][-6:]
				}

	def favouriteWeapon(self, soup):
		fav = self.soupfind(soup, 'div', 'id', 'faveWeaponWrapper')
		if 'noData' in fav['class']:
			return False
		stats = fav.table.find_all('tr')
		meta = self.soupfind(fav, 'ul', 'class', 'clearfix').find_all('li')
		return {
			'name' : self.soupfind(fav, 'div', 'class', 'imageHolder').h4.text,
			'image' : self.soupfind(fav, 'div', 'class', 'imageHolder').img.src,
			'stats' : {
				'damage' : int(stats[0].td.span.text[-1:]),
				'fire-rate': int(stats[1].td.span.text[-1:]),
				'accuracy': int(stats[2].td.span.text[-1:]),
				'range': int(stats[3].td.span.text[-1:]),
				'clip-size': int(stats[4].td.span.text[-1:])
			},
			'kills': int(meta[0].p.text),
			'headshots': int(meta[1].p.text),
			'accuracy': float(meta[2].p.text[-1:]),
			'time-held': meta[3].p.text
		}
		