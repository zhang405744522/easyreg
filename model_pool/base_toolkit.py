from .base_model import BaseModel
from model_pool.utils import *
import SimpleITK as sitk
from .metrics import get_multi_metric






class ToolkitBase(BaseModel):
    def initialize(self, opt):
        BaseModel.initialize(self, opt)
        network_name = opt['tsk_set']['network_name']
        self.network_name = network_name
        self.affine_on = False
        self.warp_on = False

    def set_input(self, data, is_train=True):
        input = (data[0]['image']+1)/2
        moving, target, l_moving,l_target = get_pair(data[0])
        self.moving = moving
        self.target = target
        self.l_moving = l_moving
        self.l_target = l_target
        self.input = input
        self.input_img_sz  = list(moving.shape)[2:]
        self.original_im_sz = data[0]['original_sz']
        self.original_spacing = data[0]['original_spacing']
        self.fname_list = list(data[1])
        self.pair_path = data[0]['pair_path']
        self.pair_path = [path[0] for path in self.pair_path]
        self.resized_moving_path = self.resize_input_img_and_save_it_as_tmp(self.pair_path[0],is_label=False,fname='moving.nii.gz',keep_physical=self.use_physical_coord)
        self.resized_target_path = self.resize_input_img_and_save_it_as_tmp(self.pair_path[1],is_label= False, fname='target.nii.gz',keep_physical=self.use_physical_coord)
        self.resized_l_moving_path = self.resize_input_img_and_save_it_as_tmp(self.pair_path[2],is_label= True, fname='l_moving.nii.gz',keep_physical=self.use_physical_coord)
        self.resized_l_target_path = self.resize_input_img_and_save_it_as_tmp(self.pair_path[3],is_label= True, fname='l_target.nii.gz',keep_physical=self.use_physical_coord)


    def resize_input_img_and_save_it_as_tmp(self, img_pth, is_label=False,fname=None,keep_physical=False):
        """
        :param img: sitk input, factor is the outputsize/patched_sized
        :return:
        """
        img_org = sitk.ReadImage(img_pth)
        img = self.__read_and_clean_itk_info(img_pth)
        dimension = 3
        img_sz = img.GetSize()
        resize_factor = np.array(self.input_img_sz) / np.flipud(img_sz)
        resize = not all([factor == 1 for factor in resize_factor])
        factor = np.flipud(resize_factor)
        if resize:
            resampler = sitk.ResampleImageFilter()
            affine = sitk.AffineTransform(dimension)
            matrix = np.array(affine.GetMatrix()).reshape((dimension, dimension))
            after_size = [round(img_sz[i] * factor[i]) for i in range(dimension)]
            after_size = [int(sz) for sz in after_size]
            matrix[0, 0] = 1. / factor[0]
            matrix[1, 1] = 1. / factor[1]
            matrix[2, 2] = 1. / factor[2]
            affine.SetMatrix(matrix.ravel())
            resampler.SetSize(after_size)
            resampler.SetTransform(affine)
            if is_label:
                resampler.SetInterpolator(sitk.sitkNearestNeighbor)
            else:
                resampler.SetInterpolator(sitk.sitkBSpline)
            img_resampled = resampler.Execute(img)
        else:
            img_resampled = img
        fpth = os.path.join(self.record_path, fname)
        self.spacing = np.array([1.,1.,1.])
        #############################  be attention the origin of the image pair is no consistent which may cause the demos fail
        if keep_physical:
            itk_spacing = resize_spacing(img_sz, img_org.GetSpacing(), factor)
            self.spacing = np.flipud(itk_spacing)
            img_resampled.SetSpacing(itk_spacing)
            img_resampled.SetOrigin(img_org.GetOrigin())
            img_resampled.SetDirection(img_org.GetDirection())
        sitk.WriteImage(img_resampled, fpth)
        return fpth

    def __read_and_clean_itk_info(self,path):
        return sitk.GetImageFromArray(sitk.GetArrayFromImage(sitk.ReadImage(path)))




    def save_fig(self,phase,standard_record=False,saving_gt=True):
        from model_pool.visualize_registration_results import  show_current_images
        visual_param={}
        visual_param['visualize'] = False
        visual_param['save_fig'] = True
        visual_param['save_fig_path'] = self.record_path
        visual_param['save_fig_path_byname'] = os.path.join(self.record_path, 'byname')
        visual_param['save_fig_path_byiter'] = os.path.join(self.record_path, 'byiter')
        visual_param['save_fig_num'] = 8
        visual_param['pair_path'] = self.fname_list
        visual_param['iter'] = phase+"_iter_" + str(self.iter_count)
        disp=None
        extra_title = 'disp'
        if self.disp is not None and len(self.disp.shape)>2 and not self.warp_on:
            disp = ((self.disp[:,...]**2).sum(1))**0.5


        if self.warp_on and self.disp is not None:
            disp = self.disp[:,0,...]
            extra_title='affine'
        show_current_images(self.iter_count,  self.moving, self.target,self.output, self.l_moving,self.l_target,self.warped_label_map,
                            disp, extra_title, self.phi, visual_param=visual_param)




    def get_evaluation(self):
        self.output, _,_= self.forward(input=None)
        if self.l_moving is not None:
            warped_label_map_np= self.warped_label_map
            self.l_target_np= self.l_target.detach().cpu().numpy()
            self.val_res_dic = get_multi_metric(warped_label_map_np, self.l_target_np,rm_bg=False)
        self.jacobi_val= None
        self.jacobi_val = self.compute_jacobi_map(self.jacobian)
        print(" the current jcobi value of the phi is {}".format(self.jacobi_val))

    def save_image_into_original_sz_with_given_reference(self):
        try:
            raise ValueError(" save_image_into_original_sz_with_given_reference has not implemented yet for Ants/ Demons/Niftyreg")
        except:
            pass


    def set_val(self):
        self.is_train = False

    def set_debug(self):
        self.is_train = False

    def set_test(self):
        self.is_train = False

    def get_extra_res(self):
        return self.jacobi_val

    def cal_val_errors(self):
        self.cal_test_errors()

    def cal_test_errors(self):
        self.get_evaluation()