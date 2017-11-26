import json
import pandas as pd
import csv
from sklearn import preprocessing
import numpy as np

# path leds to the folder containing the Champion json files
# match_path leads to the folder containing the LeagueofLegends file
path = 'C:/Users/Janine Prukop/Documents/MATH5364/ProjectRepo/ProjectRepo/Champions/'
match_path = 'C:/Users/Janine Prukop/Documents/MATH5364/ProjectRepo/ProjectRepo/'





# Read in the match information and turn it into a dataframe
match_results = pd.read_csv(match_path + 'LeagueofLegends.csv', header = None)
match_results.columns = match_results.iloc[0] # set column names
match_results = match_results.iloc[1:,:] # get rid of the first row

# Create series of the picks for each lane position
top = match_results['blueTopChamp'].append(match_results['redTopChamp'])
jungle = match_results['blueJungleChamp'].append(match_results['redJungleChamp'])
middle = match_results['blueMiddleChamp'].append(match_results['redMiddleChamp'])
adc = match_results['blueADCChamp'].append(match_results['redADCChamp'])
support = match_results['blueSupportChamp'].append(match_results['redSupportChamp'])

# Create Series of the count for each Champ, with the name as the index value
top_champs = top.value_counts()
jungle_champs = jungle.value_counts()
middle_champs = middle.value_counts()
adc_champs = adc.value_counts()
support_champs = support.value_counts()

#Append all the series into one dataframe, and set any NA value to 0 - 0 occurances of that champ in that position
full_counts = pd.concat([top_champs, jungle_champs, middle_champs, adc_champs, support_champs], axis = 1, ignore_index=False)
full_counts = full_counts.rename(index=str, columns= {0 : 'top', 1 : 'jungle', 2 : 'middle', 3 : 'adc', 4 : 'support'})
full_counts = full_counts.fillna(0)

# Realized I had rows that had a single count of one for the red and blue labels, dropped them
full_counts = full_counts.drop(['blueADCChamp', 'blueJungleChamp', 'blueMiddleChamp', 'blueSupportChamp', 'blueTopChamp', 'redADCChamp', 'redJungleChamp', 'redMiddleChamp', 'redSupportChamp', 'redTopChamp'])

# Turning the counts into a percentage of that position for the champion
index_li = full_counts.index
for p in index_li: full_counts.loc[p] = full_counts.loc[p]/sum(full_counts.loc[p])

# "true" positions for each champion
true_pos = full_counts.idxmax(axis = 1)





