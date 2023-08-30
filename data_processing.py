import open3d as o3d
import numpy as np

def add_noise(point_cloud, mean = 0, stddev = 0.0001):

    # add gaussian noise
    noise = np.random.normal(mean, stddev, size=(len(point_cloud.points), 3))
    noisy_point_cloud_array = np.asarray(point_cloud.points) + noise
    noisy_point_cloud = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(noisy_point_cloud_array))

    return noisy_point_cloud

def add_outliers(point_cloud, rotio_outliers = 0.1):

    Size = np.max(np.ptp(np.asarray(point_cloud.points)), axis=0)

    # add random outliers
    num_outliers = int(len(point_cloud.points) * rotio_outliers)
    outliers = np.random.rand(num_outliers, 3) * Size
    outlier_point_cloud = point_cloud + o3d.geometry.PointCloud(o3d.utility.Vector3dVector(outliers))


    return outlier_point_cloud

def random_downsampling(point_cloud, number_points):

    # calculate downsampling ratio
    downsamling_ratio = number_points / len(point_cloud.points)

    # random downsampling
    downsampled_point_cloud = point_cloud.random_down_sample(downsamling_ratio)

    return downsampled_point_cloud

def uniform_downsampling(point_cloud, number_points):

    # calculate downsampling ratio
    every_k_points = int(len(point_cloud.points) / number_points)

    # uniform downsampling
    downsampled_point_cloud = point_cloud.uniform_down_sample(every_k_points)

    return downsampled_point_cloud
