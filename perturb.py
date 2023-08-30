import numpy as np

def perturb(size, num_perturbations, current_iteration, max_iterations, angel, translation):
    # Implement your perturbation logic here and return R_p and T_p
    # R_p = np.zeros((3, 3, num_perturbations + 1))
    # T_p = np.zeros((num_perturbations + 1, 3))

    
    # Initial perturbation number of rotation: angel degrees normal distribution (Right hand coordinate system)
    # Around x, y, and z
    a = np.random.normal(0, angel * ((max_iterations + 1 - current_iteration) / max_iterations), num_perturbations)
    b = np.random.normal(0, angel * ((max_iterations + 1 - current_iteration) / max_iterations), num_perturbations)
    c = np.random.normal(0, angel * ((max_iterations + 1 - current_iteration) / max_iterations), num_perturbations)
    
    # Convert to radians
    a = a * (np.pi / 180)
    b = b * (np.pi / 180)
    c = c * (np.pi / 180)
    
    # Initialize T_P
    T_p = np.zeros((num_perturbations + 1, 4, 4))    # num_perturbations+1: Transformation without disturbance
    T_p[-1] = np.eye(4)                              # T_p[-1]: Transformation without disturbance
    T_p[:, -1, -1] = 1                               # T_p[:, -1, -1]: Homogeneous coordinates
    
    # Generate num_perturbations disturbances respectively
    for j in range(num_perturbations):
        # Rotation matrices
        r1 = np.array([[1, 0, 0], [0, np.cos(a[j]), -np.sin(a[j])], [0, np.sin(a[j]), np.cos(a[j])]])
        r2 = np.array([[np.cos(b[j]), 0, np.sin(b[j])], [0, 1, 0], [-np.sin(b[j]), 0, np.cos(b[j])]])
        r3 = np.array([[np.cos(c[j]), -np.sin(c[j]), 0], [np.sin(c[j]), np.cos(c[j]), 0], [0, 0, 1]])
        
        # Perturbation Rotation
        T_p[j, :3, :3] = np.dot(np.dot(r1, r2), r3)

    # Initial translation disturbance: translation ratio
    T_p[:-1, : 3, 3] = np.random.normal(0, translation * size * ((max_iterations + 1 - current_iteration) / max_iterations), (num_perturbations, 3))    

    
    return T_p