# Reading all the json files with the champion data, reads in as dictionaries
aatrox_dic = json.load(open(path + 'Aatrox.json'))
ahri_dic = json.load(open(path + 'Ahri.json'))
akali_dic = json.load(open(path + 'Akali.json'))
alistar_dic = json.load(open(path + 'Alistar.json'))
amumu_dic = json.load(open(path + 'Amumu.json'))
anivia_dic = json.load(open(path + 'Anivia.json'))
annie_dic = json.load(open(path + 'Annie.json'))
ashe_dic = json.load(open(path + 'Ashe.json'))
aurelionsol_dic = json.load(open(path + 'AurelionSol.json'))
azir_dic = json.load(open(path + 'Azir.json'))
bard_dic = json.load(open(path + 'Bard.json'))
blitzcrank_dic = json.load(open(path + 'Blitzcrank.json'))
brand_dic = json.load(open(path + 'Brand.json'))
braum_dic = json.load(open(path + 'Braum.json'))
caitlyn_dic = json.load(open(path + 'Caitlyn.json'))
camille_dic = json.load(open(path + 'Camille.json'))
cassiopeia_dic = json.load(open(path + 'Cassiopeia.json'))
chogath_dic = json.load(open(path + 'Chogath.json'))
corki_dic = json.load(open(path + 'Corki.json'))
darius_dic = json.load(open(path + 'Darius.json'))
diana_dic = json.load(open(path + 'Diana.json'))
draven_dic = json.load(open(path + 'Draven.json'))
drmundo_dic = json.load(open(path + 'DrMundo.json'))
ekko_dic = json.load(open(path + 'Ekko.json'))
elise_dic = json.load(open(path + 'Elise.json'))
evelynn_dic = json.load(open(path + 'Evelynn.json'))
ezreal_dic = json.load(open(path + 'Ezreal.json'))
fiddlesticks_dic = json.load(open(path + 'FiddleSticks.json'))
fiora_dic = json.load(open(path + 'Fiora.json'))
fizz_dic = json.load(open(path + 'Fizz.json'))
galio_dic = json.load(open(path + 'Galio.json'))
gangplank_dic = json.load(open(path + 'Gangplank.json'))
garen_dic = json.load(open(path + 'Garen.json'))
gnar_dic = json.load(open(path + 'Gnar.json'))
gragas_dic = json.load(open(path + 'Gragas.json'))
graves_dic = json.load(open(path + 'Graves.json'))
hecarim_dic = json.load(open(path + 'Hecarim.json'))
heimerdinger_dic = json.load(open(path + 'Heimerdinger.json'))
illaoi_dic = json.load(open(path + 'Illaoi.json'))
irelia_dic = json.load(open(path + 'Irelia.json'))
ivern_dic = json.load(open(path + 'Ivern.json'))
janna_dic = json.load(open(path + 'Janna.json'))
jarvaniv_dic = json.load(open(path + 'JarvanIV.json'))
jax_dic = json.load(open(path + 'Jax.json'))
jayce_dic = json.load(open(path + 'Jayce.json'))
jhin_dic = json.load(open(path + 'Jhin.json'))
jinx_dic = json.load(open(path + 'Jinx.json'))
kalista_dic = json.load(open(path + 'Kalista.json'))
karma_dic = json.load(open(path + 'Karma.json'))
karthus_dic = json.load(open(path + 'Karthus.json'))
kassadin_dic = json.load(open(path + 'Kassadin.json'))
katarina_dic = json.load(open(path + 'Katarina.json'))
kayle_dic = json.load(open(path + 'Kayle.json'))
kennen_dic = json.load(open(path + 'Kennen.json'))
khazix_dic = json.load(open(path + 'Khazix.json'))
kindred_dic = json.load(open(path + 'Kindred.json'))
kled_dic = json.load(open(path + 'Kled.json'))
kogmaw_dic = json.load(open(path + 'KogMaw.json'))
leblanc_dic = json.load(open(path + 'Leblanc.json'))
leesin_dic = json.load(open(path + 'LeeSin.json'))
leona_dic = json.load(open(path + 'Leona.json'))
lissandra_dic= json.load(open(path + 'Lissandra.json'))
lucian_dic = json.load(open(path + 'Lucian.json'))
lulu_dic = json.load(open(path + 'Lulu.json'))
lux_dic = json.load(open(path + 'Lux.json'))
malphite_dic = json.load(open(path + 'Malphite.json'))
malzahar_dic = json.load(open(path + 'Malzahar.json'))
maokai_dic = json.load(open(path + 'Maokai.json'))
masteryi_dic = json.load(open(path + 'MasterYi.json'))
missfortune_dic = json.load(open(path + 'MissFortune.json'))
monkeyking_dic = json.load(open(path + 'MonkeyKing.json'))
mordekaiser_dic = json.load(open(path + 'Mordekaiser.json'))
morgana_dic = json.load(open(path + 'Morgana.json'))
nami_dic = json.load(open(path + 'Nami.json'))
nasus_dic = json.load(open(path + 'Nasus.json'))
nautilus_dic = json.load(open(path + 'Nautilus.json'))
nidalee_dic = json.load(open(path + 'Nidalee.json'))
nocturne_dic = json.load(open(path + 'Nocturne.json'))
nunu_dic = json.load(open(path + 'Nunu.json'))
olaf_dic = json.load(open(path + 'Olaf.json'))
orianna_dic = json.load(open(path + 'Orianna.json'))
pantheon_dic = json.load(open(path + 'Pantheon.json'))
poppy_dic = json.load(open(path + 'Poppy.json'))
quinn_dic = json.load(open(path + 'Quinn.json'))
rammus_dic = json.load(open(path + 'Rammus.json'))
reksai_dic = json.load(open(path + 'RekSai.json'))
renekton_dic = json.load(open(path + 'Renekton.json'))
rengar_dic = json.load(open(path + 'Rengar.json'))
riven_dic = json.load(open(path + 'Riven.json'))
rumble_dic = json.load(open(path + 'Rumble.json'))
ryze_dic = json.load(open(path + 'Ryze.json'))
sejuani_dic = json.load(open(path + 'Sejuani.json'))
shaco_dic = json.load(open(path + 'Shaco.json'))
shen_dic = json.load(open(path + 'Shen.json'))
shyvana_dic = json.load(open(path + 'Shyvana.json'))
singed_dic = json.load(open(path + 'Singed.json'))
sion_dic = json.load(open(path + 'Sion.json'))
sivir_dic = json.load(open(path + 'Sivir.json'))
skarner_dic = json.load(open(path + 'Skarner.json'))
sona_dic = json.load(open(path + 'Sona.json'))
soraka_dic = json.load(open(path + 'Soraka.json'))
swain_dic = json.load(open(path + 'Swain.json'))
syndra_dic = json.load(open(path + 'Syndra.json'))
tahmkench_dic = json.load(open(path + 'TahmKench.json'))
taliyah_dic = json.load(open(path + 'Taliyah.json'))
talon_dic = json.load(open(path + 'Talon.json'))
taric_dic = json.load(open(path + 'Taric.json'))
teemo_dic = json.load(open(path + 'Teemo.json'))
thresh_dic = json.load(open(path + 'Thresh.json'))
tristana_dic = json.load(open(path + 'Tristana.json'))
trundle_dic = json.load(open(path + 'Trundle.json'))
tryndamere_dic = json.load(open(path + 'Tryndamere.json'))
twistedfate_dic = json.load(open(path + 'TwistedFate.json'))
twitch_dic = json.load(open(path + 'Twitch.json'))
udyr_dic = json.load(open(path + 'Udyr.json'))
urgot_dic = json.load(open(path + 'Urgot.json'))
varus_dic = json.load(open(path + 'Varus.json'))
vayne_dic = json.load(open(path + 'Vayne.json'))
veigar_dic = json.load(open(path + 'Veigar.json'))
velkoz_dic = json.load(open(path + 'Velkoz.json'))
vi_dic = json.load(open(path + 'Vi.json'))
viktor_dic = json.load(open(path + 'Viktor.json'))
vladimir_dic = json.load(open(path + 'Vladimir.json'))
volibear_dic = json.load(open(path + 'Volibear.json'))
warwick_dic = json.load(open(path + 'Warwick.json'))
xerath_dic = json.load(open(path + 'Xerath.json'))
xinzhao_dic = json.load(open(path + 'XinZhao.json'))
yasuo_dic = json.load(open(path + 'Yasuo.json'))
yorick_dic = json.load(open(path + 'Yorick.json'))
zac_dic = json.load(open(path + 'Zac.json'))
zed_dic = json.load(open(path + 'Zed.json'))
ziggs_dic = json.load(open(path + 'Ziggs.json'))
zilean_dic = json.load(open(path + 'Zilean.json'))
zyra_dic = json.load(open(path + 'Zyra.json'))


