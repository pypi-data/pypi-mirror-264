#!/usr/bin/env python3

# Adds a (retextured) item into the game. Will need to be modified slightly
# to add items other than armor. Remember to use dumpxdt.py (and make it read
# the generated _new TableData!) so your server allows you to spawn the
# new items. Will also need to be modified to work with girls' or unisex items.

from unitypack.asset import Asset
from unitypack.object import FFOrderedDict
from unitypack.modding import import_texture

# asset bundles
TABLEDATA_PATH = 'CustomAssetBundle-1dca92eecee4742d985b799d8226666d'
CHARTEX_PATH = 'CustomAssetBundle-aa120043d3c634fe9adfb5cbe08e6970'
ICONS_PATH = 'CustomAssetBundle-784fa24bcf2da4f5eabe9547958616eb'

# template items
TEMPL_ITEMID = 152 # changing this is one way to change the base model
TEMPL_TEXTURE_PATHID = 589 # these other two can stay the same
TEMPL_ICON_PATHID = 1000

# new item properties
ITEM_TEXTURE_PATH = 'shirt_davestrider2.png'
ITEM_ICON_PATH = 'shirt_davestrider2_icon.png'

ITEM_NAME = 'Dave Strider Shirt'
ITEM_COMMENT = 'Dave Strider from Homestuck! (I know nothing about this character)'
ITEM_TEXTURE_NAME = 'shirt_davestrider2'
ITEM_TYPE = 'Shirts' # one of Shirts, Pants, Shoes, Hat, Glass, Back, Weapon, Vehicle
ITEM_DEFENSE = 50

def findnexticon(tabledata, typ):
	xdtdata = tabledata.objects[7].contents
	categories = ['Shirts', 'Pants', 'Shoes', 'Hat', 'Glass', 'Back', 'Weapon', 'Vehicle']

	ret = 1
	for cat in categories:
		icontable = xdtdata['m_p' + cat + 'ItemTable']['m_pItemIconData']
		if icontable[1]['m_iIconType'] == typ:
			ret = max(ret, *[x['m_iIconNumber'] for x in icontable])
	
	return ret + 1

def fromtempl(table, src, dst):
	table.append(FFOrderedDict())
	for k, v in table[src].items():
		table[dst][k] = v

def mod_tabledata(tabledata):
	itemtable = tabledata.objects[7].contents['m_p' + ITEM_TYPE + 'ItemTable']
	itemid = len(itemtable['m_pItemData'])

	assert len(itemtable['m_pItemData']) == len(itemtable['m_pItemStringData'])

	# construct item object
	fromtempl(itemtable['m_pItemData'], TEMPL_ITEMID, itemid)
	
	# fix item id
	itemtable['m_pItemData'][itemid]['m_iItemNumber'] = itemid
	itemtable['m_pItemData'][itemid]['m_iItemName'] = itemid
	itemtable['m_pItemData'][itemid]['m_iComment'] = itemid

	# configure properties
	itemtable['m_pItemData'][itemid]['m_iDefenseRat'] = ITEM_DEFENSE
	# ...and any other changes you want

	# construct item strings object
	fromtempl(itemtable['m_pItemStringData'], TEMPL_ITEMID, itemid)

	# set strings
	itemtable['m_pItemStringData'][itemid]['m_strName'] = ITEM_NAME
	itemtable['m_pItemStringData'][itemid]['m_strComment'] = ITEM_COMMENT

	meshid = len(itemtable['m_pItemMeshData'])
	templ_meshid = itemtable['m_pItemData'][TEMPL_ITEMID]['m_iMesh']
	itemtable['m_pItemData'][itemid]['m_iMesh'] = meshid

	# construct item mesh info object
	fromtempl(itemtable['m_pItemMeshData'], templ_meshid, meshid)

	itemtable['m_pItemMeshData'][meshid]['m_pstrMTextureString'] = ITEM_TEXTURE_NAME
	# female texture
	# itemtable['m_pItemMeshData'][meshid]['m_pstrFTextureString'] = ITEM_TEXTURE_NAME

	iconnum = findnexticon(tabledata, 3)

	# construct icon object
	iconid = len(itemtable['m_pItemIconData'])
	itemtable['m_pItemIconData'].append(FFOrderedDict())

	itemtable['m_pItemIconData'][iconid]['m_iIconType'] = 3
	itemtable['m_pItemIconData'][iconid]['m_iIconNumber'] = iconnum

	itemtable['m_pItemData'][itemid]['m_iIcon'] = iconid

	print('added itemid {} to tabledata.\n\tmeshid: {}, iconid: {}, iconum: {}'
		.format(itemid, meshid, iconid, iconnum))
	
	return iconnum

def mod_texture(asset, imgpath, load_path, name, templ_pathid, comp='dxt1'):
	obj = asset.add_object(28)
	import_texture(obj._contents, imgpath, name, comp)
	ab_ent = asset.add2ab(load_path, obj.path_id)

	print('inserted texture.\n\tpath_id: {}'.format(obj.path_id))

def main():
	print('inserting {}...'.format(ITEM_NAME))

	print('modding TableData...')
	with open(TABLEDATA_PATH, 'rb') as f:
		tabledata = Asset.from_file(f)

		iconnum = mod_tabledata(tabledata)

		with open(TABLEDATA_PATH + '_new', 'wb') as outf:
			tabledata.save(outf)
	
	icon_name = 'cosicon_{}'.format(iconnum)
	icon_path = 'icons/{}.png'.format(icon_name)

	print('icon_name: {}, icon_path: {}'.format(icon_name, icon_path))
	
	print('modding CharTexture...')
	with open(CHARTEX_PATH, 'rb') as f:
		chartex = Asset.from_file(f)

		mod_texture(chartex, ITEM_TEXTURE_PATH, 'texture/' + ITEM_TEXTURE_NAME + '.dds',
			ITEM_TEXTURE_NAME, TEMPL_TEXTURE_PATHID)

		with open(CHARTEX_PATH + '_new', 'wb') as outf:
			chartex.save(outf)
	
	print('modding Icons...')
	with open(ICONS_PATH, 'rb') as f:
		icons = Asset.from_file(f)

		mod_texture(icons, ITEM_ICON_PATH, icon_path, icon_name, TEMPL_ICON_PATHID, 'dxt5')

		with open(ICONS_PATH + '_new', 'wb') as outf:
			icons.save(outf)

	print('done.')

if __name__ == '__main__':
	main()
