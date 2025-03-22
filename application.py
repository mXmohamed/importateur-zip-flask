from app import create_app, db
from app.models.adresse import Adresse
from app.models.organisme import Organisme

app = create_app()

# Contexte pour la commande flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Adresse': Adresse,
        'Organisme': Organisme
    }

if __name__ == '__main__':
    app.run(debug=True)