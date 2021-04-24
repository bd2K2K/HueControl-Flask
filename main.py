from flask import Flask, render_template, redirect,url_for, request
from flask_bootstrap import Bootstrap
#.station_ip = "192.168.1.20"  # Your base station IP
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BROWN = "#eabf9f"
from phue import Bridge
B = Bridge('192.168.1.20')
B.connect()

app = Flask(__name__)
Bootstrap(app)
light_numbers=[]
lights_in_the_room=[]
rooms = B.groups
brightness=127
@app.route("/")
def home():
    return render_template("index.html" , rooms=rooms)

@app.route("/edit/<int:room_id>")
def edit(room_id):
    light_numbers=[]
    light_numbers = B.get_group(room_id,'lights')

    for l in light_numbers:
        light_number = int(l)
        light_name = B.get_light(light_number, 'name')
        light_status = B.get_light(light_number, 'on')
        lights =[light_number,light_name,light_status]
        lights_in_the_room.append(lights)
    return render_template("edit_room.html", lights_in_the_room=lights_in_the_room)

@app.route("/change/<int:room_id>", methods=['POST'])
def change(room_id):
   # light_numbers=[]
    light_numbers = B.get_group(room_id,'lights')

    for l in light_numbers:
        if B.get_light(int(l),'on'):
            B.set_light(int(l), 'on', False)
        else:
            B.set_light(int(l),'on',True)

    return redirect(url_for('home'))

@app.route("/bright/<int:room_id>", methods=['POST'])
def bright(room_id):
    if request.method=="POST":
        light_numbers = B.get_group(room_id,'lights')
        brightness= int(request.form["myBri"])
        print(brightness)
        for l in light_numbers:
            if B.get_light(int(l),'on'):

                B.set_light(int(l), 'bri',brightness )
    return redirect(url_for('home'))

@app.route("/color/<int:room_id>", methods=['POST'])
def color(room_id):
    if request.method=="POST":
        light_numbers = B.get_group(room_id,'lights')
        color= int(request.form["myCol"])
        print(color)
        for l in light_numbers:
            if B.get_light(int(l),'on'):

                B.set_light(int(l), 'hue',color )
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug = True)