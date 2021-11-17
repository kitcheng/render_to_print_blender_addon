# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import math
import bpy
from bpy.types import Panel, Operator, Scene, PropertyGroup
from bpy.props import (IntProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       PointerProperty,
                       BoolProperty
                       )

bl_info = {
    'name': 'Render to Print to Scale',
    'author': 'Marco Crippa <thekrypt77@tiscali.it>, Dealga McArdle, J.R.B.-Wein <radagast@ardaron.de>, Zheng Bo<zhengbo1978@gmail.com>',
    'version': (1, 0, 8),
    'blender': (2, 90, 0),
    'location': 'View_3D > UI > Print',
    'description': 'Set the size of the render for a print',
    'category': 'Generic'
}

LAYERS_ALL = (
        True, True, True, True, True,
        True, True, True, True, True,
        True, True, True, True, True,
        True, True, True, True, True
        )

paper_presets = (
    ("A5_14.8_21.0", "default (A5)", ""),
    ("custom_1_1", "custom", ""),
    ("A0_84.1_118.9", "A0 (84.1x118.9 cm)", ""),
    ("A1_59.4_84.1", "A1 (59.4x84.1 cm)", ""),
    ("A2_42.0_59.4", "A2 (42.0x59.4 cm)", ""),
    ("A3_29.7_42.0", "A3 (29.7 42.0 cm)", ""),
    ("A4_21.0_29.7", "A4 (21.0x29.7 cm)", ""),
    ("A5_14.8_21.0", "A5 (14.8x21.0 cm)", ""),
    ("A6_10.5_14.8", "A6 (10.5x14.8 cm)", ""),
    ("A7_7.4_10.5", "A7 (7.4x10.5 cm)", ""),
    ("A8_5.2_7.4", "A8 (5.2x7.4 cm)", ""),
    ("A9_3.7_5.2", "A9 (3.7x5.2 cm)", ""),
    ("A10_2.6_3.7", "A10 (2.6x3.7 cm)", ""),

    ("B0_100.0_141.4", "B0 (100.0x141.4 cm)", ""),
    ("B1_70.7_100.0", "B1 (70.7x100.0 cm)", ""),
    ("B2_50.0_70.7", "B2 (50.0x70.7 cm)", ""),
    ("B3_35.3_50.0", "B3 (35.3x50.0 cm)", ""),
    ("B4_25.0_35.3", "B4 (25.0x35.3 cm)", ""),
    ("B5_17.6_25.0", "B5 (17.6x25.0 cm)", ""),
    ("B6_12.5_17.6", "B6 (12.5x17.6 cm)", ""),
    ("B7_8.8_12.5", "B7 (8.8x12.5 cm)", ""),
    ("B8_6.2_8.8", "B8 (6.2x8.8 cm)", ""),
    ("B9_4.4_6.2", "B9 (4.4x6.2 cm)", ""),
    ("B10_3.1_4.4", "B10 (3.1x4.4 cm)", ""),

    ("C0_91.7_129.7", "C0 (91.7x129.7 cm)", ""),
    ("C1_64.8_91.7", "C1 (64.8x91.7 cm)", ""),
    ("C2_45.8_64.8", "C2 (45.8x64.8 cm)", ""),
    ("C3_32.4_45.8", "C3 (32.4x45.8 cm)", ""),
    ("C4_22.9_32.4", "C4 (22.9x32.4 cm)", ""),
    ("C5_16.2_22.9", "C5 (16.2x22.9 cm)", ""),
    ("C6_11.4_16.2", "C6 (11.4x16.2 cm)", ""),
    ("C7_8.1_11.4", "C7 (8.1x11.4 cm)", ""),
    ("C8_5.7_8.1", "C8 (5.7x8.1 cm)", ""),
    ("C9_4.0_5.7", "C9 (4.0x5.7 cm)", ""),
    ("C10_2.8_4.0", "C10 (2.8x4.0 cm)", ""),

    ("Letter_21.6_27.9", "Letter (21.6x27.9 cm)", ""),
    ("Legal_21.6_35.6", "Legal (21.6x35.6 cm)", ""),
    ("Legal junior_20.3_12.7", "Legal junior (20.3x12.7 cm)", ""),
    ("Ledger_43.2_27.9", "Ledger (43.2x27.9 cm)", ""),
    ("Tabloid_27.9_43.2", "Tabloid (27.9x43.2 cm)", ""),

    ("ANSI C_43.2_55.9", "ANSI C (43.2x55.9 cm)", ""),
    ("ANSI D_55.9_86.4", "ANSI D (55.9x86.4 cm)", ""),
    ("ANSI E_86.4_111.8", "ANSI E (86.4x111.8 cm)", ""),

    ("Arch A_22.9_30.5", "Arch A (22.9x30.5 cm)", ""),
    ("Arch B_30.5_45.7", "Arch B (30.5x45.7 cm)", ""),
    ("Arch C_45.7_61.0", "Arch C (45.7x61.0 cm)", ""),
    ("Arch D_61.0_91.4", "Arch D (61.0x91.4 cm)", ""),
    ("Arch E_91.4_121.9", "Arch E (91.4x121.9 cm)", ""),
    ("Arch E1_76.2_106.7", "Arch E1 (76.2x106.7 cm)", ""),
    ("Arch E2_66.0_96.5", "Arch E2 (66.0x96.5 cm)", ""),
    ("Arch E3_68.6_99.1", "Arch E3 (68.6x99.1 cm)", ""),
    )


def paper_enum_parse(idname):
    tipo, dim_w, dim_h = idname.split("_")
    return tipo, float(dim_w), float(dim_h)


paper_presets_data = {idname: paper_enum_parse(idname)
                      for idname, name, descr in paper_presets}


def update_settings_cb(self, context):
    # annoying workaround for recursive call
    if update_settings_cb.level == False:
        update_settings_cb.level = True
        ps = self
        rendersettings = context.scene.render
        render_x_m = pixels_to_printed_m(rendersettings.resolution_x, ps)
        render_y_m = pixels_to_printed_m(rendersettings.resolution_y, ps)
        pixels_from_print(context, ps)
        offset_camera(context)
        if ps.add_scale_ratio_text:
            height_max = ps.width_cm / m_TO_cm
            if ps.text_height > height_max:
                ps.text_height = height_max
            #elif ps.text_height < height_min:
            #    ps.text_height = height_min
        if ps.use_margins:
            # HORIZONTAL
            margin_left_m = rel_to_abs_m(ps.margin_left, render_x_m)
            margin_right_m = rel_to_abs_m(ps.margin_right, render_x_m)

            length_available = render_x_m - margin_right_m
            # May be considered a bug because it changes relative percentage to an absolute value (does no harm though).
            if margin_left_m > length_available:
                ps.margin_left = length_available

            length_available = render_x_m - margin_left_m
            # May be considered a bug because it changes relative percentage to an absolute value (does no harm though).
            if margin_right_m > length_available:
                ps.margin_right = length_available


            # VERTICAL
            margin_top_m = rel_to_abs_m(ps.margin_top, render_y_m)
            margin_bottom_m = rel_to_abs_m(ps.margin_bottom, render_y_m)

            length_available = render_y_m - margin_bottom_m
            # May be considered a bug because it changes relative percentage to an absolute value (does no harm though).
            if margin_top_m > length_available:
                ps.margin_top = length_available

            length_available = render_y_m - margin_top_m
            # May be considered a bug because it changes relative percentage to an absolute value (does no harm though).
            if margin_bottom_m > length_available:
                ps.margin_bottom = length_available

        if not ps.update_manually:
            bpy.ops.render.apply_print_settings()

        update_settings_cb.level = False

update_settings_cb.level = False



#
# First parameter 'rel_or_abs' may be either relative or absolute.
# If the value is already absolute then it itself is returned.
#
def rel_to_abs_m(rel_or_abs, ref_size):
    margin_m = rel_or_abs
    if rel_or_abs >= 1:
        # relative
        margin_m = ref_size * rel_or_abs / 100.0
    return margin_m



