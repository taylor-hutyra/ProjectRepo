# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 21:30:28 2017

@author: jarre14
"""

from setup import *

champ_info = get_champions()
print(champ_info)


game_data = Dataframe_From_CSV('LeagueofLegends.csv')
ban = Dataframe_From_CSV('banValues.csv')


ban_1_top = ban['ban_1'].value_counts().head(5).reset_index()
ban_2_top = ban['ban_2'].value_counts().head(5)
ban_3_top = ban['ban_3'].value_counts().head(5)

abc = pd.merge(ban_1_top,champ_info, left_on='index', right_on='id')
print(abc)
print(ban_1_top)
print(ban_2_top)
print(ban_3_top)

top_blue_teams = game_data[game_data['bResult'] =='1'].value_counts().reset_index()
print(top_blue_teams)
top_red_teams = game_data['redTeam'].value_counts().reset_index()


#ls = [get_champion_detail(a) for a in champ_info['id']]
#print(ls)
abcd = get_champion_detail('Aatrox')
print(abcd)

# maybe need to do a classifier, and see if the teams 