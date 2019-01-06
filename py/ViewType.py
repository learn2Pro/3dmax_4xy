# Copied from the enum ViewType in maxapi.h. This is the closest thing we have
# to an enum in python.
class ViewType(object):
    VIEW_LEFT          = 0
    VIEW_RIGHT         = 1
    VIEW_TOP           = 2
    VIEW_BOTTOM        = 3
    VIEW_FRONT         = 4
    VIEW_BACK          = 5
    VIEW_ISO_USER      = 6
    VIEW_PERSP_USER    = 7
    VIEW_CAMERA        = 8
    VIEW_GRID          = 9
    VIEW_NONE          = 10
    VIEW_TRACK         = 11
    VIEW_SPOT          = 12
    VIEW_SHAPE         = 13
    VIEW_SCHEMATIC     = 14
    VIEW_RENDER        = 15
    VIEW_SCENEEXPLORER = 16
    VIEW_OTHER         = 17

    @staticmethod
    # Looks up a Key in the class dictionary given a Value
    # Given a value for one of the members in the class above, returns a string representation of
    # the variable name. So for instance, if 14 is passed in, this function
    # returns the string "VIEW_SCHEMATIC"
    def GetKey(val):
        result = -1
        for item in ViewType.__dict__:
            theValue = ViewType.__dict__[item]
            if (theValue == val):
                result = item
                break
        return result