def rel_to_abs_m_vertical(context, rel_or_abs):
    ps = context.scene.print_settings
    ref_size = pixels_to_printed_m(context.scene.render.resolution_y, ps)
    return rel_to_abs_m(rel_or_abs, ref_size)



def rel_to_abs_m_horizontal(context, rel_or_abs):
    ps = context.scene.print_settings
    ref_size = pixels_to_printed_m(context.scene.render.resolution_x, ps)
    return rel_to_abs_m(rel_or_abs, ref_size)



def offset_camera(context):
    ps = context.scene.print_settings
    if not ps.use_margins:
        return # no offset required if no margins.
    camera = context.scene.camera
    if camera:

        margin_left_m = rel_to_abs_m(
                ps.margin_left,
                pixels_to_printed_m(context.scene.render.resolution_x, ps)
                )
        margin_right_m = rel_to_abs_m(
                ps.margin_right,
                pixels_to_printed_m(context.scene.render.resolution_x, ps)
                )
        camera.delta_location[0] = margin_left_m - margin_right_m

        margin_top_m = rel_to_abs_m(
                ps.margin_top,
                pixels_to_printed_m(context.scene.render.resolution_y, ps)
                )
        margin_bottom_m = rel_to_abs_m(
                ps.margin_bottom,
                pixels_to_printed_m(context.scene.render.resolution_y, ps)
                )
        camera.delta_location[1] = margin_bottom_m - margin_top_m



print2scale_scale_factor_previous = 1
def print2scale_recalculate_camera_focal_length_or_orthographic_scale(self, context):

    # annoying workaround for recursive call
    if print2scale_recalculate_camera_focal_length_or_orthographic_scale.level == False:
        print2scale_recalculate_camera_focal_length_or_orthographic_scale.level = True
        print2scale_processInput(self, context)
        if not self.update_manually:
            print2scale(self, context)
        print2scale_recalculate_camera_focal_length_or_orthographic_scale.level = False

print2scale_recalculate_camera_focal_length_or_orthographic_scale.level = False



def print2scale_processInput(self, context):
    global print2scale_scale_factor_previous

    ps = self

    if (print2scale_scale_factor_previous == ps.scale_factor):
        return {'FINISHED'}

    if (ps.scale_factor < 1):
        #ps.scale_factor = round(ps.scale_factor, 1)
        print2scale_scale_factor_previous = ps.scale_factor
        return {'FINISHED'}


    # If the scale factor is changed by an amount less than 1 it has to be either incremented or
    # decremented and NOT rounded as this will result in the old result.
    # This special case is treated for convenience only.
    if ps.scale_factor > print2scale_scale_factor_previous:
        #then round up:
        ps.scale_factor = math.ceil(ps.scale_factor)

    elif ps.scale_factor < print2scale_scale_factor_previous:
       ps.scale_factor = math.floor(ps.scale_factor)

    #else: equal! nothing to change!

    # Store the current value for next time:
    print2scale_scale_factor_previous = ps.scale_factor



def print2scale(ps, context):
    print2scale__calculate_camera_paramaters(ps, context)
    print2scale_add_update_text(ps, context)


def print2scale__calculate_camera_paramaters(ps, context):
    if (ps.print_to_scale):

        if (bpy.context.active_object != None and (bpy.context.active_object.type == 'OBJECT' or bpy.context.active_object.type == 'MESH')):
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            print('Switched to Object mode.')
        else:
            if (context.mode != 'OBJECT'):
                print('Warning: Switched not to Object mode but are in Edit mode.')


        find_or_create_camera_and_assign(context)
        #
        # At this point the scene must have a camera.
        #

        #######
        # SET THE CAMERA's ZOOM OR ORTHOGRAPHIC SCALE
        #######
        aspect_ratio = ps.height_cm / ps.width_cm #as it's a ratio converting to meter or not does not matter here!
        if (not context.scene.camera.type == 'CAMERA'):
            print("Camera does not have type 'CAMERA', instead: ", context.scene.camera.type)
            return {'CANCELLED'}


        longer_side = ps.height_cm / m_TO_cm

        if ps.use_margins:
            margin_top_m = rel_to_abs_m(
                    ps.margin_top,
                    pixels_to_printed_m(context.scene.render.resolution_y, ps)
                    )
            margin_bottom_m = rel_to_abs_m(
                    ps.margin_bottom,
                    pixels_to_printed_m(context.scene.render.resolution_y, ps)
                    )
            longer_side = longer_side - margin_top_m - margin_bottom_m
        if (ps.width_cm > ps.height_cm): #if (ps.orientation == 'Landscape'):
            longer_side = ps.width_cm / m_TO_cm
            if ps.use_margins:
                margin_left_m = rel_to_abs_m(
                        ps.margin_left,
                        pixels_to_printed_m(context.scene.render.resolution_x, ps)
                        )
                margin_right_m = rel_to_abs_m(
                        ps.margin_right,
                        pixels_to_printed_m(context.scene.render.resolution_x, ps)
                        )
                longer_side = longer_side - margin_left_m - margin_right_m

        #print('old ortho scale: ', context.scene.camera.data.ortho_scale)
        if not context.scene.camera.data.type == 'ORTHO':
            context.scene.camera.data.type = 'ORTHO'
        zoom_result = 1 # May result in too big a text representation of the scale ratio but better than too small (can resize later).
        if context.scene.camera.data.type == 'ORTHO':    #ORTHO, PANO, PERSP
            #blenderartists.org/forum/showthread.php?257556-Render-to-Scale-in-Blender-using-the-Render-to-Print-addon-!
            #They use the magic number 1.3648 - wonder why, its origin needs to be determined.
            #     Orthographic_scale                = 1.3648 x L_format_real x L_real / L_virtual
            # <=> Orthographic_scale * scale_factor = 1.3648 x L_format_real
            # <=> Orthographic_scale * scale_factor = H_format_real
            #                                                       where L_real = scale factor * L_virtual
            #And as the orthographic scale does not take the Scene.unit_settings scale_length into account (for some reason?):
            # The H_format_real now in the model has to be 'unscaled' too for consistency as the model is scaled with the scale_length setting
            # too while strangely the orthographic is not scaled, so the right hand side will also be divided by the scale to make it equal again:
            # <=> Orthographic_scale * scale_factor = H_format_real / unit_settings_scale_length
            # <=> Orthographic_scale = H_format_real / unit_settings_scale_length / scale_factor
            #
            #print('unit setting: ', context.scene.unit_settings.scale_length, ' longer_side in meters: ', longer_side)
            context.scene.camera.data.ortho_scale = (longer_side / context.scene.unit_settings.scale_length) / ps.scale_factor
            zoom_result = context.scene.camera.data.ortho_scale


        elif (context.scene.camera.data.type == 'PERSP'):
            #TODO: somehow involve the location and the field of view!
            context.scene.camera.data.focal_length = (longer_side / context.scene.unit_settings.scale_length) / ps.scale_factor
            zoom_result = context.scene.camera.data.focal_length

        #else:
            #PANO
            #TODO

        #print('new ortho scale: ', context.scene.camera.data.ortho_scale)



