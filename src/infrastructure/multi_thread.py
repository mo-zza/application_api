from threading import Thread

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=None, kwargs=None, Verbose=None):
        Thread.__init__(self, target=target, args=args, group=group, name=name)
        self._return = None
        
    def run(self):
        if self._target is not None:
            self._return = self._target(self._args)
        else:
            self._return = self._target()

    def join(self):
        Thread.join(self)
        return self._return

class ThreadProcess:
    def __init__(self, target, args=None):
        self.target = target
        self.args = args

    def run(self):
        thread = ThreadWithReturnValue(target=self.target, args=self.args)
        thread.start()
        return thread.join()