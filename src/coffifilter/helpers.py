def singleton(class_):
    """
    This function implements the singleton pattern.
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    def reset():
        """
        Reset the singleton instance.
        """
        instances.clear()

    class_.reset = reset
    getinstance.reset = reset
    return getinstance
