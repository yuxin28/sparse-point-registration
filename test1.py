from dSPR import *
import open3d as o3d
from visualize import *
from data_processing import *
from generatepoints import *
import matplotlib.pyplot as plt

#
A, A_subset, B, T_orig = gen_points(100, 20, 20)
# A.paint_uniform_color([1, 0.706, 0])
# A_subset.paint_uniform_color([0, 0.651, 0.929])
# B.paint_uniform_color([0, 0.651, 0.1])
# o3d.visualization.draw_geometries([A, B])
# o3d.visualization.draw_geometries([A_subset, B])
threshold = 0.02

# add noise and outliers
# B = add_noise(B, stddev = 0.01)
# B = add_outliers(B, 0.1)
# draw_registration_result(B, A_subset, T_orig)

# T = dSPR(B, A, iter_num=100, threshold = threshold, angel=360)

print(o3d.pipelines.registration.evaluate_registration(B, A_subset, threshold, T_orig))
draw_origin(B, A_subset)
draw_registration_result(B, A, T_orig)
draw_registration_result(B, A_subset, T_orig)

# print(o3d.pipelines.registration.evaluate_registration(B, A_subset, 0.05, T_orig))    