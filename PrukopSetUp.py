import json
import pandas as pd
import csv
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from ipywidgets import interact
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics   
from sklearn.cross_validation import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix

plt.style.use("fivethirtyeight")
plt.rc("figure", figsize=(5,7))
sns.set_palette('deep')

# Stuff below controls how dataframes are displayed when you use display()
import IPython.display as ipd
digits = 3
pd.options.display.chop_threshold = 10**-(digits+1)
pd.options.display.float_format = lambda x: '{0:.{1}f}'.format(x,digits)
pd.options.display.show_dimensions = True
pd.options.display.max_rows = 500

def display(X):
    if isinstance(X, pd.Series) or (isinstance(X, np.ndarray) and X.ndim <=2):
        ipd.display(pd.DataFrame(X))
    else:
        ipd.display(X)
    return





def encode_target(df, target_column):
    """Add column to df with integers for the target.

    Args
    ----
    df -- pandas DataFrame.
    target_column -- column to map to int, producing
                     new Target column.

    Returns
    -------
    df_mod -- modified DataFrame.
    targets -- list of target names.
    """
    df_mod = df.copy()
    targets = df_mod[target_column].unique()
    map_to_int = {name: n for n, name in enumerate(targets)}
    df_mod["Target"] = df_mod[target_column].replace(map_to_int)

    return (df_mod, targets)





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

#Came across some capitilzation inconsistencies, fixed it.
top = top.str.upper()
jungle = jungle.str.upper()
middle = middle.str.upper()
adc = adc.str.upper()
support = support.str.upper()

# Create Series of the count for each Champ, with the name as the index value
top_champs = top.value_counts()
jungle_champs = jungle.value_counts()
middle_champs = middle.value_counts()
adc_champs = adc.value_counts()
support_champs = support.value_counts()

#Append all the series into one dataframe, and set any NA value to 0 - 0 occurances of that champ in that position
full_counts = pd.concat([top_champs, jungle_champs, middle_champs, adc_champs, support_champs], axis = 1, ignore_index=False)
full_counts = full_counts.rename(index = str, columns = {0 : 'top', 1 : 'jungle', 2 : 'middle', 3 : 'adc', 4 : 'support'})
full_counts = full_counts.fillna(0)

# Realized I had rows that had a single count of one for the red and blue labels, dropped them
full_counts = full_counts.drop(['BLUEADCCHAMP', 'BLUEJUNGLECHAMP', 'BLUEMIDDLECHAMP', 'BLUESUPPORTCHAMP', 'BLUETOPCHAMP', 'REDADCCHAMP', 'REDJUNGLECHAMP', 'REDMIDDLECHAMP', 'REDSUPPORTCHAMP', 'REDTOPCHAMP'])

# Turning the counts into a percentage of that position for the champion
index_li = full_counts.sort_index().index
for p in index_li: full_counts.loc[p] = full_counts.loc[p]/sum(full_counts.loc[p])

for p in index_li:
    if max(full_counts.loc[p]) < .85 : full_counts.drop(p, axis = 0, inplace = True)

# "true" positions for each champion
true_pos = full_counts.idxmax(axis = 1)

true_pos_2 = []
for x in true_pos:
    if x == 'top' :
        true_pos_2.append('upper')
    elif x == 'jungle':
        true_pos_2.append('upper')
    else: true_pos_2.append('lower')
true_pos_2 = pd.DataFrame(true_pos_2, index = true_pos.index, columns = ['lane'])





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
all_champs_df = pd.DataFrame([aatrox_dic['data']['Aatrox'], ahri_dic['data']['Ahri'], akali_dic['data']['Akali'], alistar_dic['data']['Alistar'], amumu_dic['data']['Amumu'], 
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
                 zed_dic['data']['Zed'], ziggs_dic['data']['Ziggs'], zilean_dic['data']['Zilean'], zyra_dic['data']['Zyra']])

all_champs_df['name'] = all_champs_df['id'].str.upper()
all_champs_df = all_champs_df.set_index('name')
all_champs_df['id'] = all_champs_df['id'].str.upper()

# makes a list of the 'info' for each champion (attack, defense, difficulty, magic) 
info_df = pd.DataFrame([aatrox_dic['data']['Aatrox']['info'], ahri_dic['data']['Ahri']['info'], akali_dic['data']['Akali']['info'], alistar_dic['data']['Alistar']['info'], amumu_dic['data']['Amumu']['info'], 
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
             zed_dic['data']['Zed']['info'], ziggs_dic['data']['Ziggs']['info'], zilean_dic['data']['Zilean']['info'], zyra_dic['data']['Zyra']['info']])

# adding name collumn to the dataframe
info_df['name'] = all_champs_df.index

# Turns the names column into the index
info_df = info_df.set_index('name')

# makes a list of the 'stats' for each champion (armor, armorperlevel, attackdamage, etc.)
stats_df = pd.DataFrame([aatrox_dic['data']['Aatrox']['stats'], ahri_dic['data']['Ahri']['stats'], akali_dic['data']['Akali']['stats'], alistar_dic['data']['Alistar']['stats'], amumu_dic['data']['Amumu']['stats'], 
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
             zed_dic['data']['Zed']['stats'], ziggs_dic['data']['Ziggs']['stats'], zilean_dic['data']['Zilean']['stats'], zyra_dic['data']['Zyra']['stats']])

# adding name collumn to the dataframe
stats_df['name'] = all_champs_df.index

# Turns the names column into the index
stats_df = stats_df.set_index('name')

# Realized the columns 'crit' and 'critperlevel' were just all 0.  Removing them.
stats_df = stats_df.drop(['crit', 'critperlevel'], axis = 1)

