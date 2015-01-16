#! /usr/bin/python
import MySQLdb
from datetime import datetime
import os
import re

def getID(table, value): #Gets the ID of value from table; adds row if not there

    query = "SELECT `ID` FROM `"+table+"` WHERE `Name` = '" + db.escape_string(value) + "'"
    insQuery = "INSERT INTO `"+table+"` (`Name`) VALUES ('"+db.escape_string(value)+"')"
        
    cursor.execute(query)
    res = cursor.fetchone()
    
    if res:
        return int(res[0])
    else:
        cursor.execute(insQuery)
        return int(cursor.lastrowid)
        
def shrinkList(l): #takes a list from something like line.split('  ') and removes empty values
    retList = []
    for r in l:
        if r.strip():
            retList.append(r.strip())
    return retList

def countChar(string, countChar): #counts number of occurences of countChar in string
    count = 0
    for char in string:
        if char == countChar:
            count += 1
    return count

#Parses line like 'KEY VALUE1 VALUE2 KEY2 VALUE1' 
# into a dict of lists keyed with key, whose value is a list of values
# Resulting dict of example: { 'KEY': ['VALUE1', 'VALUE2'], 'Key2': ['VALUE1']}

def getKeyedValues(splitLine, keys): 
    retDict = {}
    key = ''
    for word in splitLine:
        word = word.replace('(', '').replace(')', '').strip()
        if word in keys:
            key = word
            if key not in retDict.keys():
                retDict[key] = []            
        elif key:
            retDict[key].append(word)
    return retDict
    
# Takes only the keys in needKeys of a dictionary and places them in a list
# in order of needKeys
# Used to take big dictionaries of game information and extract
# Most values needed for the mysql queries 
def dictToList(dic, needKeys):
    retList = []
    for key in needKeys:
        retList.append(dic[key])
    return retList
    
# Takes a list of tuples. 
# Returns a list of tuples with pre in pos 0 of all tuples
# Otherwise remains the same
# Used to add gameID to list of tuples for equipment, skills, etc
# for queries
def addToTupleList(pre, tupList):
    retList = []
    for tup in tupList:
        repList = []
        repList.append(pre)
        for val in tup:
            repList.append(val)
        retList.append(repList)
    return retList
    
def parseItem(line):

    worn = '(worn)' in line or ' hand)' in line or '(around neck)' in line or '(weapon)' in line or '(quivered)' in line
    
    line = line.split(' - ')[1]
    
    line = line.replace('(right hand)', '').replace('(left hand)', '').replace('(around neck)', '').replace('(worn)', '').replace('(weapon)', '').replace('(quivered)', '')
    
    item = line
    
    if 'a ' in line:
        item = re.sub('^a ', '', item)
    if 'the ' in item:
        item = re.sub('^the ', '', item)
    
    split = line.split(' ')
    mod = '0'
    effects = ''
    brand = ''
    for word in split:
        try:
            int(word)
            mod = word
            break
        except ValueError:
            needsomethingtonotgeterror = 1
    item = item.replace(mod, '')
    
    if 'vampiric' in line:
        brand = 'vampiric'
        item = item.replace('vampiric', '').strip()
    if 'antimagic' in line:
        brand = 'antimagic'
        item = item.replace('antimagic', '').strip()
        
    elif '{' in line and 'unknown' not in line:
        brand = ''
        effects = item.split('{')
        effects = effects[1].replace('}', '').strip()
        if 'pair' in item:
            item = 'pair of ' + item.split(' of')[1].strip()
        else:
            item = item.split(' of')[0].strip()
    elif 'of' in line and 'pair' not in line:

        splitItem = item.split(' of ')
        item = splitItem[0].strip()
        brand = splitItem[1].strip()
        
    elif 'gloves of' in item or 'boots of' in item:
        splitItem = item.split(' of ')
        item = 'pair of ' + splitItem[1].strip()
        brand = splitItem[2].strip()
    
    if '"' in item:
        splitItem = item.split('\"')
        item = splitItem[0].strip()
        
    if 'potion' in item:
        item = 'potion'
        if mod == '0':
            mod = '1'
    elif 'scroll' in item:
        item = 'scroll'
        if mod == '0':
            mod = '1'
    elif 'book' in item:
        item = 'book'
        if mod == '0':
            mod = '1'
    elif 'ration' in item:
        if mod == '0':
            mod = '1'
    if 'unknown' in line:
        effects = ''
        line = line.replace('{unknown}', '').strip()
        brand = brand.replace('{unknown}', '')
        known = False
    else:
        known = True
        
    if '{' in item:
        item = item.split('{')[0].strip()
    if '(' in item:
        item = item.split('(')[0].strip()
        
    if 'uncursed' in item:
        cursed = False
        item = item.split('uncursed')[1].strip()
    elif 'cursed' in item:
        cursed = True
        item = item.split('cursed')[1].strip()
    else:
        cursed = False
        
    if 'an ' in item:
        item = item.replace('an ', '').strip()
        
    if 'bread rations' in line:
        item = 'bread ration'
        
    if 'meat rations' in line:
        item = 'meat ration'
        
    return (line.strip(), mod.strip(), brand.strip(), item.strip(), effects.strip(), worn, known, cursed)

