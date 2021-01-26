import flask
from datetime import datetime
import os
from flask import send_from_directory, request, redirect, flash, url_for, jsonify
from uuid import uuid1
import json
from base64 import b64encode, b64decode, standard_b64encode
import requests
import folium
from flask_ngrok import run_with_ngrok
import pandas as pd
import networkx as nx

app = flask.Flask(__name__)
app.secret_key = "secret key"
run_with_ngrok(app)
source = ''
dest = ''
line = ''
stations_geo = pd.read_csv('station X Y.csv')
df_stations = pd.read_csv('stations data.csv')
TOKEN = b'dapic645ff9f576f1e818cd3c97e4f46c105'
headers = {"Authorization": b"Basic " + standard_b64encode(b"token:" + TOKEN)}
url = "https://eastus.azuredatabricks.net/api/2.0"
dbfs_dir = "dbfs:/FileStore/Ron_Eden/FromWeb/Stream/"

ALLOWED_SCHEMA = ['_id', 'delay', 'congestion', 'lineId', 'vehicleId', 'timestamp', 'areaId', 'areaId1', 'areaId2',
                  'areaId3', 'gridID', 'actualDelay', 'longitude', 'latitude', 'currentHour', 'dateTypeEnum', 'angle',
                  'ellapsedTime', 'vehicleSpeed', 'distanceCovered', 'journeyPatternId', 'direction', 'busStop',
                  'poiId', 'poiId2', 'systemTimestamp', 'calendar', 'filteredActualDelay', 'atStop', 'dateType',
                  'justStopped', 'justLeftStop', 'probability', 'anomaly', 'loc']


# @app.errorhandler(404)
# def page_not_found(error):
#     return flask.redirect(flask.url_for('index')), 404


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/dashboard1.html', methods=['GET', 'POST'])
def dashboard1():
    global line
    global source
    global dest
    lines = []
    all_lines = set()
    source_dest = []
    all_stations = list(df_stations['Stop 1 Name'].unique())
    for i, row in stations_geo.iterrows():
        all_lines.add(row['lineId'])
        if request.method == 'POST' and row['lineId'] == request.form.get('line', -1):
            lines.append((row['Y'], row['X'], row['stop_name']))

    all_lines = sorted(all_lines)
    all_stations = sorted(all_stations[2:-1])
    all_stations.insert(0, 'North Circular Road (Lower Dorset Street)')
    all_stations.insert(0, 'Faussagh Avenue (Church)')
    line = request.form.get('line', line)
    source = request.form.get('source', source)
    dest = request.form.get('dest', dest)
    start_coords = (53.346392, -6.270854)
    folium_map = folium.Map(location=start_coords, zoom_start=12)
    df = df_stations[(df_stations['Stop 1 Name'] == source) & (df_stations['Stop 2 Name'] == dest)].head(1)
    if len(df) == 0:
        df = pd.DataFrame(data=(['There is no direct bus line between these two stations']), columns=['Message'])
    for i, row in stations_geo.iterrows():
        if request.method == 'POST' and (row['stop_name'] == source or row['stop_name'] == dest):
            source_dest.append((row['Y'], row['X'], row['stop_name']))
    for s in source_dest:
        folium.Marker(location=s[:2], popup=s[2], tooltip=s[2],
                      icon=folium.Icon(color='red', icon_color='white', icon='bus', angle=0, prefix='fa')).add_to(
            folium_map)
    for geo in lines:
        if geo[2] in [source, dest]:
            continue
        folium.Marker(
            location=geo[:2],
            popup=geo[2],
            tooltip=geo[2],
            color='blue'
        ).add_to(folium_map)
    return flask.render_template('dashboard1.html', lines=all_lines, map=folium_map._repr_html_(), line=line, stations=all_stations, source=source, dest=dest, df=df.to_html(index=False, justify='center'),
                                 url_="http://40.121.19.5:5601/app/visualize#/edit/a8b7aee0-5820-11eb-9898-4f080e6f28a7?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A'2018-07-11T09%3A00%3A00.000Z'%2Cto%3A'2018-07-12T09%3A00%3A00.000Z'))")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/dashboard2.html')
def dashboard2():
    global line
    print(line)
    url = create_link(line)
    url = "http://da2020w-0017.eastus.cloudapp.azure.com:5601/goto/77dc15099ceb213049d09cbdb10ab971"
    return flask.render_template('dashboard2.html', url_=url)


@app.route('/upload.html')
def upload():
    return flask.render_template('upload.html')


def perform_query(path, data):
    session = requests.Session()
    resp = session.request('POST', url + path, data=json.dumps(data), verify=True, headers=headers)
    return resp.json()


def write_file(local_file, dbfs_path, overwrite):
    handle = perform_query('/dbfs/create', data={'path': dbfs_path, 'overwrite': overwrite})['handle']
    while True:
        contents = local_file.read(2**20)
        if len(contents) == 0:
            break
        perform_query('/dbfs/add-block', data={'handle': handle, 'data': b64encode(contents).decode()})
    perform_query('/dbfs/close', data={'handle': handle})


@app.route('/upload.html', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            files = request.files['files']
            fileb = request.files['fileb']
            file = fileb if files.filename == '' else files
            print(file)
            row_dict = json.loads(file.readline())
            if file and all(key in row_dict.keys() for key in ALLOWED_SCHEMA):
                filename = str(uuid1())
                print('uploading')
                write_file(local_file=file, dbfs_path=dbfs_dir + filename, overwrite=True)
                flash("File successfully uploaded to Data Bricks File System :)", 'success')
                # else:
                #     flash("File failed to upload: " + resp, 'error')
                return redirect(url_for('upload'))
            else:
                flash(f"Invalid schema. Please put it in this form: {ALLOWED_SCHEMA}", 'error')
                return redirect(request.url)
        except Exception as e:
            flash('Please try again', 'error')
            print(f"Error: {e}")
        return redirect(request.url)
    return flask.render_template('index.html', key=None)


def create_link(lineId):
    url = "http://da2020w-0017.eastus.cloudapp.azure.com:5601/app/dashboards#/view/93b3b1a0-567d-11eb-9f43-f960269201b7?embed=true&_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'2018-07-11T09:44:04.037Z',to:'2018-07-12T09:59:16.747Z'))&_a=(description:'',filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,index:'70ed2270-59af-11eb-9898-4f080e6f28a7',key:lineId,negate:!f,params:(query:'122'),type:phrase),query:(match_phrase:(lineId:'122')))),fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),query:(language:kuery,query:''),timeRestore:!f,title:'update%20to%201401',viewMode:view)&show-time-filter=true".format(lineId, lineId)
    print(url)
    return url
if __name__ == '__main__':
    app.run()
