# -- coding: utf-8 --
import csv
import sys
import time
import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

# 2015-10-07. Converts gould_books.csv to MODS. Records are for plates only but book records can be derived or use existing MARC records.
# dict[key][0] etc
# add second date for bird ksrl_sc_gould_ng_1_2_002.tif - 1880:01:01
xmlFile = 'newBatch.xml'
xmlData = open(xmlFile, 'w')
# dataFile=sys.argv[1]

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

root = Element('mods:modsCollection')
root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
root.set('xmlns:mods', 'http://www.loc.gov/mods/v3')
root.set('xsi:schemaLocation',
         'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
tree = ET.ElementTree(root)


with open(sys.argv[1], 'rU', errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:

        record = SubElement(root, 'mods:mods')
        record.set('xsi:schemaLocation',
                   'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
        # inserts filename as local identifier
        identifier = SubElement(record, 'mods:identifier')
        identifier.set('type', 'local')
        id = row['Identifier']
        identifier.text = row['Identifier']

        titleInfo = SubElement(record, 'mods:titleInfo')
        title = SubElement(titleInfo, 'mods:title')
        title.text = row['Title']

        partNo = SubElement(titleInfo, 'mods:partNumber')
        partNo.text = row['Part']
        typeImage = SubElement(record, 'mods:typeOfResource')
        typeImage.text = row['TypeOfResource']

        originInfo = SubElement(record, 'mods:originInfo')
        dateCreated = SubElement(originInfo, 'mods:dateCreated')
        dateCreated.set('encoding', 'w3cdtf')
        dateCreated.text = row['DateCreated']

        placeCreated = SubElement(originInfo, 'mods:place')
        placeCreated.set('supplied', 'yes')
        placeTerm = SubElement(placeCreated, 'mods:placeTerm')
        placeTerm.set('authorityURI', 'http://id.worldcat.org/fast')
        placeTerm.set('valueURI', 'http://id.worldcat.org/fast/1205454')
        placeTerm.text = row['PlaceCreated']

        pub = SubElement(originInfo, 'mods:publisher')
        pub.text = row['Publisher']

        language = SubElement(record, 'mods:language')
        language.text = row['Language']

        namerow = row['CreatorName'].split('|')

        name = SubElement(record, 'mods:name')
        name.set('type', 'personal')
        namePart = SubElement(name, 'mods:namePart')
        role = SubElement(name, 'mods:role')
        roleTermcode = SubElement(role, 'mods:roleTerm')
        roleTermcode.set('type', 'code')

        roleTermtext = SubElement(role, 'mods:roleTerm')
        roleTermtext.set('type', 'text')

        for x in namerow:
            y = x.split(';')
            namePart.text = y[0]
            roleTermtext.text = y[1]

        # info about the nature of the resource. not from the spreadsheet
        physDesc = SubElement(record, 'mods:physicalDescription')
        digOr = SubElement(physDesc, 'mods:digitalOrigin')
        digOr.text = row['digitalOrigin']
        form = SubElement(physDesc, 'mods:form')
        form.set('type', 'material')
        form.text = row['Form']

        interMed = SubElement(physDesc, 'mods:internetMediaType')
        interMed.text = 'audio/wav'
        #
        abstract = SubElement(record, 'mods:abstract')
        abstract.text = row['Abstract']

        genre = SubElement(record, 'mods:genre')
        genre.set('authorityURI', 'http://id.loc.gov')
        genre.set(
            'valueURI', 'http://id.loc.gov/authorities/genreForms/gf2011026431.html')
        genre.text = 'Oral histories'
        accessCond = SubElement(record, 'mods:accessCondition')
        accessCond.set('type', 'use and reproduction')
        accessCond.text = 'This Item is protected by copyright and/or related rights. You are free to use this Item in any way that is permitted by the copyright and related rights legislation that applies to your use. In addition, no permission is required from the rights-holders for non-commercial uses. For other uses you need to obtain permission from the rights-holders.'
        #

        location = SubElement(record, 'mods:location')
        physLoc = SubElement(location, 'mods:physicalLocation')
        physLoc.set('authorityURI', 'http://id.worldcat.org/fast')
        physLoc.set('valueURI', 'http://id.worldcat.org/fast/1567592')
        shelfLocator = SubElement(location, 'mods:shelfLocator')
        shelfLocator.text = row['CallNumber'] + ', ' + row['ShelfLocator']
        physLoc.text = 'University of Arizona. Library. Special Collections.'
        typeOfResource = SubElement(record, 'mods:typeOfResource')
        typeOfResource.text = row['TypeOfResource']
        # related item was used for the host parent of the plate, e.g. the
        # monographic volume
        relatedItem = SubElement(record, 'mods:relatedItem')
        relatedItem.set('type', 'host')
        relatedItem.text = row['RelatedItem']

    tree.write(id + '.xml', xml_declaration=True, encoding="UTF-8")
