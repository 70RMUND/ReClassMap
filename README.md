# ReClassMap
### Generate ReClass class descriptions using Python! 
#### Library objects documented:  [**here**](http://htmlpreview.github.io/?https://github.com/70RMUND/ReClassMap/master/docs.htm "**here**")
#### Features:
- Renders python descriptions of ReClass nodes and generates *.reclass database files
- Leverages python syntax to produce quick class descriptions
	- Overloads the python index operator to elegantly describe offset mappings
- Supports all primitive node types and most advanced ones too
- Auto-generates padding of undefined memory ranges between defined nodes
- Validates that all defined nodes do not overlap in memory based on their size
	- ReClassMap will error and provide info on any overlapping nodes

```python
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
```
![](https://i.imgur.com/3lS96x9.png)

#### Requirements
- Python 2.7.*
- ReClassEx v1.1 by Dude719 -OR-
- ReClass.NET v1.1 by KN4CK3R

#### Known Issues & Limitations
- The Vtable nodetype may cause ReClassEx v1.1 to crash
- The Custom node type does not translate to char-based C++ padding in ReClassEx v1.1
- ReClass.NET v1.1 doesn't appear to support *.reclass hidden nodetypes, it will ignore them
- ReClass.NET v1.1 doesn't appear to support *.reclass inline comments, it will ignore them
- ReClassMap does not currently support the following nodetypes:
-- nt_none
-- nt_base
-- nt_struct
-- nt_hidden
-- nt_function
-- nt_ptrarray
- ReClassMap will validate incorrect memory mapping because it knows the size of every node type. The only node type it does not validate correctly is the Instance nodetype because its size is based on 1 or more external classes

#### Examples
- Clone this repo and make sure ReClassMap.py is in the same directory as your \*_map.py files
- For the Battlefield 1 example:
-- Run: python.exe ./bf1_map.py
- For the Battlefield 4 example:
-- Run: python.exe ./bf4_map.py







