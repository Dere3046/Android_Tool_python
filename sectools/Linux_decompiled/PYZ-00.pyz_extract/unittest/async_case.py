
import asyncio
import inspect
from case import TestCase

class IsolatedAsyncioTestCase(TestCase):
    
    def __init__(self = None, methodName = None):
        super().__init__(methodName)
        self._asyncioTestLoop = None
        self._asyncioCallsQueue = None

    
    async def asyncSetUp(self):
        pass

    
    async def asyncTearDown(self):
        pass

    
    def addAsyncCleanup(self, func, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def _callSetUp(self):
        self.setUp()
        self._callAsync(self.asyncSetUp)

    
    def _callTestMethod(self, method):
        self._callMaybeAsync(method)

    
    def _callTearDown(self):
        self._callAsync(self.asyncTearDown)
        self.tearDown()

    
    def _callCleanup(self, function, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def _callAsync(self, func, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def _callMaybeAsync(self, func, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    async def _asyncioLoopRunner(self, fut):
        self._asyncioCallsQueue = queue = asyncio.Queue()
        fut.set_result(None)
        await queue.get()
        query = <NODE:28>
        queue.task_done()
        if query is None:
            return None
        (fut, awaitable) = None
    # WARNING: Decompyle incomplete

    
    def _setupAsyncioLoop(self):
        pass
    # WARNING: Decompyle incomplete

    
    def _tearDownAsyncioLoop(self):
        pass
    # WARNING: Decompyle incomplete

    
    def run(self = None, result = None):
        self._setupAsyncioLoop()
    # WARNING: Decompyle incomplete

    
    def debug(self = None):
        self._setupAsyncioLoop()
        super().debug()
        self._tearDownAsyncioLoop()

    
    def __del__(self):
        if self._asyncioTestLoop is not None:
            self._tearDownAsyncioLoop()
            return None

    __classcell__ = None

