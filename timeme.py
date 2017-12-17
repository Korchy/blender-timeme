# Nikita Akimov
# interplanety@interplanety.org

import bpy


class TimeMe(bpy.types.Operator):
    bl_idname = 'timeme.start'
    bl_label = 'TimeMe: Start'
    bl_description = 'Start monitor my time'

    def modal(self, context, event):
        print event.type
        return {'FINISHED'}


def register():
    bpy.utils.register_class(TimeMe)


def unregister():
    bpy.utils.unregister_class(TimeMe)
