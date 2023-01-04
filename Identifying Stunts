def identify_stunt(row):
    list1 = row["relative_location_list"]
    list2 = row['lag_relative_location_list']

    len1 = len(list1)
    len2 = len(list2)
    stunt_ids = []
    
    # Loosely checking if lists are from same play
    if len1 != len2:
      return "Error: mismatching lists"

    if list1 != list2:
     
      # Turning (1,2,3,4,5) into (0,1,2,3,4) for ease of indexing
      list1 = [int(x - 1) for x in list1]
      list2 = [int(x - 1) for x in list2]
  
      # Reordering lists so the relative positions are in order
      index = [0] * len1
      for i in range(len1):
          index[list1[i]] = i
  
      # (1,2,3,4,5) -> (2,1,3,4,5), or (0,1,2,3,4) -> (1,0,2,3,4)
      # far left stunt: 1
      if (list2[index[0]] == 1) & (list2[index[1]] == 0):
          stunt_ids.append(1)
  
      # (1,2,3,4,5) -> (1,2,3,5,4), or (0,1,2,3,4) -> (0,2,1,4,3)
      # far right stunt: 2
      if (list2[index[-1]] == len1-2) & (list2[index[-2]] == len1-1):
          stunt_ids.append(2)
  
      # (1,2,3,4,5) -> (3,2,1,4,5), or (0,1,2,3,4) -> (2,1,0,3,4)
      # far left-to-mid stunt: 3
      if (len1 > 2) & (list2[index[0]] in range(1,3)) & (list2[index[2]] == 0):
          stunt_ids.append(3)
      
      # (1,2,3,4,5) -> (1,2,5,4,3), or (0,1,2,3,4) -> (0,1,4,3,2)
      # far right-to-mid stunt: 4
      if (len1 > 2) & (list2[index[-1]] in range(len1-3, len1-1)) & (list2[index[-3]] == len1-1):
          stunt_ids.append(4)
  
      # (1,2,3,4,5) -> (1,3,2,4,5), or (0,1,2,3,4) -> (0,2,1,3,4)
      # left-mid stunt: 5
      if (len1 > 4) & (list2[index[1]] == 2) & (list2[index[2]] == 1):
          stunt_ids.append(5)
  
      # (1,2,3,4,5) -> (1,2,4,3,5), or (0,1,2,3,4) -> (0,1,3,2,4)
      # right-mid stunt: 6
      if (len1 > 4) & (list2[index[-2]] == len1-3) & (list2[index[-3]] == len1-2):
          stunt_ids.append(6)
  
      # If there's only a 4-man rush, left-mid & right-mid are the same
      # So we have a seventh stunt:
      # (1,2,3,4) -> (1,3,2,4), or (0,1,2,3) -> (0,2,1,4)
      # mid stunt: 7
      if (len1 == 4) & (list2[index[1]] == 2) & (list2[index[2]] == 1):
          stunt_ids.append(7)
  
      # (1,2,3,4,5) -> (1,4,3,2,5), or (0,1,2,3,4) -> (0,3,2,1,4)
      # (1,2,3,4,5,6) -> (1,5,3,4,2,6), or (0,1,2,3,4,5) -> (0,4,2,3,1,5)
      # left-bigmid: 8
      if (len1 >= 5) & (list2[index[1]] in range(3, len1-1)):
          stunt_ids.append(8)
      # (1,2,3,4,5) -> (1,4,3,2,5), or (0,1,2,3,4) -> (0,3,2,1,4)
      # (1,2,3,4,5,6) -> (1,2,5,4,3,6), or (0,1,2,3,4,5) -> (0,1,4,3,2,5)
      # right-bigmid: 9
      if (len1 >= 5) & (list2[index[len1-2]] in range(1, len1-3)):
        # if there is an 8 and a 9, then we change it to 10, the bigmid stunt because left-bigmid and right-bigmid could be identical
        if stunt_ids:
          if (stunt_ids[-1] in range(8,10)):
            stunt_ids.pop()
            stunt_ids.append(10)
          else:
            stunt_ids.append(9)
        else:
            stunt_ids.append(9)
      # really just an assortment of middle 
      # can be of length 5 (from above) or 6
      # bigmid stunt: 10
      if (len1 == 6) & ((list2[index[2]]) == 3):
        if stunt_ids:
          if (stunt_ids[-1] in range(8,10)):
            stunt_ids.pop()
        stunt_ids.append(10)

      # (1,2,3,4,5,6,7) -> (1,2,5,4,3,6,7), or (0,1,2,3,4,5,6) -> (0,1,4,3,2,5,6)
      if (len1 == 7) & (((list2[index[2]]) in range(3,5)) | list2[index[3]] == 4):
        if stunt_ids:
          if (stunt_ids[-1] in range(8,10)):
            stunt_ids.pop()
        stunt_ids.append(10)
  
      # If none of these stunts match but there is a change, we have an umbrella 'other' category
      # other stunt: 11
      if (not stunt_ids) & (list1 != list2):
          stunt_ids.append(11)

    stunt = 0
    if stunt_ids:
      stunt_ids.sort()
      s=[str(i) for i in stunt_ids]
      stunt = int("".join(s))
    
    return stunt
    
    
    
    
    
    
    
    
## pandas code to run the function    
   
   
   
m['stunt'] = None
m['lag_relative_location_list'] = m['relative_location_list'].shift(1)
m['lag_uId'] = m['uId'].shift(1)
for index, row in m.iterrows():
  if (index != 0) & (m.at[index, 'lag_uId'] == m.at[index, 'uId']) & (m.at[index, 'lag_relative_location_list'] != m.at[index, 'relative_location_list']):
    m.at[index, 'stunt'] = 1
  else:
    m.at[index, 'stunt'] = 0

  if m.at[index, 'stunt'] == 1:
    m['stunt_class'] = m[1:].apply(lambda row: identify_stunt(row), axis=1)    
