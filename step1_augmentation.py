import os
import numpy as np
import vtk
from vedo import *

def GetVTKTransformationMatrix(rotate_X=[-180, 180], rotate_Y=[-180, 180], rotate_Z=[-180, 180],
                               translate_X=[-10, 10], translate_Y=[-10, 10], translate_Z=[-10, 10],
                               scale_X=[0.8, 1.2], scale_Y=[0.8, 1.2], scale_Z=[0.8, 1.2]):
    '''
    get transformation matrix (4*4)
    return: vtkMatrix4x4
    '''
    Trans = vtk.vtkTransform()

    ry_flag = np.random.randint(0,2) #if 0, no rotate
    rx_flag = np.random.randint(0,2) #if 0, no rotate
    rz_flag = np.random.randint(0,2) #if 0, no rotate
    if ry_flag == 1:
        # rotate along Yth axis
        Trans.RotateY(np.random.uniform(rotate_Y[0], rotate_Y[1]))
    if rx_flag == 1:
        # rotate along Xth axis
        Trans.RotateX(np.random.uniform(rotate_X[0], rotate_X[1]))
    if rz_flag == 1:
        # rotate along Zth axis
        Trans.RotateZ(np.random.uniform(rotate_Z[0], rotate_Z[1]))

    trans_flag = np.random.randint(0,2) #if 0, no translate
    if trans_flag == 1:
        Trans.Translate([np.random.uniform(translate_X[0], translate_X[1]),
                         np.random.uniform(translate_Y[0], translate_Y[1]),
                         np.random.uniform(translate_Z[0], translate_Z[1])])

    scale_flag = np.random.randint(0,2)
    if scale_flag == 1:
        Trans.Scale([np.random.uniform(scale_X[0], scale_X[1]),
                     np.random.uniform(scale_Y[0], scale_Y[1]),
                     np.random.uniform(scale_Z[0], scale_Z[1])])

    matrix = Trans.GetMatrix()

    return matrix


if __name__ == "__main__":

    num_samples = 40 # need to define # of samples; e.g., 30
    vtk_path = '/content/data' # need to define the path; e.g., src
    list_dirs = os.listdir(vtk_path)
    output_save_path = './augmentation_vtk_data'
    if not os.path.exists(output_save_path):
        os.mkdir(output_save_path)

    sample_list = list(range(1, num_samples+1))
    print(sample_list)
    num_augmentations = 20

    for i_sample in sample_list:
        for i_aug in range(num_augmentations):

            file_name = list_dirs[i_sample]
            name = file_name.split('.')[0]
            output_file_name = f'{name}_aug{i_aug}_sample_0{i_sample}_d.vtp'
            vtk_matrix = GetVTKTransformationMatrix(rotate_X=[-180, 180], rotate_Y=[-180, 180], rotate_Z=[-180, 180],
                                                  translate_X=[-10, 10], translate_Y=[-10, 10], translate_Z=[-10, 10],
                                                  scale_X=[0.8, 1.2], scale_Y=[0.8, 1.2], scale_Z=[0.8, 1.2]) #use default random setting
            mesh = load(os.path.join(vtk_path, file_name))
            mesh.applyTransform(vtk_matrix)
            io.write(mesh, os.path.join(output_save_path, output_file_name))

        #flipped mesh
        for i_aug in range(num_augmentations):
            file_name = list_dirs[i_sample].format(i_sample+1000)
            output_file_name = f'{name}{i_aug}_sample_0{i_sample+1000}_d.vtp'
            vtk_matrix = GetVTKTransformationMatrix(rotate_X=[-180, 180], rotate_Y=[-180, 180], rotate_Z=[-180, 180],
                                                  translate_X=[-10, 10], translate_Y=[-10, 10], translate_Z=[-10, 10],
                                                  scale_X=[0.8, 1.2], scale_Y=[0.8, 1.2], scale_Z=[0.8, 1.2]) #use default random setting
            mesh = load(os.path.join(vtk_path, file_name))
            mesh.applyTransform(vtk_matrix)
            io.write(mesh, os.path.join(output_save_path, output_file_name))
