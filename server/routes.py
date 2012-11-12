from . import app
from flask import Response

@app.route('/show_db_name')
def test_config():
    return Response(app.config['MONGO_DBNAME'], mimetype='text/plain')
