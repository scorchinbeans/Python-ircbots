from bottle import route, run

# This is the ui for bitvoucherbot
# to place the qr code on the dollars.
# As yet it's unfinished.

ux = """<html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Brython Image Coordinate Box</title>

    <script src="https://cdn.jsdelivr.net/npm/brython@3.12.5/brython.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/brython@3.12.5/brython_stdlib.js"></script>

    <style>
        #image-container {
            position: relative;
            display: inline-block;
            border: 1px solid #333;
            overflow: hidden;
        }

        #photo {
            display: block;
            max-width: 800px;
            height: auto;
        }

        #mouse-box {
            position: absolute;
            width: 100px;
            height: 70px;
            border: 2px solid red;
            background-color: rgba(255, 0, 0, 0.2);
            box-sizing: border-box;
            pointer-events: none;
            display: none;
        }

        #coordinates {
            margin-top: 12px;
            font-family: monospace;
            font-size: 16px;
        }
    </style>
</head>

<body onload="brython()">

    <div id="filesel">
    <form id="imgform">
    <input type="file" id="imgfile">
    </form>

    </div><div id="imgcont" hidden>
    <img id="photo" alt="Displayed image">
    <div id="mouse-box"></div>
    </div>

    <div id="coordinates">
    Click inside the image to   <br>
    record the box coordinates. <br>
    </div><script type="text/python">

import json
from browser import document, ajax
document["filesel"].bind("change", imgsel)
def imgsel(event):
    if not event.target.files.length:
        return

    global imgfile
    imgfile = document["imgfile"].value
    document["photo"].attrs["src"] = imgfile
    document["imgcont"].hidden = False
    document["filesel"].hidden = True

image = document["photo"]
mouse_box = document["mouse-box"]
coordinates = document["coordinates"]

def get_ajax(uri):
    def request_complete(request):
        if request.status == 200:
            data = json.loads(request.text)
            return data
        else:
            ret = f"Error: {request.status}"
            return ret

    request = ajax.ajax()
    request.bind("complete", request_complete)
    request.open("GET", uri, True)
    request.send()

def get_box_position(event):
    # Return the box's upper-left position relative to the image.
    image_rect = image.getBoundingClientRect()

    x = int(event.clientX - image_rect.left)
    y = int(event.clientY - image_rect.top)

    box_width = mouse_box.offsetWidth
    box_height = mouse_box.offsetHeight

    # Prevent the box from extending beyond the image
    max_x = image.width - box_width
    max_y = image.height - box_height

    x = max(0, min(x, max_x))
    y = max(0, min(y, max_y))

    return x, y


def move_box(event):
    x, y = get_box_position(event)

    mouse_box.style.left = f"{x}px"
    mouse_box.style.top = f"{y}px"
    mouse_box.style.display = "block"


def click_image(event):
    x, y = get_box_position(event)

    # Keep the box at the clicked position
    mouse_box.style.left = f"{x}px"
    mouse_box.style.top = f"{y}px"
    mouse_box.style.display = "block"

    # Display the upper-left corner coordinates
    coordinates.text = (
        f"Clicked box upper-left corner: X: {x}, Y: {y}"
    )

    req = f"/imget/?im={imgfile}&x={x}&"
    req += f"y={y}&z=mouse_box.offsetWidth"
    get_ajax(req)

def leave_image(event):
    mouse_box.style.display = "none"


image.bind("mousemove", move_box)
image.bind("click", click_image)
image.bind("mouseleave", leave_image)
    </script>

</body>
</html>"""

@route('/')
def main():
    return ux

@route("/imget/")
def imget():
    img = request.query.get("im")
    xc = request.query.get("x")
    yc = request.query.get("y")
    zc = request.query.get("z")
    ext = img.split(".")[-1]
    pre = img.split(".")[:-1]
    pre = '.'.join(pre)
    cmd = f"mv {img} {pre}-{xc}"
    cmd += f"-{yc}-{zc}.{ext}"
    system(cmd)

run(host="localhost", port=8080)