def print2scale_add_update_text(ps, context):
    #ps = context.scene.print_settings
    if (ps.print_to_scale):
        ########
        # UPDATE THE TEXT OF THE SCALE RATIO TEXT OBJECT.
        #######
        # Somehow this always gives None. So much to the topic scripting languages are quicker and while python is great, C/C++ would be straight forward.
        #if (hasattr(ps, 'cache_scale_ratio_text_object')):
        #    print('cache is: ' + str(ps.cache_scale_ratio_text_object))
        #if (not hasattr(ps, 'cache_scale_ratio_text_object') or not ps.cache_scale_ratio_text_object):
        scale_ratio_text_object = None
        for o in context.scene.camera.children:
            # to allow other text/font objects as camera children, check for scale_ratio too:
            if (o and o.type == 'FONT' and o.name.find('scale_ratio') != -1):
                scale_ratio_text_object = o
                break
        set_camera_as_parent = False
        if not scale_ratio_text_object:
            for o in context.scene.objects:
                # to allow other text/font objects as camera children, check for scale_ratio too:
                if (o and o.type == 'FONT' and o.name.find('scale_ratio') != -1):
                    scale_ratio_text_object = o
                    set_camera_as_parent = True # because it's not yet been parented.
                    break

        if (not scale_ratio_text_object and ps.add_scale_ratio_text):
            # Add a text for the scale factor e.g. 1:10 on the print.
            scale_ratio_text_object = add_text(context, object_name="scale_ratio")
            scale_ratio_text_object.location[0] = 0
            scale_ratio_text_object.location[1] = 0
            scale_ratio_text_object.location[2] = 0
            # Scale the object to be visible depending on the chosen scale ratio
            # (which relates to the render size and object dimensions/scale used for modeling).
            # The smaller the scale_factor (e.g. 1:50 = 1/50) the farther away the camera will appear.
            # Thus the more the text object must be scaled up to compensate.
            # Take format => dimensions into account.
            # It's 1/10 blender unit away in negative z-direction when using the parenting approach. (TODO This z-direction distance must be taken into account should printing to scale with perspective camera ever be supported in the future.)
            # It should be readable when printed out, thus the format/size (A4, A3, ..) must be read to know
            # if setting it to 1/1000 of the space available will suffice. For A4
            #object_scale = .01 * zoom_result  # figured by experimenting.
            #text_object.scale.x = object_scale * ps.scale_factor
            #text_object.scale.y = object_scale * ps.scale_factor
            #text_object.scale.z = object_scale * ps.scale_factor
            set_camera_as_parent = True

        if scale_ratio_text_object and set_camera_as_parent:
            set_parent(context, to_be_child_objects=[scale_ratio_text_object], parent_object=context.scene.camera)

            ######
            # ADD TRACK TO CONSTRAINT (enable and debug if parenting approach above fails)
            # If enabled then increase distance of the object to the camera.
            ######
            # Make sure nothing is selected:
            bpy.ops.object.select_all(action='DESELECT')
            ## Add track to contraint to properly align the text object towards the camera even if the camera position changed and the scale ratio text object is reused:
            ## Select the objects that shall be looked to:
            #context.scene.camera.select = True
            ## Select the object where the modifier/is added and set it as active object:
            #context.scene.objects.active = scale_ratio_text_object
            #context.scene.objects.active.select = True

            ## Add a constraint to the active object with the selected object(s) as target(s):
            #bpy.ops.object.constraint_add_with_targets(type='TRACK_TO')
            #track_to = scale_ratio_text_object.constraints[-1]
            #track_to.up_axis = 'UP_Y'
            #track_to.track_axis = 'TRACK_Z'


            scale_ratio_text_object.select_set(True) #zhengbo scale_ratio_text_object.select = True
            context.view_layer.objects.active = scale_ratio_text_object #zhengbo context.scene.objects.active = scale_ratio_text_object

        #######
        # Update scale ratio factor:
        if scale_ratio_text_object and not ps.add_scale_ratio_text:
            # Remove the text object:
            #objects_to_be_deleted.append(scale_ratio_text_object)
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = scale_ratio_text_object #zhengbo context.scene.objects.active = scale_ratio_text_object
            scale_ratio_text_object.select_set(True) #zhengbo context.scene.objects.active.select = True
            bpy.ops.object.delete()
            return {'FINISHED'}

        elif not scale_ratio_text_object:
            print("Warning: No scale ratio text object.")
            return {'FINISHED'}

        #else:
        #zhengbo scale_ratio_text_object.layers = list(LAYERS_ALL)
        scale_ratio_text = convertScaleFactorToRatioString(scale_factor=ps.scale_factor);
        change_text(context, scale_ratio_text_object, scale_ratio_text)
        ensure_height(obj=scale_ratio_text_object, print_settings=ps)
        #position_in_top_right_corner(context, obj=scale_ratio_text_object, ps=ps)
        # for more flexibility let the margins be chosen freely:
        position_within_render(context, obj=scale_ratio_text_object, ps=ps)
        # Note this call can lead to endless recursion if width_px or height_px differ from resolution_x.



def find_or_create_camera_and_assign(context):
    if (context.scene.camera is None):
        for scene_o in context.scene.objects:
            if scene_o.type == 'CAMERA':
                print("Assigning found camera %s to scene." % scene_o)
                context.scene.camera = scene_o
                #zhengbo context.scene.camera.layers = list(LAYERS_ALL)
                return

    active_old = bpy.context.active_object #zhengbo active_old = context.scene.objects.active

    if (context.scene.camera is None):
        # Create a camera:
        bpy.ops.object.add(type='CAMERA')
        context.scene.camera = bpy.context.active_object #zhengbo context.scene.objects.active
        ##the added object keeps the short name, while the others are renamed
        #context.scene.selected_object['Camera']

    context.view_layer.objects.active = active_old #zhengbo context.scene.objects.active = active_old



def set_parent(context, to_be_child_objects, parent_object):

    ######
    # ENSURE CAMERA IS ON ALL LAYERS AS MOST OPERATORS CHECK THIS IN THE CONTEXT POLL FUNCTION.
    ######
    #zhengbo context.scene.camera.layers = list(LAYERS_ALL)

    ######
    # PARENT TO CAMERA
    ######
    # Make sure nothing is selected:
    bpy.ops.object.select_all(action='DESELECT')

    # Select the to-be-child objects:
    for o in to_be_child_objects:
        o.select_set(True)

    # Select the to-be-parent object and make active:
    parent_object.select_set(True) #zhengbo parent_object.select = True
    context.view_layer.objects.active = parent_object #zhengbo context.scene.objects.active = parent_object

    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)



def is_out_of_sync(context):
    ps = context.scene.print_settings

    # TODO Update once perspective camera support is added.
    if ps.width_px != context.scene.render.resolution_x or ps.height_px != context.scene.render.resolution_y:
        return True

    if not ps.print_to_scale:
        return True

    if not context.scene.camera or context.scene.camera.type != 'ORTHO':# or ps.camera_zoom_cache != context.scene.camera.ortho_scale: TODO Cache the camera parameter calculation result?
        print2scale__calculate_camera_paramaters(ps, context) # <- Currently required until the scale ratio -> camera orthographic/perspective scale calculation result is cached?

    return False



def position_in_top_left_corner(context, obj=None, ps=None):
    if not ps:
        ps = context.scene.print_settings
    if not obj:
        obj = bpy.context.active_object #zhengbo context.scene.objects.active
    find_or_create_camera_and_assign(context)

    margin_left_right_old = ps.margin_left_right
    margin_top_bottom_old = ps.margin_top_bottom

    if is_out_of_sync(context):
        bpy.ops.render.apply_print_settings()

    #ps.margin_left_right = 10
    #ps.margin_top_bottom = 10
    ps.margin_left_right = obj.dimensions[0] / 2.0 * ps.scale_factor
    #ps.margin_left_right += ps.margin_right
    ps.margin_top_bottom = obj.dimensions[1] / 2.0 * ps.scale_factor
    #ps.margin_top_bottom += ps.margin_bottom
    #bpy.ops.object.position_within_render()
    result = position_within_render(context, obj, ps)
    ps.margin_left_right = margin_left_right_old
    ps.margin_top_bottom = margin_top_bottom_old
    return result



def position_in_top_right_corner(context, obj=None, ps=None):
    if not ps:
        ps = context.scene.print_settings
    if not obj:
        obj = bpy.context.active_object #zhengbo context.scene.objects.active
    find_or_create_camera_and_assign(context)

    margin_left_right_old = ps.margin_left_right
    margin_top_bottom_old = ps.margin_top_bottom

    if is_out_of_sync(context):
        bpy.ops.render.apply_print_settings()

    #ps.margin_left_right = 90 # TODO Depends on object dimensions.
    #ps.margin_top_bottom = 1
    ps.margin_left_right = pixels_to_printed_m(context.scene.render.resolution_x, ps) - obj.dimensions[0] * ps.scale_factor
    #ps.margin_left_right -= ps.margin_right
    ps.margin_top_bottom = 0#obj.dimensions[1] / 2.0 * ps.scale_factor
    #ps.margin_top_bottom += ps.margin_bottom
    #bpy.ops.object.position_within_render()
    result = position_within_render(context, obj, ps)
    ps.margin_left_right = margin_left_right_old
    ps.margin_top_bottom = margin_top_bottom_old
    return result



