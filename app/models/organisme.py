from app import db

class Organisme(db.Model):
    """Modèle représentant un organisme dans la base de données."""
    
    __tablename__ = 't_organisme'
    
    id_organisme = db.Column(db.Integer, primary_key=True)
    type_organisme = db.Column(db.String(50))
    raison_sociale = db.Column(db.String(150))
    siret = db.Column(db.String(14))
    id_adresse = db.Column(db.Integer, db.ForeignKey('t_adresse.id_adresse'))
    
    def __repr__(self):
        """Représentation en chaîne de caractères de l'objet."""
        return f"<Organisme {self.id_organisme}: {self.raison_sociale}>"