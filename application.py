from apscheduler.schedulers.background import BackgroundScheduler
import json
import pandas as pd
import datetime
import subprocess
from flask import Flask, render_template

from FunctionExportWealth import ExportCSVWealth




# Create the application instance
app = Flask(__name__)

scheduler = BackgroundScheduler(daemon=True)

dfComptes = pd.read_excel('Param/Description_Comptes.xlsx')


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """

    return render_template('home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    
    scheduler.add_job(id = 'Scheduled Task', func=ExportCSVWealth, args=[dfComptes], trigger='cron', hour='4')
    scheduler.start()
    
    app.run(host='0.0.0.0', port=5094, debug=True)