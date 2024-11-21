from flask import Flask  # using Flask to run a web server
from djitellopy import Tello

drone = None

# 1. connect to the drone
drone = Tello()
drone.connect()
# drone.streamon()
# ^^ uncomment if you want to start the video stream (but some code is needed to display it on web page)


# 2. create a web server
# if you want this website to be served on a public domain via tunnel
# , install ngrok and run this in command line:
#    ngrok http --url=copter.ngrok.io 80
#
# (replace "copter.ngrok.io" with the domain name for your website)

# -- create a web server with three pages: '/', '/takeoff' and '/land'
app = Flask(__name__)

PAGE_BUTTONS = """
<br><a href="/">Home</a>
<br><a href="/takeoff">Take Off</a>
<br><a href="/land">Land</a>
"""


@app.route('/')
def home_page():
    return "Home page" + PAGE_BUTTONS


@app.route('/takeoff')
def takeoff_page():
    if drone is not None:
        drone.takeoff()
    return "Took off" + PAGE_BUTTONS


@app.route('/land')
def land_page():
    if drone is not None:
        drone.land()
    return "Landed" + PAGE_BUTTONS


# -- now start that web server
app.run(host="0.0.0.0", port=80, debug=False)
