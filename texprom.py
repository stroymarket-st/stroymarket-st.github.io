#!/usr/bin/env python
# -*- coding: utf-8 -*-

#sudo apt-get install python3-bs4

import requests
import re

from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag, NavigableString

def get_html(url):
	try:
		response = requests.get(url)
	except requests.Timeout:
		out = "GET_HTML: Ошибка timeout, url: " + url
		print(out)
		return "Error"
	except requests.HTTPError as error:
		out = "GET_HTML: Ошибка url  (0), код: (1)".format(url, code)
		print(out)
		return "Error"
	except requests.RequestException:
		out = "GET_HTML: Ошибка скачивания " + url
		print(out)
		return "Error"
	else:
		return response.text

def get_parse_data(html):
	parser = BeautifulSoup(html, 'html.parser')
	return parser

def get_texprom_categories_childs(url, space):
	html  = get_html(url)
	if html != "Error":
		data = get_parse_data(html)
		categories = data.find("div", { "id" : "column-left" }).find("ul", { "class" : "catalog__nav-menu" })
		if categories:
			categories = categories.find("ul", { "class" : "catalog__nav-menu" }).findAll("a")
			new_space = space + "\t"
			for category in categories:
				category_title = category.text
				category_url = category.get('href')

				if category_url != url:
					print(new_space, category_title, category_url, len(categories))
					get_texprom_categories_childs(category_url, new_space)

def get_texprom_categories(url, i, f, space):
	html  = get_html(url)
	if html != "Error":
		data = get_parse_data(html)

		categories = data.findAll("a", { "class" : "category__item" })
		if categories:
			for category in categories:
				category_title = category.find("h3").text
				category_url = category.get('href')
				new_space = "\t" + space

				print(new_space, category_title, category_url)
				f.write("<tr><td><b>" + category_title + "</b></td><td></td></tr>")

				i = i + 1

				get_texprom_categories(category_url, i, f, new_space)
		else:
			url  = url + "?limit=10000"
			html = get_html(url)
			if html != "Error":
				data = get_parse_data(html)

				items = data.findAll("div", { "class" : "products__item-desc" })
				for item in items:
					item_link  = item.find("a", { "class" : "products__item-title"})
					item_url   = item_link.get('href')
					item_text  = item_link.text
					item_price = item.find("span", { "class" : "products__item-price"}).text

					print(item_link, item_text, item_price)

					f.write("<tr><td>" + item_text + "</td><td>" + item_price + "</td></tr>")

def parse_texprom():
	content_start = """<!DOCTYPE html>
<html>
	<head>
		<meta charset=\"utf-8\" />
		<title>Texprom</title>
		<style>
			h1 {
				margin-left: auto; margin-right: auto; width: 6em;
			}
			table {
				width: 750px;
				border-top: 1px solid black;
				border-left: 1px solid black;
				border-right: 1px solid black;
				margin: auto;
				font-family: monospace;
			}
			tr {
				border-bottom: 1px solid black;
				display: block;
				padding:0px;
				margin:0px;
			}
			td {
				text-align: left;
				padding:0px;
				margin:0px;				
			}
		</style>
	</head>
<body>
	<h1>Texprom</h1>/<a href="stroymarket.html">Stroymarket</a>
	<table>"""

	content_end = "\n\t</table>\n</body>\n</html>"

	f = open('texprom.html', 'w')
	f.write(content_start)

	get_texprom_categories("https://texprom.shop/", 0, f, "")

	f.write(content_end)
	f.close()

if __name__ == "__main__":
	parse_texprom()