# -- coding: utf-8 --
import csv, copy
import sys
import glob
import time
import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

# 2015-10-07. Converts gould_books.csv to MODS. Records are for plates only but book records can be derived or use existing MARC records.
# dict[key][0] etc
# add second date for bird ksrl_sc_gould_ng_1_2_002.tif - 1880:01:01

# xmlData = open(xmlFile, 'w')
dataFile=sys.argv[1]

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')




with open(sys.argv[1], 'rU', errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)
    # root = Element('mods:modsCollection')
    # root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    # root.set('xmlns:mods', 'http://www.loc.gov/mods/v3')
    # root.set('xmlns:xlink','http://www.w3.org/1999/xlink')
    # root.set('xsi:schemaLocation',
    #          'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
    # tree = ET.ElementTree(root)
    dirFiles = glob.glob('*.xml')





    for row in reader:
        # print(row)
        root = Element('mods:mods')

        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        root.set('xmlns:mods', 'http://www.loc.gov/mods/v3')
        root.set('xmlns:xlink','http://www.w3.org/1999/xlink')
        root.set('xsi:schemaLocation',
                 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
        tree = ET.ElementTree(root)
        # record = SubElement(root, 'mods:mods')
        # record.set('xsi:schemaLocation',
        #            'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
        # inserts filename as local identifier
        identifier = SubElement(root, 'mods:identifier')
        identifier.set('type', 'local')
        id = row['Identifier']
        identifier.text = row['Identifier']

        titleInfo = SubElement(root, 'mods:titleInfo')
        title = SubElement(titleInfo, 'mods:title')
        title.text = row['Title']

        partNo = SubElement(titleInfo, 'mods:partNumber')
        partNo.text = row['Part']
        typeImage = SubElement(root, 'mods:typeOfResource')
        typeImage.text = row['TypeOfResource']

        originInfo = SubElement(root, 'mods:originInfo')
        if len(row['DateCreated']) > 0:
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


        langrow=row['Language'].split('|')
        for x in langrow:
            language = SubElement(root, 'mods:language')
            languageTerm = SubElement(language,'mods:languageTerm')
            languageTerm.set('type','text')
            languageTerm.text=x
        # if '|' in row['Language']:
        #     posh = row['Language'].split('|')
        #
        #     for x in posh:
        #         language.text=str(x)
        #     # print(language)
        #     # language.text = language
        # else:
        #     language.text = row['Language']

        namerow = row['CreatorName'].split('|')



        for x in namerow:

            name = SubElement(root, 'mods:name')
            name.set('type', 'personal')
            namePart = SubElement(name, 'mods:namePart')
            if ';' in x:
                role = SubElement(name, 'mods:role')
                # roleTermcode = SubElement(role, 'mods:roleTerm')
                # roleTermcode.set('type', 'code')

                roleTermtext = SubElement(role, 'mods:roleTerm')
                roleTermtext.set('type', 'text')
                y = x.split(';')
                namePart.text = y[0]
                roleTermtext.text = y[1]

            else:
                namePart.text = x


        # info about the nature of the resource. not from the spreadsheet
        physDesc = SubElement(root, 'mods:physicalDescription')
        if len(row['DigitalOrigin']) > 0:
            digOr = SubElement(physDesc, 'mods:digitalOrigin')
            digOr.text = row['DigitalOrigin']
        form = SubElement(physDesc, 'mods:form')
        form.set('type', 'material')
        form.text = row['Form']

        identifier = SubElement(root,'mods:identifier')
        identifier.set('type','local')
        identifier.text = row['Identifier']

        interMed = SubElement(physDesc, 'mods:internetMediaType')
        interMed.text = 'audio/wav'
        #
        abstract = SubElement(root, 'mods:abstract')
        abstract.text = row['Abstract']

        genre = SubElement(root, 'mods:genre')
        genre.set('authorityURI', 'http://id.loc.gov')
        genre.set(
            'valueURI', 'http://id.loc.gov/authorities/genreForms/gf2011026431.html')
        genre.text = row['Genre']
        accessCond = SubElement(root, 'mods:accessCondition')
        accessCond.set('type', 'use and reproduction')
        # accessCond.set('xlink:href','http://rightsstatements.org/page/UND/1.0/?language=en')
        accessCond.text = 'The copyright and related rights status of this Item has been reviewed by the organization that has made the Item available, but the organization was unable to make a conclusive determination as to the copyright status of the Item. Please refer to the organization that has made the Item available for more information. You are free to use this Item in any way that is permitted by the copyright and related rights legislation that applies to your use.'
        #

        location = SubElement(root, 'mods:location')
        physLoc = SubElement(location, 'mods:physicalLocation')
        physLoc.set('authorityURI', 'http://id.worldcat.org/fast')
        physLoc.set('valueURI', 'http://id.worldcat.org/fast/1567592')
        shelfLocator = SubElement(location, 'mods:shelfLocator')
        shelfLocator.text = row['CallNumber'] + ', ' + row['ShelfLocator']
        shelfLocator = SubElement(location, 'mods:shelfLocator')
        shelfLocator.text = row['callNumberID']
        physLoc.text = 'University of Arizona. Library. Special Collections.'
        # typeOfResource = SubElement(root, 'mods:typeOfResource')
        # typeOfResource.text = row['TypeOfResource']
        # related item was used for the host parent of the plate, e.g. the
        # monographic volume
        relatedItem = SubElement(root, 'mods:relatedItem')
        relatedItem.set('type', 'host')
        relatedTitleInfo = SubElement(relatedItem,'mods:titleInfo')
        relatedTitle = SubElement(relatedTitleInfo,'mods:title')

        relatedTitle.text = row['RelatedItem']

        recordInfo = SubElement(root,'mods:recordInfo')
        recordCreationDate = SubElement(recordInfo,'mods:recordCreationDate')
        recordCreationDate.set('encoding','w3cdtf')
        recordCreationDate.text = st
        recordOrigin = SubElement(recordInfo,'mods:recordOrigin')
        recordOrigin.text = 'Manually created by Trent Purdy. Generated into xml using a python script by Erik Radio.'
        recordSource = SubElement(recordInfo,'mods:recordContentSource')
        recordSource.text = 'University of Arizona Libraries'
        # recordID = SubElement(recordInfo,'mods:recordIdentifier')
        # recordID.text = row['CallNumber']


        extension = SubElement(root,'mods:extension')
        extension.set('xmlns','http://pbcore.org/PBCore/PBCoreNamespace.html')
        extension.set('xsi:schemaLocation','http://www.pbcore.org/PBCore/PBCoreNamespace.html http://www.pbcore.org/PBCore/PBCoreSchema.xsd')
        instDoc = SubElement(extension,'PBCoreInstantionDocument')
        files = row['relatedFile']
        fileList = files.split('|')
        for file in fileList:
            for dirFile in dirFiles:
                if file == dirFile:
                    autoMD = open(dirFile,'r')
                    ET.register_namespace('','http://www.pbcore.org/PBCore/PBCoreNamespace.html')
                    autoTree=ET.parse(autoMD)

                    autoRoot=autoTree.getroot()
                    autoInst = SubElement(instDoc,'pbcoreInstantiation')
                    for x in autoRoot:
                        chunk = copy.deepcopy(x)

                        autoInst.append(chunk)
        inst = SubElement(instDoc,'pbcoreInstantiation')
        instPhys = SubElement(inst,'instantiationPhysical')
        instPhys.text= row['instantiationPhysical']
        instStan = SubElement(inst,'instantiationStandard')
        instStan.text = row['instantiationStandard']
        instMed = SubElement(inst,'instantiationMediaType')
        instMed.text = row['instantiationMediaType']
        instGens = SubElement(inst,'instantiationGenerations')
        instGens.text = row['instantiationGenerations']
        instTracks = SubElement(inst,'instantiationTracks')
        instTracks.text = row['instantiationTracks']
        instChannel = SubElement(inst,'instantiationChannelConfiguration')
        instChannel.text = row['instantiationChannelConfiguration']
        instDuran = SubElement(inst,'instantiationDuration')
        instDuran.text = row['instantiationDuration']
        tapeType = SubElement(inst, 'instantiationAnnotation')
        tapeType.text = row['tapeType']
        tapeType.set('annotationType','Tape type')
        tapeThickness = SubElement(inst,'instantiationAnnotation')
        tapeThickness.set('annotationType','Tape thickness')
        tapeThickness.text = row['tapeThickness']
        reelSize = SubElement(inst,'instantiationAnnotation')
        reelSize.set('annotationType','Reel size')
        reelSize.text = row['reelSize']
        tapeBase = SubElement(inst,'instantiationAnnotation')
        tapeBase.set('annotationType','Tape base')
        tapeBase.text = row['tapeBase']
        noiseRed = SubElement(inst,'instantiationAnnotation')
        noiseRed.set('annotationType','Noise reduction')
        noiseRed.text = row['noiseReduction']
        stockMan = SubElement(inst,'instantiationAnnotation')
        stockMan.set('annotationType','Stock manufacturer')
        stockMan.text = row['stockManufacturer']
        comments = SubElement(inst,'instantiationAnnotation')
        comments.set('annotationType','Comments')
        comments.text = row['comments']
        transferComments = SubElement(inst,'instantiationAnnotation')
        transferComments.set('annotationType','Transfer comments')
        transferComments.text = row['transferComments']
        instEssence = SubElement(inst,'instantiationEssenceTrack')
        instType = SubElement(instEssence,'essenceTrackType')
        instType.text = row['essenceTrackType']
        instPlay = SubElement(instEssence,'essenceTrackPlaybackSpeed')
        instPlay.set('unitsOfMeasure','ips')
        instPlay.text = row['essenceTrackPlaybackSpeed']
        createApp = SubElement(inst,'instantiationAnnotation')
        createApp.set('annotationType','Creating application')
        createApp.text = row['creatingApplication']
        sourceDeck = SubElement(inst,'instantiationAnnotation')
        sourceDeck.set('annotationType','Source deck')
        sourceDeck.text = row['sourceDeck']
        digitizer = SubElement(inst,'instantiationAnnotation')
        digitizer.set('annotationType','Digitizer')
        digitizer.text = row['digitizer']
        qualCon = SubElement(inst,'instantiationAnnotation')
        qualCon.set('annotationType','Quality control')
        qualCon.text = row['qualityControl']











        tree.write(identifier.text + '.xml', xml_declaration=True, encoding="UTF-8")
