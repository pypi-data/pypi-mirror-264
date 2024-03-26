class handler:

    def __init__(self) -> None:
        self.storage = {}

    def call(self,funame,*args,**keys):
        if funame in self.storage.keys():
            try:
                func , methods = self.storage.get(funame) ; args , keys = methods
                func(*args,**keys)
            except Exception as er:
                    raise er
        else:
            AttributeError(f"can't find function {func}")

    def handle(self,funame,*args1,**keys1):
        def handle(func,*args_,**keys_):
            args = args_+args1 ; keys_.update(keys1) ;keys = keys_
            if funame in self.storage.keys():
                raise AttributeError(f"function all ready exists") 
            else:
                self.storage[funame] = (func,(args,keys))
            lfunc = lambda : func(*args,**keys)
            return lfunc
        return handle
    
    def run(self,wraper):
        while True:
            try:
                func,args,keys = wraper()
                self.call(func,*args,**keys)
            except Exception as er:
                raise er