def position_in_bottom_right_corner(context, obj=None, ps=None):
    if not ps:
        ps = context.scene.print_settings
    if not obj:
        obj = bpy.context.active_object #zhengbo context.scene.objects.active
    find_or_create_camera_and_assign(context)

    margin_left_right_old = ps.margin_left_right
    margin_top_bottom_old = ps.margin_top_bottom

    if is_out_of_sync(context):
        bpy.ops.render.apply_print_settings()

    #ps.margin_left_right = 90 #
    #ps.margin_top_bottom = 90
    smallest_index, second_largest_index, largest_index = get_smallest_central_and_largest(obj.dimensions)
    #req_space = Vector( TODO Enable if rotation no longer is cleared because then a math Vector will be required for calculations.
    req_space = [
        obj.dimensions[largest_index],
        obj.dimensions[second_largest_index],
        obj.dimensions[smallest_index]
        ]
        #)
    # The object has the camera as parent, the dimensions are in local frame and of global world amount. That means the object inherits the rotation.
    # TODO (The object may be rotated relative to the camera, which currently is cleared. Maybe a more general solution should be coded.)
    req_space_max = max(req_space[0], req_space[1], req_space[2])
    #ps.margin_left_right = ps.width_cm / m_TO_cm - req_space_max / 2.0 * ps.scale_factor
    ps.margin_left_right = pixels_to_printed_m(context.scene.render.resolution_x, ps) - obj.dimensions[0] * ps.scale_factor
    #ps.margin_left_right -= ps.margin_right
    ps.margin_top_bottom = pixels_to_printed_m(context.scene.render.resolution_y, ps) - obj.dimensions[1] * ps.scale_factor
    #ps.margin_top_bottom -= ps.margin_bottom
    #bpy.ops.object.position_within_render()
    result = position_within_render(context, obj, ps)
    ps.margin_left_right = margin_left_right_old
    ps.margin_top_bottom = margin_top_bottom_old
    return result



def position_in_bottom_left_corner(context, obj=None, ps=None):
    if not ps:
        ps = context.scene.print_settings
    if not obj:
        obj = bpy.context.active_object #zhengbo context.scene.objects.active
    find_or_create_camera_and_assign(context)

    margin_left_right_old = ps.margin_left_right
    margin_top_bottom_old = ps.margin_top_bottom

    if is_out_of_sync(context):
        bpy.ops.render.apply_print_settings()

    #ps.margin_left_right = 1
    #ps.margin_top_bottom = 90
    #ps.margin_left_right = ps.width_cm / m_TO_cm - req_space_max / 2.0 * ps.scale_factor
    ps.margin_left_right = 0#obj.dimensions[0] / 2.0 * ps.scale_factor
    #ps.margin_left_right += ps.margin_right
    ps.margin_top_bottom = pixels_to_printed_m(context.scene.render.resolution_y, ps) - obj.dimensions[1] * ps.scale_factor
    #ps.margin_top_bottom -= ps.margin_bottom
    #bpy.ops.object.position_within_render()
    result = position_within_render(context, obj, ps)
    ps.margin_left_right = margin_left_right_old
    ps.margin_top_bottom = margin_top_bottom_old
    return result



