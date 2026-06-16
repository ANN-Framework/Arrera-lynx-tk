from librairy.arrera_tk import *
from tkinter.messagebox import *
from librairy.travailJSON import *
from gestionnaire.gestion import gestionnaire
import threading as th

class arrera_lynx(aFrame):
    def __init__(self,master:aTk,gest:gestionnaire,conf_file:str,fnc_end:Callable):
        self.__json_file = jsonWork(conf_file)
        self.__master = master

        self.__assistant_name = gest.getName()
        self.__gestUser = gest.getUserConf()
        self.__arrVoice = gest.getArrVoice()
        self.__gestionnaire = gest

        self.__fnc_end = fnc_end

        super().__init__(master,width=800,height=500)

        # Var
        self.__nb_soft_add = 0
        self.__nb_web_shortcut_add = 0
        self.__varOutTriger = 0
        self.__outTexteMicro = ""
        self.__thTrigerWord = th.Thread()
        self.__thDownloadIA = th.Thread()
        self.__state_github = self.__json_file.getContentJsonFlag("github_integration")
        self.__state_lynx = False

        # Frame
        self.__welcome = self.__welcome_frame()
        self.__user = self.__user_frame()
        self.__mobility = self.__mobility_frame()
        self.__environement = self.__environment_frame()
        self.__search = self.__search_frame()
        self.__system = self.__system_frame()
        self.__work = self.__work_frame()
        if self.__state_github == "1":
            self.__token = self.__token_frame()
        self.__ia = self.__ia_frame()
        self.__end = self.__end_frame()

        self.__work_folder_setted = False
        self.__download_folder_setted = False

    def active(self):
        self.__master.configure(width=800,height=500,resizable=False)
        self.placeCenter()
        self.__welcome.placeCenter()

    def get_geometry(self):
        return "800x500+5+30"

    # Declaration de la tout les pages
    def __welcome_frame(self):
        m = aFrame(self,width=775,height=475)

        icon = aImage(250,250,self.__json_file.getContentJsonFlag("icon_unix"))
        licon = aLabel(m,text="",image=icon)

        lText = aLabel(m,text=self.__json_file.getContentJsonFlag("text_presentation"),police_size=25,
                       wraplength=400,justify="left")

        btn = aButton(m,text=f"Configurer {self.__assistant_name}",size=20,command=self.__after_welcome)

        licon.placeTopLeft()
        lText.placeTopRight()
        btn.placeBottomRight()

        return m

    def __user_frame(self):

        listGenre = self.__json_file.getFlagListJson("list_genre")

        m = aFrame(self,width=775,height=475)
        info = aFrame(m,width=350,height=200,fg_color=m.cget("fg_color"))
        lTitle = aLabel(m,text="Information de l'utilisateur",police_size=25)
        lDesc = aLabel(m,police_size=20,
                       text="Pour apprendre à vous connaître, l'assistant a besoin de savoir votre nom, prénom et le pronom que vous voulez qu'il utilise",
                       wraplength=250,justify="left")

        self.__eFirstName = aEntryLengend(info,text="Prénom",police_size=15)
        self.__eLastName = aEntryLengend(info,text="Nom",police_size=15)
        self.__mGenre = aOptionMenuLengend(info,text="Genre",values=listGenre,police_size=15)

        btn = aButton(m,text="Continuer",size=20,command=self.__after_user)

        lTitle.placeTopCenter()
        info.placeRightCenter()
        lDesc.placeCenterLeft()
        self.__eFirstName.placeTopLeft()
        self.__eLastName.placeCenterLeft()
        self.__mGenre.placeBottomLeft()
        btn.placeBottomRight()

        return m

    def __mobility_frame(self):
        m = aFrame(self,width=775,height=475)

        lTitle = aLabel(m,text="Paramètres de mobilité",police_size=25)
        btn = aButton(m,text="Continuer",size=20,command=self.__after_mobility)

        fMeteo = aFrame(m,width=365 ,height=300,fg_color=m.cget("fg_color"))
        ltMeteo = aLabel(fMeteo,text="Météo",police_size=20)
        self.__eMDomicile = aEntryLengend(fMeteo,text="Ville de domicile",
                                          police_size=15)
        self.__eMWork = aEntryLengend(fMeteo, text="Ville de travail",
                                      police_size=15)
        btnATown = aButton(fMeteo, text="Ajouter une ville", size=20,
                           command=self.__action_view_add_town)

        fGPS = aFrame(m,width=365,height=300,fg_color=m.cget("fg_color"))
        ltGPS = aLabel(fGPS, text="GPS", police_size=20)
        self.__eGDomicile = aEntryLengend(fGPS, text="Adresse de domicile",
                                          police_size=15,width=175)
        self.__eGWork = aEntryLengend(fGPS, text="Adresse de travail",
                                      police_size=15)

        lTitle.placeTopCenter()

        fMeteo.placeRightCenter()
        fGPS.placeLeftCenter()
        btn.placeBottomRight()

        ltMeteo.placeTopCenter()
        self.__eMDomicile.placeCenterOnWidth(y=75)
        self.__eMWork.placeCenterOnWidth(y=125)
        btnATown.placeCenterOnWidth(y=175)

        ltGPS.placeTopCenter()
        self.__eGDomicile.placeCenterOnWidth(y=75)
        self.__eGWork.placeCenterOnWidth(y=125)

        return  m

    def __environment_frame(self):
        m = aFrame(self,width=775,height=475)

        lTitle = aLabel(m,text="Paramètres d'environnement numérique",police_size=25)

        fWeb = aFrame(m,width=350,height=200,fg_color=m.cget("fg_color"))
        lTWeb = aLabel(fWeb,police_size=20,text="Raccourci internet")
        self.__eWebName = aEntryLengend(fWeb,text="Nom",police_size=15)
        self.__eWebLink = aEntryLengend(fWeb,text="Lien",police_size=15)
        btnWeb = aButton(fWeb,text="Ajouter",size=20,command=self.__action_add_web_shortcut)

        fSoft = aFrame(m,width=350,height=200,fg_color=m.cget("fg_color"))
        lTSoft = aLabel(fSoft,police_size=20,text="Logiciel externe")
        self.__eSoftName = aEntryLengend(fSoft,text="Nom",police_size=15)
        btnSoft = aButton(fSoft,text="Ajouter",size=20,command=self.__action_add_soft)

        btn = aButton(m,text="Continuer",size=20,command=self.__after_environment)

        fWeb.placeLeftCenter()
        fSoft.placeRightCenter()

        lTWeb.placeTopCenter()
        self.__eWebName.placeCenterOnWidth(y=75)
        self.__eWebLink.placeCenterOnWidth(y=125)
        btnWeb.placeBottomCenter()

        lTSoft.placeTopCenter()
        self.__eSoftName.placeCenterOnWidth(y=75)
        btnSoft.placeCenterOnWidth(y=125)

        lTitle.placeTopCenter()

        btn.placeBottomRight()
        return m

    def __search_frame(self):
        m = aFrame(self,width=775,height=475)

        lTitle = aLabel(m,text="Paramètres de recherche",police_size=25)

        btn = aButton(m,text="Continuer",size=20,command=self.__after_search)

        lDesc = aLabel(m,text=f"L'assistant {self.__assistant_name} vous permet de faire des recherches sur internet. Choisissez le moteur de recherche par défaut que vous voulez utiliser"
                       ,wraplength=300,justify="left",police_size=20)

        listEngine = self.__json_file.getFlagListJson("list_engine_search")
        fSearch = aFrame(m,width=258,height=200,fg_color=m.cget("fg_color"))
        lTSearch = aLabel(fSearch,police_size=20,text="Moteur de recherche\npar défaut")
        self.__mSearchEngine = aOptionMenu(fSearch,value=listEngine)

        lTitle.placeTopCenter()
        lDesc.placeLeftCenter()
        fSearch.placeRightCenter()

        lTSearch.placeTopCenter()
        self.__mSearchEngine.placeCenterOnWidth(y=75)

        btn.placeBottomRight()
        return m

    def __system_frame(self):
        m = aFrame(self,width=775,height=475)

        lTitle = aLabel(m,text="Paramètres généraux de l'assistant",police_size=25)

        fSystem = aFrame(m,width=350,height=200,fg_color=m.cget("fg_color"))
        lTSysteme = aLabel(fSystem,police_size=20,text="Paramétrage de l'assistant")
        self.__enableHist = aSwicht(fSystem,text="Activer l'historique",default_value=False,
                                     command=self.__action_btn_enable_hist)

        if self.__json_file.getContentJsonFlag("micro_use") == "1":
            fMicro = aFrame(m,width=350,height=200,fg_color=m.cget("fg_color"))
            lTMicro = aLabel(fMicro,police_size=20,text="Microphone")
            self.__enableSound = aSwicht(fMicro,text="Sons au démarrage de l'écoute",default_value=False,
                                         command=self.__action_btn_enable_micro_sound)
            btnTriger = aButton(fMicro, text="Ajouter un mot déclencheur", size=20,
                                command=self.__action_launch_record_triger_word)

            fMicro.placeLeftCenter()
            fSystem.placeRightCenter()
            lTMicro.placeTopCenter()
            self.__enableSound.placeCenterOnWidth(y=75)
            btnTriger.placeCenterOnWidth(y=125)
        else :
            fSystem.placeCenter()

        btn = aButton(m,text="Continuer",size=20,command=self.__after_system)

        lTitle.placeTopCenter()

        lTSysteme.placeTopCenter()
        self.__enableHist.placeCenter()

        btn.placeBottomRight()

        return m

    def __work_frame(self):
        m = aFrame(self,width=775,height=475)
        lTitle = aLabel(m,text="Paramétrage des dossiers",police_size=25)

        fWork = aFrame(m,width=350,height=200,fg_color=m.cget("fg_color"))
        lTWork = aLabel(fWork,police_size=20,text="Dossier de travail")
        bFWork = aButton(fWork,text="Enregistrer les dossiers\nde travail",
                         size=20,command=self.__action_add_work_folder)

        fDownload = aFrame(m,width=350,height=200,fg_color=m.cget("fg_color"))
        lTDownload = aLabel(fDownload,police_size=20,text="Dossier de téléchargement")
        bFDownload = aButton(fDownload, text="Enregistrer le dossier\nde téléchargement",
                             size=20, command=self.__action_add_download_folder)

        btn = aButton(m,text="Continuer",size=20,command=self.__after_work)

        lTitle.placeTopCenter()

        fWork.placeLeftCenter()
        fDownload.placeRightCenter()

        lTWork.placeTopCenter()
        bFWork.placeCenter()

        lTDownload.placeTopCenter()
        bFDownload.placeCenter()

        btn.placeBottomRight()

        return m

    def __token_frame(self):
        m = aFrame(self,width=775,height=475)

        lTitle = aLabel(m,police_size=25,text="Token github")

        lDesc = aLabel(m,text="Pour utiliser toutes les fonctionnalités de codehelp vous devez enregistrer votre token github. (Stocké entièrement en local)",
                       wraplength=300,justify="left",police_size=20)

        fToken = aFrame(m,width=300,height=300,fg_color=m.cget("fg_color"))
        lToken = aLabel(fToken,police_size=20,text="Enregistrement du token")
        self.__eToken = aEntryLengend(fToken,text="Token",police_size=15)
        btnGenerateToken = aButton(fToken,text="Générer un token",size=20,
                                   command=lambda : wb.open("https://github.com/settings/tokens/new"))

        btn = aButton(m,text="Continuer",size=20,
                      command=self.__after_token)

        lTitle.placeTopCenter()

        lDesc.placeLeftCenter()

        fToken.placeRightCenter()

        lToken.placeTopCenter()
        self.__eToken.placeCenter()
        btnGenerateToken.placeBottomCenter()

        btn.placeBottomRight()

        return m

    def __ia_frame(self):
        m = aFrame(self,width=775,height=475)
        lTitle = aLabel(m,police_size=25,text="Paramétrage du mode IA")
        btn = aButton(m,text="Continuer",size=20,command=self.__after_ia)

        fChooseModel = aFrame(m,width=350,height=237,fg_color=m.cget("fg_color"))
        lTModel = aLabel(fChooseModel,police_size=20,text="Choix du modèle d'IA")
        bDModel = aButton(fChooseModel,text="Choisir un modèle\nà télécharger",size=20,
                          command=self.__action_view_download_model)

        fDesc = aFrame(m,width=350,height=200,fg_color=m.cget("fg_color"))
        lDesc = aLabel(fDesc,text=f"L'assistant {self.__assistant_name} intègre des modèles d'IA pour améliorer ses réponses. Vous pouvez choisir le modèle que vous voulez utiliser et adapté à votre ordinateur",
                       wraplength=325,justify="left",police_size=20)
        self.__bEnableIA = aSwicht(fDesc,text="Activer le mode IA",
                                   default_value=False,command=self.__action_enable_ia_mode)

        if len(self.__gestUser.get_model_downloaded()) != 0:
            bDownloadedModel = aButton(fChooseModel,text="Modèle téléchargé",size=20,
                                       command = self.__action_view_choose_model_downloaded)

            bDModel.placeCenterOnWidth(y=75)
            bDownloadedModel.placeCenterOnWidth(y=155)
        else :
            bDModel.placeCenter()
        lTModel.placeTopCenter()

        lTitle.placeTopCenter()
        fChooseModel.placeRightCenter()
        btn.placeBottomRight()

        fDesc.placeLeftCenter()
        lDesc.placeTopLeft()
        self.__bEnableIA.placeBottomLeft()

        return m

    def __end_frame(self):
        m = aFrame(self,width=775,height=475)

        icon = aImage(250,250,self.__json_file.getContentJsonFlag("icon_unix"))
        licon = aLabel(m,text="",image=icon)

        lEnd = aLabel(m,text=self.__json_file.getContentJsonFlag("text_end"),
                      police_size=20,wraplength=300,justify="left")

        btn = aButton(m,text=f"Utiliser {self.__assistant_name}",size=20,command=self.__after_end)

        licon.placeTopLeft()
        lEnd.placeRightCenter()
        btn.placeBottomRight()
        return m

    # Partie Fonctionnel

    def __after_welcome(self):
        self.__welcome.place_forget()
        self.__user.placeCenter()

    def __after_user(self):

        firtName = self.__eFirstName.getEntry().get()
        lastName = self.__eLastName.getEntry().get()
        genre = self.__mGenre.getOptionMenu().getValue()

        if firtName != "" and lastName != "" :
            if (self.__gestUser.setLastnameUser(lastName) and
                self.__gestUser.setFirstnameUser(firtName) and
                self.__gestUser.setGenre(genre)):
                self.__user.place_forget()
                self.__mobility.placeCenter()
            else :
                showerror("Configurateur","Une erreur s'est produite")
        else :
            showerror("Configurateur","Vous n'avez pas rempli tous les champs")


    def __after_mobility(self):

        mDomicile = self.__eMDomicile.getEntry().get()
        mWork = self.__eMWork.getEntry().get()

        gDomicile = self.__eGDomicile.getEntry().get()
        gWork = self.__eGWork.getEntry().get()

        if mDomicile == "" or mWork == "" or gDomicile == "" or gWork == "" :
            r = askyesno("Configurateur","Vous n'avez pas rempli tous les champs. Voulez-vous continuer ?")
            if not r:
                self.__mobility.placeCenter()
                return

        if mDomicile == "":
            okMDomicile = True
        else :
            okMDomicile = self.__gestUser.setLieuDomicile(mDomicile)

        if mWork == "":
            okMWork = True
        else :
            okMWork = self.__gestUser.setLieuTravail(mWork)

        if gDomicile == "":
            okGDomicile = True
        else :
            okGDomicile = self.__gestUser.setAdresseDomicile(gDomicile)

        if gWork == "":
            okGWork = True
        else :
            okGWork = self.__gestUser.setAdresseTravail(gWork)

        self.__mobility.place_forget()
        self.__environement.placeCenter()

        if not okMDomicile and not okMWork and not okGDomicile and not okGWork:
            showerror("Configurateur",
                      "Une erreur s'est produite sur l'enregistrement des paramètres de mobilité")

    def __after_environment(self):
        if self.__nb_soft_add  == 0 or self.__nb_web_shortcut_add == 0:
            if self.__nb_soft_add  == 0 and self.__nb_web_shortcut_add == 0:
                r = askyesno("Configurateur",
                         "Vous n'avez ajouté aucun logiciel externe et raccourci internet. Voulez-vous continuer ?")
                if not r:
                    self.__environement.placeCenter()
                    return
            elif self.__nb_soft_add  == 0 and self.__nb_web_shortcut_add != 0:
                r = askyesno("Configurateur",
                             "Vous n'avez ajouté aucun logiciel externe. Voulez-vous continuer ?")
                if not r:
                    self.__environement.placeCenter()
                    return
            elif self.__nb_soft_add  != 0 and self.__nb_web_shortcut_add == 0:
                r = askyesno("Configurateur",
                             "Vous n'avez ajouté aucun raccourci internet. Voulez-vous continuer ?")
                if not r:
                    self.__environement.placeCenter()
                    return

        self.__environement.place_forget()
        self.__search.placeCenter()

    def __after_search(self):
        if not self.__gestUser.setMoteurRecherche(self.__mSearchEngine.getValue()):
            showerror("Configurateur","Une erreur s'est produite")

        self.__search.place_forget()
        self.__system.placeCenter()

    def __after_system(self):
        r = askyesno("Configurateur",
                     "L'assistant est bien configuré comme vous voulez ?")

        if r:
            self.__system.place_forget()
            self.__work.placeCenter()
        else :
            self.__system.placeCenter()

    def __after_work(self):
        if not self.__work_folder_setted or not self.__download_folder_setted:
            if not self.__work_folder_setted and self.__download_folder_setted:
                r = askyesno("Configurateur",
                             "Vous n'avez pas enregistré le dossier de travail voulez-vous continuer ?")
                if not r:
                    self.__work.placeCenter()
                    return
            elif self.__work_folder_setted and not self.__download_folder_setted:
                r = askyesno("Configurateur",
                             "Vous n'avez pas enregistré le dossier de téléchargement voulez-vous continuer ?")
                if not r:
                    self.__work.placeCenter()
                    return
            elif not self.__work_folder_setted and not self.__download_folder_setted:
                r = askyesno("Configurateur",
                             "Vous n'avez pas enregistré le dossier de téléchargement et de travail voulez-vous continuer ?")
                if not r:
                    self.__work.placeCenter()
                    return

        self.__work.place_forget()
        if self.__state_github == "1":
            self.__token.placeCenter()
        else :
            self.__ia.placeCenter()

    def __after_token(self):
        token = self.__eToken.getEntry().get()

        if token == "":
            r = askyesno("Configurateur","Aucun token sera enregistré voulez-vous continuer?")
            if not r :
                self.__token.placeCenter()
                return

        if token != "":
            if not self.__gestUser.setTokenGithub(token):
                showerror("Configurateur","Une erreur s'est produite")


        self.__token.place_forget()
        self.__ia.placeCenter()

    def __after_ia(self):
        r = askyesno("Configurateur",
                     "Les paramètres liés à l'intelligence artificielle sont configurés comme vous voulez ?")

        if r:
            self.__ia.place_forget()
            self.__end.placeCenter()
            self.__state_lynx = True
        else :
            self.__ia.placeCenter()

    def __after_end(self):
        self.__gestionnaire.getLanguageObjet().setVarUser()
        self.__fnc_end()
        del self
    # Action

    # Mobility

    def __action_view_add_town(self):
        w = aTopLevel(title="Ajout de villes",width=300,height=150)

        lTitle = aLabel(w,text="Ajout d'une ville",police_size=20)
        nameVille = aEntryLengend(w,text="Ville",police_size=15)
        btn = aButton(w,text="Ajouter",size=20,
                      command= lambda : self.__action_add_orther_town(w,nameVille))

        lTitle.placeTopCenter()
        nameVille.placeCenter()
        btn.placeBottomCenter()

    def __action_add_orther_town(self,w:aTopLevel,entry:aEntryLengend):

        town = entry.getEntry().get()
        if town == "":
            showerror("Configurateur","Aucune ville sera enregistrée")
        else :
            if not self.__gestUser.addTown(town):
                showerror("Configurateur","Une erreur s'est produite")

        for widget in w.winfo_children():
            widget.destroy()
        w.destroy()

    # environment

    def __action_add_soft(self):
        name = self.__eSoftName.getEntry().get()

        self.__eSoftName.getEntry().delete(0,END)

        if name == "":
            showerror("Configurateur","Aucun logiciel sera enregistré")
        else :
            if not self.__gestUser.setSoft(name):
                showerror("Configurateur","Une erreur s'est produite")
            else :
                self.__nb_soft_add += 1

    def __action_add_web_shortcut(self):
        name = self.__eWebName.getEntry().get()
        link = self.__eWebLink.getEntry().get()

        self.__eWebName.getEntry().delete(0,END)
        self.__eWebLink.getEntry().delete(0,END)

        if name == "" or link == "":
            showerror("Configurateur","Vous ne pouvez pas ajouter un raccourci internet sans nom ou lien")
        else :
            if not self.__gestUser.setSite(name,link):
                showerror("Configurateur","Une erreur s'est produite")
            else :
                self.__nb_web_shortcut_add += 1

    # system

    def __action_btn_enable_micro_sound(self):
        r = askyesno("Configurateur","Voulez-vous activer les sons au démarrage de l'écoute ?")
        if r :
            self.__gestUser.setSoundMicro(True)
            self.__enableSound.setOn()
        else :
            self.__gestUser.setSoundMicro(False)
            self.__enableSound.setOff()

    def __action_btn_enable_hist(self):
        r = askyesno("Configurateur",f"Voulez-vous activer l'historique de l'assistant {self.__assistant_name} ?")
        if r :
            self.__gestUser.setHist(True)
            self.__enableHist.setOn()
        else :
            self.__gestUser.setHist(False)
            self.__enableHist.setOff()

    def __action_record_tiger_word(self):
        self.__varOutTriger = 0
        self.__outTexteMicro = ""
        self.__varOutTriger =  self.__arrVoice.listen()

        if self.__varOutTriger == 0 :
            self.__outTexteMicro = self.__arrVoice.getTextMicro()

    def __action_launch_record_triger_word(self):
        if len(self.__gestUser.getListWord()) < 3:
            self.__thTrigerWord = th.Thread(target=self.__action_record_tiger_word)
            self.__thTrigerWord.start()
            w = aTopLevel(title="Ajout d'un mot déclencheur",width=300,height=150)
            self.after(100,self.__update_action_record_word,w,True)

    def __action_add_triger_word(self,w:aTopLevel):
        if self.__outTexteMicro != "":
            if not self.__gestUser.addWord(self.__outTexteMicro):
                showerror("Configurateur","Une erreur s'est produite")
            else :
                showinfo("Configarateur","Le mot a été enregistré en tant que mot déclencheur")
        else :
            showerror("Configurateur","Aucun mot n'a été enregistré")

        w.destroy()

    # Work

    def __action_add_work_folder(self):
        if self.__gestUser.setWorkFolder():
            self.__work_folder_setted = True
            showinfo("Configurateur","Le dossier de travail a été enregistré")
        else :
            showerror("Configurateur","Une erreur s'est produite")

    def __action_add_download_folder(self):
        if self.__gestUser.setWorkFolder():
            self.__download_folder_setted = True
            showinfo("Configurateur","Le dossier de téléchargement a été enregistré")
        else :
            showerror("Configurateur","Une erreur s'est produite")


    # IA

    def __action_enable_ia_mode(self):
        r = askyesno("Configurateur","Voulez-vous activer le mode IA ?")
        if r :
            self.__gestUser.set_use_ia(True)
            self.__bEnableIA.setOn()
        else :
            self.__gestUser.set_use_ia(False)
            self.__bEnableIA.setOff()

    def __action_view_choose_model_downloaded(self):
        w = aTopLevel(title=f"{self.__assistant_name} : Choix du modèle d'IA",width=500,height=400)

        lTitle = aLabel(w,text="Modèle d'IA déjà téléchargé",police_size=20)

        listModel = self.__gestUser.get_model_downloaded()

        mChooseModelDownloaded = aOptionMenuLengend(w,text="Modèle",values=listModel)

        btnValider = aButton(w,text="Valider",size=20,
                             command=lambda : self.__action_choose_model_downloaded(w,mChooseModelDownloaded))
        btnCancel = aButton(w,text="Annuler",size=20,command=w.destroy)

        lTitle.placeTopCenter()
        mChooseModelDownloaded.placeCenter()
        btnValider.placeBottomLeft()
        btnCancel.placeBottomRight()

    def __action_choose_model_downloaded(self,w:aTopLevel,m:aOptionMenuLengend):
        name_model = m.getValue()
        if self.__gestUser.set_ia_model(name_model):
            w.destroy()
            showinfo("Configurateur","Le modèle a été enregistré")
        else :
            w.destroy()
            showerror("Configurateur","Une erreur s'est produite")

    def __action_view_download_model(self):
        w = aTopLevel(title=f"{self.__assistant_name} : Choix du modèle d'IA",width=500,height=400)

        lTitle = aLabel(w,text="Modèle d'IA à télécharger",police_size=20)
        fScroll = aScrollableFrame(w,width=400,height=250)
        btnCancel = aButton(w,text="Annuler",size=20,command=w.destroy)

        listModel = []
        modelAvailable = self.__gestUser.get_list_model_ia_available()
        modelDownloaded = self.__gestUser.get_model_downloaded()

        for i in modelAvailable:
            if i not in modelDownloaded:
                listModel.append(i)

        for i in listModel:
            dataModel = self.__gestUser.get_data_model_ia_available(i)

            fModel = aFrame(fScroll,width=380,height=200)
            lTitleModel = aLabel(fModel,text=f"{dataModel[0]}\n({i})",police_size=20,justify="left")
            lDescModel = aLabel(fModel,text=dataModel[2],police_size=15,
                                wraplength=250,justify="left")
            bDownload = aButton(fModel,text="Télécharger",size=15,
                                command=lambda model=i: self.__action_download_model(w,model))

            lTitleModel.placeTopLeft()
            lDescModel.placeCenterLeft()
            bDownload.placeBottomRight()

            fModel.pack(pady=10)

        lTitle.placeTopCenter()
        fScroll.placeCenter()
        btnCancel.placeBottomCenter()

    def __action_download_model(self,w:aTopLevel,model:str):
        self.__thDownloadIA = th.Thread(target=self.__gestUser.download_ia_model,args=(model,))
        self.__thDownloadIA.start()
        self.after(100,self.__update_action_download_model,w,True,model)

    # Update

    def __update_action_download_model(self,w:aTopLevel,state:bool,model:str):
        if self.__thDownloadIA.is_alive():
            if state:
                for widget in w.winfo_children():
                    widget.destroy()
                l = aLabel(w,text="Téléchargement en cours....",police_size=20)
                l.placeCenter()
            self.after(100,self.__update_action_download_model,w,False,model)
        else :
            del self.__thDownloadIA
            self.__thDownloadIA = th.Thread()
            for widget in w.winfo_children():
                widget.destroy()
            w.destroy()
            showinfo("Configurateur","Le modèle a été téléchargé et enregistré comme modèle par défaut")
            self.__gestUser.set_ia_model(model)

    def __update_action_record_word(self,w:aTopLevel,state:bool):

        if self.__thTrigerWord.is_alive():
            if state:
                for widget in w.winfo_children():
                    widget.destroy()
                l = aLabel(w,text="Enregistrement en cours....",police_size=20)
                l.placeCenter()

            self.after(100,self.__update_action_record_word,w,False)
        else :
            del self.__thTrigerWord
            self.__thTrigerWord = th.Thread()
            if self.__varOutTriger == 0:
                for widget in w.winfo_children():
                    widget.destroy()
                l = aLabel(w,text=f"Mot enregistré : {self.__outTexteMicro}",police_size=20)
                b = aButton(w,text="Sauvegarder",size=15,
                            command=lambda : self.__action_add_triger_word(w))
                l.placeTopCenter()
                b.placeBottomCenter()
            else :
                showerror("Configurateur","L'enregistrement s'est mal déroulé")
                w.destroy()

    # Return

    def return_state_lynx(self):
        return self.__state_lynx