tags_df = pd.DataFrame([aatrox_dic['data']['Aatrox']['tags'], ahri_dic['data']['Ahri']['tags'], akali_dic['data']['Akali']['tags'], alistar_dic['data']['Alistar']['tags'], amumu_dic['data']['Amumu']['tags'], 
             anivia_dic['data']['Anivia']['tags'], annie_dic['data']['Annie']['tags'], ashe_dic['data']['Ashe']['tags'], aurelionsol_dic['data']['AurelionSol']['tags'], azir_dic['data']['Azir']['tags'], 
             bard_dic['data']['Bard']['tags'], blitzcrank_dic['data']['Blitzcrank']['tags'], brand_dic['data']['Brand']['tags'], braum_dic['data']['Braum']['tags'], caitlyn_dic['data']['Caitlyn']['tags'],
             camille_dic['data']['Camille']['tags'], cassiopeia_dic['data']['Cassiopeia']['tags'], chogath_dic['data']['Chogath']['tags'], corki_dic['data']['Corki']['tags'], darius_dic['data']['Darius']['tags'],
             diana_dic['data']['Diana']['tags'], draven_dic['data']['Draven']['tags'], drmundo_dic['data']['DrMundo']['tags'], ekko_dic['data']['Ekko']['tags'], elise_dic['data']['Elise']['tags'],
             evelynn_dic['data']['Evelynn']['tags'], ezreal_dic['data']['Ezreal']['tags'], fiddlesticks_dic['data']['FiddleSticks']['tags'], fiora_dic['data']['Fiora']['tags'], fizz_dic['data']['Fizz']['tags'],
             galio_dic['data']['Galio']['tags'], gangplank_dic['data']['Gangplank']['tags'], garen_dic['data']['Garen']['tags'], gnar_dic['data']['Gnar']['tags'], gragas_dic['data']['Gragas']['tags'],
             graves_dic['data']['Graves']['tags'], hecarim_dic['data']['Hecarim']['tags'], heimerdinger_dic['data']['Heimerdinger']['tags'], illaoi_dic['data']['Illaoi']['tags'], irelia_dic['data']['Irelia']['tags'],
             ivern_dic['data']['Ivern']['tags'], janna_dic['data']['Janna']['tags'], jarvaniv_dic['data']['JarvanIV']['tags'], jax_dic['data']['Jax']['tags'], jayce_dic['data']['Jayce']['tags'],
             jhin_dic['data']['Jhin']['tags'], jinx_dic['data']['Jinx']['tags'], kalista_dic['data']['Kalista']['tags'], karma_dic['data']['Karma']['tags'], karthus_dic['data']['Karthus']['tags'],
             kassadin_dic['data']['Kassadin']['tags'], katarina_dic['data']['Katarina']['tags'], kayle_dic['data']['Kayle']['tags'], kennen_dic['data']['Kennen']['tags'], khazix_dic['data']['Khazix']['tags'],
             kindred_dic['data']['Kindred']['tags'], kled_dic['data']['Kled']['tags'], kogmaw_dic['data']['KogMaw']['tags'], leblanc_dic['data']['Leblanc']['tags'], leesin_dic['data']['LeeSin']['tags'],
             leona_dic['data']['Leona']['tags'], lissandra_dic['data']['Lissandra']['tags'], lucian_dic['data']['Lucian']['tags'], lulu_dic['data']['Lulu']['tags'], lux_dic['data']['Lux']['tags'],
             malphite_dic['data']['Malphite']['tags'], malzahar_dic['data']['Malzahar']['tags'], maokai_dic['data']['Maokai']['tags'], masteryi_dic['data']['MasterYi']['tags'], missfortune_dic['data']['MissFortune']['tags'],
             monkeyking_dic['data']['MonkeyKing']['tags'], mordekaiser_dic['data']['Mordekaiser']['tags'], morgana_dic['data']['Morgana']['tags'], nami_dic['data']['Nami']['tags'], nasus_dic['data']['Nasus']['tags'],
             nautilus_dic['data']['Nautilus']['tags'], nidalee_dic['data']['Nidalee']['tags'], nocturne_dic['data']['Nocturne']['tags'], nunu_dic['data']['Nunu']['tags'], olaf_dic['data']['Olaf']['tags'],
             orianna_dic['data']['Orianna']['tags'], pantheon_dic['data']['Pantheon']['tags'], poppy_dic['data']['Poppy']['tags'], quinn_dic['data']['Quinn']['tags'], rammus_dic['data']['Rammus']['tags'],
             reksai_dic['data']['RekSai']['tags'], renekton_dic['data']['Renekton']['tags'], rengar_dic['data']['Rengar']['tags'], riven_dic['data']['Riven']['tags'], rumble_dic['data']['Rumble']['tags'],
             ryze_dic['data']['Ryze']['tags'], sejuani_dic['data']['Sejuani']['tags'], shaco_dic['data']['Shaco']['tags'], shen_dic['data']['Shen']['tags'], shyvana_dic['data']['Shyvana']['tags'],
             singed_dic['data']['Singed']['tags'], sion_dic['data']['Sion']['tags'], sivir_dic['data']['Sivir']['tags'], skarner_dic['data']['Skarner']['tags'], sona_dic['data']['Sona']['tags'], 
             soraka_dic['data']['Soraka']['tags'], swain_dic['data']['Swain']['tags'], syndra_dic['data']['Syndra']['tags'], tahmkench_dic['data']['TahmKench']['tags'], taliyah_dic['data']['Taliyah']['tags'],
             talon_dic['data']['Talon']['tags'], taric_dic['data']['Taric']['tags'], teemo_dic['data']['Teemo']['tags'], thresh_dic['data']['Thresh']['tags'], tristana_dic['data']['Tristana']['tags'],
             trundle_dic['data']['Trundle']['tags'], tryndamere_dic['data']['Tryndamere']['tags'], twistedfate_dic['data']['TwistedFate']['tags'], twitch_dic['data']['Twitch']['tags'], udyr_dic['data']['Udyr']['tags'],
             urgot_dic['data']['Urgot']['tags'], varus_dic['data']['Varus']['tags'], vayne_dic['data']['Vayne']['tags'], veigar_dic['data']['Veigar']['tags'], velkoz_dic['data']['Velkoz']['tags'],
             vi_dic['data']['Vi']['tags'], viktor_dic['data']['Viktor']['tags'], vladimir_dic['data']['Vladimir']['tags'], volibear_dic['data']['Volibear']['tags'], warwick_dic['data']['Warwick']['tags'],
             xerath_dic['data']['Xerath']['tags'], xinzhao_dic['data']['XinZhao']['tags'], yasuo_dic['data']['Yasuo']['tags'], yorick_dic['data']['Yorick']['tags'], zac_dic['data']['Zac']['tags'],
             zed_dic['data']['Zed']['tags'], ziggs_dic['data']['Ziggs']['tags'], zilean_dic['data']['Zilean']['tags'], zyra_dic['data']['Zyra']['tags']])

# adding name collumn to the dataframe
tags_df['name'] = all_champs_df.index

# Turns the names column into the index
tags_df = tags_df.set_index('name')

tags_df.columns = ['Tag 1', 'Tag 2']
tags_df = tags_df.T
tags_exp = []
for a in all_champs_df.index: tags_exp.append(tags_df[a].value_counts())
tags_exp_df = pd.DataFrame(tags_exp).fillna(0)



# Scaling the data, returns arrays.  
# Changing them all to dataframes with the correct headers.
stats_scaled = preprocessing.scale(stats_df)
stats_scaled_df = pd.DataFrame(data = stats_scaled, columns = list(stats_df))
stats_scaled_df['name'] = all_champs_df.index
stats_scaled_df = stats_scaled_df.set_index('name')

