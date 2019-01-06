import MaxPlus
import os
import math

render_path = "D:\\4xy\\RenderImg\\"


# Copied from the enum ViewType in maxapi.h. This is the closest thing we have
# to an enum in python.
class ViewType(object):
    VIEW_LEFT = 0
    VIEW_RIGHT = 1
    VIEW_TOP = 2
    VIEW_BOTTOM = 3
    VIEW_FRONT = 4
    VIEW_BACK = 5
    VIEW_ISO_USER = 6
    VIEW_PERSP_USER = 7
    VIEW_CAMERA = 8
    VIEW_GRID = 9
    VIEW_NONE = 10
    VIEW_TRACK = 11
    VIEW_SPOT = 12
    VIEW_SHAPE = 13
    VIEW_SCHEMATIC = 14
    VIEW_RENDER = 15
    VIEW_SCENEEXPLORER = 16
    VIEW_OTHER = 17

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


def RemoveRenderedFile(file):
    if os.path.exists(file):
        os.remove(file)


def CreateSpheres():
    '''Creates an array of spheres in a cone like shape'''
    cumulative = 0
    sphere_radius = 6.0  # for the sphere
    theSphere = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Sphere)
    theSphere.ParameterBlock.Radius.Value = sphere_radius
    revolutions = 9 * 360
    radius = 40.0
    z = 0.0
    for i in range(0, revolutions, 20):
        node = MaxPlus.Factory.CreateNode(theSphere)
        radians = math.radians(i)  # convert degrees to radians
        x = radius * math.cos(radians)
        y = radius * math.sin(radians)
        node.Position = MaxPlus.Point3(x, y, z)
        z += 1.0
        radius -= 0.20


def MaximizePerspective():
    '''This function finds the first perspective viewport, makes it active and maximizes it.'''
    allViewports = True
    skipPerspective = False
    # zoom out to view all the geometry, in all viewports
    MaxPlus.ViewportManager.ViewportZoomExtents(allViewports, skipPerspective)

    index = 0
    perspIndex = -1
    found = False
    # Find the first perspective view and make that viewport is active
    for view in MaxPlus.ViewportManager.Viewports:
        viewType = view.GetViewType()
        print "%d - %s - %s (%d)" % (
        index, MaxPlus.ViewportManager.getViewportLabel(index), ViewType.GetKey(viewType), viewType)
        if ((viewType == ViewType.VIEW_PERSP_USER) and (found == False)):
            typeString = ViewType.GetKey(viewType)
            perspIndex = index
            found = True
        index += 1
    # set the active viewport
    print "Found Perspective Viewport. Index:", perspIndex
    if (perspIndex != -1):
        MaxPlus.ViewportManager.SetActiveViewport(perspIndex)
        # now maximize that view
        MaxPlus.ViewportManager.SetViewportMax(True)


def getFrontView():
    index = 0
    for view in MaxPlus.ViewportManager.Viewports:
        viewType = view.GetViewType()
        print "%d - %s - %s (%d)" % (
            index, MaxPlus.ViewportManager.getViewportLabel(index), ViewType.GetKey(viewType), viewType)
        index += 1


def SetRenderParameters():
    '''Set some common render parameters'''
    outputPath = os.path.join(render_path, 'foo.jpg')

    # render settings is a static class. There is no instance of it.
    render = MaxPlus.RenderSettings
    render.SetOutputFile(outputPath)
    print "Saving file to:", render.GetOutputFile()
    render.SetSaveFile(True)
    return outputPath


def createCam():
    c = MaxPlus.Factory.CreateCameraObject(2)
    c.Enable(True)
    print c.GetCameraType


def demoRender():
    MaxPlus.FileManager.Reset(True)
    # CreateSpheres()
    # MaximizePerspective()
    path = SetRenderParameters()
    # Renders only one frame at the current time.
    RemoveRenderedFile(path)
    MaxPlus.RenderExecute.Open(createCam())
    MaxPlus.RenderExecute.QuickRender()


# demoRender()
createCam()
getFrontView()
