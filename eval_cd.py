from argparse import ArgumentParser
import torch
from models.evaluator import *

print(torch.cuda.is_available())


"""
eval the CD model
"""

def main():
    # ------------
    # args
    # ------------
    parser = ArgumentParser()
    parser.add_argument('--gpu_ids', type=str, default='0', help='gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU')
    parser.add_argument('--project_name', default='test', type=str)
    parser.add_argument('--print_models', default=False, type=bool, help='print models')

    # data
    parser.add_argument('--num_workers', default=4, type=int)
    parser.add_argument('--dataset', default='CDDataset', type=str)
    parser.add_argument('--data_name', default='LEVIR', type=str)

    parser.add_argument('--batch_size', default=8, type=int)
    parser.add_argument('--split', default="test", type=str)

    parser.add_argument('--img_size', default=256, type=int)

    # model
    parser.add_argument('--n_class', default=2, type=int)
    parser.add_argument('--net_G', default='base_transformer_pos_s4_dd8_dedim8', type=str,
                        help='base_resnet18 | base_transformer_pos_s4_dd8 | base_transformer_pos_s4_dd8_dedim8|')

    parser.add_argument('--checkpoint_name', default='best_ckpt.pt', type=str)

    parser.add_argument('--testing_mode', default='resize', type=str, help='describes testing method: resize | crop | sliding_window_avg | sliding_window_gauss')

    parser.add_argument('--window_size', default=256, type=int, help='size of the square window segment of the image that is processed with the net')

    args = parser.parse_args()
    utils.get_device(args)
    print(args.gpu_ids)

    #  checkpoints dir
    args.checkpoint_dir = os.path.join('checkpoints', args.project_name)
    # args.checkpoint_dir = os.path.join('checkpoints', 'BIT_data_256')
    os.makedirs(args.checkpoint_dir, exist_ok=True)
    #  visualize dir
    args.vis_dir = os.path.join('vis', args.project_name, args.data_name)
    args.outputs = os.path.join('outputs', args.project_name, args.data_name)
    os.makedirs(args.vis_dir, exist_ok=True)
    os.makedirs(args.outputs, exist_ok=True)

    dataloader = utils.get_loader(args.data_name, img_size=args.img_size,
                                  batch_size=args.batch_size, is_train=False,
                                  split=args.split)
    model = CDEvaluator(args=args, dataloader=dataloader)

    model.eval_models(checkpoint_name=args.checkpoint_name)


if __name__ == '__main__':
    main()

