import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from citros_data_analysis import data_access as da
from citros_data_analysis import error_analysis as analysis
from prettytable import PrettyTable, ALL
from navigation_error_class import NavigationErrorCalculation 

nec = NavigationErrorCalculation()

class NavigationErrorPlot:

    ###############

    def _create_data_bases(self, PdData, column_name, unit_lbl, scaling_method, scaling_size, scaling_parameter, re_scaling_factor):

        data_set = analysis.CitrosData(PdData, data_label = column_name, units = unit_lbl)
        if scaling_method == 'scale_data':
            db = data_set.scale_data(n_points = scaling_size, param_label= scaling_parameter)
        else: 
            db = data_set.bin_data(n_bins = scaling_size, param_label = scaling_parameter)

        db.addData = db.addData*re_scaling_factor
        
        return(db)

    def draw_data_base_stats(self, PdData, column_name, unit_lbl, scaling_method, scaling_size, scaling_parameter, dt, title, x_label, y_label, is_two_sigma):
        
        max_rid = max(PdData['rid'])*dt
        data_base = self._create_data_bases(PdData, column_name, unit_lbl, scaling_method, scaling_size, scaling_parameter, max_rid)
        fig, axs = data_base.show_statistics(return_fig = True)

        if isinstance(axs, np.ndarray):
            if (len(axs) > 1) and (y_label.find("Angle") == -1):
                labels = ['X  ','Y  ','Z  ']
            elif (len(axs) > 1) and (y_label.find("Angle") != -1):
                labels = ['Roll ','Pitch ','Yaw ']
            else:
                labels = ['','','']
            for ax,lbl in zip(axs,labels):
                ax.set_xlabel(x_label)
                ax.set_ylabel(lbl + y_label)
                ax.set_title('')
                if not is_two_sigma:
                    ax.lines[-1].remove()
        else:
            axs.set_xlabel(x_label)
            axs.set_ylabel(y_label)
            axs.set_title('')
            if not is_two_sigma:
                axs.lines[-1].remove()
                    
        fig.suptitle(title)
        fig.texts[0].set_visible(False)
        plt.show()
        return(fig)
    
    #################

    def draw_lla_routes(self, gt_lla, est_lla, gt_lla_data_name, est_lla_data_name):
    # Create a figure and axis for the plot
        
        # true_lla,est_lla,_,_ = self._lla_true_vs_est(gt_lla, est_ecef, gt_lla_data_name, est_ecef_data_name, planet_radius)

        fig, ax = plt.subplots()

        sid_count = gt_lla['sid'].unique()
        
        for i in sid_count:
            
            est_lla_df = est_lla[est_lla['sid'] == i]
            gt_lla_df = gt_lla[gt_lla['sid'] == i]

            vec_est_lla = nec._cit_list_2_array(est_lla_df[est_lla_data_name])
            vec_gt_lla = nec._cit_list_2_array(gt_lla_df[gt_lla_data_name])

            if type(vec_gt_lla[0][0]) != "<class 'numpy.float64'>":
                true_lla_arr = np.array(vec_gt_lla, dtype=np.float64)
            if type(vec_est_lla[0][0]) != "<class 'numpy.float64'>":
                est_lla_arr = np.array(vec_est_lla, dtype=np.float64)

             # Plot the true latitude-longitude route in black
            ax.plot(true_lla_arr[:, 1], true_lla_arr[:, 0], c='black', label='True LLA')

            # Plot each array in est_lla
            # for est_array in est_lla:
                    
            ax.plot(est_lla_arr[:, 1], est_lla_arr[:, 0])#, label=f'Estimate {i + 1}')

        # Set labels for the axes
        ax.set_xlabel('Longitude [Rad]')
        ax.set_ylabel('Latitude [Rad]')

        # Set the title of the plot
        ax.set_title('True LLA vs. Estimated LLA')

        # Add a legend to distinguish between true_lla and est_lla
        ax.legend(loc='upper right')

        # Show the plot
        plt.show()
        return(fig)

    #################