def position_within_render(context, obj=None, ps=None):
    print('Positioning within render ...')
    active_old = None
    if not obj:
        obj = bpy.context.active_object #zhengbo context.scene.objects.active
    else:
        active_old = bpy.context.active_object #zhengbo context.scene.objects.active
    if not obj:
        print('No object. obj: ', obj)
        return {'CANCELLED'}
    if not ps:
        ps = context.scene.print_settings
    find_or_create_camera_and_assign(context)

    if is_out_of_sync(context):
        print(ps.width_px, context.scene.render.resolution_x, ps.height_px, context.scene.render.resolution_y)
        bpy.ops.render.apply_print_settings()

    rendersettings = context.scene.render

    #Introduces bugs easily if margin is derived from initial object dimensions:ensure_height(obj=obj, print_settings=ps)

    #######
    # Position in a corner. Note: It is extra complicated in PERSPECTIVE mode which is TODO.
    #SPACE_PER_CHAR = 2
    # Extra margin also is required because dimensions of a text object can be smaller than the required space, because the center is a bit too far left because chars start farther to the right, e.g. a 1.
    if ps.margin_left_right >= 1.0: # interprete as percentage
        MARGIN_TO_EDGE_HORIZONTAL = pixels_to_printed_m(context.scene.render.resolution_x, ps) * ps.margin_left_right / 100.0
    else:
        MARGIN_TO_EDGE_HORIZONTAL = ps.margin_left_right

    if ps.margin_top_bottom >= 1.0: # interprete as percentage
        MARGIN_TO_EDGE_VERTICAL = pixels_to_printed_m(context.scene.render.resolution_y, ps) * ps.margin_top_bottom / 100.0
    else:
        MARGIN_TO_EDGE_VERTICAL = ps.margin_top_bottom

    #MARGIN_TO_EDGE_VERTICAL /= ps.scale_factor
    #MARGIN_TO_EDGE_HORIZONTAL /= ps.scale_factor
    #print('MARGIN_TO_EDGE_HORIZONTAL: ', MARGIN_TO_EDGE_HORIZONTAL)
    #print('MARGIN_TO_EDGE_VERTICAL: ', MARGIN_TO_EDGE_VERTICAL)

    # x = camera origin.x (global) + render sizeX / 2 - space * number_of_characters
    smallest_index, second_largest_index, largest_index = get_smallest_central_and_largest(obj.dimensions)
    req_space_x = obj.dimensions[largest_index] / 2.0# * zoom_result
    req_space_y = obj.dimensions[second_largest_index] / 2.0# * zoom_result
    req_space_z = obj.dimensions[smallest_index] / 2.0# * zoom_result
    #print('Object dimensions: ' + str(obj.dimensions))

    # Allow to restore the initial origin later: (NOTE This depends on the blender functionality that setting the origin maintains the position.)
    #TODO Determine why poll function fails:
    #bpy.ops.view3d.snap_cursor_to_active()
    #origin_old = context.scene.cursor_location

    # TODO Correct the wrong math, to allow for reusing blender functionality.
    p = obj.parent
    if p:
        bpy.ops.object.parent_clear(type='CLEAR')
    ## clear rotation temporarily:
    #rotation_old = obj.rotation.copy()
    #obj.rotation = [0.0, 0.0, 0.0]
    origin_old = obj.location + obj.delta_location#TODO Calc rotation matrix from obj.rotation_* # because origin_set influences location only.
    #bpy.ops.object.location_clear()
    #obj.delta_location = [0.0, 0.0, 0.0]
    # HACK Works around the need to execute position within render twice. TODO Why is rotation clear a fix for this weirdness?
    bpy.ops.object.rotation_clear()
    obj.location[0] = 0
    obj.location[1] = 0
    obj.location[2] = 0
    location_old = obj.location.copy()
    delta_location_old = obj.delta_location.copy()
    #print("origin_old: ", origin_old)
    #if not p:
    #    # No parent => Use the camera as this is the soon to be parent.
    #    p = context.scene.camera
    #origin_old = p.location + obj.location * p.matrix_world + obj.delta_location * obj.matrix_world * p.matrix_world
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')#, center='BOUNDS')
    # Create a delta, such that the missing parent information doesn't matter:
    origin_delta = location_old - obj.location
    #origin_new = obj.location + obj.delta_location
    #origin_delta = origin_new - origin_old
    #print("origin_delta: ", origin_delta, " from location_old: ", location_old, " - location: ", obj.location)


    #    Camera -
    #     | |   |
    #    |   |  z
    #   |     | |
    #   |--x--| -   Assuming global Z-axis location is the greatest may not be always true.
    # So better determine the biggest distance to scene's center first (I think this won't
    # work without taking care of the camera's local/delta rotation)?
    # Instead of scene center in this case it might be favourable to use all the objects' medians' median.
    # Not to forget that the camera object's rotation is crucial as it influences the direction of the render
    # resolution x and y. So this is TODO if the parenting approach fails but it ain't (inheriting the camera
    # rotation is easiest).
    x = - pixels_to_printed_m(rendersettings.resolution_x, ps) / 2.0 + MARGIN_TO_EDGE_HORIZONTAL + req_space_x * ps.scale_factor # Because the object's origin is moved to the center explicitely.
    y = pixels_to_printed_m(rendersettings.resolution_y, ps) / 2.0 - MARGIN_TO_EDGE_VERTICAL - req_space_y * ps.scale_factor
    print("x: %s y: %s scale_factor: %s " % (x, y, ps.scale_factor))
    #if ps.scale_factor >= 1.0:
    x /= ps.scale_factor
    y /= ps.scale_factor
    #elif ps.scale_factor < 1.0:
    #    x /= ps.scale_factor * 4
    #    y /= ps.scale_factor
    #TODO debug scale length. x = x / context.scene.unit_settings.scale_length
    #y = y / context.scene.unit_settings.scale_length
    # Because the camera's z axis points in the direction of the incoming rays, parenting and offsetting in negative Z direction is enough:
    z = -.1 - req_space_z # Along the camera's normal (Z) axis. (To move it out of the clipping minimum distance.)
    #z = z / context.scene.unit_settings.scale_length / ps.scale_factor
    obj.delta_location = (x, y, z)
    #print('Object.Delta Location: ' + str(obj.delta_location.x) + ', ' +  str(obj.delta_location.y) + ', ' + str(obj.delta_location.z) )


    # Restore the original origin, maintaining the overall location:
    #origin_new = obj.location + obj.delta_location #TODO Rotation.
    ##if obj.parent: # should have a parent object (camera).
    #origin_new = origin_new + obj.parent.location
    #origin_old_relative = origin_old - origin_new # tip - foot
    #context.scene.cursor_location = origin_old
    #context.scene.cursor_location += origin_delta
    #context.scene.cursor_location = origin_new - origin_delta # valid, because the parent object was cleared.
    delta_location_delta = obj.delta_location - delta_location_old
    cursor_location_old = context.scene.cursor.location.copy()
    context.scene.cursor.location = origin_old + delta_location_delta # valid, because the parent object was cleared
    #raise Error
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')#, center='BOUNDS')
    context.scene.cursor.location = cursor_location_old

    # Adapt the delta location to take the origin offset into account:
    # Remove the LOCAL_WITH_PARENT transform first, remember the old:
    # TODO Simply calculate the rotation matrix Rot(axis, angle) manually from obj.rotation_angles.
    #matrix_world_old = obj.matrix_world.copy()
    #matrix_world_without_parent = obj.convert_space(matrix=obj.matrix_world, from_space='LOCAL_WITH_PARENT', to_space='LOCAL')
    #obj.matrix_world = matrix_world_without_parent
    # With the transform removed, the object is effectively in world/most global space, hence the delta can be applied:
    # Possible because the origin delta is linear to the object's dimensions!
    obj.delta_location += origin_delta

    #print('origin_delta:   ', origin_delta)
    #print('delta_location: ', obj.delta_location)
    #th_i, h_i, w_i = get_smallest_central_and_largest(origin_delta)
    #if obj.delta_location[largest_index] < 0:
    #    obj.delta_location[largest_index] += abs(origin_delta[w_i])
    #else:
    #    obj.delta_location[largest_index] -= abs(origin_delta[w_i])
    #
    #if obj.delta_location[second_largest_index] < 0:
    #    obj.delta_location[second_largest_index] += abs(origin_delta[h_i])
    #else:
    #    obj.delta_location[second_largest_index] -= abs(origin_delta[h_i])

    #obj.delta_location[smallest_index] -= origin_delta[th_i]

    #obj.matrix_world = matrix_world_old * Matrix([1,0,0],[0,1,0],[0,0,1], origin_delta)
    #obj.rotation = rotation_old

    # Set camera as parent if necessary:
    if not obj.parent:
       set_parent(context, to_be_child_objects=[obj], parent_object=context.scene.camera)
    elif obj.parent.type != 'CAMERA':
        print("obj: ", obj, " shall be positioned within render area, but does have another object assigned as parent: ", obj.parent)
    # TODO Remove once the delta position in combination with parenting isn't buggy anymore. This works around random object position (sometimes at least, which is weird too):
    obj.parent_type = 'OBJECT'
    bpy.ops.object.select_all(action='DESELECT')
    context.view_layer.objects.active = obj #zhengbo context.scene.objects.active = obj
    obj.select_set(True) #zhengbo context.scene.objects.active.select = True
    #bpy.ops.object.transform_apply(rotation=True)#, location=False, scale=False)
    bpy.ops.object.rotation_clear()

    #context.scene.cursor_location = obj.parent.location + obj.parent.delta_location + (origin_old + delta_location_delta) * obj.matrix_parent_inverse # valid, because the parent object was cleared.

    if active_old:
        context.view_layer.objects.active = active_old #zhengbo context.scene.objects.active = active_old

    return {'FINISHED'}



def get_smallest_central_and_largest(vector_3d):
    x = vector_3d[0]
    y = vector_3d[1]
    z = vector_3d[2]
    #print("get_smallest_central_and_largest(): vector_3d: ", vector_3d)
    # By default it is assumed that the text is looked onto directly from positive Z axis towards negative Z axis.
    second_largest_index = 0
    largest_index = 2
    smallest_index = 1
    if x > y and x <= z or x > z and x <= y:
        second_largest_index = 0
        largest_index = 1
        smallest_index = 2
        if z > y:
            largest_index = 2
            smallest_index = 1
    elif y > x and y <= z or y > z and y <= x:
        second_largest_index = 1
        largest_index = 0
        smallest_index = 2
        if z > x:
            largest_index = 2
            smallest_index = 0
    elif z > x and z <= y or z > y and z <= x:
        second_largest_index = 2
        largest_index = 0
        smallest_index = 1
        if y > x:
            largest_index = 1
            smallest_index = 0

    #else: # All are equal length, just stick to x.
    # There had been a bug if two are equal and one differs. Then the wrong one is picked as second longest. While the transition from the < to the <= operator works around this bug, sorting a list instead might still be useful for performance (because random access in a list is constant).
    return smallest_index, second_largest_index, largest_index



#
# Changes the text of a text object.
# By default clears the text to an empty string.
#
def change_text(context, text_object, text=""):
    if not text_object:
        print('No text object: ', text_object)
    if not context:
        print('No context: ', context)

    # Make sure nothing is selected:
    #if len(context.selected_objects) > 0: complains about context.
    bpy.ops.object.select_all(action='DESELECT')

    context.view_layer.objects.active = text_object #zhengbo context.scene.objects.active = text_object
    text_object.select_set(True) #zhengbo context.scene.objects.active.select = True

    # Enter edit mode:
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    if (not text_object.visible_get()):
        print("Notice: Could not change text of text object because the object isn't visible currently.")
    elif (text_object.type == 'FONT'):
        bpy.ops.font.select_all()
        bpy.ops.font.text_cut()
        print('setting text: ' + text)
        bpy.ops.font.text_insert(text=text)
    else:
        print('Notice: Could not set scale ratio text representation because object appears to be no text/font object: ' + text_object)

    # Leave editmode to objectmode:
    #bpy.ops.object.editmode_toggle()
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    return {'FINISHED'}



#
# Adds text in a certain text/line height, aligned to the view.
#
# Returns the created text object.
#
def add_text(context, text="", object_name="", print_settings=None):
    if not print_settings:
        print_settings = context.scene.print_settings

    bpy.ops.object.text_add(align='WORLD', enter_editmode=False)
    # type='FONT'
    # The following results in the just added text object:
    #text_object = getLastObjectInSelection(context)    
    #print('active object: ' + str(context.active_object))
    text_object = context.active_object
    text_object.select_set(True)
    if object_name:
       text_object.name = object_name

    # Make sure it's easier to find, i.e. draw it in front of any other objects:
    text_object.show_in_front = True
    #zhengbo text_object.layers = list(LAYERS_ALL) # Copy to allow layer visibility changes affect only this object.
    # Note it's a constant and a reference at the same time if it's not copied using list(). Thus it should not be changed - and if then the side effect is that all objects that have LAYERS_ALL assigned, no longer show on all layers too.

    ensure_height(obj=text_object, print_settings=print_settings)# <- TODO Maybe not enforce the same height currently. Instead, the calling function should be responsible?

    # Add text.
    if text:
        change_text(context, text_object, text)

    return text_object



