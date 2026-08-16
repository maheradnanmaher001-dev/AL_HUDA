class NavigationService:
    manager=None
    @classmethod
    def go(cls,name):
        if cls.manager: cls.manager.current=name
