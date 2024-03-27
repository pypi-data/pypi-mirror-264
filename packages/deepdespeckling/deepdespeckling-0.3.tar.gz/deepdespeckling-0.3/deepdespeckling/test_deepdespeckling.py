from deepdespeckling.despeckling import despeckle, despeckle_from_coordinates, despeckle_from_crop

image_path = "/Users/hadrienmariaccia/Documents/Projects/deepdespeckling/img/entire/sar2sar_tests"
destination_directory = "/Users/hadrienmariaccia/Documents/Projects/deepdespeckling/img/entire/sar2sar_tests"
coordinates_dictionnary = {'x_start': 0,
                           'y_start': 0, 'x_end': 1500, 'y_end': 1500}

"""despeckle_from_crop(image_path, destination_directory_path=destination_directory,
                    model_name="sar2sar")"""

despeckle_from_coordinates(image_path, coordinates_dict=coordinates_dictionnary,
                           destination_directory_path=destination_directory,
                           model_name="sar2sar", symetrise=True)
