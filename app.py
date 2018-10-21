from my_calendar import app
from flask import Flask, render_template
from datetime import timedelta
app1 =Flask(__name__)


if __name__ == '__main__':

    app.run(debug=True)