# Cleans off the first layers of headers, and creating a list off of them
all_champs_li = [aatrox_dic['data']['Aatrox'], ahri_dic['data']['Ahri'], akali_dic['data']['Akali'], alistar_dic['data']['Alistar'], amumu_dic['data']['Amumu'], 
                 anivia_dic['data']['Anivia'], annie_dic['data']['Annie'], ashe_dic['data']['Ashe'], aurelionsol_dic['data']['AurelionSol'], azir_dic['data']['Azir'], 
                 bard_dic['data']['Bard'], blitzcrank_dic['data']['Blitzcrank'], brand_dic['data']['Brand'], braum_dic['data']['Braum'], caitlyn_dic['data']['Caitlyn'],
                 camille_dic['data']['Camille'], cassiopeia_dic['data']['Cassiopeia'], chogath_dic['data']['Chogath'], corki_dic['data']['Corki'], darius_dic['data']['Darius'],
                 diana_dic['data']['Diana'], draven_dic['data']['Draven'], drmundo_dic['data']['DrMundo'], ekko_dic['data']['Ekko'], elise_dic['data']['Elise'],
                 evelynn_dic['data']['Evelynn'], ezreal_dic['data']['Ezreal'], fiddlesticks_dic['data']['FiddleSticks'], fiora_dic['data']['Fiora'], fizz_dic['data']['Fizz'],
                 galio_dic['data']['Galio'], gangplank_dic['data']['Gangplank'], garen_dic['data']['Garen'], gnar_dic['data']['Gnar'], gragas_dic['data']['Gragas'],
                 graves_dic['data']['Graves'], hecarim_dic['data']['Hecarim'], heimerdinger_dic['data']['Heimerdinger'], illaoi_dic['data']['Illaoi'], irelia_dic['data']['Irelia'],
                 ivern_dic['data']['Ivern'], janna_dic['data']['Janna'], jarvaniv_dic['data']['JarvanIV'], jax_dic['data']['Jax'], jayce_dic['data']['Jayce'],
                 jhin_dic['data']['Jhin'], jinx_dic['data']['Jinx'], kalista_dic['data']['Kalista'], karma_dic['data']['Karma'], karthus_dic['data']['Karthus'],
                 kassadin_dic['data']['Kassadin'], katarina_dic['data']['Katarina'], kayle_dic['data']['Kayle'], kennen_dic['data']['Kennen'], khazix_dic['data']['Khazix'],
                 kindred_dic['data']['Kindred'], kled_dic['data']['Kled'], kogmaw_dic['data']['KogMaw'], leblanc_dic['data']['Leblanc'], leesin_dic['data']['LeeSin'],
                 leona_dic['data']['Leona'], lissandra_dic['data']['Lissandra'], lucian_dic['data']['Lucian'], lulu_dic['data']['Lulu'], lux_dic['data']['Lux'],
                 malphite_dic['data']['Malphite'], malzahar_dic['data']['Malzahar'], maokai_dic['data']['Maokai'], masteryi_dic['data']['MasterYi'], missfortune_dic['data']['MissFortune'],
                 monkeyking_dic['data']['MonkeyKing'], mordekaiser_dic['data']['Mordekaiser'], morgana_dic['data']['Morgana'], nami_dic['data']['Nami'], nasus_dic['data']['Nasus'],
                 nautilus_dic['data']['Nautilus'], nidalee_dic['data']['Nidalee'], nocturne_dic['data']['Nocturne'], nunu_dic['data']['Nunu'], olaf_dic['data']['Olaf'],
                 orianna_dic['data']['Orianna'], pantheon_dic['data']['Pantheon'], poppy_dic['data']['Poppy'], quinn_dic['data']['Quinn'], rammus_dic['data']['Rammus'],
                 reksai_dic['data']['RekSai'], renekton_dic['data']['Renekton'], rengar_dic['data']['Rengar'], riven_dic['data']['Riven'], rumble_dic['data']['Rumble'],
                 ryze_dic['data']['Ryze'], sejuani_dic['data']['Sejuani'], shaco_dic['data']['Shaco'], shen_dic['data']['Shen'], shyvana_dic['data']['Shyvana'],
                 singed_dic['data']['Singed'], sion_dic['data']['Sion'], sivir_dic['data']['Sivir'], skarner_dic['data']['Skarner'], sona_dic['data']['Sona'], 
                 soraka_dic['data']['Soraka'], swain_dic['data']['Swain'], syndra_dic['data']['Syndra'], tahmkench_dic['data']['TahmKench'], taliyah_dic['data']['Taliyah'],
                 talon_dic['data']['Talon'], taric_dic['data']['Taric'], teemo_dic['data']['Teemo'], thresh_dic['data']['Thresh'], tristana_dic['data']['Tristana'],
                 trundle_dic['data']['Trundle'], tryndamere_dic['data']['Tryndamere'], twistedfate_dic['data']['TwistedFate'], twitch_dic['data']['Twitch'], udyr_dic['data']['Udyr'],
                 urgot_dic['data']['Urgot'], varus_dic['data']['Varus'], vayne_dic['data']['Vayne'], veigar_dic['data']['Veigar'], velkoz_dic['data']['Velkoz'],
                 vi_dic['data']['Vi'], viktor_dic['data']['Viktor'], vladimir_dic['data']['Vladimir'], volibear_dic['data']['Volibear'], warwick_dic['data']['Warwick'],
                 xerath_dic['data']['Xerath'], xinzhao_dic['data']['XinZhao'], yasuo_dic['data']['Yasuo'], yorick_dic['data']['Yorick'], zac_dic['data']['Zac'],
                 zed_dic['data']['Zed'], ziggs_dic['data']['Ziggs'], zilean_dic['data']['Zilean'], zyra_dic['data']['Zyra']]
 