info_scaled = preprocessing.scale(info_df)
info_scaled_df = pd.DataFrame(data = info_scaled, columns = list(info_df))
info_scaled_df['name'] = all_champs_df.index
info_scaled_df = info_scaled_df.set_index('name')

stats_robust = preprocessing.robust_scale(stats_df)
stats_robust_df = pd.DataFrame(data = stats_robust, columns = list(stats_df))
stats_robust_df['name'] = all_champs_df.index
stats_robust_df = stats_robust_df.set_index('name')

info_robust = preprocessing.robust_scale(info_df)
info_robust_df = pd.DataFrame(data = info_robust, columns = list(info_df))
info_robust_df['name'] = all_champs_df.index
info_robust_df = info_robust_df.set_index('name')

# Upon visual inspection, "info" might not need to be normalized, it looks like it stays in the 1-10 range





# Labeled data frames, for graphing purposes
stats_labeled_df = pd.concat([stats_df, pd.DataFrame(true_pos, columns = ['lane'])], axis = 1)
stats_scaled_labeled_df = pd.concat([stats_scaled_df, pd.DataFrame(true_pos, columns = ['lane'])], axis = 1)
stats_robust_labeled_df = pd.concat([stats_robust_df, pd.DataFrame(true_pos, columns = ['lane'])], axis = 1)
info_labeled_df = pd.concat([info_df, pd.DataFrame(true_pos, columns = ['lane'])], axis = 1)
info_scaled_labeled_df = pd.concat([info_scaled_df, pd.DataFrame(true_pos, columns = ['lane'])], axis = 1)
info_robust_labeled_df = pd.concat([info_robust_df, pd.DataFrame(true_pos, columns = ['lane'])], axis = 1)

stats_labeled_df2 = pd.concat([stats_df, pd.DataFrame(true_pos_2, columns = ['lane'])], axis = 1)
stats_scaled_labeled_df2 = pd.concat([stats_scaled_df, pd.DataFrame(true_pos_2, columns = ['lane'])], axis = 1)
stats_robust_labeled_df2 = pd.concat([stats_robust_df, pd.DataFrame(true_pos_2, columns = ['lane'])], axis = 1)
info_labeled_df2 = pd.concat([info_df, pd.DataFrame(true_pos_2, columns = ['lane'])], axis = 1)
info_scaled_labeled_df2 = pd.concat([info_scaled_df, pd.DataFrame(true_pos_2, columns = ['lane'])], axis = 1)
info_robust_labeled_df2 = pd.concat([info_robust_df, pd.DataFrame(true_pos_2, columns = ['lane'])], axis = 1)






for p in all_champs_df.index :
    if p not in true_pos.index:
        all_champs_df.drop(p, axis = 0, inplace = True)

for p in stats_df.index :
    if p not in true_pos.index:
        stats_df.drop(p, axis = 0, inplace = True)

for p in stats_scaled_df.index:
    if p not in true_pos.index:
        stats_scaled_df.drop(p, axis = 0, inplace = True)

for p in stats_robust_df.index:
    if p not in true_pos.index:
        stats_robust_df.drop(p, axis = 0, inplace = True)

for p in stats_labeled_df.index :
    if p not in true_pos.index:
        stats_labeled_df.drop(p, axis = 0, inplace = True)

for p in stats_scaled_labeled_df.index:
    if p not in true_pos.index:
        stats_scaled_labeled_df.drop(p, axis = 0, inplace = True)

for p in stats_robust_labeled_df.index:
    if p not in true_pos.index:
        stats_robust_labeled_df.drop(p, axis = 0, inplace = True)

for p in stats_labeled_df2.index :
    if p not in true_pos.index:
        stats_labeled_df2.drop(p, axis = 0, inplace = True)

for p in stats_scaled_labeled_df2.index:
    if p not in true_pos.index:
        stats_scaled_labeled_df2.drop(p, axis = 0, inplace = True)

for p in stats_robust_labeled_df2.index:
    if p not in true_pos.index:
        stats_robust_labeled_df2.drop(p, axis = 0, inplace = True)

for p in info_df.index :
    if p not in true_pos.index:
        info_df.drop(p, axis = 0, inplace = True)

for p in info_scaled_df.index:
    if p not in true_pos.index:
        info_scaled_df.drop(p, axis = 0, inplace = True)

for p in info_robust_df.index:
    if p not in true_pos.index:
        info_robust_df.drop(p, axis = 0, inplace = True)

for p in info_labeled_df.index :
    if p not in true_pos.index:
        info_labeled_df.drop(p, axis = 0, inplace = True)

for p in info_scaled_labeled_df.index:
    if p not in true_pos.index:
        info_scaled_labeled_df.drop(p, axis = 0, inplace = True)

for p in info_robust_labeled_df.index:
    if p not in true_pos.index:
        info_robust_labeled_df.drop(p, axis = 0, inplace = True)

for p in info_labeled_df2.index :
    if p not in true_pos.index:
        info_labeled_df2.drop(p, axis = 0, inplace = True)

for p in info_scaled_labeled_df2.index:
    if p not in true_pos.index:
        info_scaled_labeled_df2.drop(p, axis = 0, inplace = True)

for p in info_robust_labeled_df2.index:
    if p not in true_pos.index:
        info_robust_labeled_df2.drop(p, axis = 0, inplace = True)





# Empty list to fill in with the names of each count series for the champs, so I can join easier.
all_champs = []
names = []

# Creating lists of all the spell keywords for each champion.  Will count later, then create one master DF of counts.
aatrox_spells = []
for spell in aatrox_dic['data']['Aatrox']['spells']: 
    for x in spell['leveltip']['label']: aatrox_spells.append(x)
all_champs.append(pd.Series(aatrox_spells).value_counts())
names.append("AATROX")

ahri_spells = []
for spell in ahri_dic['data']['Ahri']['spells']: 
    for x in spell['leveltip']['label']: ahri_spells.append(x)
all_champs.append(pd.Series(ahri_spells).value_counts())
names.append('AHRI')

akali_spells = []
for spell in akali_dic['data']['Akali']['spells']: 
    for x in spell['leveltip']['label']: akali_spells.append(x)
all_champs.append(pd.Series(akali_spells).value_counts())
names.append('AKALI')

alistar_spells = []
for spell in alistar_dic['data']['Alistar']['spells']: 
    for x in spell['leveltip']['label']: alistar_spells.append(x)
all_champs.append(pd.Series(alistar_spells).value_counts())
names.append('ALISTAR')

amumu_spells = []
for spell in amumu_dic['data']['Amumu']['spells']: 
    for x in spell['leveltip']['label']: amumu_spells.append(x)
all_champs.append(pd.Series(amumu_spells).value_counts())
names.append('AMUMU')

anivia_spells = []
for spell in anivia_dic['data']['Anivia']['spells']: 
    for x in spell['leveltip']['label']: anivia_spells.append(x)
