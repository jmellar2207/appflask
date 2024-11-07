from flask import Flask, request, jsonify, render_template


app = Flask(__name__)


# Lista en memoria para almacenar tareas
tasks = [
   {"id": 1, "title": "Estudiar Flask", "done": False},
   {"id": 2, "title": "Configurar Nginx", "done": False}
]


@app.route("/")
def index():
   return render_template("index.html")


# Obtener todas las tareas
@app.route("/tasks", methods=["GET"])
def get_tasks():
   return jsonify({"tasks": tasks})


# Obtener una tarea específica
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
   task = next((t for t in tasks if t["id"] == task_id), None)
   return jsonify(task) if task else ({"error": "Tarea no encontrada"}, 404)


# Crear una nueva tarea
@app.route("/tasks", methods=["POST"])
def create_task():
   new_task = {
       "id": tasks[-1]["id"] + 1 if tasks else 1,
       "title": request.json.get("title", ""),
       "done": False
   }
   tasks.append(new_task)
   return jsonify(new_task), 201


# Actualizar una tarea existente
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
   task = next((t for t in tasks if t["id"] == task_id), None)
   if not task:
       return {"error": "Tarea no encontrada"}, 404
   task["title"] = request.json.get("title", task["title"])
   task["done"] = request.json.get("done", task["done"])
   return jsonify(task)


# Eliminar una tarea
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
   global tasks
   tasks = [t for t in tasks if t["id"] != task_id]
   return {"message": "Tarea eliminada"}


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)
