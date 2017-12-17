# Nikita Akimov
# interplanety@interplanety.org

import bpy


class TimeMe(bpy.types.Operator):
    bl_idname = 'timeme.start'
    bl_label = 'TimeMe: Start'
    bl_description = 'Start monitor my time'

    def modal(self, context, event):
        print('modal')
        print(event.type)
        # return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        print('invoke')
        # if context.object:
        # context.window_manager.modal_handler_add(self)
        # return {'RUNNING_MODAL'}
        # return {'PASS_THROUGH'}

    def execute(self, context):
        print('execute')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(TimeMe)


def unregister():
    bpy.utils.unregister_class(TimeMe)
