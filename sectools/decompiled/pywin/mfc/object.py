
import sys
import win32ui

class Object:
    
    def __init__(self, initObj = (None,)):
        self.__dict__['_obj_'] = initObj
        if initObj is not None:
            initObj.AttachObject(self)
            return None

    
    def __del__(self):
        self.close()

    
    def __getattr__(self, attr):
        pass
    # WARNING: Decompyle incomplete

    
    def OnAttachedObjectDeath(self):
        self._obj_ = None

    
    def close(self):
        if '_obj_' in self.__dict__ or self._obj_ is not None:
            self._obj_.AttachObject(None)
            self._obj_ = None
            return None
        return None



class CmdTarget(Object):
    
    def __init__(self, initObj):
        Object.__init__(self, initObj)

    
    def HookNotifyRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookNotify(handler, i))
        return oldhandlers

    
    def HookCommandRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookCommand(handler, i))
        return oldhandlers

    
    def HookCommandUpdateRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookCommandUpdate(handler, i))
        return oldhandlers


