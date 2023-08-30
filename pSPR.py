import numpy as np
import open3d as o3d
import copy
import matplotlib.pyplot as plt

def dSPR(A, B, perturb_num=15, iter_num=12, RMS_ratio=0.005, bDQF_step=15):
    '''A function to perform dSPR (Stochastic Perturbation Registration) on two point clouds.
    A and B are the point clouds to be registered, perturb_num is the number of perturbations
    to be applied to the transformation matrix, iter_num is the maximum number of iterations,
    RMS is the root mean square error threshold, and threshold is the threshold for ICP
    (Iterative Closest Point) registration.'''

    # Convert point clouds A and B to NumPy arrays
    A_array = np.asarray(A.points)
    B_array = np.asarray(B.points)
    
    # Calculate the size of B along each axis
    Size = np.max(np.ptp(B_array, axis=0))
    
    # Initialize the transformation matrix
    T_init = np.eye(4)
    
    # Calculate centroids of point clouds A and B
    cen_A = np.mean(A_array, axis=0)
    cen_B = np.mean(B_array, axis=0)
    
    # Set the initial translation vector of the transformation matrix
    T_init[:3, 3] = cen_B - cen_A
    
    # Evaluate the registration using the initial transformation matrix
    # e = o3d.pipelines.registration.evaluate_registration(A, B, threshold, T_init).inlier_rmse
    e = np.inf
    RMS = RMS_ratio * Size
    
    # Initialize iteration variables
    k = 1
    x_loop = np.arange(1, iter_num + 1)
    y_error = np.zeros(iter_num)
    T = copy.deepcopy(T_init)
    T_j_hat = copy.deepcopy(T_init)
    # cost_best = np.inf
    
    # Iterate while the error is greater than RMS and within the iteration limit
    while e > RMS and k <= iter_num:
        T_k = T
        # Generate perturbations for transformation matrix
        T_p = perturb(Size, perturb_num, k, iter_num, angel, translation=translation)

        #create list to store perturbed transformation matrices and errors
        T_j_hat_list = []
        error_j_list = []
        
        # Iterate through perturbations
        for j in range(perturb_num + 1):
            # Apply perturbation to the transformation matrix
            T_j_hat[:-1, :-1] = np.dot(T_p[j, :-1, :-1], T[:-1, :-1])
            T_j_hat[:-1, -1] = T[:-1, -1] + T_p[j, :-1, -1]
            T_j_hat_list.append(T_j_hat)

            # Evaluate registration quality
            error_j = o3d.pipelines.registration.evaluate_registration(A, B, threshold, T_j_hat).inlier_rmse
            error_j_list.append(error_j)

        #find the best perturbation
        index = np.argmin(np.asarray(error_j_list))
        T_k_hat = T_j_hat_list[index]
            
        # Perform ICP registration with the best perturbation
        res = o3d.pipelines.registration.registration_icp(A, B, threshold, T_k_hat,
            o3d.pipelines.registration.TransformationEstimationPointToPoint(),
            o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=20))
        T_k = res.transformation
        error_k = res.inlier_rmse
            
            # Evaluate registration quality
            # evaluation = o3d.pipelines.registration.evaluate_registration(A, B, threshold, T_j)
            # error_k = evaluation.inlier_rmse
            
            # Update best cost and transformation if the current cost is better
        # if error_k < e:
        #         cost_best = error_k
        #         T_k = T_j
        
        # e_k = cost_best
        
        # Update error and transformation if the new error is lower
        if error_k < e:
            e = error_k
            T = T_k
        
        # Store error for plotting
        y_error[k - 1] = e
        k += 1
    
    # Plot error over iterations
    # plt.plot(x_loop, y_error)
    # plt.xlabel('Iteration')
    # plt.ylabel('Error')
    # plt.show()
    
    # Return the final transformation matrix
    return T
