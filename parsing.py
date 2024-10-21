import json
import os
import pandas as pd

original_log_file_path = '240524'
filtered_log_file_path = 'filtered_log'

user_trajectory_df = pd.read_csv(f'{original_log_file_path}/log.csv')
if not os.path.exists(filtered_log_file_path):
    os.makedirs(filtered_log_file_path)

def parse_action_sequence(action_sequence):
    try:
        parsed_trajectory = []
        for action in json.loads(action_sequence):
            state = {
                'grid': action.get('grid'),
                'object': action.get('object'),
                'overlapped': action.get('overlapped')
            }
            action_data = {
                'operation': action.get('operation'),
                'position': action.get('position'),
                'color': action.get('color')
            }
            parsed_trajectory.append((state, action_data))
        return parsed_trajectory
    except json.JSONDecodeError:
        print("Error decoding JSON data")
        return []

for task_id in range(1, 401):
    filtered_df = user_trajectory_df[user_trajectory_df['taskId'] == task_id].copy()
    
    if not filtered_df.empty:
        filtered_df['parsed_trajectory'] = filtered_df['actionSequence'].apply(parse_action_sequence)

        filtered_csv_path = f'{filtered_log_file_path}/{task_id}.csv'
        filtered_df.to_csv(filtered_csv_path, index=False)
        
        print(f"Filtered data saved to {filtered_csv_path} with {len(filtered_df)} lines.")