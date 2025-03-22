from app import db

class Adresse(db.Model):
    """Modèle représentant une adresse dans la base de données."""
    
    __tablename__ = 't_adresse'
    
    id_adresse = db.Column(db.Integer, primary_key=True)
    type_voie = db.Column(db.String(50))
    libelle_voie = db.Column(db.String(100))
    complement = db.Column(db.String(100))
    code_postal = db.Column(db.String(10))
    ville = db.Column(db.String(100))
    pays = db.Column(db.String(50), default='FRANCE')
    
    # Relation avec les organismes
    organismes = db.relationship('Organisme', backref='adresse', lazy=True)
    
    def __repr__(self):
        """Représentation en chaîne de caractères de l'objet."""
        return f"<Adresse {self.id_adresse}: {self.type_voie} {self.libelle_voie}, {self.code_postal} {self.ville}>"