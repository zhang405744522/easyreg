from __future__ import print_function
import progressbar as pb

from torch.utils.data import Dataset

from data_pre.reg_data_utils import *

from data_pre.oai_longitude_reg import *

class BaseRegDataSet(object):

    def __init__(self, dataset_type, file_type_list, sched=None):
        """

        :param name: name of data set
        :param dataset_type: ''mixed' like oasis including inter and  intra person  or 'custom' like LPBA40, only includes inter person
        :param file_type_list: the file types to be filtered, like [*1_a.bmp, *2_a.bmp]
        :param data_path: path of the dataset
        """

        self.data_path = None
        """path of the dataset"""
        self.output_path = None
        """path of the output directory"""
        self.pro_data_path = None
        self.pair_name_list = []
        self.pair_path_list = []
        self.file_type_list = file_type_list
        self.save_format = 'h5py'
        """currently only support h5py"""
        self.sched = sched
        """inter or intra, for inter-personal or intra-personal registration"""
        self.dataset_type = dataset_type
        """custom or mixed"""
        self.normalize_sched = 'tp'
        """ settings for normalization, currently not used"""
        self.divided_ratio = (0.7, 0.1, 0.2)
        """divided the data into train, val, test set"""

    def generate_pair_list(self):
        pass


    def set_data_path(self, path):
        self.data_path = path

    def set_output_path(self, path):
        self.output_path = path
        make_dir(path)

    def set_normalize_sched(self,sched):
        self.normalize_sched = sched

    def set_divided_ratio(self,ratio):
        self.divided_ratio = ratio

    def get_file_num(self):
        return len(self.pair_path_list)

    def get_pair_name_list(self):
        return self.pair_name_list

    def read_file(self, file_path, is_label=False):
        """
        currently, default using file_io, reading medical format
        :param file_path:
        :param  is_label: the file_path is label_file
        :return:
        """
        # img, info = read_itk_img(file_path)
        img, info = file_io_read_img(file_path, is_label=is_label)
        return img, info

    def extract_pair_info(self, info1, info2):
        return info1

    def save_shared_info(self,info):
        save_sz_sp_to_json(info, self.output_path)

    def save_pair_to_txt(self):
        pass

    def save_file_to_h5py(self):
        pass

    def initialize_info(self):
        pass



    def prepare_data(self):
        """
        preprocessig  data for each dataset
        :return:
        """
        print("starting preapare data..........")
        print("the output file path is: {}".format(self.output_path))
        self.initialize_info()
        self.save_file_to_h5py()
        self.pair_path_list = self.generate_pair_list()
        self.save_pair_to_txt()
        try:
            print("the total num of pair is {}".format(self.get_file_num()))
        except:
            pass
        print("data preprocessing finished")



class UnlabeledDataSet(BaseRegDataSet):
    """
    unlabeled dataset
    """
    def __init__(self,dataset_type, file_type_list, sched=None):
        BaseRegDataSet.__init__(self,dataset_type, file_type_list,sched)

    def save_pair_to_txt(self):
        """
        save the file into h5py
        :param pair_path_list: N*2  [[full_path_img1, full_path_img2],[full_path_img2, full_path_img3]
        :param pair_name_list: N*1 for 'mix': [folderName1_sliceName1_folderName2_sliceName2, .....]  for custom: [sliceName1_sliceName2, .....]
        :param ratio:  divide dataset into training val and test, based on ratio, e.g [0.7, 0.1, 0.2]
        :param saving_path_list: N*1 list of path for output files e.g [ouput_path/train/sliceName1_sliceName2.h5py,.........]
        :param info: dic including pair information
        :param normalized_sched: normalized the image
        """
        random.shuffle(self.pair_path_list)
        self.pair_name_list = generate_pair_name(self.pair_path_list, sched=self.dataset_type)
        self.num_pair = len(self.pair_path_list)
        sub_folder_dic, file_id_dic = divide_data_set(self.output_path, self.num_pair, self.divided_ratio)
        divided_path_and_name_dic = get_divided_dic(file_id_dic, self.pair_path_list, self.pair_name_list)
        saving_pair_info(sub_folder_dic,divided_path_and_name_dic)



    def save_file_to_h5py(self):
        file_path_list =  get_file_path_list(self.data_path, self.file_type_list)
        file_name_list = [get_file_name(pt) for pt in file_path_list]
        self.pro_data_path = os.path.join(self.output_path,'data')
        pro_data_path_list = [fp.replace(self.data_path,self.pro_data_path) for fp in file_path_list]
        self.pro_data_path_list =[os.path.join(os.path.split(fp)[0],file_name_list[idx]+'.h5py') for idx, fp in enumerate(pro_data_path_list)]
        make_dir(self.pro_data_path)
        img_size = ()
        info = None
        pbar = pb.ProgressBar(widgets=[pb.Percentage(), pb.Bar(), pb.ETA()], maxval=len(file_path_list)).start()
        for i, file in enumerate(file_path_list):
            img, info = self.read_file(file)
            f_name = file_name_list[i]
            if i == 0:
                img_size = img.shape
            else:
                check_same_size(img, img_size)
            saving_path = self.pro_data_path_list[i]
            make_dir(os.path.split(saving_path)[0])
            save_to_h5py(saving_path, img, None, f_name, info, verbose=False)
            pbar.update(i + 1)
        pbar.finish()




