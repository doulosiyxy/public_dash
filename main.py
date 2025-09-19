import api_client
import functions as fc
from flask import Flask, request
from flask_session import Session
from routes import routes_helpers as rs
from routes.dash_routes import dash_bp
from routes.history_routes import hist_bp
import os

app = Flask(__name__, static_url_path="/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400

#session config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem" # Store sessions in the filesystem
app.config["SESSION_FILE_DIR"] = os.path.join(app.root_path, 'flask_session')
Session(app)
app.secret_key = fc.getSessionSecret()

#routes_bp
app.register_blueprint(dash_bp)
app.register_blueprint(hist_bp)

@app.after_request
def add_security_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/")
def index():
    response = app.make_response(rs.checkSessionRedirect())
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/login", methods=["POST", "GET"])
def login():
    return rs.authAndLogin(request.form)

@app.route("/logout")
def logout():
    return rs.logout()
         
if __name__ == "__main__":
    try:
        pass
        #api_client.scheduler.start()
    except Exception as e:
        fc.log(f"{fc.dt.datetime.today()}: {e}")
    app.run(debug=True, use_reloader = False) 