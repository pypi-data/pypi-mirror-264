from pydantic import BaseModel
from faker import Faker
import os
import csv
import pandas as pd
import random
import re
from datetime import datetime
import pkg_resources
import glob
import time
import logging
import unidecode
import spacy

########################################## H E L P E R S ##########################################

faker = Faker(["fr_FR"])

########################################## V A R I A B L E S ########################################## 

# Ressources
dict_path = pkg_resources.resource_filename(__name__, 'resources')

########################################## C L A S S E S ##########################################


    




class Translation:
    """ Classe pour gérer le cache d'anomysation et fonctions de désanonymisation """

    emailsSource:dict
    emailsCode:dict
    emailsTarget:dict
    emailsCompteur:int

    websitesSource:dict
    websitesCode:dict
    websitesTarget:dict
    websitesCompteur:int

    lettres:list

    # permet de stocker les mots trouvés dans le paragraphe source après le split lors de l'appel de anonymiser_paragraphe
    listWordsInSource:list
    

    def __init__(self):
        self.anonymisations={}
        self.desanonymisations={}
        self.listExcludedWords=[]
        self.blacklists={}
        
        self.setupEmailsWebsitesAnonymisation()

        self.villes = None
        self.departements = None
        self.regions = None
        self.clients = None
        self.noms = None
        self.chaines = None
        self.acronymes = None
        self.blacklist = None

        self.logger = None
        self.currentParagraphe = None

        self.listWordsInSource = []

        self.syllabsForBlacklist=["BA","CO","CHU","NO","TA","KO","ZE","HU","PO","DI","QUE"]

        self.ambiguites={}

    def __str__(self) -> str:
        string=""
        string+="===== Détail de TRANSLATION ======\n"
        string+="___ Anonymisation ___\n"
        for key in self.anonymisations.keys():
            string+=f"Source = {key} => destination = {self.anonymisations[key]}\n"
        
        string+="\n"
        string+="___ Désanonymisation ___\n"
        for key in self.desanonymisations.keys():
            string+=f"Source = {key} => destination = {self.desanonymisations[key]}\n"
        string+="\n"
        string+="___ Emails ___\n"
        for key in self.emailsSource.keys():
            code=self.emailGetCodeFromSource(key)
            target = self.emailGetTargetFromCode(code)
            string+=f"Source = {key} => destination = {target}\n"
        string+="\n"
        string+="___ Site web ___\n"
        for key in self.websitesSource.keys():
            code=self.websiteGetCodeFromSource(key)
            target = self.websiteGetTargetFromCode(code)
            string+=f"Source = {key} => destination = {target}\n"
        string+="\n"
        string+="___ Mots blacklistés ___\n"
        for key in self.blacklists.keys():
            string+=f"Mot = {key} => remplacement = {self.blacklists[key]}\n"
        string+="\n"
        string+="___ Ambiguités ___\n"
        for key in self.ambiguites.keys():
            string+=f"{self.ambiguites[key]}\n"
        string+="\n"

        return string
    
    def setLogger(self,logger):
        self.logger=logger

    def setVilles(self,villes:list):
        if villes != None and isinstance(villes,list):
            self.villes = villes

    def setDepartements(self,departements:list):
        if departements != None and isinstance(departements,list):
            self.departements = departements
    
    def setRegions(self,regions:list):
        if regions != None and isinstance(regions,list):
            self.regions = regions
    
    def setClients(self,clients:list):
        if clients != None and isinstance(clients,list):
            self.clients = clients

    def setPrenoms(self,prenoms:list):
        if prenoms != None and isinstance(prenoms,list):
            self.prenoms = prenoms

    def setChaines(self,chaines:list):
        if chaines != None and isinstance(chaines,list):
            self.chaines = chaines

    def setAcronymes(self,acronymes:list):
        if acronymes != None and isinstance(acronymes,list):
            self.acronymes = acronymes

    def setBlacklist(self,blacklist:list):
        if blacklist != None and isinstance(blacklist,list):
            self.blacklist = blacklist


    # stocke les mots en minuscule du paragraphe en cours d'anonymisation
    def setCurrentParagraphe(self,paragraphe:str):
        if paragraphe == None:
            return
        self.currentParagraphe = paragraphe

    
    # on alimente les 2 hashmaps anonymisations et desanonymisations avec les valeurs source <-> cible de remplacements
    # /!\ ATTENTION /!\ cette méthode remplace les valeurs des 2 hashmaps
    def setRemplacements(self,remplacements:pd.DataFrame):
        """ Prépare la liste des mots à remplacer """
        
        if not isinstance(remplacements,pd.DataFrame):
            return

        df=remplacements

        if df.empty:
            return

        # on enleve les doublons dans la colonne remplacement
        df.drop_duplicates(["remplacement"], keep='first', inplace=True)

        # on enleve les doublons dans la colonne texte
        df.drop_duplicates(["texte"], keep='first', inplace=True)

        ### hashmap anonymisations ###
        self.anonymisations = df.groupby('texte')['remplacement'].agg(list).to_dict()
        for key in self.anonymisations.keys():
            self.anonymisations[key]=self.anonymisations[key][0]

        ### hashmap desanonymisations ###
        self.desanonymisations = df.groupby('remplacement')['texte'].agg(list).to_dict()
        for key in self.desanonymisations.keys():
            self.desanonymisations[key]=self.desanonymisations[key][0]


    def actionAnonymisationNombre(self,value:str,action="add") -> str:

        if value == None:
            return None

        if action == "add":
            foundNumber=False
            number=0
            # on regarde s'il existe dans la hashmap desanonymisation
            if value in self.desanonymisations:
                return self.desanonymisations[value]
            else:
                # on ajoute aux hashmaps
                while foundNumber == False:
                    number_str = str(random.randint(1,5000))
                    if not number_str in self.listWordsInSource and not number_str == value:
                        foundNumber=True

                # ajout à anonymisations
                self.anonymisations[value]=number_str
                
                # ajout à desanonymisations
                self.desanonymisations[number_str]=value
                

                return number_str
        else: 
            if value in self.anonymisations.keys():
                del self.anonymisations[value]

    def actionAnonymisationParDomaine(self,domaine:str,value:str,action="add") -> str:
        liste=None
        if domaine == "villes":
            liste=self.villes
        elif domaine == "departements":
            liste=self.departements
        elif domaine == "regions":
            liste=self.regions
        elif domaine == "clients":
            liste=self.clients
        elif domaine == "prenoms":
            liste=self.prenoms
        elif domaine == "chaines":
            liste=self.chaines
        elif domaine == "acronymes":
            liste=self.acronymes

        if liste != None:
            returnValue=self.actionAnonymisationParListe(liste=liste,value=value,action=action)
            
            # Première lettre en majuscule pour l'ajout uniquement
            if action == "add" and returnValue != None :
                if domaine in  ["prenoms","villes","regions","departements"] :
                    returnValue = returnValue.capitalize()
            
            return returnValue
        else:
            return value

    def actionAnonymisationParListe(self,liste:list,value,action) -> str:
        anonymisation = None

        if action == "add":

            self.log(f"Recupération de la valeur anonymisée pour {value}",loglevel=logging.DEBUG)

            if liste != None and len(liste) > 0 :
                if value in self.anonymisations.keys():
                    anonymisation = self.anonymisations[value] 
                else:
                    foundValue = False
                    # on cherche tant que la valeur de remplacement est identique à la valeur initiale
                    while not foundValue:
                        indexChoix=random.randint(0,len(liste)-1)
                        choix=liste[indexChoix]

                        # A TESTER : vérifier que le terme de remplacement n'existe pas dans le tableau des mots du paragraphe à anonymiser
                        flagAucunConflitAvecTexte=True

                        # on prend le texte qui est en cours d'anonymisation
                        pattern=re.compile(".*"+choix+".*",re.MULTILINE | re.IGNORECASE)
                        if self.currentParagraphe != None and re.match(pattern,self.currentParagraphe):
                            flagAucunConflitAvecTexte=False
                        
                        self.log("Test pattern " + choix + " => Aucun conflit avec le paragraphe ? " + str(flagAucunConflitAvecTexte),loglevel=logging.DEBUG)
                        

                        if flagAucunConflitAvecTexte and choix != value and not self.isInListExcludedWords(choix):
                            foundValue = True

                    # on enlève la valeur de la liste des valeurs disponibles 
                    anonymisation=liste.pop(indexChoix)
            else:
                # si pas de liste, on renvoie la valeur à anonymiser
                anonymisation = value

            # on ajoute la valeur à l'anonymisation et desanonymisation
            self.anonymisations[value]=anonymisation
            self.desanonymisations[anonymisation]=value
            
            return anonymisation
            
        if action == "remove":

            self.log(f"Suppression de la valeur anonymisée pour {value}",loglevel=logging.DEBUG)

            if liste != None and len(liste) > 0 :

                if value in self.anonymisations.keys():
                    anonymisation = self.anonymisations[value] 
                # on enleve des valeurs anonymisées
                self.anonymisations.pop(value)
                # on enleve des valeurs desanonymisées
                self.desanonymisations.pop(anonymisation)
                # on rajoute à la liste pour disponibilité
                liste.append(value)

    def addSimpleAnomynisation(self,source:str,target:str):
        if source == None or target == None:
            return
        # on ajoute ssi la source n'existe pas dans la hashmap anonymisation, et target pas dans desanonymisation
        # ??? indépendamment de la casse
        if not source in self.anonymisations and not target in self.desanonymisations:
            self.anonymisations[source]=target
            self.desanonymisations[target]=source
        
    def getDesanonymisation(self,value:str,searchWithBeginningQuote:bool=False) -> str:
        if value == None:
            return None
        
        desanonymisation = None

        # le LLM peut ajouter l' devant des mots commençant par une voyelle
        # si on veut désanonymiser des mots qui contiendraient une ' comme "l'expérience"
        # on recherche après la quote
        prefix=None
        suffix=None
        if searchWithBeginningQuote:
            pattern=re.compile("(.*')(.*)",re.IGNORECASE)
            matches=re.match(pattern,value)
            if matches:
                prefix=matches.group(1)
                suffix=matches.group(2)
        

        # https://www.tutorialspoint.com/python-program-to-compare-two-strings-by-ignoring-case
        for key in self.desanonymisations.keys():
            
            if searchWithBeginningQuote and suffix != None:
                value=suffix

            if value.lower() == key.lower():
                desanonymisation = self.desanonymisations[key]

        # on recolle le terme désanonymisé au prefix
        if searchWithBeginningQuote and desanonymisation != None and prefix != None:
                desanonymisation=prefix+desanonymisation

        return desanonymisation

    # recherche une valeur dans le cache de translation pour éviter de rechercher à nouveau
    def getAnonymisation(self,value:str) -> str:
        if value == None:
            return None
        
        anonymisation = None
        # https://www.tutorialspoint.com/python-program-to-compare-two-strings-by-ignoring-case
        for key in self.anonymisations.keys():
            if value.lower() == key.lower():
                anonymisation = self.anonymisations[key]
                break
        return anonymisation

    def checkDataInBlacklist(self,word:str) -> str:
        if word == None and not isinstance(word,str):
            return None
        
        remplacement=None
        flagMotRemplacement=False

        # est-ce c'est déjà dans la liste self.blacklists ?
        if word in self.blacklists.keys():
            return self.blacklists[word]

        # on crée un mot pour blacklister
        for item in self.blacklist:
            if item != None and item.lower() == word.lower():
                # mot blacklisté
                # genération d'un mot de remplacement
                remplacement=""
                while not flagMotRemplacement:
                    for i in range (0,10):
                        remplacement=remplacement+random.choice(self.syllabsForBlacklist)
                    if not remplacement in self.desanonymisations:
                        flagMotRemplacement=True
                        # ajout aux différents hashmaps ano et desano
                        self.addSimpleAnomynisation(word,remplacement)

                        # on ajoute à self.blacklists
                        self.blacklists[word]=remplacement

                break

        if flagMotRemplacement == False or remplacement == None or remplacement == "":
            remplacement=word
        return remplacement

    def isInListExcludedWords(self,word) -> bool:
        return word in self.listExcludedWords

    def addExcludedWord(self,word):
        if not word in self.listExcludedWords:
            self.listExcludedWords.append(word)

    def displayListExcludedWords(self):
        self.log("",loglevel=logging.DEBUG)
        self.log(f"======== Liste mots exclus ========",loglevel=logging.DEBUG)
        for item in self.listExcludedWords:
            self.log(item,loglevel=logging.DEBUG)
        self.log("",loglevel=logging.DEBUG)
 
    def log(self,text:str,loglevel:int = logging.info):
        if self.logger != None:
            if loglevel == logging.DEBUG:
                self.logger.debug(text)
            if loglevel == logging.INFO:
                self.logger.info(text)
            if loglevel == logging.ERROR:
                self.logger.error(text)

    def setupEmailsWebsitesAnonymisation(self):
        self.emailsSource={}
        self.emailsCode={}
        self.emailsTarget={}
        self.emailsCompteur=1

        self.websitesSource={}
        self.websitesCode={}
        self.websitesTarget={}
        self.websitesCompteur=1
        
        self.lettres=["a","b","c","d","e","f","g","i","j","k","l","m","n","o","p","z"]
        

    # renvoie le code
    def emailAdd(self,emailSource:str) ->str:
        if emailSource == None:
            return None
        if emailSource.lower() in self.emailsSource.keys():
            return self.emailsSource[emailSource.lower()][0]
        else:
            # genérarion d'un code
            emailCode=""
            while emailCode == "" or emailCode in self.emailsCode:
                for i in range(30):
                    emailCode+=self.lettres[random.randint(0,len(self.lettres)-1)]
            
            # generation de l'email target
            emailTarget=f"fakemail{self.emailsCompteur}@mabal.fr".lower()
            self.emailsCompteur=self.emailsCompteur+1


            # création des entrées de dictionnaires            
            self.emailsSource[emailSource]={"code": emailCode, "target": emailTarget}
            self.emailsCode[emailCode]={"source": emailSource, "target": emailTarget}
            self.emailsTarget[emailTarget]={"source": emailSource, "code":emailCode}

    def emailGetCodeFromSource(self,emailSource) ->str:
        if emailSource.lower() in self.emailsSource:
            return self.emailsSource[emailSource.lower()]["code"]
        else:
            return None
        
    def emailGetCodeFromTarget(self,emailTarget) ->str:
        if emailTarget.lower() in self.emailsTarget:
            return self.emailsTarget[emailTarget.lower()]["code"]
        else:
            return None
        
    def emailGetTargetFromCode(self,emailCode) ->str:
        if emailCode.lower() in self.emailsCode:
            return self.emailsCode[emailCode.lower()]["target"]
        else:
            return None
        
    def emailGetSourceFromCode(self,emailCode) ->str:
        if emailCode.lower() in self.emailsCode:
            return self.emailsCode[emailCode.lower()]["source"]
        else:
            return None

    def emailPrintFromSource(self,source) :
        code=self.emailGetCodeFromSource(source)
        target=self.emailGetTargetFromCode(code)
        print(f"Source={source} | code={code} | target={target}")

    def emailPrintFromCode(self,code) :
        source=self.emailGetSourceFromCode(code)
        target=self.emailGetTargetFromCode(code)
        print(f"Source={source} | code={code} | target={target}")
    
    def emailPrintFromTarget(self,target) :
        code=self.emailGetCodeFromTarget(target)
        source=self.emailGetSourceFromCode(code)
        print(f"Source={source} | code={code} | target={target}")

    def emailReplaceCodeByTarget(self,texte) ->str:
        if texte == None:
            return None
        
        for code in self.emailsCode.keys():
            texte = texte.replace(code,self.emailGetTargetFromCode(code))
        
        return texte
    
    def emailReplaceTargetByCode(self,texte) ->str:
        if texte == None:
            return None
        
        for target in self.emailsTarget.keys():
            texte = texte.replace(target,self.emailGetCodeFromTarget(target))
        
        return texte
    
    def emailReplaceCodeBySource(self,texte) ->str:
        if texte == None:
            return None
        
        for code in self.emailsCode.keys():
            texte = texte.replace(code,self.emailGetSourceFromCode(code))
        
        return texte
    

     # renvoie le code website
    def websiteAdd(self,websiteSource:str) ->str:
        if websiteSource == None:
            return None
        if websiteSource.lower() in self.websitesSource.keys():
            return self.websitesSource[websiteSource.lower()][0]
        else:
            # genérarion d'un code
            websiteCode=""
            while websiteCode == "" or websiteCode in self.websitesCode:
                for i in range(30):
                    websiteCode+=self.lettres[random.randint(0,len(self.lettres)-1)]
            
            # generation du website target
            websiteTarget=f"fakewebsite{self.websitesCompteur}@monsite.fr".lower()
            self.websitesCompteur=self.websitesCompteur+1

            # création des entrées de dictionnaires            
            self.websitesSource[websiteSource]={"code": websiteCode, "target": websiteTarget}
            self.websitesCode[websiteCode]={"source": websiteSource, "target": websiteTarget}
            self.websitesTarget[websiteTarget]={"source": websiteSource, "code":websiteCode}

    def websiteGetCodeFromSource(self,websiteSource) ->str:
        if websiteSource.lower() in self.websitesSource:
            return self.websitesSource[websiteSource.lower()]["code"]
        else:
            return None
        
    def websiteGetCodeFromTarget(self,websiteTarget) ->str:
        if websiteTarget.lower() in self.websitesTarget:
            return self.websitesTarget[websiteTarget.lower()]["code"]
        else:
            return None
        
    def websiteGetTargetFromCode(self,websiteCode) ->str:
        if websiteCode.lower() in self.websitesCode:
            return self.websitesCode[websiteCode.lower()]["target"]
        else:
            return None
        
    def websiteGetSourceFromCode(self,websiteCode) ->str:
        if websiteCode.lower() in self.websitesCode:
            return self.websitesCode[websiteCode.lower()]["source"]
        else:
            return None

    def websitePrintFromSource(self,source) :
        code=self.websiteGetCodeFromSource(source)
        target=self.websiteGetTargetFromCode(code)
        print(f"Source={source} | code={code} | target={target}")

    def websitePrintFromCode(self,code) :
        source=self.websiteGetSourceFromCode(code)
        target=self.websiteGetTargetFromCode(code)
        print(f"Source={source} | code={code} | target={target}")
    
    def websitePrintFromTarget(self,target) :
        code=self.websiteGetCodeFromTarget(target)
        source=self.websiteGetSourceFromCode(code)
        print(f"Source={source} | code={code} | target={target}")

    def websiteReplaceCodeByTarget(self,texte) ->str:
        if texte == None:
            return None
        
        for code in self.websitesCode.keys():
            texte = texte.replace(code,self.websiteGetTargetFromCode(code))
        
        return texte

    def websiteReplaceTargetByCode(self,texte) ->str:
        if texte == None:
            return None
        
        for target in self.websitesTarget.keys():
            texte = texte.replace(target,self.websiteGetCodeFromTarget(target))
        
        return texte
    
    def websiteReplaceCodeBySource(self,texte) ->str:
        if texte == None:
            return None
        
        for code in self.websitesCode.keys():
            texte = texte.replace(code,self.websiteGetSourceFromCode(code))
        
        return texte

