import config

def getCanonical(path):
    return "%s%s" % (config.domain, path)

def getCanonicalImage(image):
    return "%s/images/%s" % (config.domain, image)
