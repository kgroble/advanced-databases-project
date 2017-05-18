def arango_up(arango, redis):
    if redis.llen('recovery_queue') > 0:
        return False

    try:
        arango.reload()
        return True
    except:
        return False

def mongo_up(mongo):
    try:
        mongo.current_op()
        return True
    except:
        return False
