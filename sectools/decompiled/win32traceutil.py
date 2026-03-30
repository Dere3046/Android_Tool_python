
import win32trace

def RunAsCollector():
    import sys
# WARNING: Decompyle incomplete


def SetupForPrint():
    win32trace.InitWrite()
    
    try:
        print('Redirecting output to win32trace remote collector')
    finally:
        pass
    win32trace.setprint()
    return None


if __name__ == '__main__':
    RunAsCollector()
    return None
None()