# Turns the list into a data frame 
all_champs_df = pd.DataFrame(all_champs_li)
 
# makes a list of the 'info' for each champion (attack, defense, difficulty, magic) 
info_li = [aatrox_dic['data']['Aatrox']['info'], ahri_dic['data']['Ahri']['info'], akali_dic['data']['Akali']['info'], alistar_dic['data']['Alistar']['info'], amumu_dic['data']['Amumu']['info'], 
             anivia_dic['data']['Anivia']['info'], annie_dic['data']['Annie']['info'], ashe_dic['data']['Ashe']['info'], aurelionsol_dic['data']['AurelionSol']['info'], azir_dic['data']['Azir']['info'], 
             bard_dic['data']['Bard']['info'], blitzcrank_dic['data']['Blitzcrank']['info'], brand_dic['data']['Brand']['info'], braum_dic['data']['Braum']['info'], caitlyn_dic['data']['Caitlyn']['info'],
             camille_dic['data']['Camille']['info'], cassiopeia_dic['data']['Cassiopeia']['info'], chogath_dic['data']['Chogath']['info'], corki_dic['data']['Corki']['info'], darius_dic['data']['Darius']['info'],
             diana_dic['data']['Diana']['info'], draven_dic['data']['Draven']['info'], drmundo_dic['data']['DrMundo']['info'], ekko_dic['data']['Ekko']['info'], elise_dic['data']['Elise']['info'],
             evelynn_dic['data']['Evelynn']['info'], ezreal_dic['data']['Ezreal']['info'], fiddlesticks_dic['data']['FiddleSticks']['info'], fiora_dic['data']['Fiora']['info'], fizz_dic['data']['Fizz']['info'],
             galio_dic['data']['Galio']['info'], gangplank_dic['data']['Gangplank']['info'], garen_dic['data']['Garen']['info'], gnar_dic['data']['Gnar']['info'], gragas_dic['data']['Gragas']['info'],
             graves_dic['data']['Graves']['info'], hecarim_dic['data']['Hecarim']['info'], heimerdinger_dic['data']['Heimerdinger']['info'], illaoi_dic['data']['Illaoi']['info'], irelia_dic['data']['Irelia']['info'],
             ivern_dic['data']['Ivern']['info'], janna_dic['data']['Janna']['info'], jarvaniv_dic['data']['JarvanIV']['info'], jax_dic['data']['Jax']['info'], jayce_dic['data']['Jayce']['info'],
             jhin_dic['data']['Jhin']['info'], jinx_dic['data']['Jinx']['info'], kalista_dic['data']['Kalista']['info'], karma_dic['data']['Karma']['info'], karthus_dic['data']['Karthus']['info'],
             kassadin_dic['data']['Kassadin']['info'], katarina_dic['data']['Katarina']['info'], kayle_dic['data']['Kayle']['info'], kennen_dic['data']['Kennen']['info'], khazix_dic['data']['Khazix']['info'],
             kindred_dic['data']['Kindred']['info'], kled_dic['data']['Kled']['info'], kogmaw_dic['data']['KogMaw']['info'], leblanc_dic['data']['Leblanc']['info'], leesin_dic['data']['LeeSin']['info'],
             leona_dic['data']['Leona']['info'], lissandra_dic['data']['Lissandra']['info'], lucian_dic['data']['Lucian']['info'], lulu_dic['data']['Lulu']['info'], lux_dic['data']['Lux']['info'],
             malphite_dic['data']['Malphite']['info'], malzahar_dic['data']['Malzahar']['info'], maokai_dic['data']['Maokai']['info'], masteryi_dic['data']['MasterYi']['info'], missfortune_dic['data']['MissFortune']['info'],
             monkeyking_dic['data']['MonkeyKing']['info'], mordekaiser_dic['data']['Mordekaiser']['info'], morgana_dic['data']['Morgana']['info'], nami_dic['data']['Nami']['info'], nasus_dic['data']['Nasus']['info'],
             nautilus_dic['data']['Nautilus']['info'], nidalee_dic['data']['Nidalee']['info'], nocturne_dic['data']['Nocturne']['info'], nunu_dic['data']['Nunu']['info'], olaf_dic['data']['Olaf']['info'],
             orianna_dic['data']['Orianna']['info'], pantheon_dic['data']['Pantheon']['info'], poppy_dic['data']['Poppy']['info'], quinn_dic['data']['Quinn']['info'], rammus_dic['data']['Rammus']['info'],
             reksai_dic['data']['RekSai']['info'], renekton_dic['data']['Renekton']['info'], rengar_dic['data']['Rengar']['info'], riven_dic['data']['Riven']['info'], rumble_dic['data']['Rumble']['info'],
             ryze_dic['data']['Ryze']['info'], sejuani_dic['data']['Sejuani']['info'], shaco_dic['data']['Shaco']['info'], shen_dic['data']['Shen']['info'], shyvana_dic['data']['Shyvana']['info'],
             singed_dic['data']['Singed']['info'], sion_dic['data']['Sion']['info'], sivir_dic['data']['Sivir']['info'], skarner_dic['data']['Skarner']['info'], sona_dic['data']['Sona']['info'], 
             soraka_dic['data']['Soraka']['info'], swain_dic['data']['Swain']['info'], syndra_dic['data']['Syndra']['info'], tahmkench_dic['data']['TahmKench']['info'], taliyah_dic['data']['Taliyah']['info'],
             talon_dic['data']['Talon']['info'], taric_dic['data']['Taric']['info'], teemo_dic['data']['Teemo']['info'], thresh_dic['data']['Thresh']['info'], tristana_dic['data']['Tristana']['info'],
             trundle_dic['data']['Trundle']['info'], tryndamere_dic['data']['Tryndamere']['info'], twistedfate_dic['data']['TwistedFate']['info'], twitch_dic['data']['Twitch']['info'], udyr_dic['data']['Udyr']['info'],
             urgot_dic['data']['Urgot']['info'], varus_dic['data']['Varus']['info'], vayne_dic['data']['Vayne']['info'], veigar_dic['data']['Veigar']['info'], velkoz_dic['data']['Velkoz']['info'],
             vi_dic['data']['Vi']['info'], viktor_dic['data']['Viktor']['info'], vladimir_dic['data']['Vladimir']['info'], volibear_dic['data']['Volibear']['info'], warwick_dic['data']['Warwick']['info'],
             xerath_dic['data']['Xerath']['info'], xinzhao_dic['data']['XinZhao']['info'], yasuo_dic['data']['Yasuo']['info'], yorick_dic['data']['Yorick']['info'], zac_dic['data']['Zac']['info'],
             zed_dic['data']['Zed']['info'], ziggs_dic['data']['Ziggs']['info'], zilean_dic['data']['Zilean']['info'], zyra_dic['data']['Zyra']['info']]

