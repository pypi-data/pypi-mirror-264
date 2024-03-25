# -*- coding: UTF-8 -*-

testSuite = [
    # 稳态丢包
    {'testcase': 'UP_20%', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 10, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'UP_30%', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'UP_50%', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'UP_70%', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 70, 'packet': 1000, 'style': 'stable', 'only_udp': False},

    {'testcase': 'DOWN_20%', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 10, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'DOWN_30%', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'DOWN_50%', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'DOWN_70%', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 70, 'packet': 1000,'style': 'stable', 'only_udp': False},
    # 稳态带宽限制
    {'testcase': 'UP_200k', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'UP_100k', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'DOWN_200k', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'DOWN_100k', 'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    # 小缓存
    {'testcase': 'up_200k_samllcatch', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1, 'style': 'stable', 'only_udp': False},
    {'testcase': 'up_100k_samllcatch', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1,'style': 'stable', 'only_udp': False},
    {'testcase': 'down_200k_samllcatch', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1,'style': 'stable', 'only_udp': False},
    {'testcase': 'down_100k_samllcatch', 'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0, 'packet': 1,'style': 'stable', 'only_udp': False},
    # 稳态抖动
    {'testcase': 'UP_500ms_jiter', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'up_1000ms_jiter', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 1000, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'up_2000ms_jiter', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 2000, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'down_500ms_jiter', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'down_1000ms_jiter', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 1000, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'down_2000ms_jiter', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 2000, 'loss': 0, 'packet': 1000,'style': 'stable', 'only_udp': False},
    # 带限 + 丢包
    {'testcase': 'up_300k_loss_20', 'direction': 'up', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 20, 'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'up_300k_loss_30', 'direction': 'up', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'up_300k_loss_50', 'direction': 'up', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'down_300k_loss_20', 'direction': 'down', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 20, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'down_300k_loss_30', 'direction': 'down', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000,'style': 'stable', 'only_udp': False},
    {'testcase': 'down_300k_loss_50', 'direction': 'down', 'band': 300, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000,'style': 'stable', 'only_udp': False},

    # 丢包+ 延时
    {'testcase': 'up_loss_and_delay_20_200ms', 'direction': 'up', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 20,'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'up_loss_and_delay_30_200ms', 'direction': 'up', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 30,'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'up_loss_and_delay_50_200ms', 'direction': 'up', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 50,'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'down_loss_and_delay_20_200ms', 'direction': 'down', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 20,'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'down_loss_and_delay_30_200ms', 'direction': 'down', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 30,'packet': 1000, 'style': 'stable', 'only_udp': False},
    {'testcase': 'down_loss_and_delay_50_200ms', 'direction': 'down', 'band': 0, 'delay': 200, 'jiter': 0, 'loss': 50,'packet': 1000, 'style': 'stable', 'only_udp': False},

    # 复合网络
    {'testcase': 'up_burst_complex', 'direction': 'up', 'band': 1000, 'delay': 100, 'jiter': 100, 'loss': 30,'packet': 1000, 'style': 'burst', 'only_udp': False},
    {'testcase': 'down_burst_complex', 'direction': 'down', 'band': 1000, 'delay': 100, 'jiter': 100, 'loss': 30,'packet': 1000, 'style': 'burst', 'only_udp': False},

    # 真实弱网模拟
    {'testcase': 'dl-canteen-rate', 'direction': 'down', 'band': 'dl-canteen-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'dl-drive-rate', 'direction': 'down', 'band': 'dl-drive-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'dl-parking-rate', 'direction': 'down', 'band': 'dl-parking-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'india-office-ul', 'direction': 'down', 'band': 'india-office-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'india-station-ul', 'direction': 'down', 'band': 'india-station-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'sa_ul', 'direction': 'down', 'band': 'sa_ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'vn-office-rate', 'direction': 'down', 'band': 'vn-office-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'vn-parking-ul', 'direction': 'down', 'band': 'vn-parking-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},

    {'testcase': 'india-office-ul', 'direction': 'up', 'band': 'india-office-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'india-station-ul', 'direction': 'up', 'band': 'india-station-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'sa_ul', 'direction': 'up', 'band': 'sa_ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'ul-canteen-rate', 'direction': 'up', 'band': 'ul-canteen-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'ul-drive-rate', 'direction': 'up', 'band': 'ul-drive-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'ul-parking-rate', 'direction': 'up', 'band': 'ul-parking-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'vn-office-rate', 'direction': 'up', 'band': 'vn-office-rate', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},
    {'testcase': 'vn-parking-ul', 'direction': 'up', 'band': 'vn-parking-ul', 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'real', 'only_udp': False},

    # 周期性丢包
    {'testcase': 'UP_30%_Intermittent', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30, 'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy':5,'idle':30},
    {'testcase': 'UP_40%_Intermittent', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 40, 'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy':5,'idle':30},
    {'testcase': 'UP_50%_Intermittent', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50, 'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy':5,'idle':30},

    {'testcase': 'DOWN_30%_Intermittent', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 30,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'DOWN_40%_Intermittent', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 40,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'DOWN_50%_Intermittent', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 0, 'loss': 50,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    # 周期性抖动
    {'testcase': 'UP_500ms_jiter_Intermittent', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'UP_1000ms_jiter_Intermittent', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 1000, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'UP_1500ms_jiter_Intermittent', 'direction': 'up', 'band': 0, 'delay': 0, 'jiter': 1500, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    {'testcase': 'DOWN_500ms_jiter_Intermittent', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 500, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'DOWN_1000ms_jiter_Intermittent', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 1000, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'DOWN_1500ms_jiter_Intermittent', 'direction': 'down', 'band': 0, 'delay': 0, 'jiter': 1500, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    #  周期性延时
    {'testcase': 'UP_500ms_delay_Intermittent', 'direction': 'up', 'band': 0, 'delay': 500, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'up_1500ms_delay_Intermittent', 'direction': 'up', 'band': 0, 'delay': 1000, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'up_1500ms_delay_Intermittent', 'direction': 'up', 'band': 0, 'delay': 1500, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    {'testcase': 'down_500ms_delay_Intermittent', 'direction': 'down', 'band': 0, 'delay': 500, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'down_1000ms_delay_Intermittent', 'direction': 'down', 'band': 0, 'delay': 1000, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'down_1500ms_delay_Intermittent', 'direction': 'down', 'band': 0, 'delay': 1500, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    # 周期性带限
    {'testcase': 'up_200k_Intermittent', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'up_100k_Intermittent', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'down_200k_Intermittent', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'down_100k_Intermittent', 'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},


    # 小缓存
    {'testcase': 'up_200k_Intermittent_samllcatch', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'up_100k_Intermittent_samllcatch', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'down_200k_Intermittent_samllcatch', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},
    {'testcase': 'down_100k_Intermittent_samllcatch', 'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30},

    # 周期性带限制
    {'testcase': 'up_200k_Intermittent_1s', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    {'testcase': 'up_100k_Intermittent_1s', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    {'testcase': 'down_200k_Intermittent_1s', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    {'testcase': 'down_100k_Intermittent_1s', 'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    # 小缓存
    {'testcase': 'up_200k_Intermittent_samllcatch_1s', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    {'testcase': 'up_100k_Intermittent_samllcatch_1s', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    {'testcase': 'down_200k_Intermittent_samllcatch_1s', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},
    {'testcase': 'down_100k_Intermittent_samllcatch_1s', 'direction': 'down', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 1, 'idle': 30},

    # 带宽变化
    {'testcase': 'up_400k_change_to_None', 'direction': 'up', 'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},
    {'testcase': 'down_400k_change_to_None', 'direction': 'down', 'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},

    {'testcase': 'up_400k_change_to_None_samllcatch', 'direction': 'up', 'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},
    {'testcase': 'down_400k_change_to_None_samllcatch', 'direction': 'down', 'band': 400, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60},

    {'testcase': 'up_200k_change_to_400k', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60,'change':'0_400'},
    {'testcase': 'down_200k_change_to_400k', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60,'change':'0_400'},

    {'testcase': 'up_200k_change_to_400k_samllcatch', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60, 'change': '0_400'},
    {'testcase': 'down_200k_change_to_400k_samllcatch', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60, 'change': '0_400'},
    #
    # 双向网络
    {'testcase': 'double_200k_Intermittent', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30,'doubleNet':1},
    {'testcase': 'double_100k_Intermittent', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30,'doubleNet':1},

    {'testcase': 'double_200k_Intermittent_samllcatch', 'direction': 'up', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30,'doubleNet':1},
    {'testcase': 'double_100k_Intermittent_samllcatch', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 5, 'idle': 30,'doubleNet':1},


    # 背景流量

    {'testcase': 'up_backgrpund_600k_udp', 'direction': 'up', 'band': 600, 'delay': 0, 'jiter': 0,'loss': 0, 'packet': 1000, 'style': 'background', 'bg_type':'udp'},
    {'testcase': 'down_backgrpund_600k_udp', 'direction': 'down', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'background',  'bg_type': 'udp'},
    {'testcase': 'up_backgrpund_600k_tcp', 'direction': 'up', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'background',  'bg_type': 'tcp'},
    {'testcase': 'down_backgrpund_600k_tcp', 'direction': 'down', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1000, 'style': 'background',  'bg_type': 'tcp'},

    {'testcase': 'up_backgrpund_600k_udp_smallcatch', 'direction': 'up', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'background', 'bg_type': 'udp'},
    {'testcase': 'down_backgrpund_600k_udp_smallcatch', 'direction': 'down', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'background', 'bg_type': 'udp'},
    {'testcase': 'up_backgrpund_600k_tcp_smallcatch', 'direction': 'up', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'background', 'bg_type': 'tcp'},
    {'testcase': 'down_backgrpund_600k_tcp_smallcatch', 'direction': 'down', 'band': 600, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'background', 'bg_type': 'tcp'},
]