class LabeledDataSet(BaseRegDataSet):
    """
    labeled dataset
    """
    def __init__(self, dataset_type, file_type_list, sched=None):
        BaseRegDataSet.__init__(self,dataset_type, file_type_list,sched)
        self.label_switch = ('','')
        self.label_path = None
        self.pair_label_path_list=[]


    def set_label_switch(self,label_switch):
        self.label_switch = label_switch


    def set_label_path(self, path):
        self.label_path = path

    def convert_to_standard_label_map(self,label_map,file_path):

        cur_label_list = list(np.unique(label_map))
        num_label = len(cur_label_list)
        if self.num_label != num_label:  # s37 in lpba40 has one more label than others
            print("Warnning!!!!, The num of classes {} are not the same in file{}".format(num_label, file_path))

        for l_id in cur_label_list:
            if l_id in self.standard_label_index:
                st_index = self.standard_label_index.index(l_id)
            else:
                # assume background label is 0
                st_index = 0
                print("warning label: is not in standard label index, and would be convert to 0".format(l_id))
            label_map[np.where(label_map==l_id)]=st_index

    def initialize_info(self):
        file_path_list = get_file_path_list(self.data_path, self.file_type_list)
        file_label_path_list = find_corr_map(file_path_list, self.label_path,self.label_switch)
        label, linfo = self.read_file(file_label_path_list[0], is_label=True)
        label_list = list(np.unique(label))
        num_label = len(label_list)
        self.standard_label_index = tuple([int(item) for item in label_list])
        print('the standard label index is :{}'.format(self.standard_label_index))
        print('the num of the class: {}'.format(num_label))
        self.num_label = num_label
        linfo['num_label'] = num_label
        linfo['standard_label_index']= self.standard_label_index
        self.save_shared_info(linfo)


    def save_pair_to_txt(self):
        """
        save the file into h5py
        :param pair_path_list: N*2  [[full_path_img1, full_path_img2],[full_path_img2, full_path_img3]
        :param pair_name_list: N*1 for 'mix': [folderName1_sliceName1_folderName2_sliceName2, .....]  for custom: [sliceName1_sliceName2, .....]
        :param ratio:  divide dataset into training val and test, based on ratio, e.g [0.7, 0.1, 0.2]
        :param saving_path_list: N*1 list of path for output files e.g [ouput_path/train/sliceName1_sliceName2.h5py,.........]
        :param info: dic including pair information
        :param normalized_sched: normalized the image
        """
        random.shuffle(self.pair_path_list)
        self.pair_name_list = generate_pair_name(self.pair_path_list, sched=self.dataset_type)
        self.num_pair = len(self.pair_path_list)
        sub_folder_dic, file_id_dic = divide_data_set(self.output_path, self.num_pair, self.divided_ratio)
        divided_path_and_name_dic = get_divided_dic(file_id_dic, self.pair_path_list, self.pair_name_list)
        saving_pair_info(sub_folder_dic,divided_path_and_name_dic)



    def save_file_to_h5py(self):
        file_path_list =  get_file_path_list(self.data_path, self.file_type_list)
        file_label_path_list = find_corr_map(file_path_list, self.label_path,self.label_switch)
        file_name_list = [get_file_name(pt) for pt in file_path_list]
        self.pro_data_path = os.path.join(self.output_path,'data')
        pro_data_path_list = [fp.replace(self.data_path, self.pro_data_path) for fp in file_path_list]
        self.pro_data_path_list = [os.path.join(os.path.split(fp)[0], file_name_list[idx] + '.h5py') for idx, fp in
                                   enumerate(pro_data_path_list)]
        make_dir(self.pro_data_path)
        img_size = ()
        info = None
        pbar = pb.ProgressBar(widgets=[pb.Percentage(), pb.Bar(), pb.ETA()], maxval=len(file_path_list)).start()
        for i, file in enumerate(file_path_list):
            img, info = self.read_file(file)
            f_name = file_name_list[i]
            label, linfo = self.read_file(file_label_path_list[i], is_label=True)
            self.convert_to_standard_label_map(label, file_label_path_list[i])
            if i == 0:
                img_size = img.shape
                check_same_size(label, img_size)
            else:
                check_same_size(img, img_size)
                check_same_size(label, img_size)
            saving_path = self.pro_data_path_list[i]
            make_dir(os.path.split(saving_path)[0])
            save_to_h5py(saving_path, img, label, f_name, info, verbose=False)
            pbar.update(i + 1)
        pbar.finish()



    def save_file_by_default_type(self):
        file_path_list =  get_file_path_list(self.data_path, self.file_type_list)
        file_label_path_list = find_corr_map(file_path_list, self.label_path,self.label_switch)
        file_name_list = [get_file_name(pt) for pt in file_path_list]
        self.pro_data_path = os.path.join(self.output_path,'data')
        pro_data_path_list = [fp.replace(self.data_path, self.pro_data_path) for fp in file_path_list]
        self.pro_data_path_list = pro_data_path_list
        make_dir(self.pro_data_path)






