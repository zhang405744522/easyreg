cd /playpen-raid/zyshen/reg_clean/demo
#python demo_for_easyreg_train.py -o=/pine/scr/z/y/zyshen/data/oai_reg -dtn=brainstorm -tn=trans -ts=/pine/scr/z/y/zyshen/reg_clean/debug/settings/training_brainstrom_trans_oai -g=0
#python demo_for_easyreg_train.py -o=/playpen-raid/zyshen/data/oai_reg -dtn=brainstorm -tn=trans -ts=/playpen-raid/zyshen/reg_clean/debug/settings/training_brainstrom_trans_oai -g=0
#python demo_for_easyreg_train.py -o=/playpen-raid/zyshen/data/oai_reg -dtn=brainstorm -tn=color -ts=/playpen-raid/zyshen/reg_clean/debug/settings/training_brainstrom_ap_oai -g=0
python demo_for_easyreg_train.py -o=/playpen-raid/zyshen/data/oai_reg/brainstorm -dtn=color_lrfix -tn=color -ts=/playpen-raid/zyshen/reg_clean/debug/settings/training_brainstrom_ap_oai -g=0

#python /playpen-raid/zyshen/reg_clean/mermaid/mermaid_demos/gen_aug_samples.py --txt_path=/playpen-raid//zyshen/data/oai_seg/atlas/momentum_lresol_train.txt --output_path=/playpen-raid1/zyshen/data/oai_reg/brain_storm/data_aug_fluid --mermaid_setting_path=/playpen-raid/zyshen/data/oai_seg/atlas/train/reg/res/records/nonp_setting.json
python /playpen-raid/zyshen/reg_clean/mermaid/mermaid_demos/gen_aug_samples.py --txt_path=/playpen-raid//zyshen/data/oai_seg/atlas/momentum_lresol_train.txt --output_path=/playpen-raid1/zyshen/data/oai_reg/brain_storm/data_aug_fluid_sr --mermaid_setting_path=/playpen-raid/zyshen/data/oai_seg/atlas/train/reg/res/records/nonp_setting.json &
python /playpen-raid/zyshen/reg_clean/mermaid/mermaid_demos/gen_aug_samples.py --txt_path=/playpen-raid//zyshen/data/oai_seg/atlas/momentum_lresol_train.txt --output_path=/playpen-raid1/zyshen/data/oai_reg/brain_storm/data_aug_fluid_sr --mermaid_setting_path=/playpen-raid/zyshen/data/oai_seg/atlas/train/reg/res/records/nonp_setting.json &
python /playpen-raid/zyshen/reg_clean/mermaid/mermaid_demos/gen_aug_samples.py --txt_path=/playpen-raid//zyshen/data/oai_seg/atlas/momentum_lresol_train.txt --output_path=/playpen-raid1/zyshen/data/oai_reg/brain_storm/data_aug_fluid_sr --mermaid_setting_path=/playpen-raid/zyshen/data/oai_seg/atlas/train/reg/res/records/nonp_setting.json &


python demo_for_seg_train.py -o /playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/ -dtn=data_aug_real_img_disp -tn=seg -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -g=0
python demo_for_seg_train.py -o /playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/ -dtn=data_aug_fake_img_disp -tn=seg_lv -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -g=0
python demo_for_seg_train.py -o /playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/ -dtn=data_aug_fake_img_fluid -tn=seg_lv -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -g=2
python demo_for_seg_train.py -o /playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/ -dtn=data_aug_real_img_fluid -tn=seg -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -g=3
python demo_for_seg_train.py -o /playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/ -dtn=data_aug_fake_img_fluidt1 -tn=seg_lv -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -g=3
python demo_for_seg_train.py -o /playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/ -dtn=data_aug_real_img_fluidt1 -tn=seg -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -g=3
python demo_for_seg_train.py -o /playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/ -dtn=data_aug_real_img_fluid_sr -tn=seg -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -g=3
python demo_for_seg_train.py -o /playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/ -dtn=data_aug_fake_img_fluid_sr -tn=seg_lv -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -g=3


python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -txt=/playpen-raid/zyshen/data/oai_seg/test/file_path_list.txt  -m=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_real_img_disp/seg/checkpoints/model_best.pth.tar  -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_real_img_disp/res -g=2
python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -txt=/playpen-raid/zyshen/data/oai_seg/test/file_path_list.txt  -m=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_real_img_fluid/seg/checkpoints/model_best.pth.tar  -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_real_img_fluid/res -g=2
python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -txt=/playpen-raid/zyshen/data/oai_seg/test/file_path_list.txt  -m=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_real_img_fluid_sr/seg/checkpoints/epoch_80_  -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_real_img_fluid_sr/res -g=2
python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -txt=/playpen-raid/zyshen/data/oai_seg/test/file_path_list.txt  -m=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_real_img_fluidt1/seg/checkpoints/epoch_110_  -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_real_img_fluidt1_2/res -g=1
python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -txt=/playpen-raid/zyshen/data//oai_reg/brainstorm/colored_test_for_seg.txt  -m=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_fake_img_disp/seg_lv/checkpoints/epoch_50_ -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_fake_img_disp/res -g=2
python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -txt=/playpen-raid/zyshen/data//oai_reg/brainstorm/colored_test_for_seg.txt  -m=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_fake_img_fluid/seg/checkpoints/epoch_240_  -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_fake_img_fluid/res -g=2
python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -txt=/playpen-raid/zyshen/data//oai_reg/brainstorm/colored_test_for_seg.txt  -m=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_fake_img_fluid_sr/seg_lv/checkpoints/epoch_20_  -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_fake_img_fluid_sr/res -g=2
python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg_aug_brainstorm -txt=/playpen-raid/zyshen/data//oai_reg/brainstorm/colored_test_for_seg.txt  -m=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_fake_img_fluidt1/seg/checkpoints/epoch_240_  -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/data_aug_fake_img_fluidt1/res -g=2

python  /playpen-raid/zyshen/reg_clean/demo/demo_for_seg_eval.py -ts=/playpen-raid/zyshen/reg_clean/debug/settings/oai_seg -txt=/playpen-raid/zyshen/data/oai_seg/test/file_path_list.txt  -m=/playpen-raid/zyshen/data/oai_seg/baseline/100case/llf_model3/model_best.pth.tar  -o=/playpen-raid1/zyshen/data/oai_reg/brain_storm/aug_expr/upperbound/res