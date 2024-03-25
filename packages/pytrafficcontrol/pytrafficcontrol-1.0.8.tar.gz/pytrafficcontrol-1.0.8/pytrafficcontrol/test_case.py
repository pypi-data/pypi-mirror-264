# -*- coding: UTF-8 -*-
testcases = ['stable_loss_UP_30%',
             'stable_loss_UP_50%',
             'stable_loss_UP_70%',
             'stable_loss_DOWN_30%',
             'stable_loss_DOWN_50%',
             'stable_loss_DOWN_70%',
             'stable_band_UP_200k',
             'stable_band_UP_100k',
             'stable_band_DOWN_200k',
             'stable_band_DOWN_100k',
             'stable_band_up_200k_samllcatch',
             'stable_band_up_100k_samllcatch',
             'stable_band_down_200k_samllcatch',
             'stable_band_down_100k_samllcatch',
             'stable_jiter_UP_500ms_jiter',
             'stable_jiter_up_1000ms_jiter',
             'stable_jiter_down_500ms_jiter',
             'stable_jiter_down_1000ms_jiter',
             'stable_up_300k_loss_20',
             'stable_up_300k_loss_50',
             'stable_down_300k_loss_20',
             'stable_down_300k_loss_50',
             'stable_up_loss_and_delay_30_200ms',
             'stable_up_loss_and_delay_50_200ms',
             'stable_down_loss_and_delay_30_200ms',
             'stable_down_loss_and_delay_50_200ms',
             'burst_up_complex',
             'burst_down_complex',
             'dl-canteen-rate',
             'dl-drive-rate',
             'dl-parking-rate',
             'india-office-ul',
             'india-station-ul',
             'sa_ul',
             'ul-canteen-rate',
             'ul-drive-rate',
             'ul-parking-rate',
             'vn-office-rate',
             'vn-parking-ul',
             'inter_UP_30%',
             'inter_UP_50%',
             'inter_DOWN_30%',
             'inter_DOWN_50%',
             'inter_UP_500ms_jiter',
             'inter_UP_1500ms_jiter',
             'inter_DOWN_500ms_jiter',
             'inter_DOWN_1500ms_jiter',
             'inter_UP_500ms_delay',
             'inter_up_1500ms_delay',
             'inter_down_500ms_delay',
             'inter_down_1500ms_delay',
             'inter_up_200k',
             'inter_up_100k',
             'inter_down_200k',
             'inter_down_100k',
             'inter_up_200k_samllcatch',
             'inter_up_100k_samllcatch',
             'inter_down_200k_samllcatch',
             'inter_down_100k_samllcatch',
             'inter_up_200k_1s',
             'inter_up_100k_1s',
             'inter_down_200k_1s',
             'inter_down_100k_1s',
             'inter_up_200k_samllcatch_1s',
             'inter_up_100k_samllcatch_1s',
             'inter_down_200k_samllcatch_1s',
             'inter_down_100k_samllcatch_1s',
             'inter_up_400k_change_to_None',
             'inter_down_400k_change_to_None',
             'inter_up_400k_change_to_None_samllcatch',
             'inter_down_400k_change_to_None_samllcatch',
             'inter_up_200k_change_to_400k',
             'inter_down_200k_change_to_400k',
             'inter_up_200k_change_to_400k_samllcatch',
             'inter_down_200k_change_to_400k_samllcatch',
             'double_inter_200k', 'double_inter_100k',
             'double_inter_200k_samllcatch',
             'double_inter_100k_samllcatch',
             'up_backgrpund_600k_udp',
             'down_backgrpund_600k_udp',
             'up_backgrpund_600k_tcp',
             'down_backgrpund_600k_tcp',
             'up_backgrpund_600k_udp_smallcatch',
             'down_backgrpund_600k_udp_smallcatch',
             'up_backgrpund_600k_tcp_smallcatch',
             'down_backgrpund_600k_tcp_smallcatch']


