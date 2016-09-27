import os
import re
import json
import xmltodict

# default dirs
xml_dir = os.path.join("Xml", "tables", "master")
jp_xml_dir = os.path.join("jp", xml_dir)
en_xml_dir = os.path.join("en", xml_dir)
kc3_trans_dir = os.path.join("kc3-vita-translations", "en")
kc3_jp_dir = os.path.join("kc3-vita-translations", "jp")

# maybe kc3 translation should be a submodule, choose language as a argument

def ships(): # translate all ship names
	# open xml
	shipxml = xmltodict.parse(open(os.path.join(jp_xml_dir, 'mst_ship.xml'), 'rb'))

	# get KC3 JSON, kanji name as key and translation as value
	shiplist = json.load(open(os.path.join(kc3_trans_dir, 'ships.json'), 'r'))

	# replace all names with corresponding unicode string
	for item in shipxml['mst_ship_data']['mst_ship']:
		# actually, don't rename Nashi, game crashes if it can't find it
		#if item['Name'] == 'なし': # None
			#item['Name'] = 'None'
			#print(item['Id'], item['Name'])
			#continue

		# 544 装甲空母鬼 = Armored Carrier Demon
		if item['Name'] == "装甲空母鬼":
			item['Name'] = 'Armored Carrier Demon'
			print(item['Id'], item['Name'])
			continue

		# 545 装甲空母姫 = Armored Carrier Priness
		if item['Name'] == "装甲空母姫":
			item['Name'] = 'Armored Carrier Princess'
			print(item['Id'], item['Name'])
			continue

		# 650 運河棲姫 = Canal Princess, unique to Vita
		if item['Name'] == "運河棲姫":
			item['Name'] = 'Canal Princess'
			print(item['Id'], item['Name'])
			continue
		
		try:
			# render Kai and Ni to romaji with space separation
			# also render 甲 (corresponds to https://en.wikipedia.org/wiki/Celestial_stem ) as A... (in the future 乙: B, 丙: C, 丁: D)
			item['Name'] = item['Name'].replace('改', ' Kai').replace('二', ' Ni').replace('甲', ' A')
			
			# since event specifics only start from ID 901, only start checking if it is greater than this
			if int(item['Id']) >= 901:
				events = {"年末": "Year-end", "正月": "New_Year", "梅雨": "Rainy_Season", "夏": "Summer", "秋": "Autumn", "Valentine": "Valentine", "Xmas": "Xmas"} # underscore as scaffolding
				for event in events.keys():
					if item['Name'].find(event) != -1:
						processed = item['Name'].replace(event, event + " ")
						fullname = processed.split()
						fullname[0] = events[event].replace("_", " ")
						translation = shiplist[fullname[1]]
						fullname[1] = translation
						item["Name"] = " ".join(fullname)
						break # name found, no more searching needed
			else:
				# split full name into components
				fullname = item['Name'].split()
				
				# take kanji name (without trailing words) and match to translation
				translation = shiplist[fullname[0]]
				if len(fullname) == 1: # just write base name
					item['Name'] = translation
				else: # add trailing kai and ni with spaces
					fullname[0] = translation
					item['Name'] = " ".join(fullname)
			
		except KeyError: # if name doesn't exist, don't edit
			pass
		
		print(item['Id'], item['Name'])

	# save changes to file
	print("Saving changes shown above to :", os.path.join(en_xml_dir, 'mst_ship.xml'))
	with open(os.path.join(en_xml_dir, 'mst_ship.xml'), 'w') as f:
		f.write(xmltodict.unparse(shipxml, pretty=True))
	
	# open file again and convert `<Yomi></Yomi>` to `<Yomi />`, which the program expects apparently
	with open(os.path.join(en_xml_dir, 'mst_ship.xml'), 'r') as f:
		filedata = f.read()
	
	filedata = filedata.replace('<Yomi></Yomi>', '<Yomi />') # in memory but should be small

	with open(os.path.join(en_xml_dir, 'mst_ship.xml'), 'w') as f:
		f.write(filedata)