all_champs.append(pd.Series(anivia_spells).value_counts())
names.append('ANIVIA')

annie_spells = []
for spell in annie_dic['data']['Annie']['spells']: 
    for x in spell['leveltip']['label']: annie_spells.append(x)
all_champs.append(pd.Series(annie_spells).value_counts())
names.append('ANNIE')

ashe_spells = []
for spell in ashe_dic['data']['Ashe']['spells']: 
    for x in spell['leveltip']['label']: ashe_spells.append(x)
all_champs.append(pd.Series(ashe_spells).value_counts())
names.append('ASHE')

aurelionsol_spells = []
for spell in aurelionsol_dic['data']['AurelionSol']['spells']: 
    for x in spell['leveltip']['label']: aurelionsol_spells.append(x)
all_champs.append(pd.Series(aurelionsol_spells).value_counts())
names.append('AURELIONSOL')

azir_spells = []
for spell in azir_dic['data']['Azir']['spells']: 
    for x in spell['leveltip']['label']: azir_spells.append(x)
all_champs.append(pd.Series(azir_spells).value_counts())
names.append('AZIR')

bard_spells = []
for spell in bard_dic['data']['Bard']['spells']: 
    for x in spell['leveltip']['label']: bard_spells.append(x)
all_champs.append(pd.Series(bard_spells).value_counts())
names.append('BARD')

blitzcrank_spells = []
for spell in blitzcrank_dic['data']['Blitzcrank']['spells']: 
    for x in spell['leveltip']['label']: blitzcrank_spells.append(x)
all_champs.append(pd.Series(blitzcrank_spells).value_counts())
names.append('BLITZCRANK')

brand_spells = []
for spell in brand_dic['data']['Brand']['spells']: 
    for x in spell['leveltip']['label']: brand_spells.append(x)
all_champs.append(pd.Series(brand_spells).value_counts())
names.append('BRAND')

braum_spells = []
for spell in braum_dic['data']['Braum']['spells']: 
    for x in spell['leveltip']['label']: braum_spells.append(x)
all_champs.append(pd.Series(braum_spells).value_counts())
names.append('BRAUM')

caitlyn_spells = []
for spell in caitlyn_dic['data']['Caitlyn']['spells']: 
    for x in spell['leveltip']['label']: caitlyn_spells.append(x)
all_champs.append(pd.Series(caitlyn_spells).value_counts())
names.append('CAITLYN')

camille_spells = []
for spell in camille_dic['data']['Camille']['spells']: 
    for x in spell['leveltip']['label']: camille_spells.append(x)
all_champs.append(pd.Series(camille_spells).value_counts())
names.append('CAMILLE')

cassiopeia_spells = []
for spell in cassiopeia_dic['data']['Cassiopeia']['spells']: 
    for x in spell['leveltip']['label']: cassiopeia_spells.append(x)
all_champs.append(pd.Series(cassiopeia_spells).value_counts())
names.append('CASSIOPEIA')

chogath_spells = []
for spell in chogath_dic['data']['Chogath']['spells']: 
    for x in spell['leveltip']['label']: chogath_spells.append(x)
all_champs.append(pd.Series(chogath_spells).value_counts())
names.append('CHOGATH')

corki_spells = []
for spell in corki_dic['data']['Corki']['spells']: 
    for x in spell['leveltip']['label']: corki_spells.append(x)
all_champs.append(pd.Series(corki_spells).value_counts())
names.append('CORKI')

darius_spells = []
for spell in darius_dic['data']['Darius']['spells']: 
    for x in spell['leveltip']['label']: darius_spells.append(x)
all_champs.append(pd.Series(darius_spells).value_counts())
names.append('DARIUS')

diana_spells = []
for spell in diana_dic['data']['Diana']['spells']: 
    for x in spell['leveltip']['label']: diana_spells.append(x)
all_champs.append(pd.Series(diana_spells).value_counts())
names.append('DIANA')

drmundo_spells = []
for spell in drmundo_dic['data']['DrMundo']['spells']: 
    for x in spell['leveltip']['label']: drmundo_spells.append(x)
all_champs.append(pd.Series(drmundo_spells).value_counts())
names.append('DRMUNDO')

draven_spells = []
for spell in draven_dic['data']['Draven']['spells']: 
    for x in spell['leveltip']['label']: draven_spells.append(x)
all_champs.append(pd.Series(draven_spells).value_counts())
names.append('DRAVEN')

ekko_spells = []
for spell in ekko_dic['data']['Ekko']['spells']: 
    for x in spell['leveltip']['label']: ekko_spells.append(x)
all_champs.append(pd.Series(ekko_spells).value_counts())
names.append('EKKO')

elise_spells = []
for spell in elise_dic['data']['Elise']['spells']: 
    for x in spell['leveltip']['label']: elise_spells.append(x)
all_champs.append(pd.Series(elise_spells).value_counts())
names.append('ELISE')

evelynn_spells = []
for spell in evelynn_dic['data']['Evelynn']['spells']: 
    for x in spell['leveltip']['label']: evelynn_spells.append(x)
all_champs.append(pd.Series(evelynn_spells).value_counts())
names.append('EVELYNN')

ezreal_spells = []
for spell in ezreal_dic['data']['Ezreal']['spells']: 
    for x in spell['leveltip']['label']: ezreal_spells.append(x)
all_champs.append(pd.Series(ezreal_spells).value_counts())
names.append('EZREAL')

fiddlesticks_spells = []
for spell in fiddlesticks_dic['data']['FiddleSticks']['spells']: 
    for x in spell['leveltip']['label']: fiddlesticks_spells.append(x)
all_champs.append(pd.Series(fiddlesticks_spells).value_counts())
names.append('FIDDLESTICKS')

fiora_spells = []
for spell in fiora_dic['data']['Fiora']['spells']: 
    for x in spell['leveltip']['label']: fiora_spells.append(x)
all_champs.append(pd.Series(fiora_spells).value_counts())
names.append('FIORA')

fizz_spells = []
for spell in fizz_dic['data']['Fizz']['spells']: 
    for x in spell['leveltip']['label']: fizz_spells.append(x)
all_champs.append(pd.Series(fizz_spells).value_counts())
names.append('FIZZ')

galio_spells = []
for spell in galio_dic['data']['Galio']['spells']: 
    for x in spell['leveltip']['label']: galio_spells.append(x)
all_champs.append(pd.Series(galio_spells).value_counts())
names.append('GALIO')

gangplank_spells = []
for spell in gangplank_dic['data']['Gangplank']['spells']: 
    for x in spell['leveltip']['label']: gangplank_spells.append(x)
all_champs.append(pd.Series(gangplank_spells).value_counts())
names.append('GANGPLANK')

