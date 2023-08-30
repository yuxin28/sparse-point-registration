from dSPR import SPR
import open3d as o3d
from visualize import draw_registration_result
from data_processing import *
from generatepoints import *
import matplotlib.pyplot as plt
from tqdm import tqdm


# # read point cloud
# A_orig = o3d.io.read_point_cloud("/Users/yuxin/Desktop/deep learning/stanford/bunny/data/bun000.ply")
# B_orig = o3d.io.read_point_cloud("/Users/yuxin/Desktop/deep learning/stanford/bunny/reconstruction/bun_zipper.ply")

# num_points = 20
# threshold = 0.02
# angel = 10

# #random downsample
# # A = random_downsampling(A_orig, num_points)
# # B = random_downsampling(B_orig, num_points)

# #uniform downsample
# A = uniform_downsampling(A_orig, num_points)
# # B = uniform_downsampling(B_orig, num_points)

# #add noise and outliers
# A = add_noise(A)
# # B = add_noise(B)
# A = add_outliers(A, 0.1)
# # B = add_outliers(B, 0.1)

# #compute transformation
# T= SPR(A_orig, B_orig, threshold = threshold, angel=angel)
# print('Transform Matrix')
# print(T)

# #visualize
# print(o3d.pipelines.registration.evaluate_registration(A, B_orig, threshold, T))
# draw_registration_result(A, B_orig, T)
# draw_registration_result(A_orig, B_orig, T)

A, A_subset, B, T_orig = gen_points(100, 20, 20)
# A.paint_uniform_color([1, 0.706, 0])
# A_subset.paint_uniform_color([0, 0.651, 0.929])
# B.paint_uniform_color([0, 0.651, 0.929])
# o3d.visualization.draw_geometries([A, B])
# o3d.visualization.draw_geometries([A_subset, B])
# print(np.asarray(A_subset.points)- np.asarray(B.points))
threshold = 0.08

# add noise and outliers
B = add_noise(B, stddev = 0.01)
B = add_outliers(B, 0.1)

T = SPR(B, A, iter_num=10, threshold = threshold, angel=10)

print(o3d.pipelines.registration.evaluate_registration(B, A_subset, threshold, T))
draw_registration_result(B, A, T)
draw_registration_result(B, A_subset, T)

print(o3d.pipelines.registration.evaluate_registration(B, A_subset, 0.05, T_orig))
# B.paint_uniform_color([0, 0.651, 0.929])
# o3d.visualization.draw_geometries([B])
# draw_registration_result(B, A, T_orig)
# draw_registration_result(B, A_subset, T_orig)

# threshold = 0.16
# k = 20000
# x_loop = np.arange(1, k+1)
# y_error = np.empty(k)
# T_out = []
# for i in tqdm(range(k)):
#     A, A_subset, B, T_orig = gen_points(100, 20, 10, 0.1) 
#     B = add_noise(B, stddev = 0.01)
#     B = add_outliers(B, 0.1)
#     T = SPR(B, A, iter_num=30, threshold = threshold, angel=10)
#     y_error[i] = o3d.pipelines.registration.evaluate_registration(B, A_subset, threshold, T).inlier_rmse
#     # draw_registration_result(B, A_subset, T)
#     if y_error[i] >0.05:
#         T_out.append(T)
# plt.plot(x_loop, y_error)
# plt.xlabel('Iteration')
# plt.ylabel('Error')
# plt.show()
# print(len(T_out)/k)
# for j in range(len(T_out)):
#     draw_registration_result(B, A_subset, T_out[j])
#     print(o3d.pipelines.registration.evaluate_registration(B, A_subset, threshold, T_out[j]))

# for i  in tqdm(range(k)):
#     # Initialize the transformation matrix

#     A, A_subset, B, T_orig = gen_points(100, 20, 10, 0.1) 
#     T_init = np.eye(4)
#     B = add_noise(B, stddev = 0.01)
#     B = add_outliers(B, 0.1)

#     A_array = np.asarray(A.points)
#     B_array = np.asarray(B.points)
    
#     # Calculate centroids of point clouds A and B
#     cen_A = np.mean(A_array, axis=0)
#     cen_B = np.mean(B_array, axis=0)
    
#     # Set the initial translation vector of the transformation matrix
#     T_init[:3, 3] = cen_B - cen_A

#     ICP = o3d.pipelines.registration.registration_icp(B, A, threshold, T_init)
#     ICP_T = ICP.transformation
#     # print(ICP.inlier_rmse)
#     y_error[i] = o3d.pipelines.registration.evaluate_registration(B, A_subset, threshold, ICP_T).inlier_rmse
#     print(o3d.pipelines.registration.evaluate_registration(B, A_subset, threshold, ICP_T))
#     draw_registration_result(B, A_subset, ICP_T)

# plt.plot(x_loop, y_error)
# plt.xlabel('Iteration')
# plt.ylabel('Error')
# plt.show()    