class Configuration:
    def __init__(self,
                 remplacement=False, 
                 blacklist=False,
                 acronyme=False, 
                 ville=False, 
                 departement = False, 
                 region = False, 
                 chaine=False,
                 nom=False,
                 date=False,
                 heure=False,
                 nombre=False,
                 pays=False,
                 entreprise=False,
                 lien=False,
                 email=False,
                 flagAmeliorationBasiqueTexte=False,
                 searchWithBeginningQuote=False,
                 logger=None
                 ):
        self.ville = ville
        self.departement = departement
        self.region = region
        self.chaine = chaine
        self.nom = nom
        self.date = date
        self.heure = heure
        self.nombre = nombre
        self.pays = pays
        self.entreprise = entreprise
        self.lien = lien
        self.email = email
        self.acronyme = acronyme
        self.remplacement = remplacement
        self.blacklist = blacklist
        self.flagAmeliorationBasiqueTexte = flagAmeliorationBasiqueTexte
        self.searchWithBeginningQuote = searchWithBeginningQuote
        

    ville: bool
    departement : bool
    region : bool
    chaine: bool
    nom: bool
    date: bool
    heure: bool
    nombre: bool
    pays: bool
    entreprise: bool
    lien: bool
    email: bool
    acronyme: bool
    remplacement: bool
    blacklist: bool
    flagAmeliorationBasiqueTexte: bool
    searchWithBeginningQuote:bool

           
    def checkSetupLists(self,translation:Translation) -> bool:
        
        if translation == None:
            pass
            

        """
        if self.ville:

        self.departement = departement
        self.region = region
        self.chaine = chaine
        self.nom = nom
        self.pays = pays
        self.entreprise = entreprise
        self.lien = lien
        self.email = email
        self.acronyme = acronyme
        
        """
        return True

