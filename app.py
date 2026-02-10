from flask import Flask
from services.task_services import create_table
from routes.task_routes import task_bp
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s"    
)

app=Flask(__name__)

create_table()
logging.info("Database table checked/created")

app.register_blueprint(task_bp)
logging.info("Task blueprint registered")

if __name__=="__main__":
    logging.info("Application Started")
    app.run(debug=True)
    
    
    


    
    
    
    
    

