""" Script Object for creating multiple associative views from lines
"""
from __future__ import annotations

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtility
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_AllplanSettings as AllplanSettings

from BuildingElement import BuildingElement
from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from TypeCollections.ModelEleList import ModelEleList
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from Utils.LibraryBitmapPreview import create_libary_bitmap_preview

print('Load SectionsFromLines.py')

def create_preview(_build_ele, _doc):
    """
    Creation of object preview
    """

    model_ele_list = create_libary_bitmap_preview(AllplanSettings.AllplanPaths.GetStdPath() +
                                                  r"\Library\allplan-cz\Sections from lines.png")

    return (model_ele_list, None, None)

def check_allplan_version(build_ele, version):
    """    Checks the current Allplan version.

    Args:
        build_ele: The building element to check.
        version: The version information to check against.

    Returns:
        bool: True if the version is compatible, otherwise False.
    """
    return True

def create_script_object(build_ele: BuildingElement, script_object_data: BaseScriptObjectData):
    """    Creates and returns a SectionsFromLinesScriptObject instance using the provided building element and script object data.
    Args:
        build_ele (BuildingElement): The building element to be used for creating the script object.
        script_object_data (BaseScriptObjectData): The data required to initialize the script object.
    Returns:
        SectionsFromLinesScriptObject: An instance of the script object initialized with the given parameters.
    """

    return SectionsFromLinesScriptObject(build_ele, script_object_data)