class CustomDataSet(BaseRegDataSet):
    """
    dataset format that orgnized as data_path/slice1, slic2, slice3 .......
    """
    def __init__(self,dataset_type, file_type_list,full_comb=False):
        BaseRegDataSet.__init__(self, dataset_type, file_type_list)
        self.full_comb = full_comb


    def generate_pair_list(self, sched=None):
        """
        :param sched:
        :return:
        """
        pair_path_list = inter_pair(self.pro_data_path,  ['*.h5py'], self.full_comb, mirrored=True)
        return pair_path_list


class VolumetricDataSet(BaseRegDataSet):
    """
    3D dataset
    """
    def __init__(self,dataset_type, file_type_list,sched=None):
        BaseRegDataSet.__init__(self, dataset_type=dataset_type, file_type_list=file_type_list,sched=sched)
        self.slicing = -1
        self.axis = -1

    def set_slicing(self, slicing, axis):
        if slicing >0 and axis>0:
            print("slcing is set on , the slice of {} th dimension would be sliced ".format(slicing))
        self.slicing = slicing
        self.axis = axis


    def read_file(self, file_path, is_label=False, verbose=False):
        """

        :param file_path:the path of the file
        :param is_label:the file is label file
        :param verbose:
        :return:
        """
        if self.slicing != -1:
            if verbose:
                print("slicing file: {}".format(file_path))
            img, info = file_io_read_img_slice(file_path, self.slicing, self.axis, is_label=is_label)
        else:
            img, info= BaseRegDataSet.read_file(self,file_path,is_label=is_label)
        return img, info




class MixedDataSet(BaseRegDataSet):
    """
     include inter-personal and intra-personal data, which is orgnized as oasis2d, root/patient1_folder/slice1,slice2...
    """
    def __init__(self, dataset_type, file_type_list, sched, full_comb=False):
        BaseRegDataSet.__init__(self, dataset_type, file_type_list, sched=sched)
        self.full_comb = full_comb


    def generate_pair_list(self):
        """
         return the list of  paths of the paired image  [N,2]
        :param file_type_list: filter and get the image of certain type
        :param full_comb: if full_comb, return all possible pairs, if not, return pairs in increasing order
        :param sched: sched can be inter personal or intra personal
        :return:
        """
        if self.sched == 'intra':
            dic_list = list_dic(self.data_path)
            pair_path_list = intra_pair(self.pro_data_path, dic_list, ['*.h5py'], self.full_comb, mirrored=True)
        elif self.sched == 'inter':
            pair_path_list = inter_pair(self.pro_data_path,  ['*.h5py'], self.full_comb, mirrored=True)
        else:
            raise ValueError("schedule should be 'inter' or 'intra'")

        return pair_path_list