class textAnonyms(BaseModel):
    originalText: str
    textFormat: str

########################################## F O N C T I O N S ###########################################


class Anonymizer:

    logger:logging
    configuration:Configuration
    nlp:any
    doc:any

    # Données externes
    liste_pays:list
    regions_france_metropolitaine:list
    departements_france:list
    villes:list
    acronymes:list
    clients:list
    chaines:list
    prenoms:list
    units:list
    remplacements:list
    blacklist:list

    voyelles:list

    # dictionaires
    dictionaries:dict

    # formats de dates qui sont autorisés
    formatDatesForCheck:list

    # Valeurs de flags autorisées pour détecter la non ambiguité de classe
    arrayAcceptableFlags:list

    # Mapping classe et valeur pour les flags
    mappingClasses={}
    
    def __init__(self):

        self.logger = None
        self.configuration = None
        self.liste_pays=None
        self.regions_france_metropolitaine = None
        self.departements_france = None
        self.villes = None
        self.acronymes = None
        self.clients = None
        self.chaines = None
        self.prenoms = None
        self.units = None
        self.doc = None
        self.nlp = None
        self.remplacements = None
        self.blacklist = None
        

        self.voyelles=["a","e","i","o","u","y"]
        self.dictionaries={}
        self.arrayAcceptableFlags=[1,2,4,8,16,32,64,128,256,512,1024,2048,4096]
        self.formatDatesForCheck=["%d-%m-%Y","%d/%m/%Y","%y-%m-%Y","%Y/%m/%d"]


        self.mappingClasses[1]="Dictionnaire des mots communs"
        self.mappingClasses[2]="Chaines TV"
        self.mappingClasses[4]="Clients ou Entreprises"
        self.mappingClasses[8]="Date"
        self.mappingClasses[16]="Heure"
        self.mappingClasses[32]="Nombre entier ou flottant"
        self.mappingClasses[64]="Pays"
        self.mappingClasses[128]="Ville"
        self.mappingClasses[256]="Département français"
        self.mappingClasses[512]="Région française"
        self.mappingClasses[1024]="Prénom"
        self.mappingClasses[2048]="Acronyme"
        self.mappingClasses[4096]="Non classé"
        

    def log(self,text:str,loglevel:int = logging.info):
    
        if self.logger != None:
            if loglevel == logging.DEBUG:
                self.logger.debug(text)
            if loglevel == logging.INFO:
                self.logger.info(text)
            if loglevel == logging.ERROR:
                self.logger.error(text)


    def setupLogger(self,logfilename:str,loggername:str,loglevel:int):

        if logfilename == None or logfilename.strip() == "" or loggername == None or loggername.strip() == "":
            return

        try:
            log_dir=os.path.dirname(logfilename)  
            if not os.path.exists(log_dir):
                os.makedirs(log_dir) 

            # create logger
            self.logger = logging.getLogger(loggername)
            self.logger.setLevel(loglevel)

            # create console handler and set level to debug
            ch = logging.FileHandler(logfilename,mode="w",encoding='utf-8')
            ch.setLevel(loglevel)

            # create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # add formatter to ch
            ch.setFormatter(formatter)

            # add ch to logger
            self.logger.addHandler(ch)

            # Ajout d'une entete de log
            self.log(f"------------ Log avec le niveau {logging.getLevelName(loglevel)} ------------",loglevel=loglevel)


        except:
            # pas de logger disponible
            pass
        

    # Affiche le temps d'éxécution entre 2 temps
    def det(self,label:str,time1:time,time2:time):

        if label == None or time1 == None or time2 == None:
            return
        self.log(f"Execution de {label} : { time2-time1:0.4f} secondes",logging.DEBUG)
        
    # retourne une liste de string, d'objet
    def getDataExternes(self,name:str,type:str="text",csv_options={ "delimiter" : ";" },mode:str=None):
        lines=[]
        extension=None
        encoding=None
        match type:
            case "text":
                extension="txt"
                encoding="utf-8"
            case "csv":
                extension="csv"
                encoding="iso-8859-1"
            case _:
                extension=None
        
        if extension == None or encoding == None:
            return lines
        
        # en fonction du type, on charge les données dans une liste, en enlevant les doublons pour les données "texte"
        path=pkg_resources.resource_filename(__name__, f"resources/{name}.{extension}")
        if os.path.isfile(path):
            with open(path,"r",newline="\n") as file:
                match type:
                    case "text":
                        lines=[line.rstrip() for line in file]
                        # suppression des doublons
                        lines=list(dict.fromkeys(lines))
                        if mode == "lower":
                            lines=[line.lower() for line in lines if line]
                        if mode == "upper":
                            lines=[line.upper() for line in lines if line]
                        if mode == "capitalize":
                            lines=[line.capitalize() for line in lines if line]
                            
                    case "csv":
                        lines = pd.read_csv(file,delimiter=csv_options["delimiter"])
                    case _:
                        lines = []
        else:
            self.log(f"Problème de lecture du fichier {path}",loglevel=logging.ERROR)
        return lines

    # Recharge les données externes en fonction de la configuration
    def loadAllDataExternes(self):


        if self.configuration.pays:
            self.liste_pays = self.getDataExternes("pays",mode="lower")
        if self.configuration.region:
            self.regions_france_metropolitaine = self.getDataExternes("regions_france_metropolitaine",mode="lower")
        if self.configuration.departement:
            self.departements_france = self.getDataExternes("departements_france",mode="lower")
        if self.configuration.ville:
            self.villes = self.getDataExternes("villes",mode="lower")
        if self.configuration.acronyme:
            self.acronymes = self.getDataExternes("acronymes")
        if self.configuration.entreprise:
            self.clients = self.getDataExternes("clients")
        if self.configuration.chaine:
            self.chaines = self.getDataExternes("chaines")
        if self.configuration.nom:
            self.prenoms = self.getDataExternes("prenoms")
        if self.configuration.remplacement:
            self.remplacements = self.getDataExternes("remplacements",type="csv")
        if self.configuration.blacklist:
            self.blacklist = self.getDataExternes("blacklist")

        # tout le temps
        self.units = self.getDataExternes("units")
        


    # Si besoin de charger tous les dictionnaires en une seule fois
    def loadDictionnaries(self):
        # path to search all txt files 
        path = dict_path+f"/dictionnaire_*.txt"
        for fullname in glob.glob(path):
            # nom court du fichier sans extension
            filename=os.path.basename(fullname).split('.')[0]
            # extraction de la lettre dans le nom du fichier suivant le pattern dictionnaire_([A-Z]).txt
            result = re.search(r"^dictionnaire_(.+)$", filename)
            if result != None and result.groups() and len(result.groups()):
                lettre=result.groups()[0]
                # chargement du fichier 
                with open(fullname, 'r', encoding='utf-8') as file:
                    lines=[line.rstrip() for line in file]
                    self.dictionaries[lettre]=lines
            else:
                self.log(f"Impossible de trouver la première lettre dans le nom du fichier {fullname}",loglevel=logging.ERROR)

    def getDictionnary(self,premiere_lettre) ->dict:
        # dans le cache des dictionnaires
        if premiere_lettre == None or self.dictionaries == None or not isinstance(self.dictionaries,dict):
            return
        
        dictionary=None
        if premiere_lettre not in self.dictionaries.keys():
            # création du cache
            subdict = dict_path+f"/dictionnaire_{premiere_lettre}.txt"
            if (os.path.exists(subdict)):
                with open(subdict, 'r', encoding='utf-8') as file:
                    lines=[line.rstrip() for line in file]
                    self.dictionaries[premiere_lettre]=lines

        if premiere_lettre in self.dictionaries.keys():
            dictionary = self.dictionaries[premiere_lettre]
        
        return dictionary

    # Découpage d'un paragraphe en mot. Les espaces sont gardés dans le résultat
    def split(self,phrase) ->list:

        if phrase == None:
            return None

        # amélioration basique du texte
        if self.configuration != None and self.configuration.flagAmeliorationBasiqueTexte:
            helpers={
                "NEWLINE" : ("asdrYuikBFGTnjkiuZER","\n"),
                "CARRIAGE_RETURN" : ("RTbhYUJvDFRxSZEL","\r")
            }

            # On remplace les \r et \n par un placeholder pour remettre le code en fin de split
            phrase = phrase.replace(helpers["NEWLINE"][1],helpers["NEWLINE"][0])
            phrase = phrase.replace(helpers["CARRIAGE_RETURN"][1],helpers["CARRIAGE_RETURN"][0])

            # on met un blanc devant et après la phrase pour que la regex suivante avec [^\d] soit vrai pour le groupe 1
            phrase=" "+phrase+" "

            # enlève les blancs d'une chaine incluant une notion d'heure => 00:00 à 23:59
            # on crée une chaine qui sera remplacer par le format HH:mm
            regex = r"([^\d])([0-1][0-9]|2[0-4])\s*[:|h|H]\s*([0-5][0-9])([^\d])"
            subst = r"\1 __HEURE__\2|\3__HEURE__ \4"

            result = re.sub(regex, subst, phrase, 0)
            if result:
                phrase=result

            # remplace le texte ressemblance à Azerty/Bzerty par Azerty / Bzerty
            phrase = re.sub(r'([A-Z][a-z]*)\/([A-Z][a-z]*)', r'\1 / \2', phrase)

            # ajoute un espace après le point si suivi d'un mot commencant par une majuscule
            phrase = re.sub(r'\.([A-Z][a-z]*)',r'. \1',phrase)

            # découpe sur les caractères de phrase sauf le .
            #mots = re.split(r'(\s+|[;,?!:\[\]])',phrase)
            mots = re.split(r'(\s)',phrase)

            # remplacement de __HEURE__\1|\2__HEURE__ par \1h\2
            regex2 = r"(\_\_HEURE\_\_)([0-1][0-9]|2[0-4])(\|)([0-5][0-9])(\_\_HEURE\_\_)"
            subst2 = r"\2h\4"
            for index,mot in enumerate(mots):
                result2 = re.sub(regex2, subst2, mot, 0)
                if result2:
                    mots[index]=result2
        
            # remplacement de __NEWLINE__ par \n
            # remplacement de __CARRIAGE_RETURN__ par \n
            for index,mot in enumerate(mots):
                mot = mot.replace(helpers["NEWLINE"][0],helpers["NEWLINE"][1])
                mot = mot.replace(helpers["CARRIAGE_RETURN"][0],helpers["CARRIAGE_RETURN"][1])  
                mots[index] = mot
        
            completeText="".join(mots)
            # on lit ligne par ligne et on ébarde les espaces au début à la fin, on enlève les espaces multiples
            lines=completeText.splitlines()
            nbLines=len(lines)
            motsTarget=[]
            delimiter=" "
            for index,line in enumerate(lines):
                line=line.strip()
                # suppression des multiples espaces consécutifs
                line=self.shrinkDuplicateSeparator(line,source="  ",target=" ")

                #Gestion des points ( dans nombre ou séparateur de phrase, ou notation pour réduire un mot trop long (probl. pour problème))
                words=re.split(r'(\s)',line)
                nbWords=len(words)

                for index2,word in enumerate(words):
                    # on regarde si le mot contient un point ou plusieurs
                    nbDots=word.count(".")
                    # flag isFloat
                    isFloat = False

                    # si un seul point , on regarde si c'est potentiellement un nombre à partir d'un test de conversion
                    if nbDots == 1:
                        try:
                            input_1 = float(word)
                            isFloat = True
                            motsTarget.append(word)
                        except:
                            # peut-etre une mesure
                            # on extrait la partie numérique qui se suit. Exemple 35.7°C => 35.7 
                            regex3 = r"^(-?[\d]{2,}\.{0,1}[\d]*)([^\d]*)"
                            matches=re.search(regex3,word)
                            if matches and len(matches.groups())==2:
                                try:
                                    groupe1=matches.group(1)
                                    input_2 = float(groupe1)  
                                    motsTarget.append(word)                         
                                    isFloat = True

                                    # code difficile pour tester les unités comme les °
                                    # mise en commentaire pour le moment
                                    """          
                                    # est-ce que le groupe2 est une unité de mesure ?
                                    groupe2=matches.group(2)
                                    if is_unit(groupe2):
                                        print("|unit =>"+word+"|")
                                        print(word + " is a unit")
                                        isFloat = True
                                        motsTarget.append(groupe1)
                                        motsTarget.append(groupe1)
                                    """
                                except:
                                    isFloat = False
                            else:
                                isFloat = False

                    if isFloat == False: 
                        
                        if  nbDots >= 1:
                            tokens=word.split(".")
                            nbTokens=len(tokens)
                            for indexToken,token in enumerate(tokens):
                                motsTarget.append(token)
                                if indexToken < nbTokens - 1:
                                    # on met un espace après le point
                                    motsTarget.append(" . ")
                        else:
                            motsTarget.append(word)

                if index < nbLines - 1:
                    motsTarget.append("\n")

            phraseComplete="".join(motsTarget)

            # on réorganise les espaces et les .
            phraseComplete=self.shrinkDuplicateSeparator(phraseComplete,source="  ",target=" ")
            phraseComplete=self.shrinkDuplicateSeparator(phraseComplete,source=". . ",target=".. ")
            
            phrase = phraseComplete


        # fin amélioration texte

        # on recrée le tableau de mots à partir de phrase
        mots=re.split(r'(\s)',phrase)
        return mots

    # transforme une chaine pour qu'elle soit au format minuscule, pas d'accent et les espaces remplacés par des -
    # utile pour les villes / départements / régions / pays
    def transformation_text_for_search_in_list(self,text):
        if text == None:
            return None
        return unidecode.unidecode(text).replace(" ","-").lower()


    def fake_num_string(self,original) -> str:
        fakedigit=[0,1,2,3,4,5,6,7,8,9]
        fakeData = list(original)
        for i in range(len(fakeData)):
            if(fakeData[i].isnumeric()):
                digit = random.choice(fakedigit)
                fakeData[i] = str(digit)
        fakeData = "".join(fakeData)
        return fakeData

    def cherche_chaine(self,data:str) -> bool:
        data = data.upper()
        if self.chaines == None or not isinstance(self.chaines,list):
            return False
        return any( data == chaine.upper() for chaine in self.chaines if chaine)

    def cherche_ville(self,data:str) -> bool:
        liste = self.villes
        if liste == None or data == None:
            return False        
        return self.transformation_text_for_search_in_list(data) in liste

    def cherche_departement_france(self,data:str) -> bool:
        liste = self.departements_france
        if liste == None or data == None:
            return False        
        return self.transformation_text_for_search_in_list(data) in liste

    def cherche_region_france(self,data:str) -> bool:
        liste = self.regions_france_metropolitaine
        if liste == None or data == None:
            return False        
        return self.transformation_text_for_search_in_list(data) in liste

    def cherche_pays(self,data:str) -> bool:
        liste = self.liste_pays
        if liste == None or data == None:
            return False        
        return self.transformation_text_for_search_in_list(data) in liste

    # a modifier
    def is_unit(self,word:str) -> bool:
        return ( word!= None and self.units != None and any(word == x for x in self.units) )

    def is_in_dico(self,mot:str) -> bool:
        if mot == None :
            return False    
        
        premiere_lettre = mot[0].upper()   
        dictionary=self.getDictionnary(premiere_lettre)
        return ( dictionary!= None and mot.lower() in dictionary )

    def shrinkDuplicateSeparator(self,text:str,source:str,target:str) -> str:
        """ Permet de réduire une chaine où il y a des répetition de pattern """
        """ exemple : . . . vers ..."""
        # la soure ne doit pas être incluse dans la target pour éviter la boucle infinie
        if str == None or source == None or target == None or source in target:
            return text
        while source in text:
            text=text.replace(source,target)
        return text

    def anonymiser_mot(self,text: textAnonyms ):
        fakehour=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        original = text.originalText
        try:
            # Initialisation
            fakeData=original
            if (text.textFormat == "CITY" and self.configuration.ville == True):
                fakeData=None
                while fakeData == None:
                    fakeData=self.translation.actionAnonymisationParDomaine("villes",original)
                    # on verifie que la fakedata commence par une voyelle si la donnée initiale commence par une voyelle
                    if (original.lower()[0] in self.voyelles) ^ (fakeData.lower()[0] in self.voyelles) == 1:
                        fakeData = None
                        self.translation.actionAnonymisationParDomaine("villes",original,action="remove")
            elif (text.textFormat == "DEPARTEMENT" and self.configuration.departement == True):
                fakeData=None
                while fakeData == None:
                    fakeData=self.translation.actionAnonymisationParDomaine("departements",original)
                    # on verifie que la fakedata commence par une voyelle si la donnée initiale commence par une voyelle
                    if (original.lower()[0] in self.voyelles) ^ (fakeData.lower()[0] in self.voyelles) == 1:
                        fakeData = None
                        self.translation.actionAnonymisationParDomaine("departements",original,action="remove")
            elif (text.textFormat == "REGION" and self.configuration.region == True):
                fakeData=None
                while fakeData == None:
                    fakeData=self.translation.actionAnonymisationParDomaine("regions",original)
                    # on verifie que la fakedata commence par une voyelle si la donnée initiale commence par une voyelle
                    if (original.lower()[0] in self.voyelles) ^ (fakeData.lower()[0] in self.voyelles) == 1:
                        fakeData = None
                        self.translation.actionAnonymisationParDomaine("regions",original,action="remove")
            elif (text.textFormat == "CHAINE" and self.configuration.chaine == True):
                fakeData=self.translation.actionAnonymisationParDomaine("chaines",original)
            elif(text.textFormat == "PRENOM" and self.configuration.nom == True):
                fakeData=self.translation.actionAnonymisationParDomaine("prenoms",original)
            elif(text.textFormat == "DATE" and self.configuration.date == True):
                fakeData = faker.date()
                fakeData = datetime.strptime(fakeData, "%Y-%m-%d")
                fakeData = fakeData.strftime("%d/%m/%Y")
            elif(text.textFormat == "HOUR" and self.configuration.heure == True):
                hour = random.choice(fakehour)
                fakehour.remove(hour)
                fakeData = (str(hour) if hour>9 else "0"+str(hour))+"h00"
            elif(text.textFormat == "NUMBER" and self.configuration.nombre == True):
                fakeData=self.translation.actionAnonymisationNombre(original)
            elif(text.textFormat == "COUNTRY" and self.configuration.pays == True):
                fakeData=self.translation.actionAnonymisationParDomaine("pays",original)
            elif(text.textFormat == "ORGANIZATION" and self.configuration.entreprise == True):
                fakeData=self.translation.actionAnonymisationParDomaine("clients",original)
            elif(text.textFormat == "ACRONYM" and self.configuration.acronyme == True):
                fakeData=self.translation.actionAnonymisationParDomaine("acronymes",original)
            elif(text.textFormat == "TEXT"):
                # On applique le remplacement des mots issus du fichier remplacements.csv
                # fakeData=
                fakeData=self.translation.getAnonymisation(original)
                if fakeData == None:
                    fakeData = original
            else: # on ne fait rien de spécial
                fakeData = original

            # on applique pour finir le processus blacklist
            fakeData = self.translation.checkDataInBlacklist(fakeData)


            return fakeData
        except Exception as e:
            print(e)
            self.log("fonction anonymiser_mot " + str(e),loglevel=logging.ERROR)
            return original



    def is_a_prenom(self,word:str) -> bool:
        # on a chargé le fichier des prénoms à l'initialisation
        if word!= None and self.prenoms != None and any(word.lower() == x.lower() for x in self.prenoms) :
            return True
        else: 
            return False 
        
    def is_a_date(self,word:str) -> bool:
        if word == None:
            return False
        flag=False
        for formatDate in self.formatDatesForCheck:
            try:
                flag = bool(datetime.strptime(word, formatDate))
                break
            except ValueError:
                flag = False
        
        return flag

    def stringIsNumberOrFloat(self,word:str) -> bool:
        if word == None:
            return False
        isFloat=False
        isNumber=False
        try:
            # on essaie de convertir en int
            number = int(word)
            isNumber=True
        except:
            pass

        if not isNumber:
            try:
                # on essaie de convertir en float
                fl = float(word)
                
                # cas des numérotation de chapitre 1. 2.
                # on regarde quand meme si le . n'est pas le dernière caractère
                if word[-1] == ".":
                    isFloat=False
                else:
                    isFloat=True



            except:
                pass

        return isFloat or isNumber


    def setupNLP(self):
        if self.nlp == None:

            time1=time.perf_counter()
            self.nlp=spacy.load("fr_core_news_sm")

            # chargement des entités
            ruler = self.nlp.add_pipe("entity_ruler")        

            if self.configuration.entreprise:
                self.log("Chargement des clients comme entité",loglevel=logging.DEBUG)
                for client in self.clients:
                    ruler.add_patterns([{"label": "ORGANIZATION", "pattern": client}])

            if self.configuration.chaine:
                self.log("Chargement des chaines comme entité",loglevel=logging.DEBUG)
                for chaine in self.chaines:
                    ruler.add_patterns([{"label": "CHAINE", "pattern": chaine}])

            if self.configuration.acronyme:
                self.log("Chargement des acronymes comme entité",loglevel=logging.DEBUG)
                for acronyme in self.acronymes:
                    ruler.add_patterns([{"label": "ACRONYM", "pattern": acronyme}])

            if self.configuration.pays:
                self.log("Chargement des pays comme entité",loglevel=logging.DEBUG)
                for pays in self.liste_pays:
                    ruler.add_patterns([{"label": "PAYS", "pattern": pays}])

            time2=time.perf_counter()
            self.det("Setup NLP + Chargement des entités",time1,time2)



    # fonction pour lever une ambiguité
    # retourne un label 
    def GetLabelToResolveAmbiguity(self,text,word):
        label=None 
        if self.doc == None and self.nlp != None:
            self.doc=self.nlp(text)
        if self.doc != None:
            for ent in self.doc.ents:
                if word in ent.text:
                    label=ent.label_
                    break
        return label


    def anonymiser_email(self,paragraphe):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        fakemail = ["fakemail"]
        nbfakemail = 1
        adresses_email = re.findall(pattern, paragraphe)
        for adresse in adresses_email:
            self.translation.emailAdd(adresse)
            fakeData=self.translation.emailGetCodeFromSource(adresse)            
            paragraphe = paragraphe.replace(adresse,fakeData)
            nbfakemail +=1
            # self.translation.addSimpleAnomynisation(source=adresse,target=fakeData)
        return paragraphe
    
        

        
    def anonymiser_lien(self,paragraphe):
        pattern = r'\bhttps?://\S+\b'
        fakelink = ["fakelink"]
        nbfakelink = 1
        liens = re.findall(pattern, paragraphe)
        for lien in liens:
            self.translation.websiteAdd(lien)
            fakeData=self.translation.websiteGetCodeFromSource(lien) 
            paragraphe = paragraphe.replace(lien,fakeData)
            nbfakelink +=1
            #self.translation.addSimpleAnomynisation(source=lien,target=fakeData)
        return paragraphe

    def anonymiser_paragraphe(self,paragraphe):

        self.log("",loglevel=logging.DEBUG)
        self.log("="*100,loglevel=logging.DEBUG)
        self.log("Paragraphe initial",loglevel=logging.DEBUG)
        self.log("="*100,loglevel=logging.DEBUG)
        self.log("\n"+paragraphe,loglevel=logging.DEBUG)
        self.log("",loglevel=logging.DEBUG)

        # on vérifie qu'en fonction de la config, nous avons tous les listes pour anonymiser
        flagSetupList=False
        if self.configuration !=None:
            flagSetupList=self.configuration.checkSetupLists(self.translation)
            # a faire ....


        time1=time.perf_counter()

        if (self.configuration.email == True):
            phrase = self.anonymiser_email(paragraphe)
        
        if (self.configuration.lien == True):
            phrase = self.anonymiser_lien(phrase)



        tokens = self.split(phrase)

        # pour éviter d'avoir les termes d'anonymisations dans la liste des mots de la source à anonymiser
        self.translation.listWordsInSource = tokens

        listmot = []
        entites_nommees = []
        index = 0
        pos_word = 0

        
        # compteur flags , contiendra la somme logigue 1|2|4|8|16|32|64|128|256
        # flagInDico=1
        # flagChaine=2
        # flagClient=4
        # flagDate=8
        # flagHour=16
        # flagNumber=32
        # flagCountry=64
        # flagCity=128
        # flagDepartement=256
        # flagRegion=512
        # flagPerson=1024
        # flagAcronyme=2048
        # flagEmpty=4096
        compteurFlag=0
        
        

        last_was_dot = True
        for word in tokens:
            compteurFlag=0
            index=index+1
            listmot.append(word)
            if ((word != " " and word != "" and word != "\n" and word != "\r")):

                # pour accélérer les comparaisons dans les listes
                wordLC = word.lower() if word != None else None
                
                

                flagIsInDico=self.is_in_dico(word)
            
                if flagIsInDico:
                    compteurFlag+=1
                if (self.cherche_chaine(word)):
                    compteurFlag+=2
                if word in self.clients or word.lower() in self.clients:
                    compteurFlag+=4
                if self.is_a_date(word):
                    compteurFlag+=8
                if (re.match("^([0-1][0-9]|2[0-3])h([0-5][0-9])$",word)):
                    compteurFlag+=16
                if self.stringIsNumberOrFloat(word):
                    compteurFlag+=32
                if self.cherche_pays(wordLC):
                    compteurFlag+=64
                if self.cherche_ville(wordLC):
                    compteurFlag+=128
                if self.cherche_departement_france(wordLC):
                    compteurFlag+=256
                if self.cherche_region_france(wordLC):
                    compteurFlag+=512
                if re.match("[A-Z].*",word) and self.is_a_prenom(word) == True:
                    compteurFlag+=1024
                if word.upper() in self.acronymes:
                    compteurFlag+=2048
                if compteurFlag == 0 and not flagIsInDico:
                    compteurFlag+=4096


                # calcul du nombre de classes
                decompte=compteurFlag
                nbClasses=0
                rangCompteur=0
                while decompte>0:
                    puissance=pow(2,rangCompteur)
                    if decompte & puissance == puissance:
                        decompte=decompte-puissance
                        nbClasses=nbClasses+1
                    rangCompteur=rangCompteur+1
                    
                # check des flags
                # print("============ " + word + " => " + str(compteurFlag) + " ===========")
                if not compteurFlag in self.arrayAcceptableFlags:

                    # on passe d'abord par le model spacy pour comprendre le mot dans son contexte
                    label=self.GetLabelToResolveAmbiguity(paragraphe,word)
                    # print(f"label = {label} pour {word}")

                    if label == "PER":
                        entites_nommees.append(("PRENOM", word,pos_word))
                        compteurFlag=1024
                    if label == "ACRONYM":
                        compteurFlag=2048
                        entites_nommees.append(("ACRONYM", word,pos_word))
                    elif label == "ORG":
                        entites_nommees.append(("ORGANIZATION", word,pos_word))
                        compteurFlag=4
                    elif label == "LOC":
                        entites_nommees.append(("CITY", word,pos_word))
                        compteurFlag=128
                    else:
                        # si ce n'est aucun des labels au dessus
                        # on applique une règle simple pour enlever l'ambiguité
                        # si 2 classes et une des classes est celle des mots communs, et commence par une minuscule alors on choisit le mot commun.
                        if nbClasses == 2 and compteurFlag & 1 == 1 and word[0].islower():
                            compteurFlag=1
                        else:
                            # On ne peut trancher, on indique au service de translation que le mot ne peut pas être utilisé pour anonymiser
                            self.translation.addExcludedWord(word)



                if compteurFlag in self.arrayAcceptableFlags:
                    # on append les entitées nommées pour les données non ambigues
                    if compteurFlag == 1:
                        entites_nommees.append(("",word,pos_word))
                    elif compteurFlag == 2:    
                        entites_nommees.append(("CHAINE",word,pos_word))
                    elif compteurFlag == 4:    
                        entites_nommees.append(("ORGANIZATION",word,pos_word))
                    elif compteurFlag == 8:    
                        entites_nommees.append(("DATE", word,pos_word))
                    elif compteurFlag == 16:    
                        entites_nommees.append(("HOUR", word, pos_word))
                    elif compteurFlag == 32:    
                        entites_nommees.append(("NUMBER", word, pos_word))
                    elif compteurFlag == 64:    
                        entites_nommees.append(("COUNTRY", word,pos_word))
                    elif compteurFlag == 128:    
                        entites_nommees.append(("CITY", word,pos_word))
                    elif compteurFlag == 256:    
                        entites_nommees.append(("DEPARTEMENT",word,pos_word))
                    elif compteurFlag == 512:    
                        entites_nommees.append(("REGION",word,pos_word))
                    elif compteurFlag == 1024:    
                        entites_nommees.append(("PRENOM",word,pos_word))
                    elif compteurFlag == 2048:    
                        entites_nommees.append(("ACRONYM",word,pos_word))
                    elif compteurFlag == 4096:    
                        entites_nommees.append(("TEXT",word,pos_word))
                    else:
                        pass
                else:
                    # on ajoute la raison de l'ambiguité dans self.ambiguites
                    decompte=compteurFlag
                    rangCompteur=0
                    texteAmbiguite="Ambiguités sur le mot << " + word + " >> car appartient aux classes :\n"
                    while decompte>0:
                        puissance=pow(2,rangCompteur)
                        if decompte & puissance == puissance:
                            if puissance in self.mappingClasses.keys():
                                texteAmbiguite=texteAmbiguite+"- "+self.mappingClasses[puissance]+"\n"
                                decompte=decompte-puissance
                        rangCompteur=rangCompteur+1

                    self.translation.ambiguites[word]=texteAmbiguite
                    

            pos_word += 1

        for entity_type, entity_value,position in entites_nommees:
            text = textAnonyms(originalText=entity_value, textFormat=entity_type)
            faketext=self.translation.getAnonymisation(entity_value)
            
            if faketext == None:
                faketext = self.anonymiser_mot(text)
            
            listmot[position]=faketext
                
            #print(entity_type + "/" + str(position) + "/" + entity_value  + " / found = ")
            #print("           ==========> faketest = " + str(faketext))
                
        paragraphe = ("".join(listmot))

        # on recolle les " ." au mot précédent
        paragraphe=self.shrinkDuplicateSeparator(paragraphe,source=" .",target=".")


        # on remplace les emails format code par le target email
        paragraphe=self.translation.emailReplaceCodeByTarget(paragraphe)

        # on remplace les sites web format code par le target siteweb
        paragraphe=self.translation.websiteReplaceCodeByTarget(paragraphe)

        # On stocke les mots dans translation pour éviter de réutiliser les mots initiaux
        self.translation.setCurrentParagraphe(paragraphe)

        
        time2=time.perf_counter()
        self.det("Anonymisation paragraphe",time1,time2)

        self.log("",loglevel=logging.DEBUG)
        self.log("="*100,loglevel=logging.DEBUG)
        self.log("Paragraphe désanonymisé",loglevel=logging.DEBUG)
        self.log("="*100,loglevel=logging.DEBUG)
        self.log("\n"+paragraphe,loglevel=logging.DEBUG)
        self.log("",loglevel=logging.DEBUG)

        # debug de la translation
        self.log("=" * 100,loglevel=logging.DEBUG)
        self.log("Tables de traduction",loglevel=logging.DEBUG)
        self.log("=" * 100,loglevel=logging.DEBUG)
        self.log("\n"+str(self.translation),loglevel=logging.DEBUG)
        self.log("",loglevel=logging.DEBUG)


        return paragraphe

    def desanonymiser_paragraphe(self,anonymous_paragraphe):

        time1=time.perf_counter()


        # on remplace les emails et siteweb par leur code
        anonymous_paragraphe = self.translation.emailReplaceTargetByCode(anonymous_paragraphe)
        anonymous_paragraphe = self.translation.websiteReplaceTargetByCode(anonymous_paragraphe)

        listmot = self.split(anonymous_paragraphe)
        
        for index,mot in enumerate(listmot):
            nouveauMot=self.translation.getDesanonymisation(mot,self.configuration.searchWithBeginningQuote)
            if nouveauMot != None :
                listmot[index]=nouveauMot
        
        anonymous_paragraphe = "".join(listmot)

        # on remplace les "  " par " "
        anonymous_paragraphe=self.shrinkDuplicateSeparator(anonymous_paragraphe,source="  ",target=" ")
        # on recolle les " ." au mot précédent
        anonymous_paragraphe=self.shrinkDuplicateSeparator(anonymous_paragraphe,source=" .",target=".")


        # on remplace les emails et siteweb par leur source
        anonymous_paragraphe = self.translation.emailReplaceCodeBySource(anonymous_paragraphe)
        anonymous_paragraphe = self.translation.websiteReplaceCodeBySource(anonymous_paragraphe)


        time2=time.perf_counter()
        self.det("Desanonymisation paragraphe",time1,time2)

        return anonymous_paragraphe


    def setConfiguration(self,configuration:Configuration):
        self.configuration = configuration
        self.loadAllDataExternes()
        self.setTranslation()
        self.setupNLP()

    def setTranslation(self):
        # Structure de translation
        translation = Translation()
        
        translation.setClients(self.clients)
        translation.setPrenoms(self.prenoms)
        translation.setVilles(self.villes)
        translation.setDepartements(self.departements_france)
        translation.setRegions(self.regions_france_metropolitaine)
        translation.setChaines(self.chaines)
        translation.setAcronymes(self.acronymes)
        translation.setRemplacements(self.remplacements)
        translation.setBlacklist(self.blacklist)
        translation.setLogger(self.logger)
        
        
        self.translation = translation
    
    def getTranslation(self):
        return self.translation