class SectionsFromLinesScriptObject(BaseScriptObject):
    """SectionsFromLinesScriptObject is a script object for creating multiple associative section views from 2D lines in Allplan.
    """
    def __init__(self, build_ele: BuildingElement, script_object_data: BaseScriptObjectData):
        super().__init__(script_object_data)
        self.build_ele = build_ele
        self.run_action = False  # Flag for executing action
        self.delete_elements = False  # Flag for deleting elements

    def on_control_event(self, event_id: int):
        if event_id == 1000:
            self.run_action = True
            self.delete_elements = False

        elif event_id == 1001:
            self.run_action = True
            self.delete_elements = True


    def execute(self) -> CreateElementResult:
        """Executes the creation and/or deletion of section elements based on the current state.
        Returns:
            CreateElementResult: The result containing the created elements and their placement point.
        """
        if self.run_action:
            horni_hrana = self.build_ele.section_top.value
            dolni_hrana = self.build_ele.section_bottom.value
            hloubka_rezu = self.build_ele.section_depth.value
            layer_filter = self.build_ele.layer_filter.value
            direction = self.build_ele.direction.value
            first_no = self.build_ele.first_no.value

            all_elements = AllplanBaseElements.ElementsSelectService.SelectAllElements(self.document)
            model_ele_list = ModelEleList()

            common_prop = AllplanBaseElements.CommonProperties()
            common_prop.GetGlobalProperties()

            view_props = AllplanBasisElements.SectionGeneralProperties(True)
            view_format_props = view_props.FormatProperties
            view_filter_props = view_props.FilterProperties
            view_label_props = view_props.LabelingProperties

            label_prop = AllplanReinf.ReinforcementLabelProperties()
            label_prop.ShowBarDiameter = False
            label_prop.ShowBarCount = False
            label_prop.ShowBarDistance = False

            view_format_props.IsEliminationOn = True
            view_format_props.EliminationAngle = 22
            view_label_props.HeadingOn = False
            view_label_props.AddProjectionName = False

            view_draw_files_props = AllplanBasisElements.SectionDrawingFilesProperties()
            drawing_file_numbers = AllplanUtility.VecIntList()
            for _, number in AllplanEleAdapter.DocumentNameService.GetLoadedDocumentsNameData():
                drawing_file_numbers.append(number)
            view_draw_files_props.DrawingNumbers = drawing_file_numbers

            view_filter_props.DrawingFilesProperties = view_draw_files_props
            view_filter_props.IsAssociativityOn = True

            view_props.Status = AllplanBasisElements.SectionGeneralProperties.State.Hidden
            view_props.ShowSectionBody = True
            view_props.FormatProperties = view_format_props
            view_props.FilterProperties = view_filter_props
            view_props.LabelingProperties = view_label_props

            count = 0
            sect_ele_list = []
            delete = AllplanEleAdapter.BaseElementAdapterList()

            for element in all_elements:
                com_prop = element.GetCommonProperties()
                if com_prop.Layer == layer_filter and element.GetElementAdapterType().GetTypeName() == "Line2D_TypeUUID":
                    count += 1
                    line = element.GetGeometry()
                    angle = line.GetAngle()
                    angle_deg = AllplanGeo.Angle.GetDeg(angle)
                    print(angle_deg)
                    if (direction is False and (angle_deg > 90 and angle_deg <= 270)):
                        line.Reverse()

                    start_point = line.GetStartPoint()
                    end_point = line.GetEndPoint()
                    vector = line.GetVector()

                    angle = line.GetAngle()
                    angle_rad = AllplanGeo.Angle(angle)
                    angle_rad = AllplanGeo.Angle.Get(angle_rad)
                    angle_deg = AllplanGeo.Angle.GetDeg(angle)

                    tangent_vector = AllplanGeo.PerpendicularCalculus.Calculate(vector, 1)
                    tangent_vector.Normalize(hloubka_rezu)
                    tangent_vector_3d = AllplanGeo.Vector3D(tangent_vector)
                    transformation_matrix = AllplanGeo.Matrix2D()
                    transformation_matrix.SetTranslation(tangent_vector)

                    start_point_1 = start_point * transformation_matrix
                    end_point_1 = end_point * transformation_matrix

                    listpoint = [start_point, end_point, end_point_1, start_point_1, start_point]
                    rect = AllplanGeo.Polyline2D(listpoint)

                    sect_ele = AllplanBasisElements.ViewSectionElement()

                    posun = AllplanGeo.PerpendicularCalculus.Calculate(line2d=line, inputPnt=AllplanGeo.Point3D(0, 0, 0))
                    bod_posun = posun[1]
                    bod_posun = bod_posun.To2D

                    tangent_vector.Normalize(dolni_hrana)

                    view_props.PlacementPoint = start_point + bod_posun - tangent_vector
                    view_props.PlacementAngle = angle_rad
                    view_props.ShowSectionBody = False

                    sect_ele.GeneralSectionProperties = view_props
                    sect_ele.ViewMatrix = RotationAngles(0, 0, -angle_deg).get_rotation_matrix()

                    section_def_data = AllplanBasisElements.SectionDefinitionData()
                    section_def_data.ClippingPath = rect
                    section_def_data.DirectionVector = tangent_vector_3d

                    sec_def_prop = section_def_data.DefinitionProperties
                    sec_def_prop.IsSectionBodyOn = True


                    clip_path_prop = sec_def_prop.ClippingPathProperties
                    clip_path_prop.TopLevel = horni_hrana
                    clip_path_prop.BottomLevel = dolni_hrana
                    clip_path_prop.IsHeightFromElementOn = False
                    clip_path_prop.SectionIdentifier = str(count+first_no-1)
                    clip_path_prop.IsClippingLineOn = False

                    sec_def_prop.ClippingPathProperties = clip_path_prop

                    section_def_data.DefinitionProperties = sec_def_prop
                    sect_ele.SectionDefinitionData = section_def_data

                    sect_ele_list.append(sect_ele)


                    delete.append(element)

            if self.delete_elements:
                AllplanBaseElements.DeleteElements(self.document, delete)

            model_ele_list.extend(sect_ele_list)

            return CreateElementResult(elements=model_ele_list, placement_point=AllplanGeo.Point2D(0, 0))
        else:
            return CreateElementResult(elements=[], placement_point=AllplanGeo.Point2D(0, 0))
