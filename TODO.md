# TODO — Arrera Lynx (Migration ANN v4.0 & Modularisation Python)

Ce document détaille toutes les étapes et modifications techniques nécessaires pour faire évoluer **Arrera Lynx** (l'interface de premier démarrage des assistants Arrera) vers sa nouvelle version compatible avec **ANN v4.0** (`ann-core`), et le transformer en **module Python installable** (`pyproject.toml`).

---

## 🎯 Objectifs principaux

1. **Découplage complet et suppression du code dupliqué** : Retirer l'intégralité du code ANN v3 dupliqué dans le projet (`brain/`, `fnc/`, `neuron/`, etc.) pour s'appuyer exclusivement sur le moteur headless officiel `ann-core`.
2. **Modularisation Python** : Transformer le dépôt en un package Python propre et distribuable via `pip` (`pyproject.toml`), directement importable par n'importe quel assistant (`from arrera_lynx import arrera_lynx`).
3. **Compatibilité avec l'API ANN v4 (Headless Core)** :
   - Corriger les appels de configuration qui ne gèrent plus de fenêtres Tkinter dans le Core (`setWorkFolder`, `setVideoDownloadFolder`, `setSoft`).
   - Corriger le bug existant où `setWorkFolder` était appelé à la place de `setVideoDownloadFolder`.
   - Adapter la page Mobilité aux nouvelles méthodes d'adresses structurées (`set_home_adresse`, `set_work_adresse`).
   - Exploiter le nouveau catalogue de 9 modèles GGUF, la recommandation matérielle automatique et le moteur Piper TTS.
4. **Utilisation du package officiel `arrera-tk`** : S'appuyer sur le paquet pip officiel `arrera-tk` plutôt que sur des fichiers locaux obsolètes.

---

## 📋 Checklist des tâches

### 1. Nettoyage architectural (Suppression du code dupliqué de ANN v3)
- [ ] **Supprimer les dossiers clonés du moteur ANN v3** :
  - `brain/`
  - `fnc/`
  - `neuron/`
  - `objet/`
  - `instruction_ia/`
  - `keyword/`
  - `language/`
  - `gestionnaire/`
  - `config/`
  - `gui/` (ancienne interface Tkinter v3)
  - `librairy/` (en particulier l'ancien `arrera_tk.py`)
  - `__pycache__/`
- [ ] **Nettoyer les assets non utilisés** :
  - Conserver uniquement les icônes de premier démarrage (`asset/Ryley.png`, `asset/Ryley.ico`, `asset/logo.png`, `asset/icon.png`, `asset/baniere.png`) et les thèmes dans `asset/theme/`.
  - Supprimer les dossiers d'icônes spécifiques à ANN (`asset/meteo/`, `asset/calendar/`, `asset/horloge/`, `asset/tache/`, `asset/work/`, `asset/sound/`).

---

### 2. Packaging Python (`pyproject.toml` & structure de module)
- [ ] **Restructurer le code source en package Python** :
  - Renommer/déplacer `lynx_gui/` vers `arrera_lynx/` (ou structure standard `src/arrera_lynx/`).
  - Créer `arrera_lynx/__init__.py` pour exposer la classe principale :
    ```python
    from .arrera_lynx import arrera_lynx

    __all__ = ["arrera_lynx"]
    ```
- [ ] **Créer le fichier `pyproject.toml`** :
  ```toml
  [build-system]
  requires = ["setuptools>=61.0"]
  build-backend = "setuptools.build_meta"

  [project]
  name = "arrera-lynx"
  version = "3.0.0"
  description = "Assistant de premier démarrage pour les assistants Arrera (compatible ANN v4)"
  readme = "README.md"
  requires-python = ">=3.10"
  dependencies = [
      "ann-core @ git+https://github.com/ANN-Framework/Arrera-Neuron-Network-Core.git@version4.0",
      "arrera-tk>=3.0.0",
      "customtkinter",
      "pillow"
  ]

  [tool.setuptools.packages.find]
  where = ["."]
  include = ["arrera_lynx*"]

  [tool.setuptools.package-data]
  "*" = ["*.json", "*.png", "*.ico"]
  ```
- [ ] **Alléger `requirements.txt`** pour l'environnement de développement :
  ```txt
  # Dépendance Core (en dev local : pip install -e ../ArreraNeuronNetwork)
  ann-core @ git+https://github.com/ANN-Framework/Arrera-Neuron-Network-Core.git@version4.0
  arrera-tk>=3.0.0
  customtkinter
  pillow
  ```

---

### 3. Modifications du code source (`arrera_lynx.py`)

#### A. Importations externes
- [ ] Remplacer l'import local `from librairy.arrera_tk import *` par le module officiel :
  ```python
  from arrera_tk import *
  from tkinter import filedialog
  from tkinter.messagebox import showinfo, showerror, askyesno
  ```
- [ ] Importer les composants nécessaires depuis `ann-core` :
  ```python
  from librairy.travailJSON import jsonWork
  from gestionnaire.gestion import gestionnaire
  ```

#### B. Adaptation aux méthodes Headless de `gestUserSetting` & Correction de bugs
- [ ] **Correction du bug et adaptation de la Page Work** :
  - **Dossier de travail (`__action_add_work_folder`)** :
    ```python
    folder = filedialog.askdirectory(title="Choisir le dossier de travail Arrera Work")
    if folder:
      if self.__gestUser.setWorkFolder(folder):
        self.__work_folder_setted = True
        showinfo("Configurateur", "Le dossier de travail a été enregistré")
      else:
        showerror("Configurateur", "Une erreur s'est produite")
    ```
  - **Dossier de téléchargement (`__action_add_download_folder`)** :
    *(Attention : la version précédente appelait `setWorkFolder()` par erreur au lieu de `setVideoDownloadFolder()`)*
    ```python
    folder = filedialog.askdirectory(title="Choisir le dossier de téléchargement")
    if folder:
      if self.__gestUser.setVideoDownloadFolder(folder):
        self.__download_folder_setted = True
        showinfo("Configurateur", "Le dossier de téléchargement a été enregistré")
      else:
        showerror("Configurateur", "Une erreur s'est produite")
    ```
- [ ] **Page Environnement — Ajout de logiciels (`__add_soft`)** :
  - Dans ANN v4, `setSoft(name, path)` requiert impérativement le chemin vers le fichier exécutable.
  - Ajouter la sélection de fichier avec `filedialog.askopenfilename()` :
    ```python
    path = filedialog.askopenfilename(
      title=f"Sélectionner le programme pour {name}",
      filetypes=[("Exécutables / Applications", "*.*")]
    )
    if path:
      if not self.__gestUser.setSoft(name, path):
        showerror("Configurateur", f"Erreur lors de l'enregistrement de {name}")
    ```

#### C. Page Mobilité (Nouvelle API d'adresse ANN v4)
- [ ] Mettre à jour la saisie des adresses pour renseigner le triplet `(adresse, code postal, ville)` :
  - Domicile : `self.__gestUser.set_home_adresse(adresse, code_postal, ville)`
  - Travail : `self.__gestUser.set_work_adresse(adresse, code_postal, ville)`
  - Mettre à jour les champs texte dans `__mobility_frame()` pour inclure les champs de code postal si nécessaire.

#### D. Page IA (Catalogue 9 modèles & Recommandation matérielle)
- [ ] **Intégration du catalogue complet (9 modèles)** :
  - Afficher les modèles disponibles via `self.__gestUser.get_list_model_ia_available()` (qui retourne désormais les 9 modèles officiels Gemma 4, Mistral et Qwen 2.5).
- [ ] **Mise en avant du modèle recommandé** :
  - Récupérer le modèle optimal pour la machine de l'utilisateur avec `self.__gestUser.get_recommended_ia_model()`.
  - Mettre en évidence ou pré-sélectionner ce modèle sur l'interface avec un badge "Recommandé pour votre PC".
- [ ] **Activation / Désactivation du mode IA** :
  - Remplacer l'appel déprécié `self.__gestUser.set_use_ia(True)` par la sélection active du modèle :
    - L'activation se fait via `self.__gestUser.set_ia_model(model)`.
    - Si l'utilisateur refuse le mode IA, s'assurer que `set_ia_model("")` est configuré.

#### E. Synthèse vocale Piper TTS (Choix de la voix au premier démarrage)
- [ ] Proposer sur la page Système ou une nouvelle étape le choix de la voix de l'assistant :
  - Liste des voix disponibles : `self.__gestUser.get_list_voice_available()`
  - Définition de la voix : `self.__gestUser.set_voice(selected_voice)`

---

### 4. Mise à jour des scripts de test et de configuration

- [ ] **Mettre à jour `src/create_conf.py` et `main.py`** :
  - Nettoyer l'instanciation de `confNeuron` en retirant les champs obsolètes (`assistant_color`, `assistant_texte_color`).
  - Importer `confNeuron` et `gestionnaire` depuis `config.confNeuron` et `gestionnaire.gestion` fournis par `ann-core`.
  - Importer `arrera_lynx` depuis le nouveau module local ou installé.

---

### 5. Documentation
- [ ] Actualiser `README.md` et `README_en.md` :
  - Expliquer l'installation comme package Python (`pip install arrera-lynx`).
  - Présenter l'intégration simplifiée avec `ann-core` v4.
