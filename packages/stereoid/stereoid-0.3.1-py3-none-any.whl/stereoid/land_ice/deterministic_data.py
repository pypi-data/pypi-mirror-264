import numpy as np


class DeterministicData():

    @staticmethod
    def density2transmissivity(polarisation='horizontal'):
        """
        Create a fit for horizontal or vertical polarisation to translate density to transmissivity.
        Data taken from: Fujita, S.; Hirabayashi, M.; Goto-Azuma, K.; Dallmayr, R.; Satow, K.; Zheng, J.; Dahl-Jensen, D. Densification
        of Layered Firn of the Ice Sheet at NEEM, Greenland. J. Glaciol. 2014, 60, 905–921.

        :param polarisation:
        :return:
        """

        density = [334,317,344,358,410,438,452,537,549,556,604,606,611,650,659,658,705,706,703,738,747,757,784,789,799,
                   809,823,806,843,835,840,859,857,861,869,871,872]
        e_v = [1.705,1.638,1.688,1.723,1.863,1.911,1.917,2.165,2.172,2.183,2.302,2.310,2.314,2.423,2.441,2.452,2.559,
               2.563,2.565,2.652,2.675,2.704,2.781,2.800,2.821,2.870,2.895,2.848,2.957,2.939,2.952,3.011,3.019,2.990,
               3.061,3.043,3.056]
        e_v_std = [0.045,0.059,0.071,0.050,0.038,0.036,0.048,0.031,0.028,0.028,0.018,0.017,0.034,0.019,0.024,0.024,
                   0.034,0.034,0.044,0.038,0.044,0.046,0.050,0.034,0.042,0.046,0.031,0.046,0.040,0.025,0.047,0.026,
                   0.031,0.041,0.021,0.016,0.018]
        e_h = [1.647,1.594,1.637,1.664,1.795,1.862,1.873,2.138,2.149,2.164,2.288,2.292,2.301,2.405,2.421,2.435,2.542,
               2.546,2.551,2.635,2.663,2.691,2.768,2.786,2.807,2.856,2.884,2.833,2.944,2.926,2.939,2.999,3.008,2.977,
               3.051,3.033,3.044]
        e_h_std = [0.038,0.057,0.058,0.046,0.033,0.036,0.036,0.031,0.027,0.021,0.019,0.018,0.030,0.019,0.025,0.024,
                   0.035,0.037,0.045,0.042,0.045,0.047,0.051,0.036,0.043,0.049,0.029,0.048,0.042,0.028,0.049,0.027,
                   0.030,0.042,0.021,0.018,0.019]

        if polarisation == 'horizontal':
            density2transmissivity = np.polyfit(density, e_h, 2)
        elif polarisation == 'vertical':
            density2transmissivity = np.polyfit(density, e_v, 2)
        else:
            raise TypeError('Only horizontal and vertical polarizations possible.')

        return density2transmissivity

    @staticmethod
    def penetration_depth_from_ice_type(ice_type, radar_type='C_band'):
        """
        Penetration depths of different ice types.

        Possible types are:
        - dry snow zone
        - percolation zone
        - wet snow zone
        - ablation zone

        :param ice_type:
        :param radar_type:
        :return:
        """

        # Data taken from 'Characterization of Snow Facies in the Greenland Ice Sheet observed by TanDEM-X
        # Interferometric SAR Data' Rizzole et al. 2017
        data = dict()
        data['dry_snow'] = [5.38, 1.90]
        data['percolation'] = [4.70, 1.49]
        data['wet_snow'] = [3.89, 1.54]
        data['ablation'] = [3.74, 2.32]

        penetration_depth = data[ice_type][0]
        std_penetration_depth = data[ice_type][0]

        if radar_type == 'C_band':
            # In case of C band penetration depths are doubled. H. Rott, K. Sturm and H. Miller, “Active and passive
            # microwave signatures of Antarctic firn by means of field measurements and satellite data”, Annals of
            # Glaciology, 17, 337-343, 1993
            penetration_depth *= 2
            std_penetration_depth *= 2

        return penetration_depth, std_penetration_depth

    @staticmethod
    def load_ENVEO_poly():
        """
        Loads the polynomial for deterministic functions from ENVEO documentation

        :return: polynomials for VV and VH for 4 different ice zones.
        """

        poly_enveo = dict()
        poly_enveo['glacier_ice'] = dict()
        poly_enveo['percolation_zone'] = dict()
        poly_enveo['dry_snow_zone'] = dict()
        poly_enveo['wet_snow'] = dict()

        # Glacier ice
        poly_enveo['glacier_ice']['VV'] = [16.893, -34.352, 10.883, -5.0762]
        poly_enveo['glacier_ice']['VV_std'] = [17.503, -36.345, 14.487, -10.114]
        poly_enveo['glacier_ice']['VH'] = [9.7529, -17.469, 1.1148, -13.481]

        # Percolation zone
        poly_enveo['percolation_zone']['VV'] = [13.410, -30.483, 9.1681, -0.8095]
        poly_enveo['percolation_zone']['VV_std'] = [14.020, -32.476, 12.771, -5.476]
        poly_enveo['percolation_zone']['VH'] = [2.6142, -11.607, 3.747, -6.8143]

        # Dry snow zone
        poly_enveo['dry_snow_zone']['VV'] = [-16.545, 55.394, -68.528, 12.303]        # Amundsen Ice
        poly_enveo['dry_snow_zone']['VV_2'] = [-31.697, 88.691, -88.284, 8.7173]        # Base camp
        poly_enveo['dry_snow_zone']['VH'] = [-11.320, 38.628, -50.701, -4.8256]         # Amundsen Ice

        # Wet snow
        poly_enveo['wet_snow']['VV'] = [-26.995, 75.739, -77.468, 8.42238]
        poly_enveo['wet_snow']['VV_std'] = [-21.857, 63.663, -66.923, 1.9905]
        poly_enveo['wet_snow']['VH'] = [4.8764, -11.138, 3.1056, -32.562]

        return poly_enveo

    @staticmethod
    def backscatter_wet_snow():
        pass
