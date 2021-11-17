from html_text import *
import pandas as pd
import numpy as np
from env import *
from services import *
from functions import *

# ['Antal elever (52 st)', 'Godkänt Augusti (35 st)', 35],
# ['Antal elever (52 st)', 'Ej Godkänt Augusti (17 st)', 17],
# ['Godkänt Augusti (35 st)', 'Godkänt December (32 st)', 30],
# ['Godkänt Augusti (35 st)', 'Ej Godkänt December (20 st)', 5],
# ['Ej Godkänt Augusti (17 st)', 'Godkänt December (32 st)', 2],
# ['Ej Godkänt Augusti (17 st)',
#  'Ej Godkänt December (20 st)', 15],
# ['Godkänt December (32 st)', 'Godkänt Slutbetyg (34 st)', 31],
# ['Godkänt December (32 st)',
#  'Ej Godkänt Slutbetyg (18 st)', 1],
# ['Ej Godkänt December (20 st)',
#  'Godkänt Slutbetyg (34 st)', 3],
# ['Ej Godkänt December (20 st)',
#  'Ej Godkänt Slutbetyg (18 st)', 17],

# html_text = HTML_TEXT

service_sheet = get_sheet_service()


sheet_name = '7A'

# dict som skall spara data på hur många 'F' och 'G' som varje nod har.
nodes = {}

# dict för att hämta kalkylaret till en dataframe.
col_map = {
    'Elever': 'Elever',
}

# Förbereder col_map som används för att hämta kalkylaret till en dataframe
# samt nodes som senare skall fyllas med antalet 'F' och 'G' för varje nod.
for i, k in enumerate(etapper):
    col_map[str(i+1)] = etapper[i]
    nodes[etapper[i]] = {'F': [], 'G': []}

# kalkylarkets range
_range = sheet_name+'!A1:D'

# Get df and errors
df, errors = get_sheet_as_df(service_sheet, SPREADSHEET_ID, _range, col_map)

# Replace empty strings with NaN
df.replace('', np.nan, inplace=True)

# Drop rows with NaN
df.dropna(inplace=True)

#Tar ut antalet rader som har F eller inte F enligt följande syntax:
# df[etapper[0]] == 'F'][etapper[0]].index.tolist()
# då får man ut indexlista över de som skall vara i respektive grupp
for k in nodes.keys():
    f = df[df[k] == 'F'][k].index.tolist()
    g = df[df[k] != 'F'][k].index.tolist()
    nodes[k]['F'] = f
    nodes[k]['G'] = g


# ['Antal elever', 'Godkänt Augusti', 35],
# ['Antal elever', 'Ej Godkänt Augusti', 17],

# ['Godkänt Augusti', 'Godkänt December', 30],
# ['Godkänt Augusti', 'Ej Godkänt December', 5],

# ['Ej Godkänt Augusti', 'Godkänt December', 2],
# ['Ej Godkänt Augusti', 'Ej Godkänt December', 15],

# ['Godkänt December', 'Godkänt Slutbetyg', 31],
# ['Godkänt December', 'Ej Godkänt Slutbetyg', 1],

# ['Ej Godkänt December', 'Godkänt Slutbetyg', 3],
# ['Ej Godkänt December', 'Ej Godkänt Slutbetyg', 17]

# räknar samman totala antalet elever mha g och g från for-loopen
# ett f/g-par i vilken av noderna som helst utgör totala antalet elever.
antal_elever = len(f) + len(g)

# print(antal_elever)
# print(nodes)


info_text = "<div style='width: 20%; float: left;'> <h5>EJ GODKÄNT " + etapper[0] + "</h5><ul>"
for e in nodes[etapper[0]]['F']:
    info_text += "<li>"+df.loc[e]['Elever'] + "</li>"
info_text += "</ul></div>"

