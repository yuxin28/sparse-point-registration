import numpy as np
import open3d as o3d
import copy

def dense_points(point_cloud1):    

    number_points = len(point_cloud1.points) 

    point_cloud1 = np.asarray(point_cloud1.points)
    
    # 生成随机点坐标，注意这里的坐标值范围较小
    point_cloud2 = copy.deepcopy(point_cloud1)
    point_cloud3 = copy.deepcopy(point_cloud1)

    points_near1 = np.random.rand(number_points, 3) * 0.005
    point_cloud2 = point_cloud2 + points_near1

    points_near2 = np.random.rand(number_points, 3) * 0.005
    point_cloud3 = point_cloud3 + points_near2

    combined_point_cloud = np.vstack((point_cloud2, point_cloud3))

    combined_point_cloud = o3d.utility.Vector3dVector(combined_point_cloud)

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(combined_point_cloud)
    return point_cloud



def gen_points(points_num, subset_num, rotation_angle):
    """
    Generates random 3D points and creates a point cloud object and its subset point cload using Open3D.

    Args:
        points_num (int): The total number of random points to generate.
        subset_num (int): The number of points to randomly select from the generated points.

    Returns:
        pcd (open3d.geometry.PointCloud): The point cloud object containing all generated points.
        selected_points (open3d.geometry.PointCloud): The subset of points randomly selected from the point cloud.
    """

    dense_points_num = np.random.randint(10, 20)
    points_num = points_num - dense_points_num * 2
    # Generate 3D random points
    points = np.random.rand(points_num, 3) * 0.25


    # Create a point cloud object
    pcd = o3d.geometry.PointCloud()

    # Assign the generated points to the point cloud object
    pcd.points = o3d.utility.Vector3dVector(points)

    # Randomly select 'subset_num' points from the point cloud

    dense_point_subset_num = np.random.randint(1, 5) #3个点的数量   

    dense_point_indices = np.random.choice(np.arange(points_num), size=dense_points_num, replace=False)    #选出dense点的索引
    sparse_point_indices = np.setdiff1d(np.arange(points_num), dense_point_indices)   #剩下的sparse点索引
    sparse_point_indices_subset = np.random.choice(sparse_point_indices, subset_num - 3 * dense_point_subset_num, replace=False)   #选出sparse点的subset索引
    dense_point_indices_subset = np.random.choice(dense_point_indices, dense_point_subset_num, replace=False)    #选出dense点的subset索引
    dense_point_indices_diff = np.setdiff1d(dense_point_indices, dense_point_indices_subset)   #剩下的dense点索引

    dense_point_diff = pcd.select_by_index(dense_point_indices_diff)   #dense点
    dense_point_diff_1 = dense_points(dense_point_diff)   #dense点的subset
    dense_point_diff += dense_point_diff_1
    dense_point_subset = pcd.select_by_index(dense_point_indices_subset)   #dense点subset
    dense_point_subset_1 = dense_points(dense_point_subset)   #dense点的subset
    dense_point_subset += dense_point_subset_1
    sparse_point_subset = pcd.select_by_index(sparse_point_indices_subset)   #sparse点subset

    pcd += dense_point_diff_1 + dense_point_subset_1
    selected_points= dense_point_subset + sparse_point_subset

    transformed_points = copy.deepcopy(selected_points)

    T = random_transform(np.random.rand() * 360, np.random.rand() * 2)
    T_rev = np.linalg.inv(T) 
    T_rev = T_rev / T_rev[3,3]

    transformed_points = transformed_points.transform(T)

    return pcd, selected_points, transformed_points, T_rev



def random_transform(rotation_angle, translation_size):
    """
    Generates a random 4x4 transformation matrix with specified rotation angle and translation size.

    Args:
        rotation_angle (float): Maximum rotation angle(degree) in degrees for each axis (x, y, z).
        translation_size (float): Maximum translation size for each axis (x, y, z).

    Returns:
        transform_matrix (numpy.ndarray): Randomly generated 4x4 transformation matrix.
    """
    transform_matrix = np.eye(4)

    # Generate random Euler angles for rotation around x, y, and z axes
    theta_x = np.random.rand() * rotation_angle * np.pi / 180
    theta_y = np.random.rand() * rotation_angle * np.pi / 180
    theta_z = np.random.rand() * rotation_angle * np.pi / 180

    # Create rotation matrices for each axis
    rotation_x = np.array([[1, 0, 0],
                           [0, np.cos(theta_x), -np.sin(theta_x)],
                           [0, np.sin(theta_x), np.cos(theta_x)]])

    rotation_y = np.array([[np.cos(theta_y), 0, np.sin(theta_y)],
                           [0, 1, 0],
                           [-np.sin(theta_y), 0, np.cos(theta_y)]])

    rotation_z = np.array([[np.cos(theta_z), -np.sin(theta_z), 0],
                           [np.sin(theta_z), np.cos(theta_z), 0],
                           [0, 0, 1]])

    # Combine the rotation matrices to get the final rotation matrix
    transform_matrix[:-1, :-1] = rotation_z @ rotation_y @ rotation_x

    # Generate a random translation vector
    translation_vector = np.random.rand(3, 1) * translation_size
    transform_matrix[0:3, 3] = translation_vector.flatten()

    return transform_matrix

# pcd, selected_points, transformed_points, T_rev = gen_points(100, 20, 20)
# pcd.paint_uniform_color([1, 0.706, 0])
# selected_points.paint_uniform_color([0, 0.651, 0.929])
# transformed_points.paint_uniform_color([0, 0, 1])
# o3d.visualization.draw_geometries([pcd, selected_points])









