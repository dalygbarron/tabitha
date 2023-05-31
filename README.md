# Tabitha
![alt text](Saint_Tabitha.jpg "Saint Tabitha - image couresy of https://commons.wikimedia.org/wiki/User:Wolfymoza under CC-SA 4")

A blender spritesheet renderer that works from the commandline and leaves as
much configuration as possible in their usual places inside blender.

Essentially all this script does is operates on a blender file rendering
whatever animation you have configured inside that scene, then appends all of
the frames into a single image file. It can either operate on a single scene
within the file, or it can operate on all of them. The final outputs are named
after the scenes that they are renders of.

## Examples
You wanna render all scenes in the file to the current directory:

```blender -b file.blend --python tabitha.py```

You wanna render all scenes to a different folder:

```blender -b file.blend --python tabitha.py -- -o out_folder```

You wanna render a specific scene to a specific folder:

```blender -b file.blend --python tabitha.py -- -o out_folder -s scene```

Yeah that's basically it, you can run `tabitha.py --help` to see documentation
for each argument.