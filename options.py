gpu = '0'
random_seed = 0
# video_path = '/home/vvn/PycharmProjects/lip_reading/data/GRID/s1/imgs/'
# train_list = f'/home/vvn/PycharmProjects/lip_reading/data/GRID/s1/sample.txt'
# val_list = f'/home/vvn/PycharmProjects/lip_reading/data/GRID/s1/sample.txt'
# anno_path = '/home/vvn/PycharmProjects/lip_reading/data/GRID/s1/align'

video_path = '/home/vvn/PycharmProjects/lip_reading/data/vvn/imgs/'
train_list = f'/home/vvn/PycharmProjects/lip_reading/data/vvn/train.txt'
val_list = f'/home/vvn/PycharmProjects/lip_reading/data/vvn/val.txt'

vid_padding = 75
txt_padding = 200
batch_size = 32
base_lr = 1e-4
num_workers = 8
max_epoch = 9999
display = 10
test_step = 1000
is_optimize = True

save_prefix = 'LipNet_'
save_dir = '/home/vvn/PycharmProjects/lip_reading/LipNet-PyTorch/weights'

weights = '/home/vvn/PycharmProjects/lip_reading/LipNet-PyTorch/weights/LipNet_vvn_loss_4.590000152587891_wer_0.83_cer_0.64.pt'