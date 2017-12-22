from ReClassMap import *

r = Map("./MyClasses.reclass")

C = r.Class(name="Foo0")
C[0x00] = Int64(name="Bar0")
C[0x08] = Int32(name="Bar1")
C[0x0C] = Int16(name="Bar2")
C[0x0E] = Int8(name="Bar3")
C[0x0F] = Int8(name="Bar4")
C[0x20] = Pointer(classname="Foo1",name="pFoo1")

C = r.Class(name="Foo1")
C[0x00] = Double(name="Bar5")
C[0x08] = Float(name="Bar6")

r.write()