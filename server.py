# Config
DB = "vito.db"
IP = "0.0.0.0" 

import json
import sqlite3
import cherrypy
import os
import subprocess

conn = sqlite3.connect(DB)
conn.execute("""
CREATE TABLE IF NOT EXISTS log(
  id INTEGER PRIMARY KEY,
  date TEXT,
  temp_ext REAL,
  temp_ecs REAL,
  temp_eau_cc1 REAL,
  temp_eau_cc2 REAL,
  mode_nr INT
);
""")

conn.commit()
conn.close()

class VclientWeb(object):
  def index(self):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT strftime('%s', date) * 1000, temp_ext, temp_ecs, temp_eau_cc1, temp_eau_cc2, mode_nr FROM log WHERE date(date) >= date('now', '-7 days');")
    
    series = [
      {
        "name": "Temp Ext",
        "data": []
      },
      {
        "name": "Temp Ecs",
        "data": []
      },
      {
        "name": "Temp eau CC1",
        "data": []
      },
      {
        "name": "Temp eau CC2",
        "data": []
      },
      {
        "name": "Mode NR",
        "data": []
      },
    ]

    for v in cursor.fetchall():
      for i in range(0, 5):
        series[i]["data"].append([v[0], v[i + 1]])

    data = json.dumps(series)

    return """
<!doctype html>
<html>
  <head>
    <title>Vclient</title>
  </head>

  <body>
  <div id="chart" style="width: 100%%; height: 500px;"></div>

  <form action="/command/" method="POST">
    <input name="command" placeholder="Execute command">
    <input type="submit">
  </form>

  <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
  <script src="/highstock.js"></script>
  <script>
  $(function () {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    $('#chart').highcharts('StockChart', {
        chart: {
            type: 'spline'
        },
        title: {
            text: "Vclient",
            x: -20 //center
        },
        subtitle: {
            text: "Charts",
            x: -20
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Temperature (C)'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: %s
    });
  });
  </script>
  </body>
</html>
""" % data

  index.exposed = True

#  def command(self, command=None):
    # FIXME: this is highly unsecure
#    subprocess.call(command.split())
#    raise cherrypy.HTTPRedirect("/")
#
#  command.exposed = True

# Allow all IPs to access the web server
cherrypy.server.socket_host = IP

conf = {
  '/highstock.js':
    {'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))},
      '/highstock.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bower_components/highstock-release/highstock.js')
      }
    }

cherrypy.quickstart(VclientWeb(), config=conf)

