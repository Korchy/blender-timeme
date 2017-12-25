# Nikita Akimov
# interplanety@interplanety.org

bl_info = {
    'name': 'TimeMe',
    'category': 'System',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 79, 0),
    'location': '',
    'wiki_url': '',
    'tracker_url': '',
    'description': 'TimeMe - add-on to manage the project time'
}

from . import timeme
from . import timeme_panel
import bpy
from bpy.app.handlers import persistent

@persistent
def onsceneupdatepost(scene):
    print('init on scene update')
    bpy.app.handlers.scene_update_post.remove(onsceneupdatepost)
    # if not hasattr(bpy.ops, 'timeme'):
    # if not hasattr(bpy.types, bpy.ops.timeme.start.idname()):
    bpy.ops.timeme.start()
    # bpy.ops.timeme.start('INVOKE_DEFAULT')

# @persistent
# def onsceneload_post(scene):
#     timeme.TimeMe.start()
#     # print('on scene load')
#     # bpy.ops.timeme.start()
#     # bpy.ops.timeme.start('INVOKE_DEFAULT')
#
# @persistent
# def onsceneload_pre(scene):
#     timeme.TimeMe.stop()


def register():
    timeme.register()
    timeme_panel.register()
    if onsceneupdatepost not in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.append(onsceneupdatepost)
    # if onsceneload_pre not in bpy.app.handlers.load_pre:
    #     bpy.app.handlers.load_pre.append(onsceneload_pre)
    # if onsceneload_post not in bpy.app.handlers.load_post:
    #     bpy.app.handlers.load_post.append(onsceneload_post)


def unregister():
    if onsceneupdatepost in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.remove(onsceneupdatepost)
    timeme.unregister()
    timeme_panel.unregister()


if __name__ == "__main__":
    register()
