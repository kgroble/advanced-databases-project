def arango_up(arango):
    try:
        arango.reload()
        return True
    except:
        return False

def mongo_up(mongo):
    try:
        mongo.list()
        return True
    except:
        return False