SPECIES = ['Centaur', 'Deep Dwarf', 'Deep Elf', 'Demigod', 'Demonspawn', 'Draconian', 'Felid', 'Formicid', 'Gargoyle', 'Ghoul', 'Halfling', 'High Elf', 'Hill Orc', 'Human', 'Kobold', 'Merfolk', 'Minotaur', 'Mummy', 'Naga', 'Octopode', 'Ogre', 'Spriggan', 'Tengu', 'Troll', 'Vampire', 'Vine Stalker']

DIR = 'crawl.develz.org/morgues/0.15/'
TESTFILE = DIR + 'Moridor/morgue-Moridor-20141010-081422.txt'
TESTFILE2 = DIR + 'abysmalminton/morgue-abysmalminton-20140902-044749.txt'


GAMEINS = 'INSERT INTO `Game` (`File`, `ServerID`, `PlayerID`, `VersionID`, `RaceID`, `ClassID`, `DeityID`, `DeityPiety`, `Title`, `StartTime`, `EndTime`, `Turns`, `PlayTime`, `DeathBy`, `DeathLvl`, `DeathBranch`, `DeathNotes`, `Score`, `Won`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

GAMEBRANCHINS = 'INSERT INTO `Crawl`.`GameBranches` (`GameID`, `BranchID`, `ExploredFloors`, `TotalFloors`) VALUES (%s, %s, %s, %s)'

GAMEEQUIPMENTINS = 'INSERT INTO `Crawl`.`GameEquipment` (`GameID`, `FullName`, `Modifier`, `Brand`, `BaseType`, `Effects`, `Worn`, `Known`, `Cursed`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

GAMERESINS = 'INSERT INTO `Crawl`.`GameResistance` (`GameID`, `rFire`, `rCold`, `rNeg`, `rPois`, `rElec`, `SustAb`, `rMut`, `Gourm`, `MR`, `SeeInvis`, `Clarity`, `rCorr`, `rRot`, `Spirit`, `Warding`, `NoTele`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

GAMERUNEINS = 'INSERT INTO `Crawl`.`GameRunes` (`GameID`, `Rune`) VALUES (%s, %s)'

GAMESPELLINS = 'INSERT INTO `Crawl`.`GameSpells` (`GameID`, `SpellID`) VALUES (%s, %s)'

GAMESKILLINS = 'INSERT INTO `Crawl`.`GameSkills` (`GameID`, `Skill`, `Level`) VALUES (%s, %s, %s)'

GAMESTATINS = 'INSERT INTO `Crawl`.`GameStats` (`GameID`, `CurHP`, `MaxHP`, `CurMP`, `MaxMP`, `Gold`, `AC`, `EV`, `SH`, `Str`, `Intel`, `Dex`, `XL`, `SpellMem`, `SpellMax`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

USERNAME = 'root'
PASSWORD = 'password'

db = MySQLdb.connect(passwd=PASSWORD, db='Crawl', user=USERNAME)
cursor = db.cursor()

players = os.listdir(DIR)
serverID = getID('Server', 'crawl.develz.org')

