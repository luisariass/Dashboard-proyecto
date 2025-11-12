from bson import ObjectId

def serializar_documento(doc):
    """Convierte el _id de MongoDB a string para que sea JSON serializable."""
    doc["_id"] = str(doc["_id"])
    return doc

def obtener_todos(db, coleccion):
    """Devuelve todos los documentos de una colección."""
    return [serializar_documento(d) for d in db[coleccion].find()]

def obtener_por_id(db, coleccion, id_str):
    """Busca un documento por su _id."""
    try:
        doc = db[coleccion].find_one({"_id": ObjectId(id_str)})
        return serializar_documento(doc) if doc else None
    except Exception:
        return None
