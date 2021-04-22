from flask import Flask
from flask_security import *

app = Flask ( __name__ )

@app.route ('/')
def hello_world ():
    return 'Hello , World, ciao mondo!'