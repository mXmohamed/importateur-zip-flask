// Attendre que le DOM soit complètement chargé
document.addEventListener('DOMContentLoaded', function() {
    // Amélioration de l'interface d'upload de fichier
    const fileInput = document.getElementById('file');
    const fileDropZone = document.querySelector('.file-drop-zone');
    
    // Si ces éléments existent dans la page
    if (fileInput && fileDropZone) {
        // Afficher le nom du fichier sélectionné
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0] ? this.files[0].name : 'Aucun fichier sélectionné';
            const fileLabel = document.querySelector('.file-name');
            
            if (fileLabel) {
                fileLabel.textContent = fileName;
            }
            
            // Validation du type de fichier
            if (this.files[0] && !this.files[0].name.endsWith('.zip')) {
                alert('Veuillez sélectionner un fichier ZIP.');
                this.value = '';
                if (fileLabel) {
                    fileLabel.textContent = 'Aucun fichier sélectionné';
                }
            }
        });
        
        // Support du drag & drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileDropZone.addEventListener(eventName, function(e) {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });
        
        // Effet visuel lors du drag
        ['dragenter', 'dragover'].forEach(eventName => {
            fileDropZone.addEventListener(eventName, function() {
                this.classList.add('highlight');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            fileDropZone.addEventListener(eventName, function() {
                this.classList.remove('highlight');
            }, false);
        });
        
        // Gestion du drop
        fileDropZone.addEventListener('drop', function(e) {
            fileInput.files = e.dataTransfer.files;
            
            // Déclencher l'événement change pour mettre à jour l'interface
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }, false);
    }
    
    // Animation des alertes
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(alert => {
        // Les alertes se ferment automatiquement après 5 secondes
        // sauf celles marquées comme persistantes
        if (!alert.classList.contains('alert-persistent')) {
            setTimeout(() => {
                alert.classList.add('fade-out');
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }, 5000);
        }
    });
    
    // Activer les tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Activer les popovers Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});