for player in players:

    contents = os.listdir(DIR+player+'/')
    morgues = [morgue for morgue in contents if 'morgue' in morgue and '.txt' in morgue]
    if len(morgues) > 0:
        print 'Processing ' + player
        playerID = getID('Player', player)
        for morgue in morgues:
            print 'Processing ' + morgue
            filename = DIR + player + '/' + morgue

            with open(filename, 'r') as openMorgue:
                lineNum = 0
                crawlGame = True
                deathMsgStart = False
                # parse variables flag when to extract info    
                parseInv = False 
                parseSkill = False
                parseSpell = False
                parseBranch = False
                
                
                gameInfo = {}
                gameInfo['serverID'] = serverID
                gameInfo['playerID'] = playerID
                gameInfo['file'] = morgue
                gameStats = {}
                gameRes = {}
                
                gameSpells = []
                gameSkills = []
                gameBranches = []
                gameEquipment = []
                gameRunes = []
                
                for line in openMorgue:
                    line = line.strip()
                    ### Extract version and make sure right game type ###
                    ### (Not Sprint or other)
                    if lineNum == 0:
                        if 'Dungeon Crawl Stone Soup' not in line:
                            crawlGame = False
                            print 'Wrong Game Mode'
                            break
                        line = line.split('version ')
                        line = line[1].split(' (')
                        version = line[0]
                        versID = getID('Version', version) 
                        gameInfo['version'] = version
                        gameInfo['versionID'] = versID
                    ## Extract score, title, deathLvl ##
                    elif lineNum == 2:
                        splitLine = line.split(' ')
                        gameInfo['score'] = splitLine[0].strip()
                        
                        splitLine = line.split(player+' the ')
                        splitLine = splitLine[1].split('(level ')
                        

                        gameInfo['title'] = splitLine[0].strip()
                        deathLvl = splitLine[1].split(' ')
                        gameInfo['deathLvl'] = deathLvl[0].replace(',', '').strip()
                    ## Begin deathmsg and extract start time ##
                    elif lineNum == 3:
                        introLine = line
                        split = line.split('Began as a ')
                        if len(split) == 1:
                            split = line.split('Began as an ')
                        split = split[1].split(' on ')
                        specback = split[0]
                        start = split[1]
                        startSplit = start.split(' ')
                        startSplit[0] = startSplit[0][:3]
                        start = ' '.join(startSplit)
                        startTime = datetime.strptime(start, '%b %d, %Y.')
                        startForm = startTime.strftime('%Y-%m-%d')
                        gameInfo['start'] = split[1]
                        gameInfo['startForm'] = startForm
                        deathMsgStart = True
                        deathMsg = ''
                    ## Handle deathmsg extraction (it crosses lines, etc) ###
                    ## Pull relevant info from deathmsg when extraction finished #
                    elif deathMsgStart:
                        if 'The game lasted' in line:
                            print deathMsg
                            deathMsgStart = False
                            end = deathMsg.split(' on ')
                            endTimeFind = end
                            if len(end) < 2:
                                end = deathMsg.split(' in ')
                            if 'Escaped with the Orb' in deathMsg:
                                gameInfo['won'] = True
                                gameInfo['deathLoc'] = ''
                                gameInfo['deathBy'] = 'Won'
                                gameInfo['deathBranch'] = ''
                                gameInfo['deathBranchID'] = ''
                            elif 'Got out of the dungeon' in deathMsg:
                                gameInfo['won'] = False
                                gameInfo['deathLoc'] = ''
                                gameInfo['deathBy'] = 'Escaped'
                                gameInfo['deathBranch'] = ''
                                gameInfo['deathBranchID'] = ''                                
                            else:
                                gameInfo['won'] = False
                                if 'Quit the game' in deathMsg:
                                    gameInfo['deathBy'] = 'Quitting'
                                else:
                                    if 'Drowned in' in deathMsg:
                                        gameInfo['deathBy'] = 'Drowned'
                                    elif 'Fell down ' in deathMsg:
                                        gameInfo['deathBy'] = 'Fell down stairs'
                                    elif 'Asphyxiated ' in deathMsg:
                                        gameInfo['deathBy'] = 'Asphyxiation'
                                    elif 'Killed themself ' in deathMsg:
                                        deathBy = deathMsg.split(' with a ')
                                        deathBy = deathBy[1].split('(')
                                        gameInfo['deathBy'] = 'Killed themself with a ' + deathBy[0].strip()
                                    else:
                                        deathBy = deathMsg.split(' by a ')
                                        if len(deathBy) < 2:
                                            deathBy = deathMsg.split(' by ')
                                        if len(deathBy) < 2:
                                            deathBy = deathMsg.split(' to ')
                                        if len(deathBy) < 2:
                                            deathBy = deathMsg.split(' with an ')
                                                                                   
                                            
                                        deathBy = deathBy[1]
                                        if 'wielding' in deathBy:
                                            deathBy = deathBy.split(' wielding ')
                                            gameInfo['deathBy'] = deathBy[0].strip()
                                        elif 'invoked by an' in deathMsg:
                                            deathBy = deathMsg.split('invoked by an')
                                            deathBy = deathBy[1].split('(')
                                            gameInfo['deathBy'] = deathBy[0].strip()
                                        elif 'invoked by a' in deathMsg:
                                            deathBy = deathMsg.split('invoked by a')
                                            deathBy = deathBy[1].split('(')
                                            gameInfo['deathBy'] = deathBy[0].strip()                                          
                                        elif 'invoked by' in deathMsg:
                                            deathBy = deathMsg.split('invoked by')
                                            deathBy = deathBy[1].split('(')
                                            gameInfo['deathBy'] = deathBy[0].strip()
                                        elif "'s poison" in deathMsg:
                                            deathBy = deathBy.split(' on ')
                                            gameInfo['deathBy'] = deathBy[0].strip()
                                        else:  
                                            deathBy = deathBy.split('(')
                                            gameInfo['deathBy'] = deathBy[0].strip()
                                        
                                deathLoc = end[1]
                                deathLoc = deathLoc.split(' of the ')
                                if len(deathLoc) >= 2:
                                    deathLoc = deathLoc[1].replace('.', '').strip()
                                else:
                                    deathLoc = deathLoc[0].replace('.', '').strip()
                                gameInfo['deathBranch'] = deathLoc
                                gameInfo['deathBranchID'] = getID('Branch', deathLoc)
                            if len(endTimeFind) <= 2:
                                end = gameInfo['start']
                            else:
                                end = endTimeFind[2]
                            gameInfo['end'] = end
                            endSplit = end.split(' ')
                            endSplit[0] = endSplit[0][:3]
                            end = ' '.join(endSplit)
                            endTime = datetime.strptime(end, '%b %d, %Y.')
                            endForm = endTime.strftime('%Y-%m-%d')

                            gameInfo['endForm'] = endForm
                            gameInfo['deathMsg'] = introLine + ' ' + deathMsg
                        else:
                             deathMsg += ' ' + line.replace('...', '').strip()
                    elif 'Turns: ' in line:
                        spl = line.split('(')
                        line = spl[1]
                        abbr = line.split(')')[0].strip()
                        abbrSplit = specback.split(' ')

                        if abbrSplit[0] in SPECIES:
                            species = abbrSplit[0]
                            background = ' '.join(abbrSplit[1:])
                        else:
                            species = ' '.join(abbrSplit[:2])
                            background = ' '.join(abbrSplit[2:])
                                

                        specID = getID('Race', species)
                        backID = getID('Class', background)
                        
                        gameInfo['species'] = species
                        gameInfo['specID'] = specID
                        gameInfo['background'] = background
                        gameInfo['backID'] = backID
                        
                        spl = line.split('Turns: ')[1]
                        spl = spl.split(', Time: ')
                        gameInfo['turns'] = spl[0].strip()
                        gameInfo['time'] = spl[1].strip()
                        time = spl[1].strip()
                        timeInMin = 0
                        if ', ' in time:
                            timeSpl = time.split(', ')
                            timeInMin = int(timeSpl[0])*24*60
                            timeSpl = timeSpl[1].split(':')
                        else:
                            timeSpl = time.split(':')
                            
                        gameInfo['min'] = timeInMin + int(timeSpl[0])*60+int(timeSpl[1])
                        
                    elif 'XL: ' in line:
                        split = shrinkList(line.split(' '))
                        XLKeys = ['HP', 'AC', 'Str', 'XL:', 'Next:'] 
                        values = getKeyedValues(split, XLKeys)
                            
                        hp = values['HP'][0].split('/')
                        gameStats['curHP'] = hp[0]
                        gameStats['maxHP'] = hp[1]
                        
                        for key in XLKeys[1:4]:
                            if len(values[key]) > 1:
                                gameStats[key] = values[key][1]
                            else:
                                gameStats[key] = values[key][0]
                    elif 'God:' in line:
                        split = shrinkList(line.split(' '))
                        GodKeys = ['MP', 'EV', 'Int', 'God:']
                        values = getKeyedValues(split, GodKeys)
                        mp = values['MP'][0].split('/')
                        gameStats['curMP'] = mp[0]
                        gameStats['maxMP'] = mp[1]
                        
                        for key in GodKeys[1:3]:
                            if len(values[key]) > 1:
                                gameStats[key] = values[key][1]
                            else:
                                gameStats[key] = values[key][0]
                                
                        if len(values['God:']) == 0:
                            gameInfo['god'] = 'NO DEITY'
                            gameInfo['piety'] = 0
                        elif len(values['God:']) == 1:
                            gameInfo['god'] = values['God:'][0]
                            gameInfo['piety'] = 0
                        else:
                            if '*' in values['God:'][0]:
                                gameInfo['piety'] = 0
                                values['God:'][0] = values['God:'][0].replace('*','').strip()
                            else:
                                gameInfo['piety'] = countChar(values['God:'].pop(), '*')
                            gameInfo['god'] = ' '.join(values['God:'])

                        gameInfo['godID'] = getID('Deity', gameInfo['god'])
                    elif 'Gold ' in line:
                        split = shrinkList(line.split(' '))
                        GoldKeys = ['Gold', 'SH', 'Dex', 'Spells:']
                        values = getKeyedValues(split, GoldKeys)
                        
                        for key in GoldKeys[:3]:
                            if len(values[key]) > 1:
                                gameStats[key] = values[key][1]
                            else:
                                gameStats[key] = values[key][0]

                        gameStats['spellMem'] = int(values['Spells:'][0])
                        gameStats['spellMax'] = int(values['Spells:'][2])+gameStats['spellMem']
                    elif 'rFire  ' in line:
                        split = shrinkList(line.split('  '))
                        gameRes['rFire'] = countChar(split[1], '+')
                        gameRes['SeeInvis'] = countChar(split[3], '+')
                    elif 'rCold  ' in line:                        
                        split = shrinkList(line.split('  '))
                        gameRes['rCold'] = countChar(split[1], '+')
                        gameRes['Clarity'] = countChar(split[3], '+')        
                    elif 'rNeg  ' in line:                        
                        split = shrinkList(line.split('  '))
                        gameRes['rNeg'] = countChar(split[1], '+')
                        gameRes['rCorr'] = countChar(split[3], '+')
                    elif 'rPois  ' in line:                        
                        split = shrinkList(line.split('  '))
                        gameRes['rPois'] = countChar(split[1], '+')
                        gameRes['rRot'] = countChar(split[3], '+')                    
                    elif 'rElec  ' in line:                        
                        split = shrinkList(line.split('  '))
                        gameRes['rElec'] = countChar(split[1], '+')
                        gameRes['Spirit'] = countChar(split[3], '+')                                    
                    elif 'Warding  ' in line:                        
                        split = shrinkList(line.split('  '))
                        gameRes['SustAb'] = countChar(split[1], '+')
                        gameRes['Warding'] = countChar(split[3], '+')                                    
                    elif 'rMut  ' in line:                        
                        split = shrinkList(line.split('  '))
                        gameRes['rMut'] = countChar(split[1], '+')
                        gameRes['NoTele'] = countChar(split[3], '+')                                               
                    elif 'Gourm  ' in line or 'Saprov ' in line:                        
                        split = shrinkList(line.split('  '))
                        gameRes['Gourm'] = countChar(split[1], '+')
                    elif 'MR  ' in line:                        
                        split = shrinkList(line.split('  '))
                        gameRes['MR'] = countChar(split[1], '+')
                    elif 'runes' in line and '}: ' in line:
                        split = line.split('runes: ')
                        split = split[1].split(',')
                        for r in split:
                            gameRunes.append( (r.strip(), ))
                    elif 'Inventory:' in line:
                        parseInv = True
                    elif parseInv and ' - ' in line:
                        itemInfo = parseItem(line)    
                        gameEquipment.append( itemInfo)
                        
                    elif 'Skills:' in line:
                        parseInv = False
                        parseSkill = True
                    elif parseSkill and 'Level' in line:
                        line = line.split('Level ')[1]
                        line = line.split(' ')
                        skillLvl = line[0]
                        if '(' in skillLvl:
                            skillLvl = skillLvl.split('(')[0].strip()
                        skillName = ' '.join(line[1:])
                        gameSkills.append( (skillName, skillLvl) )
                    elif 'spell levels left' in line or 'spell level left' in line or " couldn't memorise" in line:
                        parseSkill = False
                        parseSpell = True
                    elif parseSpell and ' - ' in line:
                        line = line.split(' - ')[1]
                        line = line.split('  ')
                        spell = line[0].strip()
                        spellID = getID('Spell', spell)
                        gameSpells.append( (spellID,))
                    elif 'Branches:' in line:
                        parseSpell = False
                        parseBranch = True
                    elif parseBranch and '(' in line:
                        split = shrinkList(line.split('  '))

                        branchName = ''
                        expFloors = ''
                        totalFloors = ''
                        for w in split:
                            dSplit = w.split(' ')
                            for d in dSplit:
                                d = d.strip()
                                if '(' not in d and ':' not in d:
                                    if expFloors and branchName:
                                        branchID = getID('Branch', branchName)
                                        gameBranches.append( (branchID, expFloors, totalFloors) )
                                        branchName = ''
                                        expFloors = ''
                                        totalFloors = ''
                                    branchName = d
                                    
                                elif '(' in d:
                                    d = d.replace('(', '').replace(')', '')
                                    floors = d.split('/')
                                    expFloors = floors[0]
                                    totalFloors = floors[1]
                        if expFloors and branchName:
                            branchID = getID('Branch', branchName)
                            gameBranches.append( (branchID, expFloors, totalFloors) )            
                    elif 'Altars:' in line or 'Message History' in line or 'Shops:' in line:
                        parseBranch = False

                    lineNum += 1
                if crawlGame:
                    gameVal = dictToList(gameInfo, ['file', 'serverID', 'playerID', 'versionID', 'specID', 'backID', 'godID', 'piety', 'title', 'startForm', 'endForm', 'turns', 'min', 'deathBy', 'deathLvl', 'deathBranchID', 'deathMsg', 'score', 'won'])

                    cursor.execute(GAMEINS, gameVal)
                    gameID = cursor.lastrowid
                    
                    gameStats['gameID'] = gameID
                    statVal = dictToList(gameStats, ['gameID', 'curHP', 'maxHP', 'curMP', 'maxMP', 'Gold', 'AC', 'EV', 'SH', 'Str', 'Int', 'Dex', 'XL:', 'spellMem', 'spellMax'])
                    gameRes['gameID'] = gameID
                    resVal = dictToList(gameRes, ['gameID', 'rFire', 'rCold', 'rNeg', 'rPois', 'rElec', 'SustAb', 'rMut', 'Gourm', 'MR', 'SeeInvis','Clarity', 'rCorr', 'rRot', 'Spirit', 'Warding', 'NoTele'])
                
                
                    cursor.execute(GAMESTATINS, statVal)
                    cursor.execute(GAMERESINS, resVal)
                    cursor.executemany(GAMESPELLINS, addToTupleList(gameID, gameSpells))
                    cursor.executemany(GAMESKILLINS, addToTupleList(gameID, gameSkills))    
                    cursor.executemany(GAMEBRANCHINS, addToTupleList(gameID, gameBranches))
                    cursor.executemany(GAMEEQUIPMENTINS, addToTupleList(gameID, gameEquipment))
                    cursor.executemany(GAMERUNEINS, addToTupleList(gameID, gameRunes))               
                    
                    db.commit()
                ## use gameInfo to insert into Game, then grab ID for rest of inserts
            #    gameInfo = {} - serverID, playerID, versionID, specID, backID, godID, piety, title, startForm, endForm, turns, min, deathBy, deathLvl, deathBranchID, deathMsg, score
            #    gameStats = {} - gameID, curHP, maxHP, curMP, maxMP, gold, ac, ev, sh, str, intel, dex, XL, spellMem, spellMax 
            #    gameRes = {} - gameID, rFire, rCold, rNeg, rElec, SustAb, rMut, Gourm, MR, SeeInvis, Clarity, rCorr, rRot, Spirt, Warding, NoTele 
            #    
            #    gameSpells = []
            #    gameSkills = []
            #    gameBranches = []
            #    gameEquipment = []
            #    gameRunes = []        