# Turns that list into a datafrme
info_df = pd.DataFrame(info_li)

# Adds the name column to the info dataframe
info_df['name'] = all_champs_df['id']

# Turns the names column into the index
info_df = info_df.set_index('name')

# makes a list of the 'stats' for each champion (armor, armorperlevel, attackdamage, etc.)
stats_li = [aatrox_dic['data']['Aatrox']['stats'], ahri_dic['data']['Ahri']['stats'], akali_dic['data']['Akali']['stats'], alistar_dic['data']['Alistar']['stats'], amumu_dic['data']['Amumu']['stats'], 
             anivia_dic['data']['Anivia']['stats'], annie_dic['data']['Annie']['stats'], ashe_dic['data']['Ashe']['stats'], aurelionsol_dic['data']['AurelionSol']['stats'], azir_dic['data']['Azir']['stats'], 
             bard_dic['data']['Bard']['stats'], blitzcrank_dic['data']['Blitzcrank']['stats'], brand_dic['data']['Brand']['stats'], braum_dic['data']['Braum']['stats'], caitlyn_dic['data']['Caitlyn']['stats'],
             camille_dic['data']['Camille']['stats'], cassiopeia_dic['data']['Cassiopeia']['stats'], chogath_dic['data']['Chogath']['stats'], corki_dic['data']['Corki']['stats'], darius_dic['data']['Darius']['stats'],
             diana_dic['data']['Diana']['stats'], draven_dic['data']['Draven']['stats'], drmundo_dic['data']['DrMundo']['stats'], ekko_dic['data']['Ekko']['stats'], elise_dic['data']['Elise']['stats'],
             evelynn_dic['data']['Evelynn']['stats'], ezreal_dic['data']['Ezreal']['stats'], fiddlesticks_dic['data']['FiddleSticks']['stats'], fiora_dic['data']['Fiora']['stats'], fizz_dic['data']['Fizz']['stats'],
             galio_dic['data']['Galio']['stats'], gangplank_dic['data']['Gangplank']['stats'], garen_dic['data']['Garen']['stats'], gnar_dic['data']['Gnar']['stats'], gragas_dic['data']['Gragas']['stats'],
             graves_dic['data']['Graves']['stats'], hecarim_dic['data']['Hecarim']['stats'], heimerdinger_dic['data']['Heimerdinger']['stats'], illaoi_dic['data']['Illaoi']['stats'], irelia_dic['data']['Irelia']['stats'],
             ivern_dic['data']['Ivern']['stats'], janna_dic['data']['Janna']['stats'], jarvaniv_dic['data']['JarvanIV']['stats'], jax_dic['data']['Jax']['stats'], jayce_dic['data']['Jayce']['stats'],
             jhin_dic['data']['Jhin']['stats'], jinx_dic['data']['Jinx']['stats'], kalista_dic['data']['Kalista']['stats'], karma_dic['data']['Karma']['stats'], karthus_dic['data']['Karthus']['stats'],
             kassadin_dic['data']['Kassadin']['stats'], katarina_dic['data']['Katarina']['stats'], kayle_dic['data']['Kayle']['stats'], kennen_dic['data']['Kennen']['stats'], khazix_dic['data']['Khazix']['stats'],
             kindred_dic['data']['Kindred']['stats'], kled_dic['data']['Kled']['stats'], kogmaw_dic['data']['KogMaw']['stats'], leblanc_dic['data']['Leblanc']['stats'], leesin_dic['data']['LeeSin']['stats'],
             leona_dic['data']['Leona']['stats'], lissandra_dic['data']['Lissandra']['stats'], lucian_dic['data']['Lucian']['stats'], lulu_dic['data']['Lulu']['stats'], lux_dic['data']['Lux']['stats'],
             malphite_dic['data']['Malphite']['stats'], malzahar_dic['data']['Malzahar']['stats'], maokai_dic['data']['Maokai']['stats'], masteryi_dic['data']['MasterYi']['stats'], missfortune_dic['data']['MissFortune']['stats'],
             monkeyking_dic['data']['MonkeyKing']['stats'], mordekaiser_dic['data']['Mordekaiser']['stats'], morgana_dic['data']['Morgana']['stats'], nami_dic['data']['Nami']['stats'], nasus_dic['data']['Nasus']['stats'],
             nautilus_dic['data']['Nautilus']['stats'], nidalee_dic['data']['Nidalee']['stats'], nocturne_dic['data']['Nocturne']['stats'], nunu_dic['data']['Nunu']['stats'], olaf_dic['data']['Olaf']['stats'],
             orianna_dic['data']['Orianna']['stats'], pantheon_dic['data']['Pantheon']['stats'], poppy_dic['data']['Poppy']['stats'], quinn_dic['data']['Quinn']['stats'], rammus_dic['data']['Rammus']['stats'],
             reksai_dic['data']['RekSai']['stats'], renekton_dic['data']['Renekton']['stats'], rengar_dic['data']['Rengar']['stats'], riven_dic['data']['Riven']['stats'], rumble_dic['data']['Rumble']['stats'],
             ryze_dic['data']['Ryze']['stats'], sejuani_dic['data']['Sejuani']['stats'], shaco_dic['data']['Shaco']['stats'], shen_dic['data']['Shen']['stats'], shyvana_dic['data']['Shyvana']['stats'],
             singed_dic['data']['Singed']['stats'], sion_dic['data']['Sion']['stats'], sivir_dic['data']['Sivir']['stats'], skarner_dic['data']['Skarner']['stats'], sona_dic['data']['Sona']['stats'], 
             soraka_dic['data']['Soraka']['stats'], swain_dic['data']['Swain']['stats'], syndra_dic['data']['Syndra']['stats'], tahmkench_dic['data']['TahmKench']['stats'], taliyah_dic['data']['Taliyah']['stats'],
             talon_dic['data']['Talon']['stats'], taric_dic['data']['Taric']['stats'], teemo_dic['data']['Teemo']['stats'], thresh_dic['data']['Thresh']['stats'], tristana_dic['data']['Tristana']['stats'],
             trundle_dic['data']['Trundle']['stats'], tryndamere_dic['data']['Tryndamere']['stats'], twistedfate_dic['data']['TwistedFate']['stats'], twitch_dic['data']['Twitch']['stats'], udyr_dic['data']['Udyr']['stats'],
             urgot_dic['data']['Urgot']['stats'], varus_dic['data']['Varus']['stats'], vayne_dic['data']['Vayne']['stats'], veigar_dic['data']['Veigar']['stats'], velkoz_dic['data']['Velkoz']['stats'],
             vi_dic['data']['Vi']['stats'], viktor_dic['data']['Viktor']['stats'], vladimir_dic['data']['Vladimir']['stats'], volibear_dic['data']['Volibear']['stats'], warwick_dic['data']['Warwick']['stats'],
             xerath_dic['data']['Xerath']['stats'], xinzhao_dic['data']['XinZhao']['stats'], yasuo_dic['data']['Yasuo']['stats'], yorick_dic['data']['Yorick']['stats'], zac_dic['data']['Zac']['stats'],
             zed_dic['data']['Zed']['stats'], ziggs_dic['data']['Ziggs']['stats'], zilean_dic['data']['Zilean']['stats'], zyra_dic['data']['Zyra']['stats']]

# Again, making a dataframe from the list
stats_df = pd.DataFrame(stats_li)

# adding name collumn to the dataframe
stats_df['name'] = all_champs_df['id']

# Turns the names column into the index
stats_df = stats_df.set_index('name')





# Scaling the data
stats_scaled = preprocessing.scale(stats_df)
info_scaled = preprocessing.scale(info_df)

stats_robust = preprocessing.robust_scale(stats_df)
info_robust = preprocessing.robust_scale(info_df)

# Upon visual inspection, "info" might not need to be normalized, it looks like it stays in the 1-10 range









