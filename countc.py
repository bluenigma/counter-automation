from app import create_app, db
from app.models import Counter, Unit, Client, User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Counter': Counter, 'Unit': Unit, 'Client': Client,
            'User': User}
