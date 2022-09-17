# recursive_3d
Blender python script


## To execute script in Blender: 

```
filename = "FULL PARTH to tri_mesh.py"
exec(compile(open(filename).read(), filename, 'exec'))
```


```
import bpy
import os

filename = os.path.join(os.path.dirname(bpy.data.filepath), "myscript.py")
exec(compile(open(filename).read(), filename, 'exec'))
```