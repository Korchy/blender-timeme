# Nikita Akimov
# interplanety@interplanety.org

import bpy


class TimeMe_panel(bpy.types.Panel):
    bl_idname = 'timeme.panel'
    bl_label = 'TimeMe'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        # self.layout.operator('uv_int.separate_meshloops', icon = 'UNLINKED', text = 'Blast')
        # self.layout.operator('uv_int.separate_meshloops_by_edge', icon = 'UNLINKED', text = 'Seam by edge')
        # self.layout.operator('uv_int.weld_meshloops', icon = 'LINKED', text = 'Weld')
        pass


def register():
    bpy.utils.register_class(TimeMe_panel)


def unregister():
    bpy.utils.unregister_class(TimeMe_panel)
