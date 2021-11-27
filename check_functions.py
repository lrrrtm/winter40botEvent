
def checkInputName(current):
    try:
        if len(current.split(" ")) == 2:
            return True
    except Exception:
        return False
    return False