#
# Set dimension such that the given height is ensured on render/print out.
#
# If no desired height is given, then constants are resolved.
# If none are found, the print settings are evaluated for a text height.
# If still no desired height could be determined, it defaults to .01 meter resulting height.
def ensure_height(obj, print_settings, resulting_height=0.0):
    # Reset scale for the case the value was set to zero earlier (which leads to division by zero):
    #obj.scale.x = 1.0
    #obj.scale.y = 1.0
    #obj.scale.z = 1.0
    target_height = max(resulting_height, 0.0) # 0, i.e. invisible by default.
    if resulting_height < 1:
        # speedier try: x except NameError: not exists else: exists.
        # EITHER
        if ('TEXT_SIZE_PERCENTAGE' in locals() or 'TEXT_SIZE_PERCENTAGE' in globals()) and TEXT_SIZE_PERCENTAGE:
            height_available = print_settings.width_cm / m_TO_cm
            target_height = height_available * TEXT_SIZE_PERCENTAGE / 100
        # OR (Overrides the above if both height percentage and absolute value are given.)
        elif ('RESULTING_TEXT_HEIGHT' in locals() or 'RESULTING_TEXT_HEIGHT' in globals()) and RESULTING_TEXT_HEIGHT:
            resulting_height = RESULTING_TEXT_HEIGHT
        elif print_settings.text_height:
            resulting_height = print_settings.text_height
        else:
            print('WARNING: No text size defined, defaulting to .01m text height when printed out.')
            resulting_height = .010 # meters = 1cm = 10mm

    # TODO Support more text sizes, e.g. a GUI field for getting input.
    if resulting_height:
        target_height = resulting_height / print_settings.scale_factor
    else:
        print("Desired resulting height (as printed) is invalid: %s => Defaulting to 0, i.e. invisible." % resulting_height)

    # Assumption: text object's width is largest. Height is 2nd longest. Depth/thickness comes third.
    # TODO Figuring text height directly possible?
    smallest_index, second_largest_index, largest_index = get_smallest_central_and_largest(obj.dimensions)
    #print("object dimensions: ", obj.dimensions, " smallest: ", smallest_index, " central: ", second_largest_index, " largest: ", largest_index)
    object_height = obj.dimensions[second_largest_index]
    #print(object_height, ' target height: ', target_height)
    # The height determines the scale factor, the other dimensions are scaled with the same factor to avoid distortion:
    scale_factor = target_height / object_height
    #target_dim = obj.dimensions * scale_factor # Vector times scalar.
    #scale_object_to_target_dimensions(target_dim=target_dim)
    obj.scale.x *= scale_factor
    obj.scale.y *= scale_factor
    obj.scale.z *= scale_factor
    # Workaround scale not taking effect until mode was toggled:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')

    return {'FINISHED'}



def convertScaleFactorToRatioString(scale_factor, precision=2):
    text = None
    if (scale_factor < 1):
        num = scale_factor
        #while str(num).find('.') != -1:
        #denominator = 1
        #while round(num * denominator, 0) != num * denominator:
        #    denominator = denominator * 10
        if (num != 0):
            rounded = round(1 / num, precision)
            rounded_to_integer = round(rounded, 0)
            if rounded_to_integer == rounded:
                rounded = int(rounded_to_integer)
            text = ' 1:' + str(rounded)

    else:
        rounded = round(scale_factor, precision)
        rounded_to_integer = round(rounded, 0)
        if rounded_to_integer == rounded:
            rounded = int(rounded_to_integer)
        text = str(rounded) + ':1'

    return text


in_TO_cm = 2.54 # conversion factor



#def printed_distance_to_pixel(resulting_distance_m):
def printed_m_to_pixels(m, ps): # inline function
    return round(m * m_TO_cm / in_TO_cm * float(ps.dpi))



def derive_width_pixels(context, ps):
    m = ps.width_cm / m_TO_cm
    if ps.use_margins:
        m = m - rel_to_abs_m(ps.margin_left, pixels_to_printed_m(context.scene.render.resolution_x, ps)) - rel_to_abs_m(ps.margin_right, pixels_to_printed_m(context.scene.render.resolution_x, ps))
    ps.width_px = max(printed_m_to_pixels(m, ps), 4)



def derive_height_pixels(context, ps):
    m = ps.height_cm / m_TO_cm
    if ps.use_margins:
        m = m - rel_to_abs_m(ps.margin_top, pixels_to_printed_m(context.scene.render.resolution_y, ps)) - rel_to_abs_m(ps.margin_bottom, pixels_to_printed_m(context.scene.render.resolution_y, ps))
    ps.height_px = max(printed_m_to_pixels(m, ps), 4)



def pixels_to_printed_m(pixel, ps):
    return float(pixel) / float(ps.dpi) * in_TO_cm / m_TO_cm



def pixels_from_print(context, ps):
    tipo, dim_w, dim_h = paper_presets_data[ps.preset]

    if tipo != "custom":
        # (Re)load all parameters from the preset:
        if ps.orientation == "Landscape":
            ps.width_cm = dim_h
            ps.height_cm = dim_w
        elif ps.orientation == "Portrait":
            ps.width_cm = dim_w
            ps.height_cm = dim_h
        # Update potentially outdated pixel values:
        derive_width_pixels(context, ps)
        derive_height_pixels(context, ps)

    else:
        #dim_w = ps.width_cm
        #dim_h = ps.height_cm
        if ps.unit_from == "CM_TO_PIXELS":
            derive_width_pixels(context, ps)
            derive_height_pixels(context, ps)
        else: #PIXELS_TO_CM
            ps.width_cm = float(ps.width_px) / float(ps.dpi) * in_TO_cm
            ps.height_cm = float(ps.height_px) / float(ps.dpi) * in_TO_cm
            if ps.use_margins:
                margin_left_m = rel_to_abs_m(
                        ps.margin_left,
                        pixels_to_printed_m(context.scene.render.resolution_x, ps)
                        )
                margin_right_m = rel_to_abs_m(
                        ps.margin_right,
                        pixels_to_printed_m(context.scene.render.resolution_x, ps)
                        )
                ps.width_cm += margin_left_m * m_TO_cm + margin_right_m * m_TO_cm
            if ps.use_margins:
                margin_top_m = rel_to_abs_m(
                        ps.margin_top,
                        pixels_to_printed_m(context.scene.render.resolution_y, ps)
                        )
                margin_bottom_m = rel_to_abs_m(
                        ps.margin_bottom,
                        pixels_to_printed_m(context.scene.render.resolution_y, ps)
                        )
                ps.height_cm += margin_top_m * m_TO_cm + margin_bottom_m * m_TO_cm






