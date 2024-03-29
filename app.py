from flask import Flask, jsonify, request

from models.task import Task

app = Flask(__name__)


tasks = []
task_id_control = 1


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(
        id=task_id_control,
        title=data.get("title"),
        description=data.get("description", ""),
    )
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Task created!"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
        "tasks": task_list,
        "total_tasks": len(task_list),
    }

    return jsonify(output)


@app.route("/tasks/<int:id>", methods=["GET"])
def get_task_by_id(id):
    task_list = [task.to_dict() for task in tasks]

    try:
        task_selected = next(filter(lambda task: task["id"] == id, task_list))
        return jsonify(task_selected)
    except StopIteration:
        return jsonify({"message": "Task not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