def slot_items():
	# open xml
	itemxml = xmltodict.parse(open(os.path.join(jp_xml_dir, 'mst_slotitem.xml'), 'rb'))

	# get KC3 JSON, kanji name as key and translation as value
	itemlist = json.load(open(os.path.join(kc3_trans_dir, 'items.json'), 'r'))

	# replace all names with corresponding unicode string
	for item in itemxml['mst_slotitem_data']['mst_slotitem']:
		# take kanji name (without trailing words) and match to translation
		item['Name'] = itemlist[item['Name']]
		print(item['Id'], item['Name'])
	
	# save changes to file
	print("Saving changes shown above to :", en_xml_dir + 'mst_slotitem.xml')
	with open(os.path.join(en_xml_dir, 'mst_slotitem.xml'), 'w') as f:
		f.write(xmltodict.unparse(itemxml, pretty=True))

# needs to parse from wiki: 
#def quests():
	## open xml
	#xml_fname = 'mst_quest.xml'
	#xml = xmltodict.parse(open(os.path.join(jp_xml_dir, xml_fname), 'rb'))

	## get KC3 JSON, id as key and translation as value
	#list_fname = 'quests.json'
	#datalist = json.load(open(os.path.join(kc3_trans_dir, list_fname), 'r'))

	## replace all names with corresponding unicode string
	#for item in xml['mst_quest_data']['mst_quest']:
		## take kanji name (without trailing words) and match to translation
		#item['Name'] = datalist[item['Id']]['Name']
		#item['Details'] = datalist[item['Id']]['Name']
		#print(item['Id'], item['Name'], item['Details'])
	
	## save changes to file
	#print("Saving changes shown above to :", en_xml_dir + xml_fname)
	##with open(os.path.join(en_xml_dir, xml_fname), 'w') as f:
	##	f.write(xmltodict.unparse(xml, pretty=True))
	#print(xmltodict.unparse(xml, pretty=True))

# needs to parse from wiki: 
def quest_hash():
	# open xml
	xml_fname = 'mst_quest.xml'
	xml = xmltodict.parse(open(os.path.join(jp_xml_dir, xml_fname), 'rb'))

	# get KC3 JSON, name as key, id as value
	list_fname = 'quests.json'
	jp_datalist = json.load(open(os.path.join(kc3_jp_dir, list_fname), 'r'))
	name_hash = {}
	desc_hash = {}
	for key in jp_datalist.keys():
		name_hash[jp_datalist[key]['name']] = key
		desc_hash[jp_datalist[key]['desc']] = key
	
	list_fname = 'quests.json'
	datalist = json.load(open(os.path.join(kc3_trans_dir, list_fname), 'r'))
	
	# replace all names with corresponding unicode string
	for item in xml['mst_quest_data']['mst_quest']:
		# take kanji name (without trailing words) and match to translation
		try: # first search for name
			# replace weird characters
			orig_id = name_hash[item['Name'].replace('第１次', '第一次').replace('第２次', '第二次').replace('１', '1').replace('２', '2').replace('３', '3').replace('４', '4')]
			
			if item['Name'] == '機種転換':
				print('KC:', orig_id, 'KCV:', item['Id'], '\n', item['Name'], '\n', item['Details'], '\n', datalist[item['Id']]['name'], '\n', datalist[item['Id']]['desc'])
				continue
			
			print('KC:', orig_id, 'KCV:', item['Id'], '\n', item['Name'], '\n', item['Details'], '\n', datalist[orig_id]['name'], '\n', datalist[orig_id]['desc'])
		except KeyError:
			try: # second search for details
				orig_id = desc_hash[item['Details'].replace('１', '1').replace('２', '2').replace('３', '3').replace('４', '4')]
				print('KC:', orig_id, 'KCV:', item['Id'], '\n', item['Name'], '\n', item['Details'], '\n', datalist[orig_id]['name'], '\n', datalist[orig_id]['desc'])
			except KeyError:
				print('KCV:', item['Id'], '\n', item['Name'], '\n', item['Details'])
	
	# save changes to file
	print("Saving changes shown above to :", en_xml_dir + xml_fname)
	#with open(os.path.join(en_xml_dir, xml_fname), 'w') as f:
	#	f.write(xmltodict.unparse(xml, pretty=True))
	#print(xmltodict.unparse(xml, pretty=True))

