import json
import numpy as np
import pandas as pd

def preprocess():
    df = pd.read_csv(f'./240524/log.csv',parse_dates=['startedAt','endedAt'])
        # id,startedAt,endedAt,userId,taskId,actionSequence

    df_userrecord = pd.read_csv(f'./240524/userrecord.csv')
        # id,userId,taskId,logId,trial,success,action,score,time
    df.drop(3093,inplace=True)
    df['dt']=df['endedAt']-df['startedAt']
    df.drop(['endedAt','startedAt'],axis=1,inplace=True)
    df=df.merge(df_userrecord,left_on='id',right_on='logId',how='inner')

    df.drop(['id_x','id_y', 'userId_y','taskId_y','time','action'],axis=1,inplace=True)
    df.rename(columns={'userId_x':'userId','taskId_x':'taskId'},inplace=True)
    
    return df

def action_sequence_parser(action_sequence):
    action_sequence = json.loads(action_sequence.strip())
    
    
    return json.dumps(action_sequence)
    return action_sequence

# Categories = {'Critical', 'Clipboard', 'Coloring', 'History', 'O2', 'Selection'}
# operation = {'Submit',  'ResizeGrid', 'Undo', 'Redo'
#               'SelectObject', ''SelectGrid', SelectCell', 
#               'Rotate', 'Move', 'Flip', 
#               'Copy', 'Paste',
#               'Paint'
#             }

# 'SelectGrid'


if __name__ == '__main__':
    df = preprocess()
    #print(df[['taskId','userId']].groupby(['taskId']).agg(lambda d: len(np.unique(d))).sort_values(by='userId')[-20:].sort_values(by='taskId'))
    #print(df[['taskId','userId']][df['success']==1].groupby(['taskId']).count().sort_values(by='userId')[-20:])
    #print(json.loads(df['actionSequence'][0]))
    
    actseq = df['actionSequence']
    
    categories = set()
    for i in range(len(actseq)):
        action_sequence = json.loads(actseq[i])
        for action in action_sequence:
            categories.add(action['operation'])
    #print(categories)

    
    #df['actionSequence'] = df['actionSequence'].apply(action_sequence_parser)
    print(df.head())