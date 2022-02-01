import pandas as pd
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def home():
    return '''
          <style>
          input {width: 100%;margin: 10px 0;padding: 10px;}
          form {display: table;width: 400px;margin: 20% auto;}
          </style>
          <form action="/grade">
              <div><label>Matrikel: <input type="text" name="matrik"></label></div>
              <input type="submit" value="Submit">
          </form>'''


@app.route("/grade", methods=['GET'])
def grade():
    try_again = "<p>Try again.</p>"
    not_found = "<p>Not found, contact teaching-team.</p>"

    matrik = escape(request.args.get("matrik"))
    if matrik is None:
        return try_again

    try:
        report = pd.read_csv('grades.csv', sep=';', index_col='ID number')
        matrik = str(int(matrik))
        row = report.loc[matrik].to_dict()

        html = "<style>table{width:300px;margin: 0 auto;border-collapse: collapse;}td{padding: 5px;}</style><table border='1'>"
        skip = 0
        for k, val in row.items():
            if skip < 3:
                skip += 1
                continue

            html += f"<tr><td>{k}</td><td>{val}</td></tr>"
            skip += 1

        html += "</table>"
        return html
    except:
        return not_found


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)