from librairy.travailJSON import *
from gestionnaire.gestion import gestionnaire
from tkinter import filedialog,messagebox
import os
import shutil

DICTUSER = {
    "firstname-user":"",
    "lastname-user":"",
    "genre":"",
    "listVille":[""],
    "lieuDomicile":"",
    "lieuTravail":"",
    "adresseDomicile" : "",
    "adresseTravail":"",
    "dictSoft":{},
    "dictSite":{},
    "moteurRecherche":"",
    "tokenGithub":"",
    "wordFolder":"",
    "videoDownloadFolder":"",
    "soundMicro":"0",
    "listWord":[],
    "bootHist":1,
    "ia_use":0,
    "ia_model":""
}

class gestUserSetting:
    def __init__(self,gestionnaire:gestionnaire):
        self.__osDect = gestionnaire.getOSObjet()
        self.__gestionnaire = gestionnaire
        self.__firstRun = False
        # Mise en place du chemin du fichier de configuration utilisateur
        if self.__osDect.osLinux() or self.__osDect.osMac():
            home = os.path.expanduser("~")
            self.__conf_folder = str(home)+"/.config/arrera-assistant/"
            self.__userSettingPath = self.__conf_folder+"user-config.json"
            self.__userTaskPath = self.__conf_folder+"user-task.json"
            self.__userHistoriquePath = self.__conf_folder+"user-hist.json"
            self.__userEventPath = self.__conf_folder+"user-event.json"
        elif self.__osDect.osWindows():
            home = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
            self.__conf_folder = str(home)+"/arrera-assistant/"
            self.__userSettingPath = self.__conf_folder+"user-config.json"
            self.__userTaskPath = self.__conf_folder+"user-task.json"
            self.__userHistoriquePath = self.__conf_folder+"user-hist.json"
            self.__userEventPath = self.__conf_folder+"user-event.json"
        else :
            self.__userSettingPath = None


        # Teste si le fichier de configuration utilisateur existe
        if not os.path.isfile(self.__userSettingPath):
            os.makedirs(os.path.dirname(self.__userSettingPath), exist_ok=True)
            with open(self.__userSettingPath, "x", encoding="utf-8") as f:
                json.dump(DICTUSER, f, ensure_ascii=False, indent=2)

        if not os.path.isfile(self.__userTaskPath):
            with open(self.__userTaskPath, "x", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

        if not os.path.isfile(self.__userHistoriquePath):
            with open(self.__userHistoriquePath, "x", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

        if not os.path.isfile(self.__userEventPath):
            with open(self.__userEventPath, "x", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

            self.__firstRun = True

        # Chargement du fichier de configuration utilisateur
        self.__fileUser = jsonWork(self.__userSettingPath)

    def del_conf_folder(self):
        try:
            shutil.rmtree(self.__conf_folder)
            return True
        except FileNotFoundError:
            return False
        except PermissionError:
            return False
        except Exception as e:
            return False

    def getFirstRun(self):
        return self.__firstRun

    def getTaskPath(self):
        return self.__userTaskPath

    def getEventPath(self):
        return self.__userEventPath

    def getHistoriquePath(self):
        return self.__userHistoriquePath

    # Partie USER

    def setFirstnameUser(self, user:str):
        if user == "":
            return False
        return self.__fileUser.setValeurJson("firstname-user", user)

    def setLastnameUser(self, user:str):
        if user == "":
            return False
        return self.__fileUser.setValeurJson("lastname-user", user)

    def getFirstnameUser(self):
        return self.__fileUser.getContentJsonFlag("firstname-user")

    def getLastnameUser(self):
        return self.__fileUser.getContentJsonFlag("lastname-user")

    # Partie Genre

    def setGenre(self, genre:str):
        if genre == "":
            return False
        return self.__fileUser.setValeurJson("genre", genre)

    def getGenre(self):
        return self.__fileUser.getContentJsonFlag("genre")

    # Partie Ville

    def addTown(self,ville:str):
        if ville == "":
            return False

        listVille = self.__fileUser.getFlagListJson("listVille")

        if listVille is None:
            listVille = []

        if ville not in listVille:
            listVille.append(ville)
            return self.__fileUser.setValeurJson("listVille", listVille)
        else:
            return False

    def removeTown(self, ville:str):
        if ville == "":
            return False

        listVille = self.__fileUser.getFlagListJson("listVille")

        if listVille is None:
            return False

        if ville in listVille:
            listVille.remove(ville)
            return self.__fileUser.setValeurJson("listVille", listVille)
        else:
            return False

    def getTowns(self):
        listVille = self.__fileUser.getFlagListJson("listVille")
        if listVille is None:
            return None
        return listVille

    # Lieu Domicile

    def setLieuDomicile(self, lieu:str):
        if lieu == "":
            return False
        return self.__fileUser.setValeurJson("lieuDomicile", lieu)

    def getLieuDomicile(self):
        lieuDomicile = self.__fileUser.getContentJsonFlag("lieuDomicile")
        if lieuDomicile is None:
            return ""
        return lieuDomicile

    # Lieu Travail
    def setLieuTravail(self, lieu:str):
        if lieu == "":
            return False
        return self.__fileUser.setValeurJson("lieuTravail", lieu)

    def getLieuTravail(self):
        lieuTravail = self.__fileUser.getContentJsonFlag("lieuTravail")
        if lieuTravail is None:
            return ""
        return lieuTravail

    # Adresse Domicile
    def setAdresseDomicile(self, adresse:str):
        if adresse == "":
            return False
        return self.__fileUser.setValeurJson("adresseDomicile", adresse)

    def delAdresseDomicile(self):
        return self.__fileUser.setValeurJson("adresseDomicile", "")

    def getAdresseDomicile(self):
        adresseDomicile = self.__fileUser.getContentJsonFlag("adresseDomicile")
        if adresseDomicile is None:
            return ""
        return adresseDomicile

    # Adresse Travail

    def setAdresseTravail(self, adresse:str):
        if adresse == "":
            return False
        return self.__fileUser.setValeurJson("adresseTravail", adresse)

    def delAdresseTravail(self):
        return self.__fileUser.setValeurJson("adresseTravail", "")

    def getAdresseTravail(self):
        adresseTravail = self.__fileUser.getContentJsonFlag("adresseTravail")
        if adresseTravail is None:
            return ""
        return adresseTravail

    # SOFT

    def setSoft(self, soft:str):
        if soft == "":
            return False

        if self.__osDect.osLinux():
            # Demande à l'utilisateur si le programme est dans son répertoire home
            reponse = messagebox.askquestion(
                "Choix répertoire",
                "Le programme se trouve-t-il dans votre répertoire /home ?",
                icon="question"
            )

            # Définir le répertoire initial en fonction de la réponse
            initial_dir = os.path.expanduser("~") if reponse == "yes" else "/bin"

            # Boîte de dialogue pour sélectionner le fichier
            command = filedialog.askopenfilename(
                title="Sélectionner un programme",
                initialdir=initial_dir,
                filetypes=[("Tous les fichiers", "*")]
            )

            # Si l'utilisateur annule la sélection
            if not command:
                return False

            # Enregistrer le logiciel dans le fichier JSON pour Linux
            return self.__fileUser.setDictJson("dictSoft", soft, command)
        elif self.__osDect.osMac():
            reponse = messagebox.askquestion(
                "Choix répertoire",
                "Votre application se trouve-t-elle dans le dossier Applications ?",
                icon="question"
            )
            if reponse == "yes":
                reponse = messagebox.askquestion(
                    "Choix répertoire",
                    "Votre application se trouve-t-elle dans le dossier Applications utilisateur ?",
                    icon="question"
                )
                if reponse == "yes":
                    initial_dir = "/Users/Applications"
                else :
                    initial_dir = "/Applications"
            else:
                initial_dir = "/"

            command = filedialog.askopenfilename(
                title="Sélectionner un programme",
                initialdir=initial_dir,
                filetypes=[("Tous les fichiers", "*")]
            )

            if not command:
                return False

            return self.__fileUser.setDictJson("dictSoft", soft, command)
        elif self.__osDect.osWindows():
            reponse = messagebox.askquestion(
                "Choix répertoire",
                "Est-ce que votre application est dans le menu Démarrer de l’utilisateur ?",
                icon="question"
            )
            if reponse == "yes":
                shorcutDir = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs")
            else :
                shorcutDir = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs"

            command = filedialog.askopenfilename(
                title="Sélectionner un programme",
                initialdir=shorcutDir,
                filetypes=[("Raccourcis Windows", "*.lnk")]
            )
            if not command:
                return False

            return self.__fileUser.setDictJson("dictSoft", soft, command)
        else:
            return False

    def getSoft(self):
        """
        Retourne le dictionnaire des logiciels
        """
        return self.__fileUser.getFlagDictJson("dictSoft")

    def removeSoft(self, soft:str):
        """
        Supprime un logiciel du dictionnaire
        """
        if soft == "":
            return False

        return self.__fileUser.unsetDictJson("dictSoft", soft)
    # Site

    def setSite(self, site:str, url:str):
        if site == "" or url == "":
            return False
        return  self.__fileUser.setDictJson("dictSite", site, url)

    def getSite(self):
        return  self.__fileUser.getFlagDictJson("dictSite")

    def removeSite(self, site:str):
        if site == "":
            return False

        return self.__fileUser.unsetDictJson("dictSite", site)

    # Moteur de recherche
    def setMoteurRecherche(self, moteur:str):
        if moteur == "":
            return False
        return self.__fileUser.setValeurJson("moteurRecherche", moteur)

    def getMoteurRecherche(self):
        return  self.__fileUser.getContentJsonFlag("moteurRecherche")

    # Token Github
    def setTokenGithub(self, token:str):
        if token == "":
            return False
        return self.__fileUser.setValeurJson("tokenGithub", token)

    def getTokenGithub(self):
        return self.__fileUser.getContentJsonFlag("tokenGithub")

    def delTokenGithub(self):
        return self.__fileUser.setValeurJson("tokenGithub", "")

    # Work Folder

    def setWorkFolder(self):
        folder = filedialog.askdirectory(title="Dossier de travail")
        if folder == "":
            return False
        return self.__fileUser.setValeurJson("wordFolder", folder)

    def removeWorkFolder(self):
        return self.__fileUser.setValeurJson("wordFolder","")

    def getWorkFolder(self):
        return self.__fileUser.getContentJsonFlag("wordFolder")

    # Video Download Folder
    def setVideoDownloadFolder(self):
        folder = filedialog.askdirectory(title="Dossier de téléchargement de vidéo")
        if folder == "":
            return False
        return self.__fileUser.setValeurJson("videoDownloadFolder", folder)

    def removeVideoDownloadFolder(self):
        return self.__fileUser.setValeurJson("videoDownloadFolder", "")

    def getVideoDownloadFolder(self):
        return self.__fileUser.getContentJsonFlag("videoDownloadFolder")

    # Sound Micro
    def setSoundMicro(self, value:bool):
        if value:
            return self.__fileUser.setValeurJson("soundMicro", "1")
        else:
            return self.__fileUser.setValeurJson("soundMicro", "0")

    def getSoundMicro(self):
        soundMicro = self.__fileUser.getContentJsonFlag("soundMicro")
        if soundMicro is None:
            return "0"
        return soundMicro

    # List Word
    def addWord(self, word:str):
        if word == "":
            return False

        listWord = self.__fileUser.getFlagListJson("listWord")

        if listWord is None:
            listWord = []

        if word not in listWord:
            listWord.append(word)
            return self.__fileUser.setValeurJson("listWord", listWord)
        else:
            return False

    def removeWord(self, word:str):
        if word == "":
            return False

        listWord = self.__fileUser.getFlagListJson("listWord")

        if listWord is None:
            return False

        if word in listWord:
            listWord.remove(word)
            return self.__fileUser.setValeurJson("listWord", listWord)
        else:
            return False

    def getListWord(self):
        listWord = self.__fileUser.getFlagListJson("listWord")
        if listWord is None:
            return []
        return listWord

    # Partie hist
    def getHist(self):
        return int(self.__fileUser.getContentJsonFlag("bootHist"))

    def setHist(self,v:bool):
        return self.__fileUser.setValeurJson("bootHist",int(v))

    # Partie ia

    def get_use_ia(self):
        return int(self.__fileUser.getContentJsonFlag("ia_use"))

    def get_ia_model(self):
        return self.__fileUser.getContentJsonFlag("ia_model")

    def set_use_ia(self,v:bool):
        b =  self.__fileUser.setValeurJson("ia_use",int(v))
        if b:
            return self.__gestionnaire.getGestIA().loadIA()
        else :
            return False


    def set_ia_model(self,v:str):
        b = self.__fileUser.setValeurJson("ia_model",v)
        if b:
            return self.__gestionnaire.getGestIA().loadIA()
        else :
            return False

    # Partie IA pour l'inteface setting

    def get_list_model_ia_available(self):
        return self.__gestionnaire.getGestIA().get_list_model_available()

    def get_model_ia_on_directory(self):
        return self.__gestionnaire.getGestIA().get_list_model_on_dir()

    def get_data_model_ia_available(self,model:str):
        return self.__gestionnaire.getGestIA().gest_data_model(model)

    def download_ia_model(self,model:str):
        return self.__gestionnaire.getGestIA().download_model(model)

    def del_ia_model(self,model:str):
        return self.__gestionnaire.getGestIA().del_model(model)

    def get_model_downloaded(self):
        return self.__gestionnaire.getGestIA().get_list_model_download()