# -*- coding: UTF-8 -*-
testcases = [
             # 稳态弱网
             'stable_loss_30%',
             'stable_loss_50%',
             'stable_loss_70%',
             'stable_band_200k',
             'stable_band_100k',
             'stable_band_200k_samllcatch',
             'stable_band_100k_samllcatch',
             'stable_jiter_500ms_jiter',
             'stable_jiter_1000ms_jiter',
             'stable_300k_loss_20',
             'stable_300k_loss_50',
             'stable_loss_and_delay_30_200ms',
             'stable_loss_and_delay_50_200ms',
              # 突发弱网
             'burst_complex',
              #典型网络
             '3g',
             'edge',
             'LTE',
             'VERY_BAD_NETWORK',
              # 现网模拟
             'canteen',
             'drive',
             'dl-parking-rate',
             'india-office',
             'india-station',
             'sa',
             'vn-parking',
              # 周期性弱网
             'inter_loss_30%',
             'inter_loss_50%',
             'inter_500ms_jiter',
             'inter_1500ms_jiter',
             'inter_500ms_delay',
             'inter_1500ms_delay',
             'inter_200k',
             'inter_100k',
             'inter_200k_samllcatch',
             'inter_100k_samllcatch',
             'inter_200k_1s',
             'inter_100k_1s',
             'inter_200k_1s_samllcatch',
             'inter_100k_1s_samllcatch',
             'inter_400k_change_to_None',
             'inter_400k_change_to_None_samllcatch',
             'inter_200k_change_to_400k',
             'inter_200k_change_to_400k_samllcatch',
              # 背景流量
             'backgrpund_600k_udp',
             'backgrpund_600k_tcp',
             'backgrpund_600k_udp_smallcatch',
             'backgrpund_600k_tcp_smallcatch'
             ]