class RENDER_PT_print(Panel):
    bl_idname = "OBJECT_PT_print_panel"
    bl_label = "Print"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Print'

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        ps = scene.print_settings


        #PRINT2SCALE
        row00 = layout.row(align=True)
        text = "Print to scale "
        text = text + convertScaleFactorToRatioString(ps.scale_factor)

        row00.prop(ps, "print_to_scale", text=text)

        row = layout.row(align=True)
        row.active = ps.print_to_scale
        row.prop(ps, "scale_factor", text="Scale factor")

        row = layout.row(align=True)
        row.active = ps.print_to_scale
        row.prop(ps, "add_scale_ratio_text", text="Add scale ratio text")

        row = layout.row(align=True)
        row.active = ps.print_to_scale
        row.prop(ps, "text_height", text="Text height")

        row = layout.row(align=True)
        row.active = ps.print_to_scale
        #row.label(text="Positioning margins:")
        row.operator("object.position_within_render")#, icon="",
        row.prop(ps, "margin_left_right", text="Margin left, right.")
        row.prop(ps, "margin_top_bottom", text="Margin top, bottom.")
        #PRINT2SCALE -END

        #GENERAL PRINT SETTINGS
        # Not needed directly by render to print, nevertheless located in print settings for single source principle, may be used by various extensions that require margin information:
        row = layout.row(align=True)
        row.prop(ps, "use_margins", text="")
        row.prop(ps, "margin_top", text="Top margin")
        row.prop(ps, "margin_right", text="Right margin")
        row.prop(ps, "margin_bottom", text="Bottom margin")
        row.prop(ps, "margin_left", text="Left margin")
        row.active = ps.use_margins

        row = layout.row(align=True)
        row1 = layout.row(align=True)
        row2 = layout.row(align=True)
        row3 = layout.row(align=True)
        row4 = layout.row(align=True)
        row5 = layout.row(align=True)
        row6 = layout.row(align=True)
        row7 = layout.row(align=True)
        col = layout.column(align=True)

        row.prop(ps, "unit_from")
        row1.prop(ps, "orientation")
        row2.prop(ps, "preset")

        col.separator()
        row3.prop(ps, "width_cm")
        row3.separator()
        row3.prop(ps, "height_cm")
        col.separator()
        row4.prop(ps, "dpi")
        col.separator()
        row5.prop(ps, "width_px")
        row5.separator()
        row5.prop(ps, "height_px")

        col.separator()
        row6.label(text="Inch Width: %.2f" % (ps.width_cm / in_TO_cm))
        row6.label(text="Inch Height: %.2f" % (ps.height_cm / in_TO_cm))
        col.separator()

        #split = row7.split()
        #row = split.row()
        row71 = row7
        row71.active = True
        row71.prop(ps, "update_manually")
        #row = split.row()
        if ps.update_manually:
        #    row.active = True
        #else:
        #    row.active = False
            row71.operator("render.apply_print_settings", icon="RENDER_STILL")

        # Hide UI elements when logic demands it:
        tipo = paper_presets_data[ps.preset][0]

        if tipo != "custom":
            #ps.unit_from = 'CM_TO_PIXELS' TODO
            row.active = False
            row.enabled = False

        if ps.unit_from == "CM_TO_PIXELS":
            row5.active = False
            row5.enabled = False

            if tipo == "custom":
                row3.active = True
                row3.enabled = True
                row1.active = False
                row1.enabled = False
            elif tipo != "custom" and ps.orientation == "Landscape":
                row3.active = False
                row3.enabled = False
                row1.active = True
                row1.enabled = True
            elif tipo != "custom" and ps.orientation == "Portrait":
                row3.active = False
                row3.enabled = False
                row1.active = True
                row1.enabled = True
        else:
            row3.active = False
            row3.enabled = False

            if tipo == "custom":
                row1.active = False
                row1.enabled = False
            elif tipo != "custom" and ps.orientation == "Landscape":
                row1.active = True
                row1.enabled = True
                row5.active = False
                row5.enabled = False
            elif tipo != "custom" and ps.orientation == "Portrait":
                row1.active = True
                row1.enabled = True
                row5.active = False
                row5.enabled = False


m_TO_cm = 100.0

class OBJECT_OT_text_change(Operator):
    bl_idname = "object.text_change"
    bl_label = "Change text."
    bl_description = "Change the text of a text object."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):#, text_object, text=""):
        return change_text(context, text_object=bpy.context.active_object, text=context.scene.name)#<- HACK. TODO Solve properly. Maybe blender could add this as a built-in operator. Or use self.text if possible and reliable?)



class OBJECT_OT_position_within_render(Operator):
    '''Position within render, e.g. in a corner if margins are set as such. Note that proper results may require the print settings to be applied to the camera, render settings.'''
    bl_idname = "object.position_within_render"
    bl_label = "Position within render"
    bl_description = "Position within render, e.g. in a corner if margins are set as such. Note that proper results may require the print settings to be applied to the camera, render settings."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):#, text_object, text=""):
        #HACK rotation_clear() now fixed it. position_within_render(context)
        #bpy.ops.render.apply_print_settings() <- some extensions may prefer or require to handle this own their own. Also if the position within render operator is called frequently then not applying the print settings may save performance (this could be mitigated by checking if the settings changed before applying, e.g. comparing render settings' and the print settings' resolution).
        return position_within_render(context)



class OBJECT_OT_position_in_top_left_corner(Operator):
    bl_idname = "object.position_in_top_left_corner"
    bl_label = "Position in top left corner."
    bl_description = "Position within render, in the top left corner."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):#, text_object, text=""):
        return position_in_top_left_corner(context)



class OBJECT_OT_position_in_top_right_corner(Operator):
    bl_idname = "object.position_in_top_right_corner"
    bl_label = "Position in top right corner."
    bl_description = "Position within render, in the top right corner."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return position_in_top_right_corner(context)



class OBJECT_OT_position_in_bottom_right_corner(Operator):
    bl_idname = "object.position_in_bottom_right_corner"
    bl_label = "Position in bottom right corner."
    bl_description = "Position within render, in the bottom right corner."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):#, text_object, text=""):
        return position_in_bottom_right_corner(context)



class OBJECT_OT_position_in_bottom_left_corner(Operator):
    bl_idname = "object.position_in_bottom_left_corner"
    bl_label = "Position in bottom left corner."
    bl_description = "Position within render, in the bottom left corner."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):#, text_object, text=""):
        return position_in_bottom_left_corner(context)



class RENDER_OT_ensure_height(Operator):
    bl_idname = "render.ensure_height"
    bl_label = "Ensure a certain printed height."
    bl_description = "Set the dimensions of a text object such that it is printed out in a certain height."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):#, resulting_height, obj):
        return ensure_height(obj=bpy.context.active_object, print_settings=context.scene.print_settings)