garen_spells = []
for spell in garen_dic['data']['Garen']['spells']: 
    for x in spell['leveltip']['label']: garen_spells.append(x)
all_champs.append(pd.Series(garen_spells).value_counts())
names.append('GAREN')

gnar_spells = []
for spell in gnar_dic['data']['Gnar']['spells']: 
    for x in spell['leveltip']['label']: gnar_spells.append(x)
all_champs.append(pd.Series(gnar_spells).value_counts())
names.append('GNAR')

gragas_spells = []
for spell in gragas_dic['data']['Gragas']['spells']: 
    for x in spell['leveltip']['label']: gragas_spells.append(x)
all_champs.append(pd.Series(gragas_spells).value_counts())
names.append('GRAGAS')

graves_spells = []
for spell in graves_dic['data']['Graves']['spells']: 
    for x in spell['leveltip']['label']: graves_spells.append(x)
all_champs.append(pd.Series(graves_spells).value_counts())
names.append('GRAVES')

hecarim_spells = []
for spell in hecarim_dic['data']['Hecarim']['spells']: 
    for x in spell['leveltip']['label']: hecarim_spells.append(x)
all_champs.append(pd.Series(hecarim_spells).value_counts())
names.append('HECARIM')

illaoi_spells = []
for spell in illaoi_dic['data']['Illaoi']['spells']: 
    for x in spell['leveltip']['label']: illaoi_spells.append(x)
all_champs.append(pd.Series(illaoi_spells).value_counts())
names.append('ILLAOI')

irelia_spells = []
for spell in irelia_dic['data']['Irelia']['spells']: 
    for x in spell['leveltip']['label']: irelia_spells.append(x)
all_champs.append(pd.Series(irelia_spells).value_counts())
names.append('IRELIA')

ivern_spells = []
for spell in ivern_dic['data']['Ivern']['spells']: 
    for x in spell['leveltip']['label']: ivern_spells.append(x)
all_champs.append(pd.Series(ivern_spells).value_counts())
names.append('IVERN')

janna_spells = []
for spell in janna_dic['data']['Janna']['spells']: 
    for x in spell['leveltip']['label']: janna_spells.append(x)
all_champs.append(pd.Series(janna_spells).value_counts())
names.append('JANNA')

jarvaniv_spells = []
for spell in jarvaniv_dic['data']['JarvanIV']['spells']: 
    for x in spell['leveltip']['label']: jarvaniv_spells.append(x)
all_champs.append(pd.Series(jarvaniv_spells).value_counts())
names.append('JARVANIV')
#If I made a mistake in here and it doesn't spit an error, just copies the wrong values....

jax_spells = []
for spell in jax_dic['data']['Jax']['spells']:
    for x in spell['leveltip']['label']: jax_spells.append(x)
all_champs.append(pd.Series(jax_spells).value_counts())
names.append('JAX')

jayce_spells = []
for spell in jayce_dic['data']['Jayce']['spells']: 
    for x in spell['leveltip']['label']: jayce_spells.append(x)
all_champs.append(pd.Series(jayce_spells).value_counts())
names.append('JAYCE')

jhin_spells = []
for spell in jhin_dic['data']['Jhin']['spells']: 
    for x in spell['leveltip']['label']: jhin_spells.append(x)
all_champs.append(pd.Series(jhin_spells).value_counts())
names.append('JHIN')

jinx_spells = []
for spell in jinx_dic['data']['Jinx']['spells']: 
    for x in spell['leveltip']['label']: jinx_spells.append(x)
all_champs.append(pd.Series(jinx_spells).value_counts())
names.append('JINX')

kalista_spells = []
for spell in kalista_dic['data']['Kalista']['spells']: 
    for x in spell['leveltip']['label']: kalista_spells.append(x)
all_champs.append(pd.Series(kalista_spells).value_counts())
names.append('KALISTA')

karma_spells = [] #who is a b####
for spell in karma_dic['data']['Karma']['spells']: 
    for x in spell['leveltip']['label']: karma_spells.append(x)
all_champs.append(pd.Series(karma_spells).value_counts())
names.append('KARMA')

karthus_spells = []
for spell in karthus_dic['data']['Karthus']['spells']: 
    for x in spell['leveltip']['label']: karthus_spells.append(x)
all_champs.append(pd.Series(karthus_spells).value_counts())
names.append('KARTHUS')

kassadin_spells = []
for spell in kassadin_dic['data']['Kassadin']['spells']: 
    for x in spell['leveltip']['label']: kassadin_spells.append(x)
all_champs.append(pd.Series(kassadin_spells).value_counts())
names.append('KASSADIN')

katarina_spells = []
for spell in katarina_dic['data']['Katarina']['spells']: 
    for x in spell['leveltip']['label']: katarina_spells.append(x)
all_champs.append(pd.Series(katarina_spells).value_counts())
names.append('KATARINA')

kayle_spells = []
for spell in kayle_dic['data']['Kayle']['spells']: 
    for x in spell['leveltip']['label']: kayle_spells.append(x)
all_champs.append(pd.Series(kayle_spells).value_counts())
names.append('KAYLE')

kennen_spells = []
for spell in kennen_dic['data']['Kennen']['spells']: 
    for x in spell['leveltip']['label']: kennen_spells.append(x)
all_champs.append(pd.Series(kennen_spells).value_counts())
names.append('KENNEN')

khazix_spells = []
for spell in khazix_dic['data']['Khazix']['spells']: 
    for x in spell['leveltip']['label']: khazix_spells.append(x)
all_champs.append(pd.Series(khazix_spells).value_counts())
names.append('KHAZIX')

kindred_spells = []
for spell in kindred_dic['data']['Kindred']['spells']: 
    for x in spell['leveltip']['label']: kindred_spells.append(x)
all_champs.append(pd.Series(kindred_spells).value_counts())
names.append('KINDRED')

kled_spells = []
for spell in kled_dic['data']['Kled']['spells']: 
    for x in spell['leveltip']['label']: kled_spells.append(x)
all_champs.append(pd.Series(kled_spells).value_counts())
names.append('KLED')

kogmaw_spells = []
for spell in kogmaw_dic['data']['KogMaw']['spells']: 
    for x in spell['leveltip']['label']: kogmaw_spells.append(x)
all_champs.append(pd.Series(kogmaw_spells).value_counts())
names.append('KOGMAW')

leblanc_spells = []
for spell in leblanc_dic['data']['Leblanc']['spells']: 
    for x in spell['leveltip']['label']: leblanc_spells.append(x)
all_champs.append(pd.Series(leblanc_spells).value_counts())
names.append('LEBLANC')

leesin_spells = []
for spell in leesin_dic['data']['LeeSin']['spells']: 
    for x in spell['leveltip']['label']: leesin_spells.append(x)
