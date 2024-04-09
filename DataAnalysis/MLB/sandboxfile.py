from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup

# find Chris Sale's player id (mlbam_key)
plid = playerid_lookup('wheeler','zack')

# # get all available data Start and end date
data = statcast_pitcher('2023-04-01', '2023-10-4', player_id = plid['key_mlbam'])

# # get data for July 15th, 2017
# data = statcast_pitcher('2017-07-15', player_id = 519242)