class RenderPrintSettings(PropertyGroup):
    update_manually = BoolProperty(
            name="Update manually"
            ,description="If enabled apply settings manually instead of realtime update."
            ,default=False
            ,update=update_settings_cb
    )

    unit_from = EnumProperty(
            name="Set from",
            description="Set from",
            items=(
                ("CM_TO_PIXELS", "CM -> Pixel", "Centermeters to Pixels"),
                ("PIXELS_TO_CM", "Pixel -> CM", "Pixels to Centermeters")
                ),
            default="CM_TO_PIXELS",
            )
    orientation = EnumProperty(
            name="Page Orientation",
            description="Set orientation",
            items=(
                ("Portrait", "Portrait", "Portrait"),
                ("Landscape", "Landscape", "Landscape")
            ),
            default="Portrait",
            update=update_settings_cb,
            )
    preset = EnumProperty(
            name="Select Preset",
            description="Select from preset",
            items=paper_presets,
            default="custom_1_1",
            update=update_settings_cb,
            )
    dpi = IntProperty(
            name="DPI",
            description="Dots per Inch",
            default=300,
            min=72, max=1800,
            update=update_settings_cb,
            )
    width_cm = FloatProperty(
            name="Width",
            description="Width in CM",
            default=5.0,
            min=1.0, max=100000.0,
            update=update_settings_cb,
            )
    height_cm = FloatProperty(
            name="Height",
            description="Height in CM",
            default=3.0,
            min=1.0, max=100000.0,
            update=update_settings_cb,
            )
    width_px = IntProperty(
            name="Pixel Width",
            description="Pixel Width",
            default=900,
            min=4, max=10000,
            update=update_settings_cb,
            )
    height_px = IntProperty(
            name="Pixel Height",
            description="Pixel Height",
            default=600,
            min=4, max=10000,
            update=update_settings_cb,
            )
    #PRINT TO SCALE
    print_to_scale = BoolProperty(
            name="Print to scale"
            ,description="Print to scale by automatically calculate the correct distance of the camera to the object or the center of scene."
            ,default=True
            #,update=print2scale_reset_camera_focal_length_or_orthographic_scale
    )
    # Remapping probably will lead to much confusion. e.g. model 10 -> 1 on the plan means the output will be a model copy 10 times smaller.
    # Many architects will accidentally fill in 1:10 instead because they forget that here the ratio is (model:plan) and not (plan:model) like printed
    # on the plan. So unfortunately this will cost a lot of trees as the prints in that a size will be rendered useless.
    # => SO NOW WE USE SCALE FACTOR ONLY! THAT'S MUCH MORE INTUITIVE AND IS NOTHING ELSE than print ratio but without the confusion.
    #in_print2scale_scale_remap_source_model = IntProperty(
    #        name="Model - Print ratio denominator (Model, Map source)"
    #        ,description="If the model value is greater than the real world value (e.g. 2:1) then the printed output will be scaled down to 1/2 the model size. is e.g. 10 and the real world value 1, then we have a print ratio of 10:1, that is 10 model units print to 1 real world unit. So a 10m model becomes 1m. Thus the printed plan is to scale in a ratio of 1:10 (while the model is in the opposite ratio of 10:1)."
    #        ,default=1
    #        ,min=1
    #        ,max=10000
    #        ,update=print2scale_recalculate_camera_focal_length_or_orthographic_scale
    #)
    #in_print2scale_scale_remap_target_printed = IntProperty(

    # NOTE:
    # The print ratio is nothing else than a scale factor. E.g. 1:10 on a plan means the original real measurements are scaled down by factor 10.
    # ATTENTION:
    # Precondition is that the 3D model must be modelled to scale. Only then printing a plan to scale, scaled down or up, gives meaningful dimensions.
    # E.g. if a 1m long wing is modelled with 1mm length in blender instead, then it has to be printed with a 1000:1 for a 1:1 scale on a 1m sheet
    # or 100:1 on a 1/10m sheet, resulting in a factor of 1:10. Unfortunately the program can't know if the model now really is that small (1mm) or
    # not and labels the plan as 100:1 in scale - obviously confusing all engineers and architects involved.
    # Either scaling the model up or changing the unit settings scale can solve this. From experience the first approach can prove difficult
    # as this can lead to strange behaviour of modifiers and any kind of relationsships of objects of the model - often messing up the complete model.
    # The latter - changing the unit settings - is okay, but results in modularity problems if this setting is different in each scene,
    # so when finally importing one model into another scene, a lot of new problems arise. Also problematic are discrepancies in the grid and blender's
    # buildin-measurement functionality (N panel, e.g. edge info) as well as the bullet engine or other features that rely on physically accurate units
    # (and from what reason ever (there are plenty!) don't take the unit scale into account correctly).
    # The loss of modularity is such a big problem that it's good to know that all this trouble can be avoided by simply modelling to scale.
    # (While model accuracy might prove inaccurate if modelling to scale without scaling up the model as the grids resolution is limited! So there is no silverbullet.)
    scale_factor = FloatProperty(
            name="Print scale factor"
            ,description="Scale big models down (scale factor <1) or tiny models up (scale factor >1). E.g. 10 results in scaling up tenfold, a 1meter model will fill 10m on a giant sheet of papyrus when printed out with this setting. On the other hand 0.1 = 1/10 results in a 1:10 plan being printed."
            ,default=1
            ,min=0.00000001 #If zero is possible, problems will arise due to division by zero!
            ,max=10000
            ,update=print2scale_recalculate_camera_focal_length_or_orthographic_scale
    )
    #cache_scale_ratio_text_object = None # ObjectProperty or ReferenceProperty
    add_scale_ratio_text = BoolProperty(
            name="Add scale ratio text."
            ,description="Whether to add a text representation of the scale factor (as ratio) or not."
            ,default=True
            ,update=print2scale#_reset_camera_focal_length_or_orthographic_scale
    )
    # Remapping probably will lead to much confusion. e.g. model 10 -> 1 on the plan means the output will be a model copy 10 times smaller.
    # Many architects will accidentally fill in 1:10 instead because they forget that here the ratio is (model:plan) and not (plan:model) like printed
    text_height = FloatProperty(
            name="Text height."
            ,description="Text height as printed. Given in Standard International units. Defaults to 1cm if zero."
            ,default=.005 # m = .5cm = 5mm
            ,min=0.0
            ,max=100.0 # 100m is quite huge already, even for graffity.
            #,update=ensure_height <- if text object is selected and active.
            ,update=update_settings_cb
    )

    # Margins for printers that require a blank border (due to technical or visual reasons):
    use_margins = BoolProperty(
            name="Use margins"
            ,description="Calculate the render size such that margins won't be rendered (results in smaller rendered image)."
            ,default=True
            ,update=update_settings_cb
    )
    margin_top = FloatProperty(
            name="Top margin"
            ,description="Blank space from the top paper edge."
            ,default=.015 # 1.5cm  #1 # 1%
            ,min=0.0
            ,max=100.0
            ,update=update_settings_cb
    )
    margin_right = FloatProperty(
            name="Right margin"
            ,description="Blank space from the right paper edge."
            ,default=.015 # 1.5cm  #1 # 1%
            ,min=0.0
            ,max=100.0
            ,update=update_settings_cb
    )
    margin_bottom = FloatProperty(
            name="Bottom margin"
            ,description="Blank space from the bottom paper edge."
            ,default=.015 # 1.5cm  #1 # 1%
            ,min=0.0
            ,max=100.0
            ,update=update_settings_cb
    )
    margin_left = FloatProperty(
            name="Left margin"
            ,description="Blank space from the left paper edge."
            ,default=.015 # 1.5cm  #1 # 1%
            ,min=0.0
            ,max=100.0
            ,update=update_settings_cb
    )


    # Position within render:
    margin_top_bottom = FloatProperty(
            name="Vertical margin"
            ,description="Distance to top, bottom edges. Interpreted as percentage if >= 1."
            ,default=1 # 1%
            ,min=0.0
            ,max=100.0
    )
    margin_left_right = FloatProperty(
            name="Horizontal margin"
            ,description="Distance to left, right edges. Interpreted as percentage if >= 1."
            ,default=1 # 1%
            ,min=0.0
            ,max=100.0
            #,update=position_within_render <- requires parameters.
    )





class RENDER_OT_apply_print_settings(Operator):
    bl_idname = "render.apply_print_settings"
    bl_label = "Apply print settings."
    bl_description = "Set the render dimension."

    def execute(self, context):

        ps = context.scene.print_settings

        pixels_from_print(context, ps)

        render = context.scene.render
        render.resolution_x = max(ps.width_px, 4)
        render.resolution_y = max(ps.height_px, 4)

        print2scale(ps, context)

        return {'FINISHED'}






def getLastObjectInSelection(context):
    return context.selected_objects[len(context.selected_objects) - 1]




def register():
    bpy.utils.register_class(RENDER_OT_apply_print_settings)
    bpy.utils.register_class(RENDER_OT_ensure_height)
    bpy.utils.register_class(OBJECT_OT_text_change)
    bpy.utils.register_class(OBJECT_OT_position_within_render)
    bpy.utils.register_class(OBJECT_OT_position_in_top_left_corner)
    bpy.utils.register_class(OBJECT_OT_position_in_top_right_corner)
    bpy.utils.register_class(OBJECT_OT_position_in_bottom_right_corner)
    bpy.utils.register_class(OBJECT_OT_position_in_bottom_left_corner)
    bpy.utils.register_class(RENDER_PT_print)
    bpy.utils.register_class(RenderPrintSettings)

    Scene.print_settings = PointerProperty(type=RenderPrintSettings)


def unregister():
    bpy.utils.unregister_class(RENDER_OT_apply_print_settings)
    bpy.utils.unregister_class(RENDER_OT_ensure_height)
    bpy.utils.unregister_class(OBJECT_OT_text_change)
    bpy.utils.unregister_class(OBJECT_OT_position_within_render)
    bpy.utils.unregister_class(OBJECT_OT_position_in_top_left_corner)
    bpy.utils.unregister_class(OBJECT_OT_position_in_top_right_corner)
    bpy.utils.unregister_class(OBJECT_OT_position_in_bottom_right_corner)
    bpy.utils.unregister_class(OBJECT_OT_position_in_bottom_left_corner)
    bpy.utils.unregister_class(RENDER_PT_print)
    bpy.utils.unregister_class(RenderPrintSettings)
    del Scene.print_settings


if __name__ == "__main__":
    register()
