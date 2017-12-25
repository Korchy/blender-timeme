# Nikita Akimov
# interplanety@interplanety.org

import bpy
import datetime
from . import datetimeex
from bpy.app.handlers import persistent


class TimeMe(bpy.types.Operator):
    bl_idname = 'timeme.start'
    bl_label = 'TimeMe: Start'
    bl_description = 'Start monitor my time'

    status = None
    eventslist = []
    time = datetime.datetime.now()
    check_interval = 1 # sec 60

    def modal(self, context, event):
        if self.status:
            if event.type not in self.eventslist:
                self.eventslist.append(event.type)

            # if event.type == 'Q':
            #     self.cancel(context)

            if datetime.datetime.now() - datetime.timedelta(seconds=self.check_interval) > self.time:
                # whole time
                catitem = __class__.getcat('ALL TIME')
                catitem.cattime += (datetime.datetime.now() - self.time).total_seconds()
                catitem.cattime_str = datetimeex.DateTimeEx.deltatimetostr(catitem.cattime)
                # work time
                is_work = False
                for event in self.eventslist:
                    if event not in ['NONE', 'WINDOW_DEACTIVATE', 'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'] and event[:5] not in ['TIMER', 'NDOF_']:
                        is_work = True
                if is_work:
                    catitem = __class__.getcat('WORK TIME')
                    catitem.cattime += self.check_interval
                    catitem.cattime_str = datetimeex.DateTimeEx.deltatimetostr(catitem.cattime)
                # reset
                self.time = datetime.datetime.now()
                del self.eventslist[:]
            for area in bpy.context.screen.areas:
                area.tag_redraw()

            return {'PASS_THROUGH'}
        else:
            return {'FINISHED'}

    def execute(self, context):
        print('timeme execute')
        if self.status:
            return {'FINISHED'}
    # def invoke(self, context, event):
        # __class__.clear()
        # if self not in context.window_manager:
        if self not in bpy.context.window_manager.items():
            context.window_manager.modal_handler_add(self)
        # print(hasattr(context.window_manager,'TimeMe'))
        # if self in context.window_manager.operators:
        #     print('a')
        # print(bpy.context.window_manager.items())
        # self.status = 'RUNNING'
        __class__.start()
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        print('timeme cancel')
        __class__.stop()
        # __class__.clear()
        # self.status = None
        # return {'CANCELLED'}
        return None

    # @classmethod
    # def geteventslist(cls):
    #     print(__class__.eventslist)
    #     return cls.eventslist

    # @staticmethod
    # def getCats(self, context):
    #     itemlist = []
    #     for i, key in enumerate(TimeMe.cats.keys()):
    #         itemlist.append((key, key, '', TimeMe.cats[key]))
    #     return itemlist

    # @staticmethod
    @classmethod
    def clear(cls):
        bpy.context.scene.timeMeVars.cats.clear()

    @classmethod
    def start(cls):
        if not cls.status:
            bpy.types.Scene.timeMeVars = bpy.props.PointerProperty(type=TimeMeVars)
            cls.status = 'RUNNING'

    @classmethod
    def stop(cls):
        cls.status = None
        if hasattr(bpy.types.Scene, 'timeMeVars'):
            del bpy.types.Scene.timeMeVars

    @staticmethod
    def getcat(catname):
        for cat in bpy.context.scene.timeMeVars.cats:
            if cat.catname == catname:
                return cat
        newcat = bpy.context.scene.timeMeVars.cats.add()
        newcat.catname = catname
        newcat.cattime = datetime.timedelta().total_seconds()
        newcat.cattime_str = datetimeex.DateTimeEx.deltatimetostr(newcat.cattime)
        return newcat


# class TimeMeStatic(bpy.types.PropertyGroup):
#     status = bpy.props.StringProperty(name='TimeMe Status',default='None')


class TimeMePrint(bpy.types.Operator):
    bl_idname = 'timeme.print'
    bl_label = 'TimeMe: Print'

    def execute(self, context):
        print(TimeMe.eventslist)
        # print(TimeMe.geteventslist())
        # print(TimeMe.cats)
        # print('---')
        # for item in bpy.context.scene.timeMeVars.cats:
        #     print(item.catname, item.cattime)
        return {'FINISHED'}


class TimeMeCatsItem(bpy.types.PropertyGroup):
    catname = bpy.props.StringProperty(name='catname', default='')
    cattime = bpy.props.FloatProperty(name="cattime")
    cattime_str = bpy.props.StringProperty(name="cattime")


class TimeMeVars(bpy.types.PropertyGroup):
    cats = bpy.props.CollectionProperty(type=TimeMeCatsItem, name='cats')
    activecat = bpy.props.IntProperty(name='activecat', default=-1)


@persistent
def onsceneload_post(scene):
    print('timeme scene load post')
    # bpy.types.Scene.timeMeVars = bpy.props.PointerProperty(type=TimeMeVars)
    # TimeMe.start()
    # if not hasattr(bpy.ops, 'timeme'):
    bpy.ops.timeme.start()

@persistent
def onsceneload_pre(scene):
    print('timeme scene load pre')
    TimeMe.stop()
    # del bpy.types.Scene.timeMeVars


def register():
    print('timeme register')
    bpy.utils.register_class(TimeMe)
    bpy.utils.register_class(TimeMePrint)
    bpy.utils.register_class(TimeMeCatsItem)
    bpy.utils.register_class(TimeMeVars)
    if onsceneload_pre not in bpy.app.handlers.load_pre:
        bpy.app.handlers.load_pre.append(onsceneload_pre)
    if onsceneload_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(onsceneload_post)


def unregister():
    print('timeme un register')
    TimeMe.stop()
    if onsceneload_pre in bpy.app.handlers.load_pre:
        bpy.app.handlers.load_pre.remove(onsceneload_pre)
    if onsceneload_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(onsceneload_post)
    bpy.utils.unregister_class(TimeMe)
    bpy.utils.unregister_class(TimeMePrint)
    bpy.utils.unregister_class(TimeMeCatsItem)
    bpy.utils.unregister_class(TimeMeVars)
