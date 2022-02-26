import base64
import datetime
import json
import logging
import sys
import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO
from networktables import NetworkTables
from pymongo import MongoClient

app = Flask(__name__)
socketio = SocketIO(app)
db = MongoClient("mongodb://localhost:27017")["feather"]

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    logging.error("No NetworkTables server specified")
    exit(0)
nt_server = sys.argv[1]

logging.info("Connecting to " + nt_server)
NetworkTables.initialize(server=nt_server)


def nt_change_callback(table, key, value, isNew):
    # print(f"nt change table: {table} key {key} value {value} new {isNew}")
    if key == "shotTaken":
        print("Shot taken!")
        # TODO: Add document


fms = NetworkTables.getTable("FMSInfo")
feather = NetworkTables.getTable("SmartDashboard/feather")
feather.addEntryListener(nt_change_callback)

time.sleep(0.5)  # Wait for NetworkTables
if not NetworkTables.isConnected():
    logging.error("Unable to connect to NetworkTables server " + nt_server)
    exit(1)


@socketio.on("message")
def handle_message(data):
    logging.info(data)


@socketio.on("ping")
def pong():
    socketio.emit("matchState", feather.getString("matchState", "disabled").title())
    socketio.emit("matchTimer", str(datetime.timedelta(seconds=round(feather.getNumber("matchTimer", 0)))))
    socketio.emit("matchNumber", fms.getString("MatchNumber", 0))

    alliance_string = "Red" if fms.getBoolean("IsRedAlliance", False) else "Blue"
    socketio.emit("alliance", f"{alliance_string} {round(fms.getNumber('StationNumber', 0))}")


@app.route("/")
def route_index():
    return render_template("index.html")


@app.route("/app")
def route_app():
    return render_template("app.html")


@app.route("/scanner")
def route_scanner():
    return render_template("scanner.html")


@app.route("/submit")
def route_submit():
    qr_data = json.loads(base64.b64decode(request.args.get("qr")).decode())
    print(qr_data)
    return render_template("import.html", match_number=qr_data["matchNumber"], shots=len(qr_data["shots"]))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
