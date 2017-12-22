from ReClassMap import *

r = Map("./MyClasses2.reclass")

for i in range(3):
	C = r.Class(name="Foo" + str(i))
	C[i*0x8] = Int8(name="Int8_at_0x%02x_exa" % (i*0x8))
	C[i*0x8+0x8] = Pointer(classname="Foo"+str(i+1),name="next_foo")

r.write()