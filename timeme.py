# Nikita Akimov
# interplanety@interplanety.org

import bpy
import sys


class TimeMe(bpy.types.Operator):
    bl_idname = 'timeme.start'
    bl_label = 'TimeMe: Start'
    bl_description = 'Start monitor my time'

    cats = {}

    def modal(self, context, event):
        if event.type in self.cats:
            self.cats[event.type] += 1
        else:
            self.cats[event.type] = 1
            newitem = bpy.context.scene.timeMeVars1.cats.add()
            print(newitem.catname)
            newitem.catname = event.type
            # print('add ',event.type)
        return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    @staticmethod
    def getCats(self, context):
        itemlist = []
        for i, key in enumerate(TimeMe.cats.keys()):
            itemlist.append((key, key, '', TimeMe.cats[key]))
        return itemlist


class TimeMePrint(bpy.types.Operator):
    bl_idname = 'timeme.print'
    bl_label = 'TimeMe: Print'

    def execute(self, context):
        print(TimeMe.cats)
        print('---')
        for item in bpy.context.scene.timeMeVars1.cats:
            print(item.catname, item.cattime)
        return {'FINISHED'}


class TimeMeVars(bpy.types.PropertyGroup):
    cats = bpy.props.EnumProperty(
        items = lambda self, context: TimeMe.getCats(self, context)
    )


def setCatsItemName(self, value):
    self['catname'] = value


class TimeMeCatsItem(bpy.types.PropertyGroup):
    catname = bpy.props.StringProperty(
        name="catname",
        default="",
        # set=lambda self, context, value: TimeMe.setCatsItemName(self, context, value)
        set=setCatsItemName
    )
    cattime = bpy.props.StringProperty(name="cattime", default="")


class TimeMeVars1(bpy.types.PropertyGroup):
    # cats = bpy.props.CollectionProperty(type=TimeMeVars, name='cats')
    cats = bpy.props.CollectionProperty(type=TimeMeCatsItem, name='cats')
    activecat = bpy.props.IntProperty(name='activecat', default=-1)


def register():
    bpy.utils.register_class(TimeMe)
    bpy.utils.register_class(TimeMePrint)
    bpy.utils.register_class(TimeMeCatsItem)
    bpy.utils.register_class(TimeMeVars)
    bpy.utils.register_class(TimeMeVars1)
    bpy.types.Scene.timeMeVars = bpy.props.PointerProperty(type=TimeMeVars)
    bpy.types.Scene.timeMeVars1 = bpy.props.PointerProperty(type=TimeMeVars1)


def unregister():
    del bpy.types.Scene.timeMeVars
    del bpy.types.Scene.timeMeVars1
    bpy.utils.unregister_class(TimeMe)
    bpy.utils.unregister_class(TimeMePrint)
    bpy.utils.unregister_class(TimeMeCatsItem)
    bpy.utils.unregister_class(TimeMeVars)
    bpy.utils.unregister_class(TimeMeVars1)
