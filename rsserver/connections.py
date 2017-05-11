def arango_up(arango):
    try:
        arango.reload()
        return True
    except:
        return False
