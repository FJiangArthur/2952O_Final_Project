import numpy as np

# Input: expects Nx3 matrix of points
# Returns R,t
# R = 3x3 rotation matrix
# t = 3x1 column vector

# P_B is the coordinate system in Mirobot
# P_A is the coordinate system in our camera view
# P_B = P_A * R + t
def rigid_transform_3D(A, B):
    assert len(A) == len(B)

    N = A.shape[0]  # total points
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    # centre the points
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))

    H = np.matmul(np.transpose(AA),BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.matmul(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
        print("Reflection detected")
        Vt[2, :] *= -1
        R = np.matmul(Vt.T,U.T)

    t = -np.matmul(R, centroid_A) + centroid_B
    # err = B - np.matmul(A,R.T) - t.reshape([1, 3])
    return R, t


if __name__=='__main__':
	a = np.array([[90, -212, 1856],
                  [145, -220, 859],
                  [0.074728, -0.081546, 0.895]])


    b = np.array([[20, -15, 0],
                  [20, 20, 0],
                  [0.38551146, 0.51143277, 0.28599533]])

  	c = np.reshape(a[-2:], (2, 3))
    test_a1 = np.reshape(c[0],(1,3))
    test_a2 = np.reshape(c[1],(1,3))

    c=np.reshape(b[-2:], (2, 3))
    test_b1 = np.reshape(c[0],(1,3))
    test_b2 = np.reshape(c[1],(1,3))

    a = a[:-2]
    b = b[:-2]
    r, t = rigid_transform_3D(a, b)
    print('r:',r)
    print('t:',t)

    bb = np.matmul(a, r.T) + t.reshape([1, 3])
    print('b-bb:', b - bb)

    c = np.matmul(test_a1, r.T) + t.reshape([1, 3])
    print('c-test_b1:', c - test_b1)

    c = np.matmul(test_a2, r.T) + t.reshape([1, 3])
    print('c-test_b2:', c - test_b2)

