"""
Tabitha sprite sheet renderer for Blender
Copyright 2023 Daly Graham Barron
Licensed under GPL 2
"""

import bpy, math, tempfile, argparse, sys

def blit(src, dst, x, y):
    """Draws one picture onto another at a given location, doesn't concern
    itself with things like you make the picture go over the edge or
    transparancy. It always assumes 4 channels and that you have not set it to
    draw over an edge which would cause crazy stuff. The edge thing really
    doesn't matter but I might want to deal with the channel question at some
    point in future."""
    for iy in range(src.size[1]):
        write_index = (x + (y + iy) * dst.size[0]) * 4
        read_index = iy * src.size[0] * 4
        dst.pixels[write_index:write_index + src.size[0] * 4] = \
            src.pixels[read_index:read_index + src.size[0] * 4]

def render_scene(scene, temp_dir, out_dir):
    """Takes the given scene and renders all it's animation frames and appends
    them into a file. Temporary renderings of frames are stored in temp_dir
    which should be a string path to a folder."""
    bpy.context.window.scene = scene
    n_frames = scene.frame_end - scene.frame_start + 1
    columns = math.ceil(math.sqrt(n_frames))
    sheet = bpy.data.images.new(
        scene.name, 
        bpy.context.scene.render.resolution_x * columns,
        bpy.context.scene.render.resolution_y * math.ceil(n_frames / columns),
        alpha=True
    )
    sheet.pixels[:] = [0] * len(sheet.pixels)
    for i in range(n_frames):
        path = '%s/%s_%d.png' % (temp_dir, scene.name, i)
        bpy.context.scene.render.filepath = path
        bpy.context.scene.frame_current = i + scene.frame_start
        bpy.ops.render.render(write_still=True)
        image = bpy.data.images.load(path)
        blit(
            image,
            sheet,
            bpy.context.scene.render.resolution_x * (i % columns),
            sheet.size[1] - bpy.context.scene.render.resolution_y * \
                (math.floor(i / columns) + 1)
        )
    sheet.save(filepath=('%s/%s.png' % (out_dir, scene.name)))

def main():
    """Entry point. Parses arguments and does very high level directing of
    functionality based on them."""
    parser = argparse.ArgumentParser(
        prog='Tabitha',
        description='Blender Spritesheet renderer'
    )
    parser.add_argument(
        '-o',
        '--out-dir',
        default='.',
        help='The directory where rendered spritesheets will be saved. ' + \
            'Defaults to current dir.'
    )
    parser.add_argument(
        '-s',
        '--scene',
        help='If you only want to render one scene name it with this.'
    )
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    out_dir = args.out_dir
    temp_folder = tempfile.TemporaryDirectory(prefix='tabitha', dir='.')
    for scene in bpy.data.scenes:
        if not args.scene or args.scene == scene.name:
            render_scene(scene, temp_folder.name, out_dir)

if __name__ == '__main__':
    main()
