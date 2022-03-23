from app.setup import app
from app.models import db_status, create_db, init

if __name__ == '__main__':
    if not db_status():
        create_db()
        init()
    
    app.run(host='0.0.0.0')