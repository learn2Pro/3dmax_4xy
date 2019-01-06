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


def GeneratePlugins(sid, cls):
    Conform_cid = MaxPlus.Class_ID(0x1ab13757, 0x12365b98)  # Known bug
    for cd in MaxPlus.PluginManager.GetClassList().Classes:
        if cd.SuperClassId == sid and cd.ClassId != Conform_cid:
            o = MaxPlus.Factory.CreateAnimatable(sid, cd.ClassId, False)
            if o:
                r = cls._CastFrom(o)
                if r:
                    yield r


def CreateTeapot():
    box = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Teapot)
    box.ParameterBlock.Radius.Value = 5.0
    return box


def CreateText(pos, message):
    tex = MaxPlus.Factory.CreateShapeObject(MaxPlus.ClassIds.text)
    tex.ParameterBlock.size.Value = 20.0
    tex.ParameterBlock.text.Value = message
    node = MaxPlus.Factory.CreateNode(tex)
    node.Position = MaxPlus.Point3(pos.X, pos.Y - 5, pos.Z)
    node.WireColor = MaxPlus.Color(1.0, 0.5, 1.0)


def getCamViewPort():
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
        if ((viewType == ViewType.VIEW_CAMERA) and (found == False)):
            typeString = ViewType.GetKey(viewType)
            perspIndex = index
            found = True
        index += 1
    # set the active viewport
    print "Found VIEW_CAMERA Viewport. Index:", perspIndex
    if (perspIndex != -1):
        MaxPlus.ViewportManager.SetActiveViewport(perspIndex)
        # now maximize that view
        # MaxPlus.ViewportManager.SetViewportMax(True)


def getFilePath():
    fm = MaxPlus.FileManager
    fm.Save(render_path + r"test.max")
    print fm.GetFileNameAndPath()


def renderCamera():
    '''Set some common render parameters'''
    outputPath = os.path.join(render_path, 'foo.jpg')

    # render settings is a static class. There is no instance of it.
    render = MaxPlus.RenderSettings
    render.SetOutputFile(outputPath)
    render.SetHeight(540)
    render.SetWidth(960)
    print "Saving file to:", render.GetOutputFile()
    render.SetSaveFile(True)
    MaxPlus.RenderExecute.QuickRender()


def createRenderBm(w, h):
    # Create a bitmap
    rendbm = MaxPlus.Factory.CreateBitmap()

    # First allocate some storage. This is where the type of bitmap is determined.
    BMM_TRUE_64 = 7
    storage = MaxPlus.Factory.CreateStorage(BMM_TRUE_64)

    # Now we can get the bitmap info
    info = storage.GetBitmapInfo()

    # Set some common properties on the bitmap
    info.SetWidth(w)
    info.SetHeight(h)

    # Allocate storage for writing to the bitmap
    storage.Allocate(info, 2)

    # Set the storage on the bitmap
    rendbm.SetStorage(storage)

    # Set the bitmap output base file name
    info.SetName(render_path + r'\FramesRender.bmp')
    return rendbm, info, storage


def renderPic(rendbm, info):
    '''Set some common render parameters'''
    # render settings is a static class. There is no instance of it.
    view = MaxPlus.ViewportManager.GetActiveViewport()
    MaxPlus.RenderExecute.Open(view, MaxPlus.RendType.Region, rendbm.GetWidth(), rendbm.GetHeight())
    rendbm.OpenOutput(info)
    for frame in range(0, 2, 1):
        MaxPlus.RenderExecute.RenderFrame(rendbm, frame * 160)
        rendbm.Write(info, frame)
    MaxPlus.RenderExecute.CloseCurrent()
    rendbm.Close(info)
    return rendbm


def CreateCameras(p3):
    idx = 0
    for obj in GeneratePlugins(MaxPlus.SuperClassIds.Camera, MaxPlus.CameraObject):
        if idx==0:
            node = MaxPlus.Factory.CreateNode(obj)
            node.Position = p3
            break

def ScatterPic(storage):
    for x in range(720):
        for y in range(620):
            storage.PutPixel(x, y, (MaxPlus.Color64(64000 - (x * (64000 / 720)), (y * (64000 / 720)), 64000, 64000)))
    print 'scatter done'


if __name__ == '__main__':
    getCamViewPort()
    bm, info, storage = createRenderBm(960, 480)
    CreateCameras(MaxPlus.Point3(0,10,10))
    renderPic(bm, info)
    bm.Display()
