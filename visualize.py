import copy
import open3d as o3d
import numpy as np


def draw_registration_result(source, target, transformation, point_size=5):
    # Create a window object
    vis = o3d.visualization.Visualizer()
    # Set window title
    vis.create_window(window_name="registration result")
    # Set point cloud size
    vis.get_render_option().point_size = point_size
    # Set background color to black
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])

    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])  # Set source color
    target_temp.paint_uniform_color([0, 0.651, 0.929])  # Set target color
    # Apply transformation to the source point cloud
    source_temp.transform(transformation)
    # Add point clouds to the window
    vis.add_geometry(source_temp)
    vis.add_geometry(target_temp)

    vis.run()
    vis.destroy_window()

def draw_origin(source, target, point_size=5):
    # Create a window object
    vis = o3d.visualization.Visualizer()
    # Set window title
    vis.create_window(window_name="registration result")
    # Set point cloud size
    vis.get_render_option().point_size = point_size
    # Set background color to black
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])

    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])  # Set source color
    target_temp.paint_uniform_color([0, 0.651, 0.929])  # Set target color
    # Add point clouds to the window
    vis.add_geometry(source_temp)
    vis.add_geometry(target_temp)

    vis.run()
    vis.destroy_window()
