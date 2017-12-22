# Copyright 2017 Tormund
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import sys

class NodeType:    # type , size
	nt_none         = [-1 , 0 ] # Not Supported yet
	nt_base         = [0  , 0 ] # Not Supported yet
	nt_instance     = [1  , 8 ]
	nt_struct       = [2  , 0 ] # Not Supported yet
	nt_hidden       = [3  , 0 ] # Not Supported yet
	nt_hex32        = [4  , 4 ] 
	nt_hex64        = [5  , 8 ] 
	nt_hex16        = [6  , 2 ] 
	nt_hex8         = [7  , 1 ] 
	nt_pointer      = [8  , 8 ] 
	nt_int64        = [9  , 8 ] 
	nt_int32        = [10 , 4 ]
	nt_int16        = [11 , 2 ]
	nt_int8         = [12 , 1 ]
	nt_float        = [13 , 4 ]
	nt_double       = [14 , 8 ]
	nt_uint32       = [15 , 4 ] 
	nt_uint16       = [16 , 2 ] 
	nt_uint8        = [17 , 1 ] 
	nt_text         = [18 , 8 ]
	nt_unicode      = [19 , 8 ]
	nt_functionptr  = [20 , 8 ]
	nt_custom       = [21 , 8 ]
	nt_vec2         = [22 , 8 ]
	nt_vec3         = [23 , 12] 
	nt_quat         = [24 , 16] 
	nt_matrix       = [25 , 64]
	nt_vtable       = [26 , 8 ]
	nt_array        = [27 , 8 ]
	nt_class        = [28 , 0 ]
	nt_pchar        = [29 , 8 ] 
	nt_pwchar       = [30 , 8 ]
	nt_bits         = [31 , 1 ]
	nt_uint64       = [32 , 8 ]
	nt_function     = [33 , 0 ] # Not Supported yet
	nt_ptrarray     = [34 , 0 ] # Not Supported yet
	
class Node(object):
	def __init__(self,name,comment):
		self._name = name
		self._comment = comment
		self._bHidden = 0
		
	def _write(self,cls):
		attrib = {}
		attrib["Name"]    = str(self._name)
		attrib["Type"]    = str(self._type)
		attrib["Size"]    = str(self._size)
		attrib["bHidden"] = str(self._bHidden)
		attrib["Comment"] = str(self._comment)
		SubElement(cls,"Node",attrib)
		return cls

class Array(Node):
	def __init__(self,classname,name,total=1,comment=""):
		super(Array, self).__init__(name,comment)
		self._classname = classname
		self._type = NodeType.nt_array[0]
		self._size = NodeType.nt_array[1]
		self._total = total
	def _write(self,cls):
		attrib = {}
		attrib["Name"]    = str(self._name)
		attrib["Type"]    = str(self._type)
		attrib["Size"]    = str(self._size)
		attrib["bHidden"] = str(self._bHidden)
		attrib["Comment"] = str(self._comment)
		attrib["Total"]   = str(self._total)
		nd = SubElement(cls,"Node",attrib)
		arr = {}
		arr["Name"] = str(self._classname)
		arr["Type"] = str(NodeType.nt_class[0])
		arr["Size"] = str(28)
		arr["Comment"] = str(self._comment)
		SubElement(nd,"Array",arr)
		return cls


class Vfunc(Node):
	def __init__(self,name,comment=""):
		super(Vfunc, self).__init__(name,comment)
		
class Vtable(Node):
	def __init__(self,name,comment=""):
		super(Vtable, self).__init__(name,comment)
		self._type = NodeType.nt_vtable[0]
		self._size = NodeType.nt_vtable[1]
		self._vfuncs = {}
		
	def __setitem__(self,key,value):
		self._vfuncs[key] = value
		
	def _write(self,cls):
		attrib = {}
		attrib["Name"]    = str(self._name)
		attrib["Type"]    = str(self._type)
		attrib["Size"]    = str(self._size)
		attrib["bHidden"] = str(self._bHidden)
		attrib["Comment"] = str(self._comment)
		nd = SubElement(cls,"Node",attrib)
		last = sorted(self._vfuncs.iterkeys())[-1]
		for i in range(last+1):
			arr0 = {}
			arr0["bHidden"] = str(0)
			if i in self._vfuncs:
				vfunc = self._vfuncs[i]
				arr0["Name"] = vfunc._name
				arr0["Comment"] = vfunc._comment
			else:
				arr0["Name"] = "Function" + str(i)
				arr0["Comment"] = ""
			f = SubElement(nd,"Function",arr0)
			arr1 = {"Assembly":""}
			SubElement(f,"Code",arr1)
		return cls		
		
		
		
