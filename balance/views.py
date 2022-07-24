from email import message
from flask import jsonify, request

from . import app
from .models import DBManager


"""
Verbos y formato de endpoints
GET /movimientos ------> LISTAR movimientos
POST /movimientos -----> CREAR movimiento
GET /movimientos/1 ----> LEER el movimiento con ID 1
POST /movimientos/1 ---> ACTUALIZAR el movimiento con ID 1 (sobreescribe todo el objeto)
PUT /movimientos/1 ----> ACTUALIZAR el movimiento con ID 1 (sobreescriba parcialmente)
DELETE /movimientos/1 -> ELIMINAR el movimiento con ID 1
importante versionar los endpoint (son un contrato)
/api/v1/...

"""

RUTA = app.config.get("RUTA")   

@app.route("/api/v1/movimientos/1")
def listar_movimientos():
    try:
        db = DBManager(RUTA)
        sql = "SELECT * from movimientos ORDER BY fecha, id"
        movimientos = db.consultaSQL(sql)
        resultado = {
            "status": "success",
            "results": movimientos
        }
    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }

    return jsonify(resultado)


@app.route("/api/v1/movimientos/", methods=["POST"])
def insertar_movimiento():
    try:
        sql = ("INSERT INTO movimientos (fecha, concepto, tipo, cantidad)"
               "VALUES (:fecha, :concepto, :tipo, :cantidad)")   
        db = DBManager(RUTA)
        ha_ido_bien = db.consultaConParametros(sql, request.json)
        if ha_ido_bien:
            resultado = {
                "status": "success"
            }
        else:
            resultado = {
                "status": "error",
                "message": "Error al insertar el movimiento en la base de datos"
            }
    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }

    return jsonify(resultado)

