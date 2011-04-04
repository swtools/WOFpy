
from frontends.wofpy_flask import app as flask_app

if __name__ == '__main__':
	
	flask_app.run(host='0.0.0.0', port=8080, threaded=True)