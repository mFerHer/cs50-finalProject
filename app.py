from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

@app.route("/")
def index():
    
    db = sqlite3.connect("data.db")
    db.row_factory = sqlite3.Row
    curs = db.cursor()

    # Get stations data
    curs.execute("SELECT * FROM info JOIN prices ON info.id = prices.id")
    rows = curs.fetchall()
    stations = [dict(row) for row in rows]

    # Get last update
    curs.execute("SELECT value FROM metadata WHERE key = 'last_update'")
    row = curs.fetchone()
    last_update = row["value"] if row else "Unknown"

    # Get lat & lng for localities
    curs.execute("SELECT locality, AVG(latitude) AS lat, AVG(longitude) AS lng \
        FROM info \
        GROUP BY locality \
        ORDER BY locality")
    localidades = [dict(row) for row in curs.fetchall()]


    db.close()


    return render_template("index.html", stations=stations, last_update=last_update, localidades=localidades)


if __name__ == "__main__":
    app.run(debug=True)
