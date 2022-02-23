import logging
import sys

from flask import Flask, render_template
from networktables import NetworkTables

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    logging.error("No NetworkTables server specified")
    exit(0)
nt_server = sys.argv[1]

logging.info("Connecting to " + nt_server)
NetworkTables.initialize(server=nt_server)


def nt_change_callback(table, key, value, isNew):
    print(f"nt change table: {table} key {key} value {value} new {isNew}")


def nt_connection_callback(connected, info):
    print(info, "; Connected=%s" % connected)


NetworkTables.addConnectionListener(nt_connection_callback, immediateNotify=True)

sd = NetworkTables.getTable("SmartDashboard")
sd.addEntryListener(nt_change_callback)


@app.route("/")
def route_index():
    return render_template("index.html",
                           match_state="Waiting for robot connection",
                           nt_connected=NetworkTables.isConnected(),
                           match=0
                           )


@app.route("/app")
def route_app():
    return render_template("app.html")


if __name__ == "__main__":
    app.run()
