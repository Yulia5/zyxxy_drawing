from zyxxy_shapes_demo import run_demo

shapename = "a_double_smile"
shape_params_dict = {'centre_x' : [0, 12, 6], 
                     'width' : [0, 6, 3], 
                     'corners_y' : [0, 10, 8], 
                     'mid1_y' : [0, 10, 6], 
                     'mid2_y' : [0, 10, 5]}

run_demo(shapename=shapename, shape_params_dict=shape_params_dict)

