from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.zip_import_service import ZipImportService
import os

imports_bp = Blueprint('imports', __name__)

@imports_bp.route('/', methods=['GET'])
def index():
    """Page d'importation principale."""
    return render_template('imports/index.html')

@imports_bp.route('/upload-zip', methods=['POST'])
def upload_zip():
    """Traite l'importation du fichier ZIP."""
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné', 'danger')
        return redirect(url_for('imports.index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Aucun fichier sélectionné', 'danger')
        return redirect(url_for('imports.index'))
    
    # Traitement du fichier ZIP
    resultats = ZipImportService.traiter_import_zip(file)
    
    if not resultats['success']:
        flash(resultats['message'], 'danger')
        return redirect(url_for('imports.index'))
    
    # Traitement réussi
    if resultats['adresses']['importé']:
        flash(resultats['adresses']['message'], 'success')
    else:
        flash(f"Adresses: {resultats['adresses']['message']}", 'warning')
    
    if resultats['organismes']['importé']:
        flash(resultats['organismes']['message'], 'success')
    else:
        flash(f"Organismes: {resultats['organismes']['message']}", 'warning')
    
    return redirect(url_for('imports.index'))