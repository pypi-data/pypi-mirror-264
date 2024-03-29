import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from citros_data_analysis import data_access as da
from citros_data_analysis import error_analysis as analysis
from prettytable import PrettyTable, ALL


class NavigationErrorCalculation():

    def get_var(self, citros, var_name, topic_name, data_name, sid_list=None, rid_ind=None):

        if (sid_list == None) or (citros.info()['sid_count'] < len(sid_list)):
            sid_count = list(range(citros.info()['sid_count']))
        else:
            sid_count = sid_list
 
        
        if rid_ind == None:

            val = citros.topic(topic_name).set_order({'sid':'asc','rid':'asc'}).sid(sid_count).data(data_name)
        else:
            val = citros.topic(topic_name).set_order({'sid':'asc','rid':'asc'}).sid(sid_count).rid(start = rid_ind[0], end = rid_ind[1]).data(data_name)


        setattr(self, var_name, val)


    #################


    def _get_var_data(self, citros, i, topic, var_name, rid_ind=None):
       
        if rid_ind == None:
            var_data = citros.topic(topic).set_order({'sid':'asc','rid':'asc'}).sid(i).data(var_name)[var_name]
        else:
            var_data = citros.topic(topic).set_order({'sid':'asc','rid':'asc'}).sid(i).rid(start = rid_ind[0], end = rid_ind[1]).data(var_name)[var_name]

        return(var_data)

    #################

    def _array_2_cit_list(self, arr):

        cit_list = []
        for row in arr: 
            
            cit_list.append(list(row))

        return(cit_list)
    
    #################

    def _cit_list_2_array(self, cit_list):

        arr = []
        for row in cit_list: 
            arr.append(np.array(row))
            # print(np.array(row))
        arr = np.array(arr)
        return(arr)
    
    #################

    def _massage_count(self, citros, sid_list, topic):

        if (citros.info()['sid_count'] < len(sid_list)):
            sid_count = list(range(citros.info()['sid_count']))
        else:
            sid_count = sid_list

        msg_count = np.zeros(len(sid_count))

        for i in sid_count:
            
            inf = citros.sid(sid_count).info()
            
            msg_count[i] = inf['sids'][i]['topics'][topic]['message_count']

        return(msg_count)

    ##################

    def quat_diff(self, q1,q2):


        q1_conj = np.array([q1[0], -q1[1],-q1[2],-q1[3]])
        q_difference = np.zeros(4)
        
        q_difference[0] = q1_conj[0] * q2[0] - q1_conj[1] * q2[1] - q1_conj[2] * q2[2] - q1_conj[3] * q2[3]
        q_difference[1] = q1_conj[0] * q2[1] + q1_conj[1] * q2[0] + q1_conj[2] * q2[3] - q1_conj[3] * q2[2]
        q_difference[2] = q1_conj[0] * q2[2] - q1_conj[1] * q2[3] + q1_conj[2] * q2[0] + q1_conj[3] * q2[1]
        q_difference[3] = q1_conj[0] * q2[3] + q1_conj[1] * q2[2] - q1_conj[2] * q2[1] + q1_conj[3] * q2[0]

        angular_error = 2*np.arccos(abs(q_difference[0]))

        return(angular_error,q_difference)

        ###############

    def dcm_to_euler_angles(self, dcm):
    # Calculate pitch
        if isinstance(dcm, list): 
            dcm = np.array(dcm)
        if dcm[2, 0] < 1:
            if dcm[2, 0] > -1:
                pitch = np.arcsin(-dcm[2, 0])
                yaw = np.arctan2(dcm[1, 0], dcm[0, 0])
                roll = np.arctan2(dcm[2, 1], dcm[2, 2])
            else:
                pitch = np.pi / 2
                yaw = -np.arctan2(-dcm[0, 1], dcm[0, 2])
                roll = 0
        else:
            pitch = -np.pi / 2
            yaw = np.arctan2(-dcm[0, 1], dcm[0, 2])
            roll = 0

        return(roll, pitch, yaw)

    ###############

    def quat2dcm(self, q):
    # Normalize the quaternion if necessary
        q /= np.linalg.norm(q)
        
        # Extract quaternion components
        w, x, y, z = q
        
        # Calculate rotation matrix elements
        r00 = 1 - 2*y*y - 2*z*z
        r01 = 2*x*y - 2*w*z
        r02 = 2*x*z + 2*w*y
        r10 = 2*x*y + 2*w*z
        r11 = 1 - 2*x*x - 2*z*z
        r12 = 2*y*z - 2*w*x
        r20 = 2*x*z - 2*w*y
        r21 = 2*y*z + 2*w*x
        r22 = 1 - 2*x*x - 2*y*y
        
        # Construct the rotation matrix
        matrix = np.array([[r00, r01, r02],
                        [r10, r11, r12],
                        [r20, r21, r22]])
        
        return(matrix)

    ###############

    def dcm2quat(self, dcm):

        if isinstance(dcm, list): 
            dcm = np.array(dcm)

        quat_array = []

        eta = 0.0025 # % eta is a threshhold parameter set to help with numerical accuracy,
                    #for more on the subject read: "Accurate Computation of Quaternions from Rotation Matrices" 
                    # https://upcommons.upc.edu/bitstream/handle/2117/124384/2068-Accurate-Computation-of-Quaternions-from-Rotation-Matrices.pdf?sequence=1
        
        q = [0,0,0,0]

        r11 = dcm[0,0]
        r12 = dcm[0,1]
        r13 = dcm[0,2]
        r21 = dcm[1,0]
        r22 = dcm[1,1]
        r23 = dcm[1,2]
        r31 = dcm[2,0]
        r32 = dcm[2,1]
        r33 = dcm[2,2]

        # q0
        if ((r11 + r22 + r33) > eta):
            q[0]= 0.5*np.sqrt(1 + r11 + r22 + r33)
        else:
            num0 = (r32 - r23)**2 + (r13 - r31)**2 + (r21 - r12)**2 
            denum0 = 3 - r11 - r22 - r33
            q[0] = 0.5*np.sqrt(num0 / denum0)

        # q1
        if ((r11 - r22 - r33) > eta):
            q[1]= 0.5*np.sqrt(1 + r11 - r22 - r33)
        else:
            num1 = (r32 - r23)**2 + (r12 + r21)**2 + (r31 + r13)**2
            denum1 = 3 - r11 + r22 + r33
            q[1] = 0.5*np.sqrt(num1 / denum1)
        q[1] = q[1]*self._quat_sign(r23-r32)
        
        # q2
        if ((- r11 + r22 - r33) > eta):
            q[2] = 0.5*np.sqrt(1 - r11 + r22 - r33)
        else:
            num2 = (r13 - r31)**2 + (r12 + r21)**2 + (r23 + r32)**2  
            denum2 = 3 + r11 - r22 + r33
            q[2] = 0.5*np.sqrt(num2 / denum2 )
        q[2] = q[2]*self._quat_sign(r31-r13)

        # q3
        if ((- r11 - r22 + r33) > eta):
            q[3]= 0.5*np.sqrt(1 - r11 - r22 + r33)
        else:
            num3 = (r12 - r21)**2 + (r31 + r13)**2 + (r32 + r23)**2 
            denum3 = 3 + r11 + r22 - r33
            q[3] = 0.5*np.sqrt(num3 / denum3)
        q[3] = q[3]*self._quat_sign(r12-r21)

        return q


    def _quat_sign(self, x):
        s = 1
        if x<-1e-10:
            s =-1
        return s 


    ###############

    def _ecef2lla(self, r_ecef, r_planet):

        l = r_ecef.shape[0]
        lla = np.zeros([l, 3])
        r = np.linalg.norm(r_ecef, axis=1)  # Calculate the norm along axis 1

        lla[:, 0] = np.arcsin(r_ecef[:, 2] / r)
        lla[:, 1] = np.arctan2(r_ecef[:, 1], r_ecef[:, 0])
        lla[lla[:, 1] > np.pi, 1] -= 2 * np.pi

        lla[:, 2] = r - r_planet

        return lla

    ###############

    def ecef2lla(self, r_ecef, r_ecef_data_name, planet_radius, data_name):

        lla = []
        sid = []
        rid = []

        sid_count = r_ecef['sid'].unique()

        for i in sid_count:
            
            ecef_df = r_ecef[r_ecef['sid'] == i]

            vec_ecef = self._cit_list_2_array(ecef_df[r_ecef_data_name])

            if type(vec_ecef[0][0]) != "<class 'numpy.float64'>":
                r_ecef_est = np.array(vec_ecef, dtype=np.float64)


            l = len(r_ecef_est)
            
            lla.append(self._ecef2lla(r_ecef_est, planet_radius))

            sid.append(np.full(l, i, dtype=int))
            rid.append(list(range(0,l)))
        
        sid = self._list_2_pd_data_frame(sid, 'sid')
        sid = self._list_2_pd_data_frame(rid, 'rid', sid)
        lla = self._list_2_pd_data_frame(lla, data_name, sid)
        
        setattr(self, data_name, lla)

    ###############

    def _lla2ecef(self, lla, r_planet):

        l = lla.shape[0]
        r_ecef = np.zeros([l, 3])
        r =  r_planet + lla[:,2]

        r_ecef[:, 0] = np.cos(lla[:,0])*np.cos(lla[:,1])*(r_planet + lla[:,2])
        r_ecef[:, 1] = np.cos(lla[:,0])*np.sin(lla[:,1])*(r_planet + lla[:,2])
        r_ecef[:,2] = np.sin(lla[:,0])*(r_planet + lla[:,2])

        return r_ecef

    ###############

    def lla2ecef(self, lla, lla_data_name, planet_radius, data_name):

        r_ecef = []
        sid = []
        rid = []

        sid_count = lla['sid'].unique()

        for i in sid_count:
            
            lla_df = lla[lla['sid'] == i]

            vec_lla = self._cit_list_2_array(lla_df[lla_data_name])

            if type(vec_lla[0][0]) != "<class 'numpy.float64'>":
                vec_lla = np.array(vec_lla, dtype=np.float64)

            l = len(vec_lla)
            
            r_ecef.append(self._lla2ecef(vec_lla, planet_radius))

            sid.append(np.full(l, i, dtype=int))
            rid.append(list(range(0,l)))
        
        sid = self._list_2_pd_data_frame(sid, 'sid')
        sid = self._list_2_pd_data_frame(rid, 'rid', sid)
        r_ecef = self._list_2_pd_data_frame(r_ecef, data_name, sid)
        
        setattr(self, data_name, r_ecef)
    
    ###############

    def _lla2ned_dcm(self, lat, long):

        l = len(lat)

        csLAT = np.cos(lat)
        snLAT = np.sin(lat)
        csLONG = np.cos(long)
        snLONG = np.sin(long)

        row_array_0 = np.stack([-snLAT*csLONG , -snLAT*snLONG, csLAT], axis=-1)
        row_array_1 = np.stack([-snLONG,   csLONG,  np.zeros(l)], axis=-1)
        row_array_2 = np.stack([ -csLAT*csLONG, -csLAT*snLONG, -snLAT], axis=-1)

        dcm_lla_2_ned = np.stack((row_array_0, row_array_1, row_array_2), axis = -2)

        return(dcm_lla_2_ned)

    #################

    def roll_pitch_yaw_error(self, gt_data, est_data, gt_data_name, est_data_name, name_of_angular_error, quat_or_matrix='quat', name_of_quat_error = ''):


        quat_angular_error = []
        roll_pitch_yaw_error = []
        sid = []
        rid = []

        sid_count = gt_data['sid'].unique()
        
        for i in sid_count:

            angular_error = []
            euler_angles = []

            df_est = est_data[est_data['sid'] == i]
            df_true = gt_data[gt_data['sid'] == i]

            if quat_or_matrix != 'dcm':
                
                q_l2b_true = self._cit_list_2_array(df_true[gt_data_name])
                q_l2b_est = self._cit_list_2_array(df_est[est_data_name])
                
                if type(q_l2b_true[0][0]) != "<class 'numpy.float64'>":
                    q_l2b_true = np.array(q_l2b_true, dtype=np.float64)
                if type(q_l2b_est[0][0]) != "<class 'numpy.float64'>":
                    q_l2b_est = np.array(q_l2b_est, dtype=np.float64)
            
                l = len(q_l2b_true)

                for q_true,q_est in zip(q_l2b_true, q_l2b_est):

                    q_true = np.array(q_true)
                    q_est = np.array(q_est)

                    error_q_angle, q_error = self.quat_diff(q_true,q_est)

                    angular_error.append(error_q_angle)

                    error_dcm = self.quat2dcm(q_error)        

                    roll, pitch, yaw = self.dcm_to_euler_angles(error_dcm)

                    euler_angles.append([roll, pitch, yaw])

                quat_angular_error.append(np.array(angular_error))
                roll_pitch_yaw_error.append(np.array(euler_angles))

                sid.append(np.full(l, i, dtype=int))
                rid.append(list(range(0,l)))

                
            else:
                
                l2b_dcm_true = self._cit_list_2_array(df_true[gt_data_name])
                l2b_dcm_est = self._cit_list_2_array(df_est[est_data_name])
            
                l = len(l2b_dcm_true)

                for dcm_true,dcm_est in zip(l2b_dcm_true, l2b_dcm_est):
                    
                    if type(dcm_true[0][0]) != "<class 'numpy.float64'>":
                        dcm_true = np.array(dcm_true, dtype=np.float64)
                    if type(dcm_est[0][0]) != "<class 'numpy.float64'>":
                        dcm_est = np.array(dcm_est, dtype=np.float64)


                    error_dcm = np.dot(np.transpose(dcm_true), dcm_est)        

                    roll, pitch, yaw = self.dcm_to_euler_angles(error_dcm)

                    euler_angles.append([roll, pitch, yaw])


                quat_angular_error = None
                roll_pitch_yaw_error.append(np.array(euler_angles))
                sid.append(np.full(l, i, dtype=int))
                rid.append(list(range(0,l)))

       
        sid = self._list_2_pd_data_frame(sid, 'sid')
        sid = self._list_2_pd_data_frame(rid, 'rid', sid)
        roll_pitch_yaw_error = self._list_2_pd_data_frame(roll_pitch_yaw_error, name_of_angular_error, sid)
        roll_pitch_yaw_error = self._list_2_pd_data_frame(quat_angular_error, name_of_quat_error, roll_pitch_yaw_error)
        
        setattr(self, name_of_angular_error, roll_pitch_yaw_error)

    ###############

    def vec_error(self, gt_data, est_data, gt_data_name, est_data_name, name_of_error = ''):

        vec_error = []
        sid = []
        rid = []

        sid_count = gt_data['sid'].unique()

        for i in sid_count:
            

            df_est = est_data[est_data['sid'] == i]
            df_true = gt_data[gt_data['sid'] == i]

            vec_est = self._cit_list_2_array(df_est[est_data_name])
            vec_true = self._cit_list_2_array(df_true[gt_data_name])

            if type(vec_true[0][0]) != "<class 'numpy.float64'>":
                vec_true = np.array(vec_true, dtype=np.float64)
            if type(vec_est[0][0]) != "<class 'numpy.float64'>":
                vec_est = np.array(vec_est, dtype=np.float64)
            
            l = len(vec_true)

            vec_error.append(vec_true - vec_est)
            
            sid.append(np.full(l, i, dtype=int))
            rid.append(list(range(0,l)))


        sid = self._list_2_pd_data_frame(sid, 'sid')
        sid = self._list_2_pd_data_frame(rid, 'rid', sid)
        vec_error = self._list_2_pd_data_frame(vec_error, name_of_error, sid)
        
        setattr(self, name_of_error, vec_error)
        

    ###############

    def side_and_down_error(self, vector_data, vector_data_name, vec_name = ' '):
  

        cross_track_error = []
        down_track_error = []
        sid = []
        rid = []
        
        sid_count = vector_data['sid'].unique()

        for i in sid_count:
            
            df = vector_data[vector_data['sid'] == i]
            arr = self._cit_list_2_array(df[vector_data_name])

            cross_track = list(np.linalg.norm(arr[:,:2], axis = 1)) 
            down_track = list(arr[:,2])
            l = len(arr)
 
            cross_track_error.append(cross_track)
            down_track_error.append(down_track)
            sid.append(np.full(l, i, dtype=int))
            rid.append(list(range(0,l)))


        sid = self._list_2_pd_data_frame(sid, 'sid')
        sid = self._list_2_pd_data_frame(rid, 'rid', sid)
        vec_side_down_error = self._list_2_pd_data_frame(cross_track_error, 'side_track_error', sid)
        vec_side_down_error = self._list_2_pd_data_frame(down_track_error, 'down_track_error', vec_side_down_error)

        if vec_name == ' ':
            vec_name = 'side_down_error'

        setattr(self, vec_name, vec_side_down_error)        

    ###############

    def transform_ecef_2_ned(self, lla_gt, lla_gt_name, data_vector_in_ecef, data_vector_in_ecef_name, column_name=' '):


        ned_data = []
        sid = []
        rid = []

        sid_count = lla_gt['sid'].unique()

        for i in sid_count:

            lla_pd = lla_gt[lla_gt['sid'] == i]
            ecef_pd = data_vector_in_ecef[data_vector_in_ecef['sid'] == i]

            lla_vec = self._cit_list_2_array(lla_pd[lla_gt_name])
            ecef_vec = self._cit_list_2_array(ecef_pd[data_vector_in_ecef_name])

            reshaped_data = ecef_vec[:, :, np.newaxis]
            ecef_2_ned_dcm = self._lla2ned_dcm(lla_vec[:,0], lla_vec[:,1])
          
            ned_data.append(np.sum(ecef_2_ned_dcm*reshaped_data, axis=1))

            l = len(lla_vec)

            sid.append(np.full(l, i, dtype=int))
            rid.append(list(range(0,l)))

        if column_name == ' ':
            column_name = "ned_pos_error" 

        sid = self._list_2_pd_data_frame(sid, 'sid')
        sid = self._list_2_pd_data_frame(rid, 'rid', sid)
        data_in_ecef = self._list_2_pd_data_frame(ned_data, column_name, sid)

        setattr(self, column_name, data_in_ecef)        


###################

    def _pd_data_frame_2_arr(self, i, pd_frame, column_name):

        
        data = pd_frame[pd_frame['sid'] == i]
        l = len((data[column_name]))
        m = len(data[column_name].iloc[0])
        arr = np.zeros((l,m))

        for i in range(0,l):
            arr[i,:] = data[column_name].iloc[i]

        return(arr)
    
    ###############

    def _list_2_pd_data_frame(self, data_list, data_name, data_frame=pd.DataFrame()):


        if isinstance(data_list[0], np.ndarray):
            data_frame = pd.concat([data_frame, pd.DataFrame({data_name: list(np.concatenate(data_list))})], axis=1)    
        else:
            data_frame = pd.concat([data_frame, pd.DataFrame({data_name: np.concatenate(data_list)})], axis=1) 


        return(data_frame)
    