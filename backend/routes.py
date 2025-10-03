from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    try:
        if data and len(data) > 0:
            return (jsonify(data), 200)
        else:
            return ({"message": "Data is empty"}, 500)
    except NameError:
        return ({"message": "Data not defined"}, 404)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        for picture in data:
            if picture["id"] == id:
                return (picture, 200)
        
        return ({"message": f"Picture with id {id} not found"}, 404)

    except Exception as e:
        return ({"message": "Internal server error", "error": str(e)}, 500)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        new_picture = request.get_json()

        if not new_picture or "id" not in new_picture:
            return ({"message": "Invalid request: 'id' not in picture"}, 400)
        
        for picture in data:
            if picture["id"] == new_picture["id"]:
                return ({"Message": f"picture with id {new_picture['id']} already present"}, 302)
        
        data.append(new_picture)

        return (new_picture, 201)

    except Exception as e:
        return ({"message": "Internal server error", "error": str(e)}), 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    try:
        updated_picture = request.get_json()

        if not update_picture:
            return ({"message": "No data provided"}, 400)
        
        for picture in data:
            if picture["id"] == id:
                picture.update(updated_picture)
                return (picture, 200)
        
        return ({"message": "picture not found"}, 404)
    
    except Exception as e:
        return ({"message": "Internal server error", "error": str(e)}, 500)

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    try:
        for idx, picture in enumerate(data):
            if picture["id"] == id:
                del data[idx]
                return ('', 204)
        
        return ({"message": "picture not found"}, 404)
    
    except Exception as e:
        return ({"message": "Internal server error", "error": str(e)}, 500)  
