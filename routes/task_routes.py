from flask import Blueprint,request,jsonify  
from services.task_services import get_connection
import logging



task_bp=Blueprint("task_bp",__name__)

@task_bp.route("/")
def home():
    return "API is running successfully "

@task_bp.route("/task", methods=["POST"])
def insert_task():

    data = request.get_json()
    if not data or 'title' not in data:
        logging.warning("Task Creation failed title missing")
        return jsonify({"error": "Title is required"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title) VALUES(?)",
            (data["title"],)
        )
        conn.commit()
        conn.close()
        logging.info("Task added successfully")
        return jsonify({"Message":"Task Added"})
    except Exception as e:
        logging.error(f"error while inserting task {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    



@task_bp.route("/task",methods=["GET"])
def get_task():
      
 try:
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("SELECT * FROM tasks")
    
    rows = cursor.fetchall()
    conn.close()
    
    tasks=[]
    
    for row in rows:
        tasks.append({
            "id":row[0],
            "title":row[1],
            "completed":bool(row[2])   
        })
        
    logging.info("Tasks are fetched")
    return jsonify(tasks),200
 except Exception as e:
     logging.error(f"Error while fetching tasks {e}")
     return jsonify({"error":"Database Error"}),500
     



@task_bp.route("/task/<int:id>/complete",methods=["PATCH"])
def complete_task(id):
    
 try:
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id=?",(id,))
    tasks=cursor.fetchone()
    logging.info("Selected record is fetched")
    if not tasks:
        conn.close()
        logging.warning(f"Task with id {id} not found")
        return jsonify({"message":"task not found"}),404
    
    cursor.execute("UPDATE tasks SET completed=1 WHERE id =?",(id,))
    conn.commit()
    conn.close()
    logging.info(f"Task with id {id} marked as successfull")
    return jsonify({"Message":"Completion Updated"})
 except Exception as e:
     logging.error(f"Error while completing task {id}:{e}")
     return jsonify({"error":"Database Error"}),500



@task_bp.route("/task/<int:id>",methods=["DELETE"])
def delete_task(id):
 try:
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id=?",(id,))
    task=cursor.fetchone()
   
    if not task:
        conn.close()
        logging.error(f"Task {id} not found for deletion.")
        return jsonify({"message":"Task not found"}),404
    
    cursor.execute("DELETE FROM tasks WHERE id=?",(id,))
    conn.commit()
    conn.close()
    logging.info(f"Task {id} deleted successfully")
    return jsonify({"message":"Task Deleted"}),200
 except Exception as e:
     logging.error(f"Error while deleting task {id}:{e}")
     return jsonify({"error":"Database Error"})

    
    
    


