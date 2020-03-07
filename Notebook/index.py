from sqlalchemy.sql.elements import Null

from Notebook import app
from flask import Blueprint, request, jsonify
from Notebook.models import Events, db

index = Blueprint("index", __name__, template_folder='templates', static_folder='static')


# 将list类转化为Event类的Json格式
def toEvent(events):
    j = []
    for i in events:
        j.append({
            "eid": i.eid,
            "addtime": i.addtime,
            "deadline": i.deadline,
            "event": i.event,
            "status": i.status
        })
    return jsonify(j)


@index.route('/test', methods=['GET'])
def test():
    return {
        "status": 0,
        "message": "successfully add new event",
        "data": {}
    }


# 测试成功
# 新建待办事项, 要求传入event，deadline
@index.route('/addevent', methods=['GET', 'POST'])
def addevent():
    if request.method == 'POST':
        error = None
        deadline = request.form['deadline']
        event = request.form['event']
        new_event = Events(
            event=event,
            deadline=deadline,
            status=False,
        )
        db.session.add(new_event)
        db.session.commit()
        response = {
            "status": 0,
            "message": "success",
            "data": {}
        }
        return response


# 通过eid将一条待办事项设置为完成
@index.route('/set', methods=['GET', 'POST'])
def set():
    if request.method == 'POST':
        eid = request.form['eid']
        error = None
        Events.query.filter_by(eid=eid).update({"status": True})
        db.session.commit()
        return {
            "status": 0,
            "message": "success",
            "data": {}
        }
    return {
        "status": 1,
        "message": "error",
        "data": {}
    }


# 测试成功
# 将所有待办事项设置为完成
@index.route('/setall', methods=['GET'])
def setall():
    if Events.query.filter_by(status=False).update({"status": True}):
        db.session.commit()
        return {
            "status": 0,
            "message": "success",
            "data": {}
        }
    return {
        "status": 1,
        "message": "error",
        "data": {}
    }


# 已测试
# 将一条已完成事项设置为未完成, 要求传入eid
@index.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        eid = request.form['eid']
        Events.query.filter_by(eid=eid).update({"status": False})
        db.session.commit()
        return {
            "status": 0,
            "message": "success",
            "data": {}
        }
    return {
        "status": 1,
        "message": "error",
        "data": {}
    }


# 已测试
# 将所有已完成事项设置为未完成
@index.route('/resetall', methods=['GET'])
def resetall():
    Events.query.filter_by(status=True).update({"status": False})
    db.session.commit()
    return {
        "status": 0,
        "message": "success",
        "data": {}
    }


# 完成
# 查看所有事项
@index.route('/query/all', methods=['GET'])
def query_all():
    events = Events.query.all()
    j = []
    for i in events:
        j.append({
            "eid": i.eid,
            "addtime": i.addtime,
            "deadline": i.deadline,
            "event": i.event,
            "status": i.status
        })
    return jsonify(j)


# 查看所有待办事项
@index.route('/query/incomplete', methods=['GET'])
def query_incomplete():
    events = Events.query.filter_by(status=False).all()
    j = []
    for i in events:
        j.append({
            "eid": i.eid,
            "addtime": i.addtime,
            "deadline": i.deadline,
            "event": i.event,
            "status": i.status
        })
    return jsonify(j)


# 查看所有已完成事项
@index.route('/query/done', methods=['GET'])
def query_done():
    events = Events.query.filter_by(status=True).all()
    j = []
    for i in events:
        j.append({
            "eid": i.eid,
            "addtime": i.addtime,
            "deadline": i.deadline,
            "event": i.event,
            "status": i.status
        })
    return jsonify(j)


# 获取所有事项的数量
@index.route('/getamount/all', methods=['GET'])
def getamount_all():
    events = Events.query.all()
    return {
        "status": 0,
        "message": "success",
        "data": {"amount_of_all": len(events)}
    }


# 获取待办事项的数量
@index.route('/getamount/incomplete')
def getamount_incomplete():
    events = Events.query.filter_by(status=False).all()
    return {
        "status": 0,
        "message": "success",
        "data": {"amount_of_incomplete": len(events)}
    }


# 获取待办事项的数量
@index.route('/getamount/done')
def getamount_done():
    events = Events.query.filter_by(status=True).all()
    return {
        "status": 0,
        "message": "success",
        "data": {"amount_of_done": len(events)}
    }


# 删除所有事项
@index.route('/delete/all')
def delete_all():
    events = Events.query.all()
    if events != Null:
        events = toEvent(events)
        Events.query.delete()
        db.session.commit()
        return events
    return {
        "status": 1,
        "message": "error",
        "data": {"error": "already empty"}
    }


# 删除所有待完成事项
@index.route('/delete/incomplete')
def delete_incomplete():
    events = Events.query.filter_by(status=False).all()
    if events != Null:
        events = toEvent(events)
        Events.query.filter_by(status=False).delete()
        db.session.commit()
        return events
    return {
        "status": 1,
        "message": "error",
        "data": {"error": "incomplete already empty"}
    }


# 删除所有已完成事项
@index.route('/delete/done')
def delete_done():
    events = Events.query.filter_by(status=True).all()
    if events != Null:
        events = toEvent(events)
        Events.query.filter_by(status=True).delete()
        db.session.commit()
        return events
    return {
        "status": 1,
        "message": "error",
        "data": {"error": "done already empty"}
    }


# 根据eid删除一条事项
@index.route('/delete/byeid', methods=['GET', 'POST'])
def delete_one():
    eid = request.form['eid']
    events = Events.query.filter_by(eid=eid).all()
    if events != Null:
        events = toEvent(events)
        Events.query.filter_by(eid=eid).delete()
        db.session.commit()
        return events
    return {
        "status": 1,
        "message": "error",
        "data": {"error": "event not exist!"}
    }
