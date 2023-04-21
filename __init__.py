bl_info = {
    "name" : "VyCam",
    "blender" : (3,4,1),
    "version" : (4,15,23),
    "category" : "3D View",
    "author" : "Kent Edoloverio",
    "location" : "3D View > VyCam",
    "description" : "Allows you to add camera and change aspect ratios and focal lengths with a single click",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
}

import bpy
# Third party
from . import addon_updater_ops

from bpy.props import EnumProperty,StringProperty
from bpy.types import Panel,Operator,PropertyGroup

class POVCamera:
    def __init__(self):
        self.camera_data = bpy.data.cameras.new(name="Camera")
        self.camera_object = bpy.data.objects.new(name="Camera", object_data=self.camera_data)
        bpy.context.scene.collection.objects.link(self.camera_object)

    def set_active_camera(self):
        bpy.context.scene.camera = self.camera_object

    def set_camera_to_point_of_view(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region, 'edit_object': self.camera_object}
                        bpy.ops.view3d.camera_to_view(override)
        return {'FINISHED'}

class Vycam_pg(PropertyGroup):
    screen_presets: EnumProperty(
        name = "",
        description = "Camera resolution presets",
        items = [
            ("R1", "640 x 480 - SD",""),
            ("R2", "1280 x 720 - HD",""),
            ("R3", "1920 x 1080 - Full HD",""),
            ("R4", "2560 x 1440 - Quad HD",""),
            ("R5", "3840 x 2160 - 4K UHD",""),
            ("R6", "7680 x 4320 - 8K UHD",""),
            ("R7", "1200 x 1800 - 6 x 4 Inches",""),
            ("R8", "1500 x 2100 - 5 x 7 Inches",""),
            ("R9", "2400 x 3000 - 10 x 8 Inches",""),
            ("R10", "3400 x 4400 - 8.5 x 11 Inches",""),
            ("R11", "3600 x 5400 - 12 x 18 Inches",""),
            ("R12", "1080 x 1080 - Instagram Post",""),
            ("R13", "1200 x 630 - Facebook Post",""),
            ("R14", "1080 x 1920 - Insta/Facebook Story",""),
            ("R15", "1600 x 900 - Twitter Post",""),
        ]
    )
    focal_length_presets: EnumProperty(
        name = "",
        description = "Camera focal length presets",
        items = [
        ("F1", "4mm+ - Fisheye", "Used for abstract and creative"),
        ("F2", "14mm+ - Wide angle", "Used for landscape and architecture"),
        ("F3", "35mm+ - Standard", "Used for street, travel and portrait"),
        ("F4", "85mm+ - Short telephoto", "Used for street photography and portraits"),
        ("F5", "135mm+ - Medium telephoto", "Used for sports, wildlife and  action"),
        ("F6", "200mm+ - Macro", "Used for closed up shots"),
        ("F7", "300mm+ - Super telephoto", "Used for sports from a distance, nature and astronomy"),
        ("F8", "Custom",""),
        ]
    )
    custom_width : StringProperty (
        name = "",
        description = "Custom Width",
        default = "500",
    )
    custom_height : StringProperty (
        name = "",
        description = "Custom Height",
        default = "500",
    )
    custom_focal_length : StringProperty (
        name = "",
        description = "Custom Focal Length",
        default = "50",
    )

class Vycam_op_Camera(Operator):
    bl_label = "ADD CAMERA"
    bl_idname = "vycam.op_camera"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        camera_manager = POVCamera()
        camera_manager.set_active_camera()
        camera_manager.set_camera_to_point_of_view()
        return {'FINISHED'}

