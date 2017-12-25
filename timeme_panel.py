# Nikita Akimov
# interplanety@interplanety.org

import bpy


class TimeMeCatsList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "catname", '')
        layout.prop(item, "cattime", '')
        layout.prop(item, "cattime_str", '')


class TimeMe_panel(bpy.types.Panel):
    bl_idname = 'timeme.panel'
    bl_label = 'TimeMe'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        if hasattr(bpy.context.scene, 'timeMeVars'):
            self.layout.template_list('TimeMeCatsList', 'Time Categories', bpy.context.scene.timeMeVars, 'cats', bpy.context.scene.timeMeVars, 'activecat', type='DEFAULT')
            self.layout.operator('timeme.print', icon = 'LINKED', text = 'Print')
        pass


def register():
    bpy.utils.register_class(TimeMe_panel)
    bpy.utils.register_class(TimeMeCatsList)


def unregister():
    bpy.utils.unregister_class(TimeMe_panel)
    bpy.utils.unregister_class(TimeMeCatsList)
