from flask import Flask, render_template, request, redirect, url_for
import taskController
import sqlite3
from datetime import date
import re


app = Flask(__name__)
connection = sqlite3.connect('tasks_data.db')
static_tittle = None
main_table = "tasks"
close_table = "closedtasks"
deteled_table = "deletedtasks"

@app.route("/", methods=['POST','GET'])
def main():
    #action = request.form.get("action")
    return render_template('task.html')

@app.route("/task", methods=['POST','GET'])
def task():
    global static_tittle
    if request.method == 'POST':
        data = taskController.getAllData(main_table)
        action = request.form.get("button")
        task_title = request.form.get("Title")
        task_title = re.sub(r'[^A-Za-z0-9 ]+', '', task_title)
        if action == "aceptar" and static_tittle != task_title:
            task_resume = request.form.get("Resume")
            task_resume = re.sub(r'[^A-Za-z0-9 ]+', '', task_resume)
            task_priority = request.form.get("Prioridad")
            task_status = 0
            task_date = str(date.today())
            taskController.insertRow(task_title,task_resume,task_priority,task_date,task_status)
        else:
            pass
        return redirect(url_for('task'))
    else:
        data = taskController.getAllData(main_table)
        return render_template('task.html', contenido = data, current_path = request.url)

@app.route("/task<name>", methods =['POST'])
def deleteRow(name):
        action = request.form.get("button")
        print(action)
        if action == "maincerrar":
            taskController.pushDataIntoTable(name, main_table, close_table)
            return redirect(url_for('task'))
        elif action == "maineliminar":
            taskController.pushDataIntoTable(name, main_table, deteled_table)
            return redirect(url_for('task'))
        elif action == "closecerrar":
            print(name)
            taskController.pushDataIntoTable(name, close_table, main_table)
            return redirect(url_for('closed_task'))
        elif action == "closeeliminar":
            taskController.pushDataIntoTable(name, close_table, deteled_table)
            return redirect(url_for('closed_task'))

@app.route("/task/closed", methods = ['POST','GET'])
def closed_task():
    data = taskController.getAllData(close_table)
    return render_template('task.html', contenido = data, current_path = request.url)


@app.route("/task/deleted", methods = ['POST','GET'])
def deleted_task():
    data = taskController.getAllData(deteled_table)
    return render_template('task.html', contenido = data, current_path = request.url)

if __name__ == '__main__':
    taskController.createDB()
    taskController.createTable()
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)