class Vycam_op(Operator):
    bl_label = "REFRESH"
    bl_idname = "vycam.op_presets"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        custom_scene_property = scene.presets

        if custom_scene_property.focal_length_presets == "F1":
            bpy.context.object.data.lens = 4
        elif custom_scene_property.focal_length_presets == "F2":
            bpy.context.object.data.lens = 14
        elif custom_scene_property.focal_length_presets == "F3":
            bpy.context.object.data.lens = 35
        elif custom_scene_property.focal_length_presets == "F4":
            bpy.context.object.data.lens = 85
        elif custom_scene_property.focal_length_presets == "F5":
            bpy.context.object.data.lens = 135
        elif custom_scene_property.focal_length_presets == "F6":
            bpy.context.object.data.lens = 200
        elif custom_scene_property.focal_length_presets == "F7":
            bpy.context.object.data.lens = 300
        elif custom_scene_property.focal_length_presets == "F8":
            bpy.context.object.data.lens = int(custom_scene_property.custom_focal_length)


        if custom_scene_property.screen_presets == "R1":
            bpy.context.scene.render.resolution_x = 640
            bpy.context.scene.render.resolution_y = 480
        elif custom_scene_property.screen_presets == "R2":
            bpy.context.scene.render.resolution_x = 1280
            bpy.context.scene.render.resolution_y = 720
        elif custom_scene_property.screen_presets == "R3":
            bpy.context.scene.render.resolution_x = 1920
            bpy.context.scene.render.resolution_y = 1080
        elif custom_scene_property.screen_presets == "R4":
            bpy.context.scene.render.resolution_x = 2560
            bpy.context.scene.render.resolution_y = 1440
        elif custom_scene_property.screen_presets == "R5":
            bpy.context.scene.render.resolution_x = 3840
            bpy.context.scene.render.resolution_y = 2160
        elif custom_scene_property.screen_presets == "R6":
            bpy.context.scene.render.resolution_x = 7680
            bpy.context.scene.render.resolution_y = 4320
        elif custom_scene_property.screen_presets == "R7":
            bpy.context.scene.render.resolution_x = 1200
            bpy.context.scene.render.resolution_y = 1800
        elif custom_scene_property.screen_presets == "R8":
            bpy.context.scene.render.resolution_x = 1500
            bpy.context.scene.render.resolution_y = 2100
        elif custom_scene_property.screen_presets == "R9":
            bpy.context.scene.render.resolution_x = 2400
            bpy.context.scene.render.resolution_y = 3000
        elif custom_scene_property.screen_presets == "R10":
            bpy.context.scene.render.resolution_x = 3400
            bpy.context.scene.render.resolution_y = 4400
        elif custom_scene_property.screen_presets == "R11":
            bpy.context.scene.render.resolution_x = 3600
            bpy.context.scene.render.resolution_y = 5400
        elif custom_scene_property.screen_presets == "R12":
            bpy.context.scene.render.resolution_x = 1080
            bpy.context.scene.render.resolution_y = 1080
        elif custom_scene_property.screen_presets == "R13":
            bpy.context.scene.render.resolution_x = 1200
            bpy.context.scene.render.resolution_y = 630
        elif custom_scene_property.screen_presets == "R14":
            bpy.context.scene.render.resolution_x = 1080
            bpy.context.scene.render.resolution_y = 1920
        elif custom_scene_property.screen_presets == "R15":
            bpy.context.scene.render.resolution_x = 1600
            bpy.context.scene.render.resolution_y = 900
        return {'FINISHED'}



class Vycam_pl(Panel):
    bl_label = "VyCam"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'TOOLS' if bpy.app.version < (2, 80) else 'UI'
    bl_category = "VyCam"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):
        layout = self.layout
        custom_pg = context.scene.presets

        col = layout.row(align=False)
        col.enabled = True
        col.scale_x = 2.0
        col.scale_y = 2.0
        col.operator("vycam.op_camera", icon="OUTLINER_OB_CAMERA")

        col = layout.row(align=False)
        col.enabled = True
        col.scale_x = 1.2
        col.scale_y = 1.2
        col.operator("vycam.op_presets", icon="FILE_REFRESH")

        col = layout.column(align=False)
        col.enabled = True
        col.scale_x = 1.0
        col.scale_y = 1.0
        col.label(text=r"Resolution Presets:",icon_value=0)
        col.prop(custom_pg, "screen_presets")
        col = layout.column(align=False)
        col.enabled = True
        col.scale_x = 1.0
        col.scale_y = 1.0
        col.label(text=r"Focal Length Presets:",icon_value=0)
        col.prop(custom_pg, "focal_length_presets")

        if custom_pg.focal_length_presets == "F8":
            box = layout.box()
            col = box.row(align=False)
            col.label(text="Focal Length")
            col.prop(custom_pg, "custom_focal_length")

        col = layout.column(align=False)
        col.label(text=r"SUPPORT ME ON:")
        op = self.layout.operator(
            'wm.url_open',
            text='KO-FI',
            icon='URL'
            )
        op.url = 'https://ko-fi.com/kents_workof_art'

        col = layout.column(align=False)
        addon_updater_ops.check_for_update_background()
        if addon_updater_ops.updater.update_ready:
            col.label(text="VyCam Successfuly Update", icon="INFO")
        addon_updater_ops.update_notice_box_ui(self, context)

@addon_updater_ops.make_annotations
class VycamPreferences(bpy.types.AddonPreferences):
	"""Demo bare-bones preferences"""
	bl_idname = __package__

	# Addon updater preferences.

	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

	updater_interval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

	updater_interval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)

	updater_interval_hours = bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

	updater_interval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)

	def draw(self, context):
		layout = self.layout

		# Works best if a column, or even just self.layout.
		mainrow = layout.row()
		col = mainrow.column()

		# Updater draw function, could also pass in col as third arg.
		addon_updater_ops.update_settings_ui(self, context)

		# Alternate draw function, which is more condensed and can be
		# placed within an existing draw function. Only contains:
		#   1) check for update/update now buttons
		#   2) toggle for auto-check (interval will be equal to what is set above)
		# addon_updater_ops.update_settings_ui_condensed(self, context, col)

		# Adding another column to help show the above condensed ui as one column
		# col = mainrow.column()
		# col.scale_y = 2
		# ops = col.operator("wm.url_open","Open webpage ")
		# ops.url=addon_updater_ops.updater.website


classes = (
    Vycam_pg,
    Vycam_op_Camera,
    Vycam_op,
    Vycam_pl,
    VycamPreferences,
)

def register():
    addon_updater_ops.register(bl_info)

    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.presets = bpy.props.PointerProperty(type= Vycam_pg)


def unregister():
    addon_updater_ops.unregister()

    for cls in classes:
        bpy.utils.unregister(cls)
        del bpy.types.Scene.presets

if __name__=="__main__":
    register()