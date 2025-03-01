import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import os, sys
from dataset import MyDataset
import numpy as np
import time
from model import LipNet
import torch.optim as optim
from tensorboardX import SummaryWriter
from datetime import datetime

opt = __import__('options')
os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpu
writer = SummaryWriter()
saved = sys.stdout
save_dir = os.path.join(opt.save_dir, datetime.now().strftime("%Y%m%d-%H%M%S"))
if(not os.path.exists(save_dir)): os.makedirs(save_dir)
log_file = os.path.join(save_dir, "train.log")
f = open(log_file, 'w')

class log_writer:
    def __init__(self, *writers):
        self.writers = writers

    def write(self, text):
        for w in self.writers:
            w.write(text)

    def flush(self):
        pass

sys.stdout = log_writer(sys.stdout, f)

def dataset2dataloader(dataset, num_workers=opt.num_workers, shuffle=True):
    return DataLoader(dataset,
        batch_size = opt.batch_size,
        shuffle = shuffle,
        num_workers = num_workers,
        drop_last = False)

def show_lr(optimizer):
    lr = []
    for param_group in optimizer.param_groups:
        lr += [param_group['lr']]
    return np.array(lr).mean()  

def ctc_decode(y):
    result = []
    y = y.argmax(-1)
    return [MyDataset.ctc_arr2txt(y[_], start=1) for _ in range(y.size(0))]
    
def test(model, net):

    with torch.no_grad():
        dataset = MyDataset(opt.video_path,
            opt.val_list,
            opt.vid_padding,
            opt.txt_padding,
            'test')
            
        print('num_test_data:{}'.format(len(dataset.data)))  
        model.eval()
        loader = dataset2dataloader(dataset, shuffle=False)
        loss_list = []
        wer = []
        cer = []
        crit = nn.CTCLoss()
        tic = time.time()
        for (i_iter, input) in enumerate(loader):            
            vid = input.get('vid').cuda()
            txt = input.get('txt').cuda()
            vid_len = input.get('vid_len').cuda()
            txt_len = input.get('txt_len').cuda()
            
            y = net(vid)
            
            loss = crit(y.transpose(0, 1).log_softmax(-1), txt, vid_len.view(-1), txt_len.view(-1)).detach().cpu().numpy()
            loss_list.append(loss)
            pred_txt = ctc_decode(y)
            
            truth_txt = [MyDataset.arr2txt(txt[_], start=1) for _ in range(txt.size(0))]
            wer.extend(MyDataset.wer(pred_txt, truth_txt)) 
            cer.extend(MyDataset.cer(pred_txt, truth_txt))              
            if(i_iter % opt.display == 0):
                v = 1.0*(time.time()-tic)/(i_iter+1)
                eta = v * (len(loader)-i_iter) / 3600.0
                
                print(''.join(101*'-'))                
                print('{:<50}|{:>50}'.format('predict', 'truth'))
                print(''.join(101*'-'))                
                for (predict, truth) in list(zip(pred_txt, truth_txt))[:10]:
                    print('{:<50}|{:>50}'.format(predict, truth))                
                print(''.join(101 *'-'))
                print('test_iter={},eta={},wer={},cer={}'.format(i_iter,eta,np.array(wer).mean(),np.array(cer).mean()))                
                print(''.join(101 *'-'))
                
        return (np.array(loss_list).mean(), np.array(wer).mean(), np.array(cer).mean())



def train(model, net):
    '''

    :param model:
    :param net:
    :return:
    '''
    dataset = MyDataset(opt.video_path,
        opt.train_list,
        opt.vid_padding,
        opt.txt_padding,
        'train')
        
    loader = dataset2dataloader(dataset) 
    optimizer = optim.Adam(model.parameters(),
                lr = opt.base_lr,
                weight_decay = 0.,
                amsgrad = True)
                
    print('num_train_data:{}'.format(len(dataset.data)))    
    crit = nn.CTCLoss()
    tic = time.time()

    train_wer = []
    for epoch in range(opt.max_epoch):
        for (i_iter, input) in enumerate(loader):
            model.train()
            vid = input.get('vid').cuda()
            txt = input.get('txt').cuda()
            vid_len = input.get('vid_len').cuda()
            txt_len = input.get('txt_len').cuda()
            
            optimizer.zero_grad()
            y = net(vid)
            loss = crit(y.transpose(0, 1).log_softmax(-1), txt, vid_len.view(-1), txt_len.view(-1))
            loss.backward()
            if(opt.is_optimize):
                optimizer.step()
            
            tot_iter = i_iter + epoch*len(loader)
            
            pred_txt = ctc_decode(y)
            
            truth_txt = [MyDataset.arr2txt(txt[_], start=1) for _ in range(txt.size(0))]
            train_wer.extend(MyDataset.wer(pred_txt, truth_txt))
            
            if(tot_iter % opt.display == 0):

                writer.add_scalar('train loss', loss, tot_iter)
                writer.add_scalar('train wer', np.array(train_wer).mean(), tot_iter)              
                print(''.join(101*'-'))
                print('{:<50}|{:>50}'.format('predict', 'truth'))
                print(''.join(101*'-'))

                for (predict, truth) in list(zip(pred_txt, truth_txt))[:3]:
                    print('{:<50}|{:>50}'.format(predict, truth))
                print(''.join(101*'-'))
                # loss = str(round(loss,4))
                print('epoch={},tot_iter={},loss={},train_wer={}'.format(epoch, tot_iter, loss, np.array(train_wer).mean()))
                print(''.join(101*'-'))

            if(tot_iter % opt.test_step == 0):                
                (loss, wer, cer) = test(model, net)
                writer.add_scalar('val loss', float(loss), tot_iter)
                writer.add_scalar('wer', wer, tot_iter)
                writer.add_scalar('cer', cer, tot_iter)
                loss = str(round(loss,4))
                wer = round(wer,2)
                cer  = round(cer,2)
                print('i_iter={},lr={},loss={},wer={},cer={}'.format(tot_iter,show_lr(optimizer),loss,wer,cer))
                save_name = 'epoch_{}_loss_{}_wer_{}_cer_{}.pt'.format(str(epoch).zfill(4), loss, wer, cer)
                torch.save(model.state_dict(), os.path.join(save_dir, save_name))
                print('save checkpoint to', os.path.join(save_dir, save_name))
                if(not opt.is_optimize):
                    exit()
                
if(__name__ == '__main__'):
    print("Loading options...")
    model = LipNet()
    model = model.cuda()
    net = nn.DataParallel(model).cuda()

    if(hasattr(opt, 'weights')):
        pretrained_dict = torch.load(opt.weights)
        model_dict = model.state_dict()
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict.keys() and v.size() == model_dict[k].size()}
        missed_params = [k for k, v in model_dict.items() if not k in pretrained_dict.keys()]
        print('loaded params/tot params:{}/{}'.format(len(pretrained_dict),len(model_dict)))
        print('miss matched params:{}'.format(missed_params))
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)
        
    torch.manual_seed(opt.random_seed)
    torch.cuda.manual_seed_all(opt.random_seed)
    train(model, net)
        
