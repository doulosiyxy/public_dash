from flask import Blueprint, request
from routes import routes_helpers as rs
from controllers import dash_controller as dc

dash_bp = Blueprint('dash_bp', __name__)

@dash_bp.route("/dashboard")
def dashboard():
    return rs.dashboard()

@dash_bp.route('/dashboard/getNext', methods=["GET"])
def getNext():
    return dc.getNextGame()

@dash_bp.route('/dashboard/getPrev', methods=["GET"])
def getPrev():
    return dc.getPrevGame()

@dash_bp.route('/dashboard/swap', methods=["GET"])
def swap():
    return dc.swapTeams()

@dash_bp.route('/dashboard/refresh', methods=["GET"])
def refresh():
    return dc.refreshDashboard()

@dash_bp.route('/dashboard/submitWinner', methods=["POST"])
def submitWinner():
    return dc.submitWinner(request.form)

@dash_bp.route('/dashboard/undo', methods=['POST'])
def undo():
    return dc.undoSubmission(request.form)

