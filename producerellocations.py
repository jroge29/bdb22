import pandas as pd
import numpy as np
import plotly.graph_objects as go

plays = pd.read_csv(r'C:\Users\18172\Desktop\Big data bowl\plays.csv')
week1 = pd.read_csv(r'C:\Users\18172\Desktop\Big data bowl\week1.csv')
pff = pd.read_csv(r'C:\Users\18172\Desktop\Big data bowl\pffScoutingData.csv')
players = pd.read_csv(r'C:\Users\18172\Desktop\Big data bowl\players.csv')

data = week1.merge(pff, how = 'left')

data['uId'] = data['gameId'].to_string() + "-" + data['playId'].to_string()

idxs = (data
        .loc[data['event'] == 'ball_snap',
                 'frameId']
        .index
        .values)

x = [(idxs+x).tolist() for x in range(0,24)]
idxs = [item for sublist in x for item in sublist]

df = data.loc[idxs]

_los = (data
        .loc[(data['team']=='football') &
             (data['frameId']==1),
             ['gameId', 'playId', 'x']]
        .rename(columns={'x':'los'}))

_ball = (data
        .loc[(data['team']=='football') &
             (data['frameId']==1),
             ['gameId', 'playId', 'y']]
        .rename(columns={'y':'cop'}))

df = df.merge(_los)
df = df.merge(_ball)

p_r = df[df['pff_role'] == "Pass Rush"]

def zones (row):
    rel_pos = row['cop'] - row['y']
    
    #add a line that accounts for non lineman, and sets their zone to something different
    #also need to determine what direction the defense is facing and adjust accordingly
    #rn I have 14 zones at half a yard each which is arbitrary
    pos = row["pff_positionLinedUp"] 
    corners = ["LCB", "RCB", "SCBiL", "SCBiR", "SCBL",  "SCBoL", "SCBoR", "SCBR"]
#     if pos in corners:
#         if row['playDirection'] == 'right':
#             if rel_pos<-3:
#                 return -100
#             else:
#                 return 100
#         if row['playDirection'] == 'left':
#             if rel_pos<-3:
#                 return 100
#             else:
#                 return -100
    
#     vert_pos = row['los'] - row['y']
    
#     if abs(vert_pos > 1.5):
#         return -2
    
    if row['playDirection'] == 'right':
        if (rel_pos < -3):
            return 1
        elif (rel_pos < -2.5):
            return 2
        elif (rel_pos < -2):
            return 3
        elif (rel_pos < -1.5):
            return 4
        elif (rel_pos < -1):
            return 5
        elif (rel_pos < -.5):
            return 6
        elif (rel_pos < 0):
            return 7
        elif (rel_pos < .5):
            return 8
        elif (rel_pos < 1):
            return 9
        elif (rel_pos < 1.5):
            return 10
        elif (rel_pos < 2):
            return 11
        elif (rel_pos < 2.5):
            return 12
        elif (rel_pos < 3):
            return 13
        elif (rel_pos >= 3):
            return 14
        return 'Other'
    else:
        if (rel_pos < -3):
            return 14
        elif (rel_pos < -2.5):
            return 13
        elif (rel_pos < -2):
            return 12
        elif (rel_pos < -1.5):
            return 1
        elif (rel_pos < -1):
            return 10
        elif (rel_pos < -.5):
            return 9
        elif (rel_pos < 0):
            return 8
        elif (rel_pos < .5):
            return 7
        elif (rel_pos < 1):
            return 6
        elif (rel_pos < 1.5):
            return 5
        elif (rel_pos < 2):
            return 4
        elif (rel_pos < 2.5):
            return 3
        elif (rel_pos < 3):
            return 2
        elif (rel_pos >= 3):
            return 1
        return 'Other'
    
    
    
p_r['zone'] = p_r.apply (lambda row: zones(row), axis=1)


current_timestamp = None
locations_at_timestamp = []
relative_locations_at_timestamp = {}

for index, row in p_r.iterrows():
    if row['time'] != current_timestamp:
        # New timestamp, so update the current timestamp and reset the list of locations
        current_timestamp = row['time']
        locations_at_timestamp = []
    pos = row["pff_positionLinedUp"] 
    corners = ["LCB", "RCB", "SCBiL", "SCBiR", "SCBL",  "SCBoL", "SCBoR", "SCBR"]
    vert_pos = (row['los'] - row['x'])
    if row['playDirection'] == "right":
        vert_pos = vert_pos * -1
    
 
    locations_at_timestamp.append(row['y'])
    
    # Step 3: Sort the list of locations at each timestamp
    locations_at_timestamp.sort()
    
    # Step 4: Assign a relative location to each player at each timestamp
    relative_locations = {}
    for i, location in enumerate(locations_at_timestamp):
        if pos in corners:
            relative_locations[location] = (i + 1,3)
        elif vert_pos>1.5:
            relative_locations[location] = (i + 1,2)
        else:
            relative_locations[location] = (i + 1,1)
        
    # Store the relative locations for each player at this timestamp
    relative_locations_at_timestamp[current_timestamp] = relative_locations
    
counte = 0
count = 0
p_r['relative_location'] = None


for index, row in p_r.iterrows():
    try:
        p_r.at[index, 'relative_location'] = relative_locations_at_timestamp[row['time']][row['y']]
        count += 1
    except KeyError:
        print("KeyError occurred at index {}".format(index))
        p_r.at[index, 'relative_location'] = 0
        counte += 1
        
def group_and_create_column(df, group_col, value_col):
  # Group the dataframe by the specified column
  grouped_df = df.groupby(group_col)
  
  # Create a new column with a list of all the values in the specified column for each group
  new_df = grouped_df[value_col].apply(list).reset_index()
  
  # Rename the column to include the name of the original column
  new_df = new_df.rename(columns={value_col: f"{value_col}_list"})
  
  return new_df

b = group_and_create_column(p_r, 'time', 'relative_location')

m = pd.merge(p_r, b, on = "time", how = "outer")

m = m[['gameId', 'playId', 'nflId', 'time', 'team', 'playDirection', 'x', 'y', 's', 'a', 'dis', 'o', 'dir', 'event', 'pff_role', 'pff_positionLinedUp', 'los', 'cop', 'zone', 'relative_location', 'relative_location_list']]
        
