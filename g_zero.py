import pandas as pd
import numpy as np


def find_moraltiy_score(string_id):
    '''
    function to return morality score of a person when unique string id is
    passed as a parameter.

    :param string_id: unique string id of a person
    :return: morality score of the string_id
    '''
    seris = ((morality_score[morality_score['person id'] ==
                            string_id]).reset_index(drop = True)).iloc[:,1]
    return seris[0]

# setting a data directory
data_dir = './data/'

# reading in all the necessary files
morality_score = pd.read_csv(data_dir + 'sample_people_morality_score.csv')
friends = pd.read_csv(data_dir + 'friends.csv')
foes = pd.read_csv(data_dir + 'foes.csv')

# segregating good and bad people
good_people_accurate =  morality_score[morality_score['score'] > 0]
bad_people_accurate = morality_score[morality_score['score'] < 0]

# It is quite unlikely for a good person to be friends with a bad person
# the for loop finds out instances where good and bad
good_bad_friends = []
for i in range(friends.shape[1]):
    df = good_people_accurate[good_people_accurate['person id'].isin(
                                    friends.iloc[:,i])]
    if(i == 0):
        for person in df['person id']:
            df_look_out = friends[friends.iloc[:, i] == person]
            df_look_out = df_look_out[df_look_out.iloc[:, i + 1].isin(
                                            bad_people_accurate['person id'])]
            if(df_look_out.shape[0] > 0):
                good_bad_friends.append(df_look_out)
    else:
        for person in df['person id']:
            df_look_out = friends[friends.iloc[:, i] == person]
            df_look_out = df_look_out[df_look_out.iloc[:,i - 1].isin(
                                            bad_people_accurate['person id'])]
            if (df_look_out.shape[0] > 0):
                good_bad_friends.append(df_look_out)

# Just concatenating the dataframes in the list to make one big dataframe
df_unlikely_friends = pd.concat(good_bad_friends)



# adding morality scores for unlikely friends to figure out least likely
# friends
df_unlikely_friends['ms_p1'] =  df_unlikely_friends['person1'].apply(
                                                        find_moraltiy_score)
df_unlikely_friends['ms_p2'] =  df_unlikely_friends['person2'].apply(
                                                        find_moraltiy_score)

# sortimg morality scores to find out the least likely of friends
df_unlikely_friends.sort_values(by = ['ms_p1','ms_p2'], ascending=[False,
                                        True],inplace=True)

# writing the file in .csv format
df_unlikely_friends.to_csv(data_dir+'unlikely_friends.csv', index = False)



# foes_vstack = pd.concat([foes['person1'], foes['person2']], axis = 0).reset_index(drop = True)
# foes_vstack_set = list(set(foes_vstack))
# bool_ms_foes = morality_score['person id'].isin(foes_vstack_set)
# ms_people_with_foes = morality_score[bool_ms_foes].reset_index(drop = True)
# ms_people_with_no_foes = morality_score[np.logical_not(
#                                         bool_ms_foes)].reset_index(drop = True)