testSuite = {
    # 稳态丢包
    'stable_loss_UP_30%':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    'stable_loss_UP_50%':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    'stable_loss_UP_70%':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 70, 'packet': 1000, 'style': 'stable', 'only_udp': False},

    'stable_loss_DOWN_30%':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_loss_DOWN_50%':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_loss_DOWN_70%':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 70, 'packet': 1000,'style': 'stable', 'only_udp': False},
    # 稳态带宽限制
    'stable_band_UP_200k':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_band_UP_100k':
        {'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    'stable_band_DOWN_200k':
        {'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_band_DOWN_100k':
        {'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    # 小缓存
    'stable_band_up_200k_samllcatch':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'stable', 'only_udp': False},
    'stable_band_up_100k_samllcatch':
        {'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1,'style': 'stable', 'only_udp': False},
    'stable_band_down_200k_samllcatch':
        {'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1,'style': 'stable', 'only_udp': False},
    'stable_band_down_100k_samllcatch':
        {'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1,'style': 'stable', 'only_udp': False},
    # 稳态抖动
    'stable_jiter_UP_500ms_jiter':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_jiter_up_1000ms_jiter':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 1000, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_jiter_down_500ms_jiter':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_jiter_down_1000ms_jiter':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 1000, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    # 带限 + 丢包
    'stable_up_300k_loss_20':
        {'direction': 'up', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 20, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    'stable_up_300k_loss_50':
        {'direction': 'up', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_down_300k_loss_20':
        {'direction': 'down', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 20, 'packet': 1000,'style': 'stable', 'only_udp': False},
    'stable_down_300k_loss_50':
        {'direction': 'down', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000,'style': 'stable', 'only_udp': False},

    # 丢包+ 延时
    'stable_up_loss_and_delay_30_200ms':
        {'direction': 'up', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 30,'packet': 1000, 'style': 'stable', 'only_udp': False},
    'stable_up_loss_and_delay_50_200ms':
        {'direction': 'up', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 50,'packet': 1000, 'style': 'stable', 'only_udp': False},
    'stable_down_loss_and_delay_30_200ms':
        {'direction': 'down', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 30,'packet': 1000, 'style': 'stable', 'only_udp': False},
    'stable_down_loss_and_delay_50_200ms':
        {'direction': 'down', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 50,'packet': 1000, 'style': 'stable', 'only_udp': False},

    # 复合网络
    'burst_up_complex':
        {'direction': 'up', 'band': 1000, 'delay': 100, 'jiter': 100, 'loss': 30,'packet': 1000, 'style': 'burst', 'only_udp': False},
    'burst_down_complex':
        {'direction': 'down', 'band': 1000, 'delay': 100, 'jiter': 100, 'loss': 30,'packet': 1000, 'style': 'burst', 'only_udp': False},

    # 真实弱网模拟
    'dl-canteen-rate':
        {'direction': 'down', 'band': 'dl-canteen-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    'dl-drive-rate':
        {'direction': 'down', 'band': 'dl-drive-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    'dl-parking-rate':
        {'direction': 'down', 'band': 'dl-parking-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},


    'india-office-ul':
        {'direction': 'up', 'band': 'india-office-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    'india-station-ul':
        {'direction': 'up', 'band': 'india-station-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    'sa_ul':
        {'direction': 'up', 'band': 'sa_ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    'ul-canteen-rate':
        {'direction': 'up', 'band': 'ul-canteen-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    'ul-drive-rate':
        {'direction': 'up', 'band': 'ul-drive-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    'ul-parking-rate':
        {'direction': 'up', 'band': 'ul-parking-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    'vn-parking-ul':
        {'direction': 'up', 'band': 'vn-parking-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},

    # 周期性丢包
    'inter_UP_30%':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy':5,'idle':30},
    'inter_UP_50%':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy':5,'idle':30},

    'inter_DOWN_30%':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_DOWN_50%':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    # 周期性抖动
    'inter_UP_500ms_jiter':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_UP_1500ms_jiter':
        {'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 1500, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    'inter_DOWN_500ms_jiter':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_DOWN_1500ms_jiter':
        {'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 1500, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    #  周期性延时
    'inter_UP_500ms_delay':
        {'direction': 'up', 'band': 0, 'delay': 500, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_up_1500ms_delay':
        {'direction': 'up', 'band': 0, 'delay': 1500, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    'inter_down_500ms_delay':
        {'direction': 'down', 'band': 0, 'delay': 500, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_down_1500ms_delay':
        {'direction': 'down', 'band': 0, 'delay': 1500, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    # 周期性带限
    'inter_up_200k':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_up_100k':
        {'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_down_200k':
        {'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_down_100k':
        {'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},


    # 小缓存
    'inter_up_200k_samllcatch':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_up_100k_samllcatch':
        {'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_down_200k_samllcatch':
        {'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    'inter_down_100k_samllcatch':
        {'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    # 周期性带限制
    'inter_up_200k_1s':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    'inter_up_100k_1s':
        {'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    'inter_down_200k_1s':
        {'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    'inter_down_100k_1s':
        {'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    # 小缓存
    'inter_up_200k_samllcatch_1s':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    'inter_up_100k_samllcatch_1s':
        {'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    'inter_down_200k_samllcatch_1s':
        {'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    'inter_down_100k_samllcatch_1s':
        {'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},

    # 带宽变化
    'inter_up_400k_change_to_None':
        {'direction': 'up', 'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},
    'inter_down_400k_change_to_None':
        {'direction': 'down', 'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},

    'inter_up_400k_change_to_None_samllcatch':
        {'direction': 'up', 'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},
    'inter_down_400k_change_to_None_samllcatch':
        {'direction': 'down', 'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},

    'inter_up_200k_change_to_400k':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60,'change':'0_400'},
    'inter_down_200k_change_to_400k':
        {'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60,'change':'0_400'},

    'inter_up_200k_change_to_400k_samllcatch':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60, 'change': '0_400'},
    'inter_down_200k_change_to_400k_samllcatch':
        {'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60, 'change': '0_400'},
    #
    # 双向网络
    'double_inter_200k':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30,'doubleNet':1},
    'double_inter_100k':
        {'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30,'doubleNet':1},

    'double_inter_200k_samllcatch':
        {'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30,'doubleNet':1},
    'double_inter_100k_samllcatch':
        {'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30,'doubleNet':1},


    # 背景流量

    'up_backgrpund_600k_udp':
        {'direction': 'up', 'band': 600, 'delay': 0, 'jiter': 0,'loss': 0, 'packet': 1000, 'style': 'background', 'bg_type':'udp'},
    'down_backgrpund_600k_udp':
        {'direction': 'down', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'background',  'bg_type': 'udp'},
    'up_backgrpund_600k_tcp':
        {'direction': 'up', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'background',  'bg_type': 'tcp'},
    'down_backgrpund_600k_tcp':
        {'direction': 'down', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'background',  'bg_type': 'tcp'},

    'up_backgrpund_600k_udp_smallcatch':
        {'direction': 'up', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'background', 'bg_type': 'udp'},
    'down_backgrpund_600k_udp_smallcatch':
        {'direction': 'down', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'background', 'bg_type': 'udp'},
    'up_backgrpund_600k_tcp_smallcatch':
        {'direction': 'up', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'background', 'bg_type': 'tcp'},
    'down_backgrpund_600k_tcp_smallcatch':
        {'direction': 'down', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'background', 'bg_type': 'tcp'},
}

if __name__ == '__main__':
    # testcases = []
    # for a in testSuite:
    #     testcases.append(a['testcase'])
    # print(testcases)
    pass