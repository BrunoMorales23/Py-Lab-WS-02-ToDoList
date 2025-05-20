from flask import Flask, render_template, request, abort, jsonify, redirect, url_for


app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def main():
    action = request.form.get("Click")
    #oa = request.form.get("Prueba")
    #jh = request.form.get("jh")
    method = request.form.get("Prioridad")

    print(action)
#    print(oa)
    print(method)
#    print(jh)
    return render_template('index.html')

@app.route("/task", methods=['POST','GET'])
def task():
    action = request.form.get("button")
    print(action)
    return render_template('task.html')

if __name__ == '__main__':
    app.run(debug=True)