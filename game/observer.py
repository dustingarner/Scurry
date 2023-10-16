class Observer:
    def __init__(self, action: callable) -> None:
        self.connect(action)

    def connect(self, action: callable) -> None:
        self.action = action
    
    def disconnect(self) -> None:
        self.action = lambda *args, **kwargs: None

    def call(self, *args, **kwargs):
        self.action(*args, **kwargs)

class Subject:
    def __init__(self) -> None:
        self.observers = []
    
    def add_observer(self, observer: Observer) -> None:
        self.observers.append(observer)
    
    def remove_observer(self, observer: Observer) -> None:
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify(self, *args, **kwargs) -> None:
        for observer in self.observers:
            observer.call(*args, **kwargs)

