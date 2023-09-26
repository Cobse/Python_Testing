class PythonClassA:
    def __init__(self):
        super().__init__()
        self.var_a = "something class A"
        self.var_b = "some other class A"

class PythonClassB:
    def __init__(self):
        #super().__init__()
        self.var_c = "something class B"
        self.var_d = "some other class B"


class PythonClassChild(PythonClassA, PythonClassB):
    def __init__(self):
        super().__init__()


'''
class PythonClassChild(PythonClassA, PythonClassB):
    def __init__(self):
        PythonClassA.__init__(self)
        PythonClassB.__init__(self)
        # Any additional initialization for PythonClassChild
'''
        
py_class = PythonClassChild()

print(py_class.var_a)
print(py_class.var_c)