all_champs.append(pd.Series(leesin_spells).value_counts())
names.append('LEESIN')

leona_spells = []
for spell in leona_dic['data']['Leona']['spells']: 
    for x in spell['leveltip']['label']: leona_spells.append(x)
all_champs.append(pd.Series(leona_spells).value_counts())
names.append('LEONA')

lissandra_spells = []
for spell in lissandra_dic['data']['Lissandra']['spells']: 
    for x in spell['leveltip']['label']: lissandra_spells.append(x)
all_champs.append(pd.Series(lissandra_spells).value_counts())
names.append('LISSANDRA')

lucian_spells = []
for spell in lucian_dic['data']['Lucian']['spells']: 
    for x in spell['leveltip']['label']: lucian_spells.append(x)
all_champs.append(pd.Series(lucian_spells).value_counts())
names.append('LUCIAN')

lulu_spells = []   # Figured out a more efficient way of doing this.  Right here.  Then went back and changed ALL OF THEM that I had already done.
for spell in lulu_dic['data']['Lulu']['spells']: 
    for x in spell['leveltip']['label']: lulu_spells.append(x)
all_champs.append(pd.Series(lulu_spells).value_counts())
names.append('LULU')

lux_spells = []
for spell in lux_dic['data']['Lux']['spells']: 
    for x in spell['leveltip']['label']: lux_spells.append(x)
all_champs.append(pd.Series(lux_spells).value_counts())
names.append('LUX')

malphite_spells = []
for spell in malphite_dic['data']['Malphite']['spells']: 
    for x in spell['leveltip']['label']: malphite_spells.append(x)
all_champs.append(pd.Series(malphite_spells).value_counts())
names.append('MALPHITE')

malzahar_spells = []
for spell in malzahar_dic['data']['Malzahar']['spells']: 
    for x in spell['leveltip']['label']: malzahar_spells.append(x)
all_champs.append(pd.Series(malzahar_spells).value_counts())
names.append('MALZAHAR')

maokai_spells = []
for spell in maokai_dic['data']['Maokai']['spells']: 
    for x in spell['leveltip']['label']: maokai_spells.append(x)
all_champs.append(pd.Series(maokai_spells).value_counts())
names.append('MAOKAI')

masteryi_spells = []
for spell in masteryi_dic['data']['MasterYi']['spells']: 
    for x in spell['leveltip']['label']: masteryi_spells.append(x)
all_champs.append(pd.Series(masteryi_spells).value_counts())
names.append('MASTERYI')

missfortune_spells = []
for spell in missfortune_dic['data']['MissFortune']['spells']: 
    for x in spell['leveltip']['label']: missfortune_spells.append(x)
all_champs.append(pd.Series(missfortune_spells).value_counts())
names.append('MISSFORTUNE')

monkeyking_spells = []
for spell in monkeyking_dic['data']['MonkeyKing']['spells']: 
    for x in spell['leveltip']['label']: monkeyking_spells.append(x)
all_champs.append(pd.Series(monkeyking_spells).value_counts())
names.append('MONKEYKING')

mordekaiser_spells = []
for spell in mordekaiser_dic['data']['Mordekaiser']['spells']: 
    for x in spell['leveltip']['label']: mordekaiser_spells.append(x)
all_champs.append(pd.Series(mordekaiser_spells).value_counts())
names.append('MORDEKAISER')

morgana_spells = []
for spell in morgana_dic['data']['Morgana']['spells']: 
    for x in spell['leveltip']['label']: morgana_spells.append(x)
all_champs.append(pd.Series(morgana_spells).value_counts())
names.append('MORGANA')

nami_spells = []
for spell in nami_dic['data']['Nami']['spells']: 
    for x in spell['leveltip']['label']: nami_spells.append(x)
all_champs.append(pd.Series(nami_spells).value_counts())
names.append('NAMI')

nasus_spells = []
for spell in nasus_dic['data']['Nasus']['spells']: 
    for x in spell['leveltip']['label']: nasus_spells.append(x)
all_champs.append(pd.Series(nasus_spells).value_counts())
names.append('NASUS')

nautilus_spells = []
for spell in nautilus_dic['data']['Nautilus']['spells']: 
    for x in spell['leveltip']['label']: nautilus_spells.append(x)
all_champs.append(pd.Series(nautilus_spells).value_counts())
names.append('NAUTILUS')

nidalee_spells = []
for spell in nidalee_dic['data']['Nidalee']['spells']: 
    for x in spell['leveltip']['label']: nidalee_spells.append(x)
all_champs.append(pd.Series(nidalee_spells).value_counts())
names.append('NIDALEE')

nocturne_spells = []
for spell in nocturne_dic['data']['Nocturne']['spells']: 
    for x in spell['leveltip']['label']: nocturne_spells.append(x)
all_champs.append(pd.Series(nocturne_spells).value_counts())
names.append('NOCTURNE')

nunu_spells = []
for spell in nunu_dic['data']['Nunu']['spells']: 
    for x in spell['leveltip']['label']: nunu_spells.append(x)
all_champs.append(pd.Series(nunu_spells).value_counts())
names.append('NUNU')

olaf_spells = [] #do you wnt to build a snowman?
for spell in olaf_dic['data']['Olaf']['spells']: 
    for x in spell['leveltip']['label']: olaf_spells.append(x)
all_champs.append(pd.Series(olaf_spells).value_counts())
names.append('OLAF')

orianna_spells = []
for spell in orianna_dic['data']['Orianna']['spells']: 
    for x in spell['leveltip']['label']: orianna_spells.append(x)
all_champs.append(pd.Series(orianna_spells).value_counts())
names.append('ORIANNA')

pantheon_spells = []
for spell in pantheon_dic['data']['Pantheon']['spells']: 
    for x in spell['leveltip']['label']: pantheon_spells.append(x)
all_champs.append(pd.Series(pantheon_spells).value_counts())
names.append('PANTHEON')

poppy_spells = []
for spell in poppy_dic['data']['Poppy']['spells']: 
    for x in spell['leveltip']['label']: poppy_spells.append(x)
all_champs.append(pd.Series(poppy_spells).value_counts())
names.append('POPPY')

quinn_spells = []
for spell in quinn_dic['data']['Quinn']['spells']: 
    for x in spell['leveltip']['label']: quinn_spells.append(x)
all_champs.append(pd.Series(quinn_spells).value_counts())
names.append('QUINN')

rammus_spells = []
for spell in rammus_dic['data']['Rammus']['spells']: 
    for x in spell['leveltip']['label']: rammus_spells.append(x)
all_champs.append(pd.Series(rammus_spells).value_counts())
names.append('RAMMUS')

