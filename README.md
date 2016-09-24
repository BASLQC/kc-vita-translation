Some items, by necessity of having an English variable name, are already in english. Other items are just pure data.

## Processing

Python with `xmltodict` will be used to parse and unparse the XML data. It requires no XML schemas, and turns it straight into a Python Dict as if it was a JSON file: and back. Which helps because the KC3 translations are also in JSON.

Installation:

```
sudo pip3 install xmltodict
```

```
import json
import xmltodict

# open file: maybe do with open
maparea = open("mst_maparea.xml", 'rb')
# get dict
mapdict = xmltodict.parse(maparea)
print(mapdict['mst_maparea_data']['mst_maparea'][0]) # display first item
# save changes to file: with open?
xmltodict.unparse(mapdict)
```

Restore closing brackets: KC3 breaks with the normal XML schema and uses `<Tag />` in place of `<Tag></Tag>`. We need to make sure to propogate this everywhere.

The first way is to simply find the exact tag to replace. Another, better way is to create a regex that will do this.

```
m = re.search(r'^\s*\<(\w+)\>\</(\w+)\>', "    <Tag></Tag>") # only finds ^\t<Tag></Tag>$
substitution = re.sub(r'\<(\w+)\>\</(\w+)\>', r'<\1 />', "    <Tag></Tag>")
```

## Match manually linked Quests

```
# iterate through xml to obtain vita matched translations
for item in xml['mst_quest_data']['mst_quest']:
	# take kanji name (without trailing words) and match to translation
	datalist['Id']
	item['Name'] = datalist[item['Id']]['Name']
	item['Details'] = datalist[item['Id']]['Name']
	print(item['Id'], item['Name'], item['Details'])

# iterate through xml and compare quest Ids
# if matched compare titles
# if titles match, is translation
```