def stype():
	# open xml
	xml_fname = 'mst_stype.xml'
	xml = xmltodict.parse(open(os.path.join(jp_xml_dir, xml_fname), 'rb'))

	# get KC3 JSON, id as key and translation as value
	list_fname = 'stype.json'
	datalist = json.load(open(os.path.join(kc3_trans_dir, list_fname), 'r'))

	# replace all names with corresponding unicode string
	for item in xml['mst_stype_data']['mst_stype']:
		# take kanji name (without trailing words) and match to translation
		item['Name'] = datalist[int(item['Id'])]
		print(item['Id'], item['Name'])
	
	# save changes to file
	print("Saving changes shown above to :", os.path.join(en_xml_dir, xml_fname))
	with open(os.path.join(en_xml_dir, xml_fname), 'w') as f:
		f.write(xmltodict.unparse(xml, pretty=True))

def quotes():
	# open xml
	xml_fname = 'mst_shiptext.xml'
	xml = xmltodict.parse(open(os.path.join(jp_xml_dir, xml_fname), 'rb'))

	# get KC3 JSON, id as key and translation as value
	list_fname = 'quotes.json'
	datalist = json.load(open(os.path.join(kc3_trans_dir, list_fname), 'r'))
	
	# get original ship name to help
	shipxml_fname = 'mst_ship.xml'
	shipxml = xmltodict.parse(open(os.path.join(en_xml_dir, shipxml_fname), 'rb'))

	# compile a shiphash table with Id as key by processing shiplist XML
	shiplist = {}
	for item in shipxml['mst_ship_data']['mst_ship']:
		shiplist[item['Id']] = item['Name']

	# compile a shiphash table with Name as key
	shipnames = {}
	for item in shipxml['mst_ship_data']['mst_ship']:
		shipnames[item['Name']] = item['Id']

	# replace all names with corresponding unicode string
	for item in xml['mst_shiptext_data']['mst_shiptext']:
		if (item['Id'] == '147'): # Verniy
			item['Getmes'] = datalist['147']['1'] # retain original getmessage
			item['Sinfo'] = datalist['35']['25']
			continue
		elif (item['Id'] == '357') or (item['Id'] == '463'): # Iowa
			item['Getmes'] = datalist['440']['1']
			item['Sinfo'] = datalist['440']['25']
			continue
		
		# Skip null shiptext IDs
		if (item['Getmes'] == None) and (item['Sinfo'] == None):
			continue
		
		try:
			item['Getmes'] = datalist[item['Id']]['1']
		except KeyError: # if get message not found, check if kai
			pass
		
		try:
			item['Sinfo'] = datalist[item['Id']]['25']
		except KeyError: # ignore ship IDs with empty slots
			# if Sinfo is missing, get base name to find and insert base ship text
			fullname = shiplist[item['Id']].split()
			
			try:
				base_id = shipnames[fullname[0]] # find basename ID
				item['Getmes'] = datalist[base_id]['1']
				item['Sinfo'] = datalist[base_id]['25']
			except KeyError:
				pass

	
	# save changes to file
	print("Saving changes shown above to :", os.path.join(en_xml_dir, xml_fname))
	with open(os.path.join(en_xml_dir, xml_fname), 'w') as f:
		f.write(xmltodict.unparse(xml, pretty=True))

	# open file again and convert `<Yomi></Yomi>` to `<Yomi />`, which the program expects apparently
	with open(os.path.join(en_xml_dir, xml_fname), 'r') as f:
		filedata = f.read()
	
	filedata = re.sub(r'\<(\w+)\>\</(\w+)\>', r'<\1 />', filedata) # in memory but should be small

	with open(os.path.join(en_xml_dir, xml_fname), 'w') as f:
		f.write(filedata)

#ships()
#slot_items()
#quests()
quest_hash()
#stype()
#quotes()
print("Changes compiled. To start over, replace the `Xml/` folder in `en/` with the one from `jp/`.")
