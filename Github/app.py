import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import xlrd
import fnmatch
from geopy.geocoders import Nominatim
from geopy import geocoders



UPLOAD_FOLDER = 'C://Users//anielsen//Desktop//Python Class//App10 - Super Geocoder//static//'

app = Flask(__name__, instance_relative_config=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'Friday'
static_folder = '/static'

@app.route('/')
def index():
    return render_template('base.html')


pd.set_option('display.max_colwidth',-1)


@app.route('/upload',methods=['GET','POST'])
def display_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if fnmatch.fnmatch(filename, '*.xlsx'):
            x = pd.read_excel(file)
        elif fnmatch.fnmatch(filename, '*.csv'):
            x = pd.read_csv(file)
        else:
            flash("File must be a .csv or .xlsx file")
            return redirect(url_for('index'))

        xf = pd.DataFrame(x)
        geolocator = Nominatim()

        if 'Address' in xf.columns:
            location = xf['Address'].apply(geolocator.geocode)
        elif 'address' in xf.columns:
            location = xf['address'].apply(geolocator.geocode)
        else:
            flash('File must contain the column "Address" or "address"')
            return redirect(url_for('index'))

        xf['lat'] = location.apply(lambda addr: addr.latitude if addr != None else None)
        xf['lon'] = location.apply(lambda addr: addr.longitude if addr != None else None)
        xf['Location'] = xf['lon'].astype(str) + ', ' + xf['lat'].astype(str)
        xf = xf.drop(['lat', 'lon'], axis=1)
        global newfile
        newfile = '(updated)'+filename
        xf.to_csv('C://Users//anielsen//Desktop//Python Class//App10 - Super Geocoder//static//'+ newfile)
        df = xf.to_html()

        return render_template('upload.html', name=filename, data=df)

    if request.method == 'GET':
        return send_from_directory(app.config['UPLOAD_FOLDER'], newfile , as_attachment=True)




if __name__ == '__main__':
    app.run(debug=False)