class Functionptr(Node):
	def __init__(self,name,comment=""):
		super(Functionptr, self).__init__(name,comment)
		self._type = NodeType.nt_functionptr[0]
		self._size = NodeType.nt_functionptr[1]

class Custom(Node):
	def __init__(self,name,size=8,comment=""):
		super(Custom, self).__init__(name,comment)
		self._type = NodeType.nt_custom[0]
		self._size = size
		
class Matrix(Node):
	def __init__(self,name,comment=""):
		super(Matrix, self).__init__(name,comment)
		self._type = NodeType.nt_matrix[0]
		self._size = NodeType.nt_matrix[1]
		
class Vec4(Node):
	def __init__(self,name,comment=""):
		super(Vec4, self).__init__(name,comment)
		self._type = NodeType.nt_quat[0]
		self._size = NodeType.nt_quat[1]
		
class Vec3(Node):
	def __init__(self,name,comment=""):
		super(Vec3, self).__init__(name,comment)
		self._type = NodeType.nt_vec3[0]
		self._size = NodeType.nt_vec3[1]
		
class Vec2(Node):
	def __init__(self,name,comment=""):
		super(Vec2, self).__init__(name,comment)
		self._type = NodeType.nt_vec2[0]
		self._size = NodeType.nt_vec2[1]
		
class Pchar(Node):
	def __init__(self,name,comment=""):
		super(Pchar, self).__init__(name,comment)
		self._type = NodeType.nt_pchar[0]
		self._size = NodeType.nt_pchar[1]
		
class Pwchar(Node):
	def __init__(self,name,comment=""):
		super(Pwchar, self).__init__(name,comment)
		self._type = NodeType.nt_pwchar[0]
		self._size = NodeType.nt_pwchar[1]

class Unicode(Node):
	def __init__(self,name,comment=""):
		super(Unicode, self).__init__(name,comment)
		self._type = NodeType.nt_unicode[0]
		self._size = NodeType.nt_unicode[1]
		
class Hex8(Node):
	def __init__(self,name,comment=""):
		super(Hex8, self).__init__(name,comment)
		self._type = NodeType.nt_hex8[0]
		self._size = NodeType.nt_hex8[1]
		
class Hex16(Node):
	def __init__(self,name,comment=""):
		super(Hex16, self).__init__(name,comment)
		self._type = NodeType.nt_hex16[0]
		self._size = NodeType.nt_hex16[1]
		
class Hex32(Node):
	def __init__(self,name,comment=""):
		super(Hex32, self).__init__(name,comment)
		self._type = NodeType.nt_hex32[0]
		self._size = NodeType.nt_hex32[1]
		
class Hex64(Node):
	def __init__(self,name,comment=""):
		super(Hex64, self).__init__(name,comment)
		self._type = NodeType.nt_hex64[0]
		self._size = NodeType.nt_hex64[1]
		
class Ascii(Node):
	def __init__(self,name,comment=""):
		super(Ascii, self).__init__(name,comment)
		self._type = NodeType.nt_text[0]
		self._size = NodeType.nt_text[1]
		
class Int64(Node):
	def __init__(self,name,comment=""):
		super(Int64, self).__init__(name,comment)
		self._type = NodeType.nt_int64[0]
		self._size = NodeType.nt_int64[1]
		
class Int32(Node):
	def __init__(self,name,comment=""):
		super(Int32, self).__init__(name,comment)
		self._type = NodeType.nt_int32[0]
		self._size = NodeType.nt_int32[1]
		
class Int16(Node):
	def __init__(self,name,comment=""):
		super(Int16, self).__init__(name,comment)
		self._type = NodeType.nt_int16[0]
		self._size = NodeType.nt_int16[1]
		
class Int8(Node):
	def __init__(self,name,comment=""):
		super(Int8, self).__init__(name,comment)
		self._type = NodeType.nt_int8[0]
		self._size = NodeType.nt_int8[1]

class Qword(Node):
	def __init__(self,name,comment=""):
		super(Qword, self).__init__(name,comment)
		self._type = NodeType.nt_uint64[0]
		self._size = NodeType.nt_uint64[1]
		
class Dword(Node):
	def __init__(self,name,comment=""):
		super(Dword, self).__init__(name,comment)
		self._type = NodeType.nt_uint32[0]
		self._size = NodeType.nt_uint32[1]
		
class Word(Node):
	def __init__(self,name,comment=""):
		super(Word, self).__init__(name,comment)
		self._type = NodeType.nt_uint16[0]
		self._size = NodeType.nt_uint16[1]
		
