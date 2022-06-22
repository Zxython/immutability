# Bug info
General Use Known Bugs
------------------
1. When returning a immutable object a \__str__ method gets called at the lower level which overwrites the returned version with the version at the branch. To fix this return a copy which will convert it into a non immutable object that can then be returned. Then make it immutable again if you want to.

Custom Class Known Bugs
-----------
1. The \__setattr__ and \__getattribute__ method are not called when using self.attribute and must be called manually. EX self.\__setattr__('attribute', None)
