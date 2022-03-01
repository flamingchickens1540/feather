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
    if key == "matchTime" and value is True:
        shot = {
            "matchTime": feather.getNumber("matchTime", -1),
            "matchId": feather.getString("matchId", "unknown-match"),
            "limelightDistance": feather.getNumber("limelightDistance", -1),
            "lidarDistance": feather.getNumber("lidarDistance", -1),
            "frontRPM": feather.getNumber("frontRPM", -1),
            "rearRPM": feather.getNumber("rearRPM", -1),
            "hoodUp": feather.getBoolean("hoodUp", False)
        }
        db["shots"].insert_one(shot)


fms = NetworkTables.getTable("FMSInfo")
feather = NetworkTables.getTable("SmartDashboard/feather")
feather.addEntryListener(nt_change_callback)

while not NetworkTables.isConnected():
    logging.error("Waiting for NetworkTables server " + nt_server)
    time.sleep(2)


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