reksai_spells = []
for spell in reksai_dic['data']['RekSai']['spells']: 
    for x in spell['leveltip']['label']: reksai_spells.append(x)
all_champs.append(pd.Series(reksai_spells).value_counts())
names.append('REKSAI')

renekton_spells = []
for spell in renekton_dic['data']['Renekton']['spells']: 
    for x in spell['leveltip']['label']: renekton_spells.append(x)
all_champs.append(pd.Series(renekton_spells).value_counts())
names.append('RENEKTON')

rengar_spells = []
for spell in rengar_dic['data']['Rengar']['spells']: 
    for x in spell['leveltip']['label']: rengar_spells.append(x)
all_champs.append(pd.Series(rengar_spells).value_counts())
names.append('RENGAR')

riven_spells = []
for spell in riven_dic['data']['Riven']['spells']: 
    for x in spell['leveltip']['label']: riven_spells.append(x)
all_champs.append(pd.Series(riven_spells).value_counts())
names.append('RIVEN')

rumble_spells = []
for spell in rumble_dic['data']['Rumble']['spells']: 
    for x in spell['leveltip']['label']: rumble_spells.append(x)
all_champs.append(pd.Series(rumble_spells).value_counts())
names.append('RUMBLE')

ryze_spells = []
for spell in ryze_dic['data']['Ryze']['spells']: 
    for x in spell['leveltip']['label']: ryze_spells.append(x)
all_champs.append(pd.Series(ryze_spells).value_counts())
names.append('RYZE')

sejuani_spells = []
for spell in sejuani_dic['data']['Sejuani']['spells']: 
    for x in spell['leveltip']['label']: sejuani_spells.append(x)
all_champs.append(pd.Series(sejuani_spells).value_counts())
names.append('SEJUANI')

shaco_spells = []
for spell in shaco_dic['data']['Shaco']['spells']: 
    for x in spell['leveltip']['label']: shaco_spells.append(x)
all_champs.append(pd.Series(shaco_spells).value_counts())
names.append('SHACO')

shen_spells = []
for spell in shen_dic['data']['Shen']['spells']: 
    for x in spell['leveltip']['label']: shen_spells.append(x)
all_champs.append(pd.Series(shen_spells).value_counts())
names.append('SHEN')

shyvana_spells = []
for spell in shyvana_dic['data']['Shyvana']['spells']: 
    for x in spell['leveltip']['label']: shyvana_spells.append(x)
all_champs.append(pd.Series(shyvana_spells).value_counts())
names.append('SHYVANA')

singed_spells = []
for spell in singed_dic['data']['Singed']['spells']: 
    for x in spell['leveltip']['label']: singed_spells.append(x)
all_champs.append(pd.Series(singed_spells).value_counts())
names.append('SINGED')

sion_spells = []
for spell in sion_dic['data']['Sion']['spells']: 
    for x in spell['leveltip']['label']: sion_spells.append(x)
all_champs.append(pd.Series(sion_spells).value_counts())
names.append('SION')

sivir_spells = []
for spell in sivir_dic['data']['Sivir']['spells']: 
    for x in spell['leveltip']['label']: sivir_spells.append(x)
all_champs.append(pd.Series(sivir_spells).value_counts())
names.append('SIVIR')

skarner_spells = []
for spell in skarner_dic['data']['Skarner']['spells']: 
    for x in spell['leveltip']['label']: skarner_spells.append(x)
all_champs.append(pd.Series(skarner_spells).value_counts())
names.append('SKARNER')

sona_spells = []
for spell in sona_dic['data']['Sona']['spells']: 
    for x in spell['leveltip']['label']: sona_spells.append(x)
all_champs.append(pd.Series(sona_spells).value_counts())
names.append('SONA')

soraka_spells = []
for spell in soraka_dic['data']['Soraka']['spells']: 
    for x in spell['leveltip']['label']: soraka_spells.append(x)
all_champs.append(pd.Series(soraka_spells).value_counts())
names.append('SORAKA')

swain_spells = []
for spell in swain_dic['data']['Swain']['spells']: 
    for x in spell['leveltip']['label']: swain_spells.append(x)
all_champs.append(pd.Series(swain_spells).value_counts())
names.append('SWAIN')

syndra_spells = []
for spell in syndra_dic['data']['Syndra']['spells']: 
    for x in spell['leveltip']['label']: syndra_spells.append(x)
all_champs.append(pd.Series(syndra_spells).value_counts())
names.append('SYNDRA')

tahmkench_spells = []
for spell in tahmkench_dic['data']['TahmKench']['spells']: 
    for x in spell['leveltip']['label']: tahmkench_spells.append(x)
all_champs.append(pd.Series(tahmkench_spells).value_counts())
names.append('TAHMKENCH')

taliyah_spells = []
for spell in taliyah_dic['data']['Taliyah']['spells']: 
    for x in spell['leveltip']['label']: taliyah_spells.append(x)
all_champs.append(pd.Series(taliyah_spells).value_counts())
names.append('TALIYAH')

talon_spells = []
for spell in talon_dic['data']['Talon']['spells']: 
    for x in spell['leveltip']['label']: talon_spells.append(x)
all_champs.append(pd.Series(talon_spells).value_counts())
names.append('TALON')

taric_spells = []
for spell in taric_dic['data']['Taric']['spells']: 
    for x in spell['leveltip']['label']: taric_spells.append(x)
all_champs.append(pd.Series(taric_spells).value_counts())
names.append('TARIC')

teemo_spells = []
for spell in teemo_dic['data']['Teemo']['spells']: 
    for x in spell['leveltip']['label']: teemo_spells.append(x)
all_champs.append(pd.Series(teemo_spells).value_counts())
names.append('TEEMO')

thresh_spells = []
for spell in thresh_dic['data']['Thresh']['spells']: 
    for x in spell['leveltip']['label']: thresh_spells.append(x)
all_champs.append(pd.Series(thresh_spells).value_counts())
names.append('THRESH')

tristana_spells = []
for spell in tristana_dic['data']['Tristana']['spells']: 
    for x in spell['leveltip']['label']: tristana_spells.append(x)
all_champs.append(pd.Series(tristana_spells).value_counts())
names.append('TRISTANA')

trundle_spells = []
for spell in trundle_dic['data']['Trundle']['spells']: 
    for x in spell['leveltip']['label']: trundle_spells.append(x)
all_champs.append(pd.Series(trundle_spells).value_counts())
names.append('TRUNDLE')

tryndamere_spells = []
for spell in tryndamere_dic['data']['Tryndamere']['spells']: 
    for x in spell['leveltip']['label']: tryndamere_spells.append(x)
all_champs.append(pd.Series(tryndamere_spells).value_counts())
names.append('TRYNDAMERE')

