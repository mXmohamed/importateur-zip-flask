import os
import zipfile
import pandas as pd
import logging
from io import BytesIO
from werkzeug.utils import secure_filename
from app.models.adresse import Adresse
from app.models.organisme import Organisme
from app import db

logger = logging.getLogger(__name__)

class ZipImportService:
    """Service pour importer et traiter des fichiers ZIP contenant des CSV."""
    
    # Noms des fichiers attendus dans le ZIP
    FICHIER_ADRESSES = "t_adresse.csv"
    FICHIER_ORGANISMES = "t_organisme.csv"
    
    @staticmethod
    def traiter_import_zip(file_storage):
        """
        Traite un fichier ZIP uploadé contenant des CSV.
        
        Args:
            file_storage: Objet FileStorage de Flask
            
        Returns:
            dict: Résultats de l'importation
        """
        if not file_storage:
            return {"success": False, "message": "Aucun fichier n'a été fourni"}
            
        filename = secure_filename(file_storage.filename)
        if not filename.endswith('.zip'):
            return {"success": False, "message": "Le fichier doit être au format ZIP"}
        
        # Lecture du fichier en mémoire
        file_content = file_storage.read()
        
        try:
            with zipfile.ZipFile(BytesIO(file_content)) as zip_ref:
                # Vérifier le contenu du ZIP
                file_list = zip_ref.namelist()
                logger.info(f"Fichiers trouvés dans le ZIP: {file_list}")
                
                resultats = {
                    "success": True,
                    "adresses": {"importé": False, "message": ""},
                    "organismes": {"importé": False, "message": ""}
                }
                
                # Traiter les adresses
                if ZipImportService.FICHIER_ADRESSES in file_list:
                    with zip_ref.open(ZipImportService.FICHIER_ADRESSES) as adresse_file:
                        adresse_result = ZipImportService._importer_adresses(adresse_file)
                        resultats["adresses"] = adresse_result
                else:
                    resultats["adresses"]["message"] = f"Fichier {ZipImportService.FICHIER_ADRESSES} non trouvé dans le ZIP"
                
                # Traiter les organismes
                if ZipImportService.FICHIER_ORGANISMES in file_list:
                    with zip_ref.open(ZipImportService.FICHIER_ORGANISMES) as organisme_file:
                        organisme_result = ZipImportService._importer_organismes(organisme_file)
                        resultats["organismes"] = organisme_result
                else:
                    resultats["organismes"]["message"] = f"Fichier {ZipImportService.FICHIER_ORGANISMES} non trouvé dans le ZIP"
                
                return resultats
                
        except zipfile.BadZipFile:
            return {"success": False, "message": "Le fichier n'est pas un ZIP valide"}
        except Exception as e:
            logger.error(f"Erreur lors de l'importation du ZIP: {str(e)}")
            return {"success": False, "message": f"Erreur lors de l'importation: {str(e)}"}
    
    @staticmethod
    def _importer_adresses(csv_file):
        """
        Importe les adresses depuis un fichier CSV.
        
        Args:
            csv_file: Fichier CSV ouvert
            
        Returns:
            dict: Résultat de l'importation
        """
        try:
            df = pd.read_csv(csv_file, delimiter=';', encoding='utf-8')
            
            count = 0
            for _, row in df.iterrows():
                adresse = Adresse(
                    id_adresse=row.get('ID_ADRESSE'),
                    type_voie=row.get('TYPE_VOIE'),
                    libelle_voie=row.get('LIBELLE_VOIE'),
                    complement=row.get('COMPLEMENT'),
                    code_postal=row.get('CODE_POSTAL'),
                    ville=row.get('VILLE'),
                    pays=row.get('PAYS')
                )
                db.session.add(adresse)
                count += 1
            
            db.session.commit()
            return {"importé": True, "message": f"{count} adresses importées avec succès"}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erreur lors de l'importation des adresses: {str(e)}")
            return {"importé": False, "message": f"Erreur: {str(e)}"}
    
    @staticmethod
    def _importer_organismes(csv_file):
        """
        Importe les organismes depuis un fichier CSV.
        
        Args:
            csv_file: Fichier CSV ouvert
            
        Returns:
            dict: Résultat de l'importation
        """
        try:
            df = pd.read_csv(csv_file, delimiter=';', encoding='utf-8')
            
            count = 0
            for _, row in df.iterrows():
                organisme = Organisme(
                    id_organisme=row.get('ID_ORGANISME'),
                    type_organisme=row.get('TYPE_ORGANISME'),
                    raison_sociale=row.get('RAISON_SOCIALE'),
                    siret=row.get('SIRET'),
                    id_adresse=row.get('ID_ADRESSE')
                )
                db.session.add(organisme)
                count += 1
            
            db.session.commit()
            return {"importé": True, "message": f"{count} organismes importés avec succès"}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erreur lors de l'importation des organismes: {str(e)}")
            return {"importé": False, "message": f"Erreur: {str(e)}"}