class Byte(Node):
	def __init__(self,name,comment=""):
		super(Byte, self).__init__(name,comment)
		self._type = NodeType.nt_uint8[0]
		self._size = NodeType.nt_uint8[1]
		
class Bits(Node):
	def __init__(self,name,comment=""):
		super(Bits, self).__init__(name,comment)
		self._type = NodeType.nt_bits[0]
		self._size = NodeType.nt_bits[1]

class Instance(Node):
	def __init__(self,classname, name,comment=""):
		super(Instance, self).__init__(name,comment)
		self._classname = classname
		self._type = NodeType.nt_instance[0]
		self._size = NodeType.nt_instance[1]
	def _write(self,cls):
		attrib = {}
		attrib["Name"]    = str(self._name)
		attrib["Type"]    = str(self._type)
		attrib["Size"]    = str(self._size)
		attrib["bHidden"] = str(self._bHidden)
		attrib["Comment"] = str(self._comment)
		attrib["Instance"] = str(self._classname)
		SubElement(cls,"Node",attrib)
		return cls
		
class Pointer(Node):
	def __init__(self,classname, name,comment=""):
		super(Pointer, self).__init__(name,comment)
		self._classname = classname
		self._type = NodeType.nt_pointer[0]
		self._size = NodeType.nt_pointer[1]
	def _write(self,cls):
		attrib = {}
		attrib["Name"]    = str(self._name)
		attrib["Type"]    = str(self._type)
		attrib["Size"]    = str(self._size)
		attrib["bHidden"] = str(self._bHidden)
		attrib["Comment"] = str(self._comment)
		attrib["Pointer"] = str(self._classname)
		SubElement(cls,"Node",attrib)
		return cls

class Double(Node):
	def __init__(self,name,comment=""):
		super(Double, self).__init__(name,comment)
		self._type = NodeType.nt_double[0]
		self._size = NodeType.nt_double[1]
		
class Float(Node):
	def __init__(self,name,comment=""):
		super(Float, self).__init__(name,comment)
		self._type = NodeType.nt_float[0]
		self._size = NodeType.nt_float[1]
	
class Class(Node):
		def __init__(self,name,offset=0,size=0,comment="",empty=False):
			super(Class, self).__init__(name,comment)
			self._offset = offset
			self._elements = {}
			self._type = NodeType.nt_class[0]
			self._size = size
			self._empty = empty
			
		def __setitem__(self,key,value):
			for i in range(key+value._size-1,-1,-1): # overlap check
				if i in self._elements:
					n = self._elements[i]
					if i+n._size-1 >= key:
						sys.stderr.write("ERROR: Index 0x%x of element %s in class %s overlaps with element %s\n" % (key,value._name,self._name,n._name))
						sys.stderr.write("ERROR: Class memory map overlap\n")
						exit(1)
					else:
						break
			self._elements[key] = value
			last = sorted(self._elements.iterkeys())[-1]
			
			lastsize = last + self._elements[last]._size # recalulate class size after adding element			
			if lastsize > self._size:
				self._size = lastsize
				
		def __getitem__(self,key):
			if key not in self._elements:
				return None
			else:
				return self._elements[key]
			
		def _write(self,et,hidepad=0,custompad=0):
			if len(self._elements) == 0:
				return et
			last = self._size
			if (custompad):
				self._fill_offsets2(last,hidepad)
			else:
				self._fill_offsets(last,hidepad)
			attrib = {}
			attrib["Name"] = self._name
			attrib["Type"] = str(28)
			attrib["Comment"] = self._comment
			attrib["Offset"] = str(self._offset)
			attrib["strOffset"] = hex(self._offset)[2:].strip('L')
			attrib["Code"] = ""
			cls = SubElement(et,"Class",attrib)
			for elem in sorted(self._elements.iterkeys()):
				if self._elements[elem] == None:
					continue
				cls = self._elements[elem]._write(cls)
			return et
			
			
		def _fill_offsets2(self,last,hidepad):
			gap_count = 0
			i = 0
			while i <= last:
				if i not in self._elements:
					gap_count += 1
					i += 1
				else:
					if gap_count > 0:
						pad = Custom(name="_PAD_CUSTOM",size=gap_count)
						pad._bHidden = hidepad
						self[i-gap_count] = pad
						gap_count = 0
					i = i + self._elements[i]._size
					

					
		def _fill_offsets(self,last,hidepad):
			gap_count = 0
			i = 0
			while i <= last:
				if i not in self._elements:
					gap_count += 1
					if gap_count == 8:
						pad = Hex64(name="_PAD8")
						pad._bHidden = hidepad
						self[i-7] = pad
						gap_count = 0
					i += 1
				else:
					if gap_count == 7:
						pad = Hex32(name="_PAD4")
						pad._bHidden = hidepad
						self[i-7] = pad
						pad = Hex16(name="_PAD2")
						pad._bHidden = hidepad
						self[i-3] = pad
						pad = Hex8(name="_PAD1")
						pad._bHidden = hidepad
						self[i-1] = pad				
					if gap_count == 6:
						Hex32(name="_PAD4")
						pad._bHidden = hidepad
						self[i-6] = pad
						Hex16(name="_PAD2")
						pad._bHidden = hidepad						
						self[i-2] = pad
					if gap_count == 5:
						pad = Hex32(name="_PAD4")
						pad._bHidden = hidepad
						self[i-5] = pad
						pad = Hex8(name="_PAD1")
						pad._bHidden = hidepad
						self[i-1] = pad
					if gap_count == 4:
						pad = Hex32(name="_PAD4")
						pad._bHidden = hidepad
						self[i-4] = pad
					if gap_count == 3:
						pad = Hex16(name="_PAD2")
						pad._bHidden = hidepad
						self[i-3] = pad
						pad = Hex8(name="_PAD1")
						pad._bHidden = hidepad
						self[i-1] = pad
					if gap_count == 2:
						pad = Hex16(name="_PAD2")
						pad._bHidden = hidepad
						self[i-2] = pad
					if gap_count == 1:
						pad = Hex8(name="_PAD1")
						pad._bHidden = hidepad
						self[i-1] = pad
					if gap_count == 0:
						pass
					i = i + self._elements[i]._size
					gap_count = 0

