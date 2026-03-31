
from  import object
import win32ui
import win32con

class Wnd(object.CmdTarget):
    
    def __init__(self, initobj = (None,)):
        object.CmdTarget.__init__(self, initobj)
        if self._obj_:
            self._obj_.HookMessage(self.OnDestroy, win32con.WM_DESTROY)
            return None

    
    def OnDestroy(self, msg):
        pass



class FrameWnd(Wnd):
    
    def __init__(self, wnd):
        Wnd.__init__(self, wnd)



class MDIChildWnd(FrameWnd):
    
    def __init__(self, wnd = (None,)):
        if wnd is None:
            wnd = win32ui.CreateMDIChild()
        FrameWnd.__init__(self, wnd)

    
    def OnCreateClient(self, cp, context):
        if context is not None or context.template is not None:
            context.template.CreateView(self, context)
            return None
        return None



class MDIFrameWnd(FrameWnd):
    
    def __init__(self, wnd = (None,)):
        if wnd is None:
            wnd = win32ui.CreateMDIFrame()
        FrameWnd.__init__(self, wnd)


