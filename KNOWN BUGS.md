# Bug info
General Use Known Bugs
------------------
1. When returning a immutable object a \__str__ method gets called at the lower level which overwrites the returned version with the version at the branch. To fix this return a copy which will convert it into a non immutable object that can then be returned. Then make it immutable again if you want to.
2. If functions are called consecutively the immutable object won't reset. To fix this type str(your_object_here) in between the function calls. You do not have to store the value from the string method
3. immutable objects are not compatible with multithreading or multiprocessing

Custom Class Known Bugs
-----------
please note that the bugs listed below do not apply if you have a mutable class in an immutable list
1. The \__setattr__ and \__getattribute__ method are not called when using self.attribute and must be called manually. EX self.\__setattr__('attribute', None)