class PatientStructureDataSet(VolumetricDataSet):
    """
    the dataset is organized in the patients,  in the way as patient_id/modality/specificity/
    each folder include a series slices which obtained at different time period


    """

    def __init__(self, dataset_type, file_type_list, sched):
        VolumetricDataSet.__init__(self, dataset_type, file_type_list,sched)
        self.patients = []
        self.__init_patients()

    def __init_patients(self):
        root_path = "/playpen/raid/zyshen/summer/oai_registration/data"
        Patient_class = Patients(full_init=True, root_path=root_path)
        self.patients= Patient_class.get_filtered_patients_list(has_complete_label= True, len_time_range=[2, 7], use_random=False)

    def __divide_into_train_val_test_set(self,root_path, patients, ratio):
        num_patient = len(patients)
        train_ratio = ratio[0]
        val_ratio = ratio[1]
        sub_path = {x: os.path.join(root_path, x) for x in ['train', 'val', 'test', 'debug']}
        nt = [make_dir(sub_path[key]) for key in sub_path]
        # if sum(nt):
        #     raise ValueError("the data has already exist, due to randomly assignment schedule, the program block\n"
        #                      "manually delete the folder to reprepare the data")

        train_num = int(train_ratio * num_patient)
        val_num = int(val_ratio * num_patient)
        sub_patients_dic = {}
        sub_patients_dic['train'] = patients[:train_num]
        sub_patients_dic['val'] = patients[train_num: train_num + val_num]
        sub_patients_dic['test'] = patients[train_num + val_num:]
        sub_patients_dic['debug'] = patients[: val_num]
        return sub_path,sub_patients_dic


    def __initialize_info(self,one_label_path):
        label = sitk.ReadImage(one_label_path)
        label = sitk.GetArrayFromImage(label)
        label_list = list(np.unique(label))
        num_label = len(label_list)
        self.standard_label_index = tuple([int(item) for item in label_list])
        print('the standard label index is :{}'.format(self.standard_label_index))
        print('the num of the class: {}'.format(num_label))
        self.num_label = num_label
        linfo={}
        linfo['num_label'] = num_label
        linfo['standard_label_index']= self.standard_label_index
        linfo['img_size'] = label.shape
        linfo['spacing']=np.array([-1])
        self.save_shared_info(linfo)



    def __gen_intra_pair_list(self,patients, pair_num_limit = 1000):
        intra_pair_list = []
        for patient in patients:
            intra_image_list = patient.get_slice_path_list()
            intra_label_list = patient.get_label_path_list()
            num_images = len(intra_image_list)
            for i, image in enumerate(intra_image_list):
                for j in range(i+1, num_images):
                    intra_pair_list.append([intra_image_list[i],intra_image_list[j],
                                            intra_label_list[i],intra_label_list[j]])
            if len(intra_pair_list)> 3*pair_num_limit:
                break
        random.shuffle(intra_pair_list)
        self.__initialize_info(patients[0].get_label_path_list()[0])
        return intra_pair_list[:pair_num_limit]


    def __gen_inter_pair_list(self, patients,pair_num_limit = 1000):
        inter_pair_list = []
        all_image_list = []
        all_label_list = []
        for patient in patients:
            all_image_list.append(patient.get_slice_path_list())
            all_label_list.append(patient.get_label_path_list())
        permute_id_list = list(range(len(all_image_list)))
        all_image_list =[all_image_list[i] for i in permute_id_list]
        all_label_list = [all_label_list[i] for i in permute_id_list]
        for _ in range(pair_num_limit):
            rand_pair_id =[int(1000*random.random()),int(1000*random.random())]
            pair = [all_image_list[rand_pair_id[0]], all_image_list[rand_pair_id[1]],
                    all_label_list[rand_pair_id[0]], all_label_list[rand_pair_id[1]]]
            inter_pair_list.append(pair)

        self.__initialize_info(patients[0].get_label_path_list()[0])
        return inter_pair_list

    def __gen_path_and_name_dic(self, pair_list_dic):
        sesses = ['train', 'val', 'test', 'debug']
        divided_path_and_name_dic={}
        divided_path_and_name_dic['pair_path_list'] = pair_list_dic
        divided_path_and_name_dic['pair_name_list'] = {sess:[get_file_name(path[0])+'_'+get_file_name(path[1]) for path in pair_list_dic[sess]] for sess in sesses}
        return divided_path_and_name_dic







    def save_pair_to_txt(self):
        sub_folder_dic, sub_patients_dic =self.__divide_into_train_val_test_set(self.output_path,self.patients,self.divided_ratio)
        sesses = ['train', 'val', 'test', 'debug']
        gen_pair_list_func = self. __gen_intra_pair_list if self.sched=='intra' else self.__gen_inter_pair_list
        max_ratio = {'train':self.divided_ratio[0],'val':self.divided_ratio[1],'test':self.divided_ratio[2],'debug':self.divided_ratio[1]}
        pair_list_dic ={sess: gen_pair_list_func(sub_patients_dic[sess],int(1000*max_ratio[sess])) for sess in sesses}
        divided_path_and_name_dic = self.__gen_path_and_name_dic(pair_list_dic)
        saving_pair_info(sub_folder_dic,divided_path_and_name_dic)

    def save_file_to_h5py(self):
        """
        for compatiblity
        :return:
        """
        pass

    def generate_pair_list(self):
        """
        for compatiblity
        :return:
        """
        return None





