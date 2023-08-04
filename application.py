from apscheduler.schedulers.background import BackgroundScheduler
import json
import pandas as pd
import datetime
import subprocess
from flask import Flask, render_template

from FunctionExportWealth import ExportCSVWealth, ExportCSVWealthDetailled




# Create the application instance
app = Flask(__name__)

schedulerExportWealth = BackgroundScheduler(daemon=True)


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
    
    schedulerExportWealth.add_job(id = 'ExportWealth', func=ExportCSVWealth, args=[dfComptes], trigger='cron',day_of_week='1-5', hour='23',minute=1)
    # schedulerExportWealth.add_job(id = 'ExportWealthDetailled', func=ExportCSVWealthDetailled, args=[dfComptes], trigger='cron',day_of_week='1-5', hour='23',minute=10)
    # schedulerExportWealth.add_job(id = 'ExportWealthEndofMonth', func=ExportCSVWealth, args=[dfComptes], trigger='cron',day='last', hour='23',minute=15)
    # schedulerExportWealth.add_job(id = 'ExportWealthDetailledEndofMonth', func=ExportCSVWealthDetailled, args=[dfComptes], trigger='cron',day='last', hour='23',minute=20)
    
    
    schedulerExportWealth.start()


    app.run(host='0.0.0.0', port=5094, debug=True)