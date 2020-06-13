import pandas as pd
import numpy as np
#import gc
import os

shared_data_path = r'C:\\Users\\Chris\\Documents\\code_kaggle_plasticc___shared_data\\PLAsTiCC-2018'

# read training data
col_dict = {'mjd': np.float64, 'flux': np.float32, 'flux_err': np.float32, 'object_id': np.int32, 'passband': np.int8,
            'detected': np.int8}
train_meta = pd.read_csv(os.path.join(shared_data_path, 'training_set_metadata.csv'))
train = pd.read_csv(os.path.join(shared_data_path, 'training_set.csv'), dtype=col_dict)


def calc_aggs(all_data, exact):

    # aggregate features
    band_aggs = all_data.groupby(['object_id', 'passband'])['flux'].agg(['mean', 'std', 'max', 'min']).unstack(-1)
    band_aggs.columns = [x + '_' + str(y) for x in band_aggs.columns.levels[0]
                          for y in band_aggs.columns.levels[1]]
    all_data.sort_values(['object_id', 'passband', 'flux'], inplace=True)
    # this way of calculating quantiles is faster than using the pandas quantile builtin on the groupby object
    all_data['group_count'] = all_data.groupby(['object_id', 'passband']).cumcount()
    all_data['group_size'] = all_data.groupby(['object_id', 'passband'])['flux'].transform('size')
    q_list = [0.25, 0.75]
    for q in q_list:
        all_data['q_' + str(q)] = all_data.loc[
            (all_data['group_size'] * q).astype(int) == all_data['group_count'], 'flux']
    quantiles = all_data.groupby(['object_id', 'passband'])[['q_' + str(q) for q in q_list]].max().unstack(-1)
    quantiles.columns = [str(x) + '_' + str(y) + '_quantile' for x in quantiles.columns.levels[0]
                         for y in quantiles.columns.levels[1]]

    new_data = pd.concat([band_aggs, quantiles], axis=1)             

    #new_data = pd.concat([band_aggs, quantiles, band_aggs_s, max_detected, time_between_detections[['det_period']],
    #                      time_between_detections_pb, extreme_max, extreme_min, extreme_max_s, extreme_min_s,
    #                      time_between_highs[['det_period_high']], quantiles_s, detection_time_dist,
    #                      detection_time_dist_all, det_aggs], axis=1)

    return new_data

# read test data
#test_meta = pd.read_csv(os.path.join(shared_data_path, 'test_set_metadata.csv'))
#test = pd.read_csv(os.path.join(shared_data_path, 'test_set_sample.csv'), dtype=col_dict)

# we observe test_set_metadata has many IDs that are not in the test_set_samples
# so create a test_meta_sub that contains only those IDs where there is accompanying data in test
#unique = test['object_id'].unique()
#criteria = test_meta['object_id'].isin(unique)
#test_meta_sub = test_meta[criteria]

# calculate features
new_data_exact = calc_aggs(train.copy(), True)