class RegDatasetPool(object):
    def create_dataset(self,dataset_name, sched, full_comb):
        self.dataset_dic = {'oasis2d':Oasis2DDataSet,
                                   'lpba':VolLabCusDataSet,
                                    'ibsr':VolLabCusDataSet,
                                     'cumc':VolLabCusDataSet,
                                    'oai':OaiDataSet}

        dataset = self.dataset_dic[dataset_name](sched, full_comb)
        return dataset

class Oasis2DDataSet(UnlabeledDataSet, MixedDataSet):
    """"
    sched:  'inter': inter_personal,  'intra': intra_personal
    """
    def __init__(self, sched, full_comb=False):
        file_type_list = ['*a.mhd'] if sched == 'intra' else ['*_1_a.mhd', '*_2_a.mhd', '*_3_a.mhd']
        UnlabeledDataSet.__init__(self, 'mixed', file_type_list, sched)
        MixedDataSet.__init__(self, 'mixed', file_type_list, sched, full_comb)




class VolLabCusDataSet(VolumetricDataSet, LabeledDataSet, CustomDataSet):
    def __init__(self, sched, full_comb=True):
        VolumetricDataSet.__init__(self, 'custom', ['*.nii'])
        LabeledDataSet.__init__(self, 'custom', ['*.nii'])
        CustomDataSet.__init__(self,'custom', ['*.nii'], full_comb)

class OaiDataSet(PatientStructureDataSet):
    def __init__(self, sched, full_comb=True):
        img_poster= ['*image.nii.gz']
        PatientStructureDataSet.__init__(self,None,None,sched)







if __name__ == "__main__":
    print('debugging')
    # #########################       OASIS TESTING           ###################################3
    #
    # path = '/playpen/zyshen/data/oasis'
    # name = 'oasis'
    # divided_ratio = (0.6, 0.2, 0.2)
    #
    # ###################################################
    # #oasis  intra testing
    # full_comb = True
    # sched= 'intra'
    #
    # output_path = '/playpen/zyshen/data/'+ name+'_pre_'+ sched
    # oasis = Oasis2DDataSet(name='oasis',sched=sched, full_comb=True)
    # oasis.set_data_path(path)
    # oasis.set_output_path(output_path)
    # oasis.set_divided_ratio(divided_ratio)
    # oasis.prepare_data()


    # ###################################################
    # # oasis inter testing
    # sched='inter'
    # full_comb = False
    # output_path = '/playpen/zyshen/data/' + name + '_pre_' + sched
    # oasis = Oasis2DDataSet(name='oasis', sched=sched, full_comb=full_comb)
    # oasis.set_data_path(path)
    # oasis.set_output_path(output_path)
    # oasis.set_divided_ratio(divided_ratio)
    # oasis.prepare_data()




    # ###########################       LPBA TESTING           ###################################
    # path = '/playpen/data/quicksilver_data/testdata/LPBA40/brain_affine_icbm'
    # label_path = '/playpen/data/quicksilver_data/testdata/LPBA40/label_affine_icbm'
    # file_type_list = ['*.nii']
    # full_comb = False
    # name = 'lpba'
    # output_path = '/playpen/zyshen/data/' + name + '_pre'
    # divided_ratio = (0.6, 0.2, 0.2)
    #
    # ###################################################
    # #lpba testing
    #
    # sched= 'intra'
    #
    # lpba = LPBADataSet(name=name, full_comb=full_comb)
    # lpba.set_data_path(path)
    # lpba.set_output_path(output_path)
    # lpba.set_divided_ratio(divided_ratio)
    # lpba.set_label_path(label_path)
    # lpba.prepare_data()


    ###########################       LPBA Slicing TESTING           ###################################
    path = '/playpen/data/quicksilver_data/testdata/LPBA40/brain_affine_icbm'
    label_path = '/playpen/data/quicksilver_data/testdata/LPBA40/label_affine_icbm'
    full_comb = False
    name = 'lpba'
    output_path = '/playpen/zyshen/data/' + name + '_pre_slicing'
    divided_ratio = (0.6, 0.2, 0.2)

    ###################################################
    #lpba testing


    lpba = VolLabCusDataSet(sched='', full_comb=full_comb)
    lpba.set_slicing(90,1)
    lpba.set_data_path(path)
    lpba.set_output_path(output_path)
    lpba.set_divided_ratio(divided_ratio)
    lpba.set_label_path(label_path)
    lpba.prepare_data()





