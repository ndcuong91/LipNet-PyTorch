import os, cv2
from torch.utils.data import DataLoader, Dataset
import time

video_in = '/home/vvn/PycharmProjects/lip_reading/data/vvn/videos'
imgs_out = '/home/vvn/PycharmProjects/lip_reading/data/vvn/imgs'
wav_dir = '/home/vvn/PycharmProjects/lip_reading/data/vvn/audio'

# video_in = '/home/vvn/PycharmProjects/lip_reading/data/GRID/s1/video'
# imgs_out = '/home/vvn/PycharmProjects/lip_reading/data/GRID/s1/imgs'
# wav_dir = '/home/vvn/PycharmProjects/lip_reading/data/GRID/s1/audio'


def get_list_file_in_folder(dir, ext=['jpg', 'png', 'JPG', 'PNG', 'jpeg','JPEG']):
    included_extensions = ext
    file_names = [fn.replace('.cpython-36m-x86_64-linux-gnu','').replace('.cpython-38-x86_64-linux-gnu','') for fn in os.listdir(dir)
                  if any(fn.endswith(ext) for ext in included_extensions)]
    file_names = sorted(file_names)
    return file_names

def with_opencv(filename):
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV v2.x used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    return duration

class MyDataset(Dataset):
    def __init__(self, num_frame = 75):
        self.IN = video_in
        self.OUT = imgs_out
        self.wav = wav_dir
        self.num_frame = num_frame

        list_files = get_list_file_in_folder(self.IN, ext = ['mp4','mpg'])
        self.files = [os.path.join(self.IN, f) for f in list_files]


    def __len__(self):
        return len(self.files)
        
    def __getitem__(self, idx):
        file = self.files[idx]
        _, ext = os.path.splitext(file)
        dst = file.replace(self.IN, self.OUT).replace(ext, '')

        if(not os.path.exists(dst)): 
            os.makedirs(dst)

        duration = with_opencv(file)
        num = (self.num_frame-2)/duration

        cmd = 'ffmpeg -i \'{}\' -qscale:v 2 -r {} \'{}/%d.jpg\''.format(file,num, dst)
       
        os.system(cmd)
        return dst

if(__name__ == '__main__'):   
    dataset = MyDataset()
    loader = DataLoader(dataset, num_workers=32, batch_size=128, shuffle=False, drop_last=False)
    tic = time.time()
    for (i, batch) in enumerate(loader):
        eta = (1.0*time.time()-tic)/(i+1) * (len(loader)-i)
        print('eta:{}'.format(eta/3600.0))