testSuite = {
    # 稳态丢包
    'stable_loss_30%':
        {
           'up': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'stable', 'only_udp': False},
           'down': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000,'style': 'stable', 'only_udp': False},
        },
    'stable_loss_50%':
        {
            'up': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000,'style': 'stable', 'only_udp': False},
        },
    'stable_loss_70%':
        {
            'up': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 70, 'packet': 1000, 'style': 'stable', 'only_udp': False},
            'down': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 70, 'packet': 1000, 'style': 'stable','only_udp': False},
        },

    # 稳态带宽限制
    'stable_band_200k':
        {
            'up': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable', 'only_udp': False},
            'down': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
        },
    'stable_band_100k':
        {
            'up': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
        },
    # 小缓存
    'stable_band_200k_samllcatch':
        {
            'up': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'stable','only_udp': False},
            'down': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'stable','only_udp': False},
        },
    'stable_band_100k_samllcatch':
        {
            'up': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'stable','only_udp': False},
            'down': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'stable','only_udp': False},
        },
    # 稳态抖动
    'stable_jiter_500ms_jiter':
        {
            'up': {'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0, 'packet': 1000, 'style': 'stable', 'only_udp': False},
            'down': {'band': 0, 'delay': 0, 'jiter':500, 'loss': 0, 'packet': 1000, 'style': 'stable', 'only_udp': False},
        },
    'stable_jiter_1000ms_jiter':
        {
            'up': {'band': 0, 'delay': 0, 'jiter': 1000, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down': {'band': 0, 'delay': 0, 'jiter': 1000, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
        },
    # 带限 + 丢包
    'stable_300k_loss_20':
        {
            'up': {'band': 300, 'delay': 0, 'jiter': 0, 'loss': 20, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down': {'band': 300, 'delay': 0, 'jiter': 0, 'loss': 20, 'packet': 1000, 'style': 'stable','only_udp': False},
        },
    'stable_300k_loss_50':
        {
            'up': {'band': 300, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down': {'band': 300, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'stable','only_udp': False},
        },

    # 丢包+ 延时
    'stable_loss_and_delay_30_200ms':
        {
            'up': {'band': 0, 'delay': 200, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'stable', 'only_udp': False},
            'down': {'band': 0, 'delay': 200, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'stable','only_udp': False},
        },
    'stable_loss_and_delay_50_200ms':
        {
            'up': {'band': 0, 'delay': 200, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down': {'band': 0, 'delay': 200, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'stable','only_udp': False},
        },

    # 复合网络
    'burst_complex':
        {
            'up': {'band': 1000, 'delay': 100, 'jiter': 100, 'loss': 30, 'packet': 1000, 'style': 'burst','only_udp': False},
            'down': {'band': 1000, 'delay': 100, 'jiter': 100, 'loss': 30, 'packet': 1000, 'style': 'burst','only_udp': False},
        },

    # 典型网络
    '3g':
        {
         'up':{'band': 330, 'delay': 100, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'stable', 'only_udp': False},
         'down':{ 'band': 780, 'delay': 100, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'stable', 'only_udp': False},
        },
    'edge':
        {
            'up':{'band': 240, 'delay': 400, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down':{'band': 200, 'delay': 440, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
        },
    'LTE':
        {
            'up':{'band': 10000, 'delay': 50, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down':{'band': 50000, 'delay': 65, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable','only_udp': False},
        },
    'VERY_BAD_NETWORK':
        {
            'up':{'direction': 'up', 'band': 1000, 'delay': 500, 'jiter': 0, 'loss': 10, 'packet': 1000, 'style': 'stable','only_udp': False},
            'down':{'direction': 'down', 'band': 1000, 'delay': 500, 'jiter': 0, 'loss': 10, 'packet': 1000,'style': 'stable', 'only_udp': False},
        },
    # 真实弱网模拟
    'canteen':
        {
            'up':{'band': 'ul-canteen-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
            'down':{'band': 'dl-canteen-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
        },
    'drive':
        {
            'up':{'band': 'ul-drive-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
            'down':{'band': 'dl-drive-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
        },
    'dl-parking-rate':
        {
            'up':{'band': 'ul-parking-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
            'down':{'band': 'dl-parking-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
        },

    'india-office':
        {
            'up':{'band': 'india-office-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
            'down':{'band': 'india-office-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
        },
    'india-station':
        {
            'up':{'band': 'india-station-ul', 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'real', 'only_udp': False},
            'down':{'band': 'india-station-ul', 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'real', 'only_udp': False},
        },
    'sa':
        {
            'up':{'band': 'sa-ul', 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'real', 'only_udp': False},
            'down':{'band': 'sa-ul', 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'real', 'only_udp': False},
        },

    'vn-parking':
        {
            'up':{'band': 'vn-parking-ul', 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'real', 'only_udp': False},
            'down':{'band': 'vn-parking-ul', 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'real', 'only_udp': False},
        },

    # 周期性丢包
    'inter_loss_30%':
        {
            'up': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'inter','only_udp': False},
            'down': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'inter', 'only_udp': False},
        },
    'inter_loss_50%':
        {
            'up': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'inter', 'only_udp': False},
            'down': {'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'inter','only_udp': False},
        },

    # 周期性抖动
    'inter_500ms_jiter':
        {
            'up': {'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0, 'packet': 1000, 'style': 'inter', 'only_udp': False},
            'down': {'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False},
        },
    'inter_1500ms_jiter':
        {
            'up': {'band': 0, 'delay': 0, 'jiter': 1500, 'loss': 0, 'packet': 1000, 'style': 'inter', 'only_udp': False},
            'down': {'band': 0, 'delay': 0, 'jiter': 1500, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False},
        },

    #  周期性延时
    'inter_500ms_delay':
        {
            'up': {'band': 0, 'delay': 500, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False},
            'down': {'band': 0, 'delay': 500, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False},
        },
    'inter_1500ms_delay':
        {
            'up': {'band': 0, 'delay': 1500, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter', 'only_udp': False},
            'down': {'band': 0, 'delay': 1500, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False},
        },

    # 周期性带限
    'inter_200k':
        {
            'up': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False},
            'down': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False},
        },
    'inter_100k':
        {
            'up': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter', 'only_udp': False},
            'down': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False},
        },


    # 小缓存
    'inter_200k_samllcatch':
        {
            'up': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter', 'only_udp': False},
            'down': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter','only_udp': False},
        },
    'inter_100k_samllcatch':
        {
            'up': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter', 'only_udp': False},
            'down': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter','only_udp': False},
        },


    # 周期性带限制
    'inter_200k_1s':
        {
            'up':{'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
            'down':{'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
        },
    'inter_100k_1s':
        {
            'up': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter', 'only_udp': False,'occupy': 1, 'idle': 30},
            'down': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'inter','only_udp': False, 'occupy': 1, 'idle': 30},
        },

    # 小缓存
    'inter_200k_1s_samllcatch':
        {
            'up': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter', 'only_udp': False,'occupy': 1, 'idle': 30},
            'down': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter','only_udp': False, 'occupy': 1, 'idle': 30},
        },
    'inter_100k_1s_samllcatch':
        {
            'up': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter', 'only_udp': False,'occupy': 1, 'idle': 30},
            'down': {'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter','only_udp': False, 'occupy': 1, 'idle': 30},
        },


    # 带宽变化
    'inter_400k_change_to_None':
        {
            'up': {'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},
            'down':{'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},
        },
    'inter_400k_change_to_None_samllcatch':
        {
            'up': {'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter', 'only_udp': False,'occupy': 30, 'idle': 60},
            'down': {'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter','only_udp': False, 'occupy': 30, 'idle': 60},
        },


    'inter_200k_change_to_400k':
        {
            'up': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60,'change':'0_400'},
            'down': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60,'change':'0_400'},
        },
    'inter_200k_change_to_400k_samllcatch':
        {
            'up': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter', 'only_udp': False,'occupy': 30, 'idle': 60, 'change': '0_400'},
            'down': {'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'inter','only_udp': False, 'occupy': 30, 'idle': 60, 'change': '0_400'},
        },

    # 背景流量
    'backgrpund_600k_udp':
        {
            'up':{'band': 600, 'delay': 0, 'jiter': 0,'loss': 0, 'packet': 1000, 'style': 'background', 'bg_type':'udp'},
            'down':{'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'background',  'bg_type': 'udp'},
        },
    'backgrpund_600k_tcp':
        {
            'up': {'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'background','bg_type': 'tcp'},
            'down': {'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'background','bg_type': 'tcp'},
        },
    'backgrpund_600k_udp_smallcatch':
        {
            'up': {'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'background','bg_type': 'udp'},
            'down': {'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'background','bg_type': 'udp'},
        },
    'backgrpund_600k_tcp_smallcatch':
        {
            'up': {'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'background','bg_type': 'tcp'},
            'down': {'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'background','bg_type': 'tcp'},
        },
}

if __name__ == '__main__':
    pass