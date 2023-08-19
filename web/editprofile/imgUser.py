import os
import time

def imgUser(id):

    imagePath = f"static/imgUsers/img{str(id)}.png"

    return (
        "/static/imgUsers/Defult.png"
        if os.path.exists(imagePath) == False
        else f"/{imagePath}?date=" + str(time.time()).split(".")[0]
    )