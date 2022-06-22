# Custom Class Info
known bugs
-----------
1. The \__setattr__ and \__getattribute__ method are not called when using self.attribute and must be called manually. EX self.\__setattr__('attribute', None)
