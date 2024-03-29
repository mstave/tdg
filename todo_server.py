import flask
import todo_file
import todo_item
from flask import json, request, g

todo_app = flask.Flask(__name__)

@todo_app.before_request
def before_request():
    g.tdfile = todo_file.TodoFile()
    g.tdfile.todo_txt_arr.sort()
    g.tdfile.update_todo_item_arr()
    g.dirty = False
    
@todo_app.after_request
def after_request(response):
    if g.dirty == True:
        g.tdfile.todo_txt_arr.sort()
        g.tdfile.update_todo_item_arr()
        g.tdfile.write_file()
    return response



def serialize(obj):
    if isinstance(obj, int):
        return obj
    if isinstance(obj, (bool, int, float)):
        return obj
    elif isinstance(obj, dict):
        obj = obj.copy()
        for key in obj:
            obj[key] = serialize(obj[key])
        return obj
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize([item for item in obj]))
    elif hasattr(obj, '__dict__'):
        return serialize(obj.__dict__)
    else:
        return repr(obj)  # Don't know how to handle, convert to string
    return json.dumps(serialize(obj))

@todo_app.route("/del/<int:td_id>", methods=['GET','POST'])
def delete_td(td_id):
    g.tdfile.delete_task(td_id)
    g.dirty = True
    return flask.redirect("/")


@todo_app.route("/")
def serve_tds():
    return flask.render_template("todo.html")

@todo_app.route("/add_new", methods=['GET','POST'])
def add_new():
    newTD = todo_item.TodoItem()
    newTD.task = request.form.get('task')
    newTD.priority = request.form.get('priority')
    newTD.project = request.form.get('project')
    newTD.create_today()
    g.tdfile.append(newTD)
    g.dirty = True

    return flask.redirect("/")



@todo_app.route("/json.up", methods=['POST'])
def receives_json():
    try:
        thejson = request.json
        print ("postass")
    # print('---------- got it ------ ')
        print ("trying....")
        print("request json was " + str(request.json))
    except:
        print ("error parsing " + str(request.__dict__))

    newTD = todo_item.TodoItem()
    newTD.parse_json(request.json)
    g.tdfile.update_task(request.json.get('gui_index', -1), newTD)
    g.tdfile.update_todo_txt_arr()
    g.dirty = True;

    return json.jsonify(dd=serialize(g.tdfile.todo_item_arr))

@todo_app.route("/todo.json")
def todo_json():
    return json.jsonify(dd=serialize(g.tdfile.todo_item_arr))


@todo_app.route("/tsd.js")
def serve_tdjs():
    return todo_app.send_static_file("td.js")

if __name__ == '__main__':
    todo_app.run(host="0.0.0.0", port=5942, debug=True)