class Map():
	def __init__(self,file):
		self._file = file
		self._classes = []
		self._classnames = []
		self._classes_dict = {}

	def add_class(self,cls):
		self._classes += [cls]
		self._classes_dict[cls._name] = cls
		self._classnames += [cls._name]
		
	def Class(self,name,offset=0,size=0,comment=""):
		cls = Class(name,offset,size,comment)
		self.add_class(cls)
		return cls
		
	def _fix_pointers(self):
		emptyclasses = []
		for cls in self._classes:
			for node in cls._elements:
				node = cls._elements[node]
				if ((node._type == NodeType.nt_pointer[0]) | (node._type == NodeType.nt_instance[0]) | (node._type == NodeType.nt_array[0])):
					if (node._classname not in self._classnames):
						node._comment = "Empty Class"
						print "Warn: Can't find class %s for pointer reference, adding later..." % (node._classname)
						c = Class(name=node._classname,comment="I'm an empty class, please define me",empty=True)
						c[0x0] = Hex64(name="")
						emptyclasses += [c]
						self._classnames += [c._name]
						self._classes_dict[c._name] = c
					else:
						if (self._classes_dict[node._classname]._empty):
							node._comment = "Empty Class"

		if len(emptyclasses) > 0:
			for cls in emptyclasses:
				self.add_class(cls)
				print "Warn: Creating empty class %s" % cls._name
						
						
	def write(self,hidepad=0,custompad=0):
		print "Info: Processing ReClass map..."
		print "Info: Fixing dangling class pointers..."
		self._fix_pointers()
		et = Element("ReClass")
		et.append(Comment("Reclass 2016")) # We Support Reclass 2016 datatypes
		TD = {}
		TD["tdHex"] = "char"
		TD["tdInt64"] = "__int64"
		TD["tdInt32"] = "__int32"
		TD["tdInt16"] = "__int16"
		TD["tdInt8"] = "__int8"
		TD["tdDWORD64"] = "DWORD64"
		TD["tdDWORD"] = "DWORD"
		TD["tdWORD"] = "WORD"
		TD["tdBYTE"] = "unsigned char" 
		TD["tdFloat"] = "float"
		TD["tdDouble"] = "double"
		TD["tdVec2"] = "Vector2"
		TD["tdVec3"] = "Vector3"
		TD["tdQuat"] = "Vector4"
		TD["tdMatrix"] = "matrix3x4_t"
		TD["tdPChar"] = "char *"
		TD["tdPWChar"] = "wchar_t *"		
		TypeDef = SubElement(et,"TypeDef",TD)
		Header = SubElement(et,"Header",{"Text":""})
		Footer = SubElement(et,"Footer",{"Text":""})
		Notes = SubElement(et,"Notes",{"Text":""})
		for cls in self._classes:
			et = cls._write(et,hidepad,custompad)
		output = tostring(et,'utf-8')
		reparse = minidom.parseString(output)
		f = open(self._file,"w")
		print "Info: Generating .reclass file at: %s" % self._file
		f.write(reparse.toprettyxml(indent="    "))
		f.close()
		print "Info: Done!"
