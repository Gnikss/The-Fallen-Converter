import xml.etree.ElementTree as ET
import os

tree = ET.parse("types.xml")
root = tree.getroot()

precursor = """<CurrencyName> #tm_ruble
	<Currency> MoneyRuble1, 	1
	<Currency> MoneyRuble5, 	5
	<Currency> MoneyRuble10, 	10
	<Currency> MoneyRuble25, 	25
	<Currency> MoneyRuble50, 	50
	<Currency> MoneyRuble100, 	100\n"""

categories = {}

traders = {
	"Consume Trader": ["Food"], # 0
	"Misc Trader": ["Containers", "Tools", "Viking", "Bbp", "Msp", "Mass", "Cp", "Mung"], # 1
	"Weapon Trader": ["Weapons", "Explosives"], # 2
	"Clothing Trader": ["Shirts", "Pants", "Coats", "Jackets", "Vests", "Bags", "Shoes", "Boots", "Belts", "Helmet", "Glasses", "Armbands", "Ghillie", "Other Clothes"], # 3
	"Weapon Supplies Trader": ["Mag", "Ammo"], # 4
	"Vehicles Trader": ["Vehiclesparts", "Vehicles"] # 5
}

banned_prefixes = [
	"animal",
	"christmastree",
	"fence",
	"land_wreck",
	"watchtower",
	"waterbottle",
	"wreck",
	"zmb",
	"slottedwood",
	"BusPsychoWheel_offroad_Ruined",
	"CigarettePack",
	"Armor_Rack"
]

for child in root:
	name = child.attrib["name"]
	category = ""
	quantity = "*"

	for childs_child in child:
		if childs_child.tag == "category":
			category = childs_child.attrib["name"]

	shouldContinue = True
	for prefix in banned_prefixes:
		if len(prefix) <= len(name):
			if name[:len(prefix)].lower() == prefix.lower():
				shouldContinue = False

	if shouldContinue == False:
		continue

	if name[:7].lower() == "skyline":
		continue

	elif category == "clothes":
		if ("shirt" in name.lower()):
			category = "Shirts"

		elif ("pant" in name.lower()):
			category = "Pants"

		elif ("coat" in name.lower()):
			category = "Coats"

		elif ("jacket" in name.lower()):
			category = "Jackets"

		elif ("vest" in name.lower() or "platecarrier" in name.lower()):
			category = "Vests"

		elif ("bag" in name.lower()):
			category = "Bags"

		elif ("shoe" in name.lower()):
			category = "Shoes"

		elif ("boot" in name.lower()):
			category = "Boots"

		elif ("belt" in name.lower()):
			category = "Belts"

		elif ("helmet" in name.lower()):
			category = "Helmets"

		elif ("glasses" in name.lower()):
			category = "Glasses"

		elif ("armband" in name.lower()):
			category = "Armbands"

		elif ("ghillie" in name.lower()):
			category = "Ghillie"
			
		else:
			category = "Other Clothes"

	elif name[:3].lower() == "bbp":
		category = "Bbp"
	
	elif name[:3].lower() == "msp":
		category = "Msp"
	
	elif name[:4].lower() == "mass":
		category = "Mass"

	elif name[:2].lower() == "cp":
		category = "Cp"

	elif name[-4:].lower() == "mung":
		category = "Mung"

	elif name[:11].lower() == "rag_hummer_":
		category = "Vehiclesparts"

	elif name[:4].lower() == "mag_":
		category = "Mag"

	elif name[:4].lower() == "ammo":
		category = "Ammo"

	elif name[-9:].lower() == "destroyed":
		continue

	elif name[-9:].lower() == "_deployed":
		continue

	elif category == "":
		category = "Vehicles"
		quantity = "V"

	if not (category.capitalize() in categories):
		categories[category.capitalize()] = []

	categories[category.capitalize()].append({"name": name, "quantity": quantity})

f = open("TraderConfig.txt", "w")
f.write(precursor)

typeNames = []

for trader in traders:
	f.write("\n\n<Trader> " + trader)
	
	for category in categories:
		if category in traders[trader]:
			f.write("\n" + 	"	<Category> " + category.capitalize() + "\n")
			for item in categories[category]:
				if (item["name"] in typeNames):
					continue

				typeNames.append(item["name"])

				writeString = "{:<70}".format("		" + item["name"] + ",")
				f.write(writeString + item["quantity"] + ",			1,			-1\n")

f.close()