twistedfate_spells = []
for spell in twistedfate_dic['data']['TwistedFate']['spells']: 
    for x in spell['leveltip']['label']: twistedfate_spells.append(x)
all_champs.append(pd.Series(twistedfate_spells).value_counts())
names.append('TWISTEDFATE')

twitch_spells = []
for spell in twitch_dic['data']['Twitch']['spells']: 
    for x in spell['leveltip']['label']: twitch_spells.append(x)
all_champs.append(pd.Series(twitch_spells).value_counts())
names.append('TWITCH')

udyr_spells = []
for spell in udyr_dic['data']['Udyr']['spells']: 
    for x in spell['leveltip']['label']: udyr_spells.append(x)
all_champs.append(pd.Series(udyr_spells).value_counts())
names.append('UDYR')

urgot_spells = []
for spell in urgot_dic['data']['Urgot']['spells']: 
    for x in spell['leveltip']['label']: urgot_spells.append(x)
all_champs.append(pd.Series(urgot_spells).value_counts())
names.append('URGOT')

varus_spells = []
for spell in varus_dic['data']['Varus']['spells']: 
    for x in spell['leveltip']['label']: varus_spells.append(x)
all_champs.append(pd.Series(varus_spells).value_counts())
names.append('VARUS')

vayne_spells = []
for spell in vayne_dic['data']['Vayne']['spells']: 
    for x in spell['leveltip']['label']: vayne_spells.append(x)
all_champs.append(pd.Series(vayne_spells).value_counts())
names.append('VAYNE')

veigar_spells = []
for spell in veigar_dic['data']['Veigar']['spells']: 
    for x in spell['leveltip']['label']: veigar_spells.append(x)
all_champs.append(pd.Series(veigar_spells).value_counts())
names.append('VEIGAR')

velkoz_spells = []
for spell in velkoz_dic['data']['Velkoz']['spells']: 
    for x in spell['leveltip']['label']: velkoz_spells.append(x)
all_champs.append(pd.Series(velkoz_spells).value_counts())
names.append('VELKOZ')

vi_spells = []
for spell in vi_dic['data']['Vi']['spells']: 
    for x in spell['leveltip']['label']: vi_spells.append(x)
all_champs.append(pd.Series(vi_spells).value_counts())
names.append('VI')

viktor_spells = []
for spell in viktor_dic['data']['Viktor']['spells']: 
    for x in spell['leveltip']['label']: viktor_spells.append(x)
all_champs.append(pd.Series(viktor_spells).value_counts())
names.append('VIKTOR')

vladimir_spells = []
for spell in vladimir_dic['data']['Vladimir']['spells']: 
    for x in spell['leveltip']['label']: vladimir_spells.append(x)
all_champs.append(pd.Series(vladimir_spells).value_counts())
names.append('VLADIMIR')

volibear_spells = []
for spell in volibear_dic['data']['Volibear']['spells']: 
    for x in spell['leveltip']['label']: volibear_spells.append(x)
all_champs.append(pd.Series(volibear_spells).value_counts())
names.append('VOLIBEAR')

warwick_spells = []
for spell in warwick_dic['data']['Warwick']['spells']: 
    for x in spell['leveltip']['label']: warwick_spells.append(x)
all_champs.append(pd.Series(warwick_spells).value_counts())
names.append('WARWICK')

xerath_spells = []
for spell in xerath_dic['data']['Xerath']['spells']: 
    for x in spell['leveltip']['label']: xerath_spells.append(x)
all_champs.append(pd.Series(xerath_spells).value_counts())
names.append('XERATH')

xinzhao_spells = []
for spell in xinzhao_dic['data']['XinZhao']['spells']: 
    for x in spell['leveltip']['label']: xinzhao_spells.append(x)
all_champs.append(pd.Series(xinzhao_spells).value_counts())
names.append('XINZHAO')

yasuo_spells = []
for spell in yasuo_dic['data']['Yasuo']['spells']: 
    for x in spell['leveltip']['label']: yasuo_spells.append(x)
all_champs.append(pd.Series(yasuo_spells).value_counts())
names.append('YASUO')

yorick_spells = []
for spell in yorick_dic['data']['Yorick']['spells']: 
    for x in spell['leveltip']['label']: yorick_spells.append(x)
all_champs.append(pd.Series(yorick_spells).value_counts())
names.append('YORICK')

zac_spells = []
for spell in zac_dic['data']['Zac']['spells']: 
    for x in spell['leveltip']['label']: zac_spells.append(x)
all_champs.append(pd.Series(zac_spells).value_counts())
names.append('ZAC')

zed_spells = []
for spell in zed_dic['data']['Zed']['spells']: 
    for x in spell['leveltip']['label']: zed_spells.append(x)
all_champs.append(pd.Series(zed_spells).value_counts())
names.append('ZED')

ziggs_spells = []
for spell in ziggs_dic['data']['Ziggs']['spells']: 
    for x in spell['leveltip']['label']: ziggs_spells.append(x)
all_champs.append(pd.Series(ziggs_spells).value_counts())
names.append('ZIGGS')

zilean_spells = []
for spell in zilean_dic['data']['Zilean']['spells']: 
    for x in spell['leveltip']['label']: zilean_spells.append(x)
all_champs.append(pd.Series(zilean_spells).value_counts())
names.append('ZILEAN')

zyra_spells = []
for spell in zyra_dic['data']['Zyra']['spells']: 
    for x in spell['leveltip']['label']: zyra_spells.append(x)
all_champs.append(pd.Series(zyra_spells).value_counts())
names.append('ZYRA')

full_spells = pd.concat(all_champs, axis = 1, ignore_index=False)
full_spells = full_spells.rename(index = str, columns = dict(zip(range(0, len(names)), names)))
full_spells = full_spells.fillna(0)





# Combining the spells counts and the stats
full_spells['total'] = full_spells.sum(axis=1)
for row in full_spells.index:
    if full_spells.loc[row]['total'] < 10:
        full_spells.drop(row, axis = 0, inplace = True)
full_spells_t = full_spells.T

full_df = stats_scaled_df.join(full_spells_t)
full_df = full_df.join(tags_exp_df)
full_labeled_df = stats_scaled_labeled_df.join(full_spells_t)
full_labeled_df = full_labeled_df.join(tags_exp_df)

full_labeled_df2 = stats_scaled_labeled_df2.join(full_spells_t)
full_labeled_df2 = full_labeled_df2.join(tags_exp_df)

for p in full_df.index :
    if p not in true_pos.index:
        full_df.drop(p, axis = 0, inplace = True)

for p in full_labeled_df.index :
    if p not in true_pos.index:
        full_labeled_df.drop(p, axis = 0, inplace = True)

for p in full_labeled_df2.index :
    if p not in true_pos.index:
        full_labeled_df2.drop(p, axis = 0, inplace = True)