# print(f"Antal elever ({antal_elever} st) -> {etapper[0]} F ({ len( nodes[etapper[0]]['F'] ) } st)")
# print(f"Antal elever ({antal_elever} st) -> {etapper[0]} F ({ len( nodes[etapper[0]]['G'] ) } st)")
rows = "['Antal elever (" + str(len(nodes[etapper[0]]['G']) + len(nodes[etapper[0]]['F'])) + " st)', 'Godkänt " + etapper[0] + " ("+str(len(nodes[etapper[0]]['G']))+" st)', " + str(len(nodes[etapper[0]]['G']))+"],\n"
rows += "['Antal elever (" + str(len(nodes[etapper[0]]['G']) + len(nodes[etapper[0]]['F'])) + " st)', 'Ej Godkänt " + etapper[0]+" ("+str(len(nodes[etapper[0]]['F']))+" st)', " + str(len(nodes[etapper[0]]['F']))+"],\n"

# print(rows)

# print(df)

# FÖRÄNDRINGARNA
for i, k in enumerate(nodes.keys()):
    if i < len(etapper) - 1:
        before_f = nodes[etapper[i]]['F']
        after_f = nodes[etapper[i+1]]['F']
        
        index_removed = list(set(before_f) - set(after_f))
        index_added = list(set(after_f) - set(before_f))
        numb_removed = len(index_removed)
        numb_added = len(index_added)

        info_text += "<div style='width: 20%; float: left;'><h5>EJ GODKÄNT " + etapper[i+1] + "</h5><ul>"
        for e in nodes[etapper[i+1]]['F']:
            info_text += "<li>"+df.loc[e]['Elever'] + "</li>"
        info_text += "</ul></div>"
        # info_text += node_elever_f

        # for e in index_removed:
        #     print(df.loc[e]['Elever'])

        # print(f"F {etapper[i+1]} - {removed} st försvann och {added} st lades till. Det gick från {len(before_f)} st till {len(after_f)} st.")

        # before_g = nodes[etapper[i]]['G']
        # after_g = nodes[etapper[i+1]]['G']

        # removed = len(list(set(before_g) - set(after_g)))
        # added = len(list(set(after_g) - set(before_g)))

        # print(f"G {etapper[i+1]} - {removed} st försvann och {added} st lades till. Det gick från {len(before_g)} st till {len(after_g)} st.")
        
        number_this_g = " ("+str(len(nodes[etapper[i]]['G']))+" st)"
        number_this_f = " ("+str(len(nodes[etapper[i]]['F']))+" st)"
        number_next_g = " ("+str(len(nodes[etapper[i+1]]['G']))+" st)"
        number_next_f = " ("+str(len(nodes[etapper[i+1]]['F']))+" st)"

        rows += "['Godkänt "+etapper[i]+number_this_g+"', 'Godkänt " + etapper[i+1] + number_next_g + "', " + str(len(set(nodes[etapper[i]]['G']) & set(nodes[etapper[i+1]]['G'])))+"],\n"
        rows += "['Godkänt "+etapper[i]+number_this_g+"', 'Ej Godkänt "+etapper[i+1] + number_next_f + "', " + str(len(set(nodes[etapper[i]]['G']) & set(nodes[etapper[i+1]]['F'])))+"],\n"
        rows += "['Ej Godkänt "+etapper[i]+number_this_f+"', 'Godkänt "+etapper[i+1] + number_next_g+"', " + str(len(set(nodes[etapper[i]]['F']) & set(nodes[etapper[i+1]]['G'])))+"],\n"
        rows += "['Ej Godkänt "+etapper[i]+number_this_f+"', 'Ej Godkänt "+etapper[i+1] + number_next_f +"', " + str(len(set(nodes[etapper[i]]['F']) & set(nodes[etapper[i+1]]['F'])))+"],\n"

# print(rows)

print(info_text)

HTML_TEXT = HTML_TEXT_1 + info_text + HTML_TEXT_2 + rows + HTML_TEXT_3 

# print(HTML_TEXT)
with open("generated_html.html", 'w') as file:
    file.write(HTML_TEXT.strip())
