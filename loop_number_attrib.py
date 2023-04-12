


class MainClass:
    def __init__(self):
        self.arg1 = "Test1"
        self.arg2 = "Test2"
        self.arg3 = "Test3"
        self.arg4 = "Test4"


my_main_class = MainClass()




attributes = [a for a in dir(my_main_class) if not a.startswith('__')]
print(attributes)

for attr, value in vars(my_main_class).items():
    print(attr, value)



