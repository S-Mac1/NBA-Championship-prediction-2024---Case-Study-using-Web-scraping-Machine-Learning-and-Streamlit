# Import der benötigten Module
import streamlit as st
import requests
import analyse

from bs4 import BeautifulSoup

# URL der Homepage
BASE_URL = "https://www.basketball-reference.com/"

# Setting der Streamlit-Homepage
st.set_page_config(layout = "wide")

# Überschrift und Info
st.header("NBA Championship Analyse - Who is next?")
st.info("Datenquelle: [Basketball Reference](https://www.basketball-reference.com)")

# Spalten setzten für die Streamlit-Homepage
col1, col2 = st.columns(2)

# Alle aktuellen NBA-Teams - Default-Index setzen
nba_teams = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"]
default_index = nba_teams.index("Los Angeles Lakers")

# Sidebar für die Streamlit-Homepage konfiguieren
with st.sidebar:
    team = st.selectbox("Welches aktuelle NBA Team möchtest du analysieren?", nba_teams, index = default_index)

    # Teamnamen in Kürzel umwandeln für das Webscraping
    if team == "Atlanta Hawks":
        team_kurz = "ATL"
    elif team == "Boston Celtics":
        team_kurz = "BOS"
    elif team == "Brooklyn Nets":
        team_kurz = "BRK"
    elif team == "Charlotte Hornets":
        team_kurz = "CHO"
    elif team == "Chicago Bulls":
        team_kurz = "CHI"
    elif team == "Cleveland Cavaliers":
        team_kurz = "CLE"
    elif team == "Dallas Mavericks":
        team_kurz = "DAL"
    elif team == "Denver Nuggets":
        team_kurz = "DEN"
    elif team == "Detroit Pistons":
        team_kurz = "DET"
    elif team == "Golden State Warriors":
        team_kurz = "GSW"
    elif team == "Houston Rockets":
        team_kurz = "HOU"
    elif team == "Indiana Pacers":
        team_kurz = "IND"
    elif team == "Los Angeles Clippers":
        team_kurz = "LAC"
    elif team == "Los Angeles Lakers":
        team_kurz = "LAL"
    elif team == "Memphis Grizzlies":
        team_kurz = "MEM"
    elif team == "Miami Heat":
        team_kurz = "MIA"
    elif team == "Milwaukee Bucks":
        team_kurz = "MIL"
    elif team == "Minnesota Timberwolves":
        team_kurz = "MIN"
    elif team == "New Orleans Pelicans":
        team_kurz = "NOP"
    elif team == "New York Knicks":
        team_kurz = "NYK"
    elif team == "Oklahoma City Thunder":
        team_kurz = "OKC"
    elif team == "Orlando Magic":
        team_kurz = "ORL"
    elif team == "Philadelphia 76ers":
        team_kurz = "PHI"
    elif team == "Phoenix Suns":
        team_kurz = "PHO"
    elif team == "Portland Trail Blazers":
        team_kurz = "POR"
    elif team == "Sacramento Kings":
        team_kurz = "SAC"
    elif team == "San Antonio Spurs":
        team_kurz = "SAS"
    elif team == "Toronto Raptors":
        team_kurz = "TOR"
    elif team == "Utah Jazz":
        team_kurz = "UTA"
    elif team == "Washington Wizards":
        team_kurz = "WAS"
    
    # Button konfiguieren für die Vorhersage
    button = st.button("Klick mich für die Vorhersage deines Teams!")
    
    if button:
        predict_df = analyse.predict_df.drop("Unnamed: 0.1", axis = 1)
        predict_df = predict_df.drop("Unnamed: 0", axis = 1)
        predict_df = predict_df.drop("champion", axis = 1)

        mein_team = predict_df.loc[predict_df["team"] == team]

        mein_team = mein_team.drop("team", axis = 1)

        predictions = analyse.logisReg.predict(mein_team)

        if predictions == "ja":
            st.write("2024: Meisterschaft!")
        else:
            st.write("2024: Leider kein Meistertitel!")

    # Info über die historischen Meistermannschaften erstellen
    st.info("Historische Meistermannschaften:")

    response = requests.get(BASE_URL + "leagues")

    if response.status_code == 200:
        data = response.text
    else:
        print(f"Fehler bei der Anfrage: {response.status_code}")
        
    data = BeautifulSoup(data, 'html.parser')

    champion = data.find_all("td")

    season = list(range(2023, 1946, -1))
    champions = []

    for i in range(9, len(champion) -1, 8):
        ausgabe = str(champion[i])
        ausgabe = ausgabe[:-9]
        ausgabe = ausgabe.split('html">')
        champions.append(ausgabe[1])

    # ABA-Teams löschen
    champions.pop(48)
    champions.pop(49)
    champions.pop(50)
    champions.pop(51)
    champions.pop(52)
    champions.pop(53)
    champions.pop(54)
    champions.pop(55)
    champions.pop(56)

    for i in range(0, 77):
        st.write(f"{season[i]}: {champions[i]}")

# Spalte 1 für die Streamlit-Homepage konfiguieren
with col1:
    
    st.subheader("Vereinsinformationen:")
    
    # Vereinsinformationen und Vereinslogo scrapen
    st.image(f"https://cdn.ssref.net/req/202404172/tlogo/bbr/{team_kurz}-2024.png", caption = "Teamfoto", width = 250)
    
    if team_kurz == "BRK":
        team_kurz = "NJN"
    elif team_kurz == "CHO":
        team_kurz = "CHA"
    elif team_kurz == "NOP":
        team_kurz = "NOH"
        
    response = requests.get(BASE_URL + f"teams/{team_kurz}")
    
    if response.status_code == 200:
        data = response.text
    else:
        print(f"Fehler bei der Anfrage: {response.status_code}")
    
    if team_kurz == "NJN":
        team_kurz = "BRK"
    elif team_kurz == "CHA":
        team_kurz = "CHO"
    elif team_kurz == "NOH":
        team_kurz = "NOP"
    
    data = BeautifulSoup(data, 'html.parser')
    
    text = data.find_all("strong")
    text2 = data.find_all("p")
    
    team_text = text[0]
    team_text = str(team_text)
    team_text = team_text[8:-9]
    st.write(f"*{team_text}*\n")
    
    for i in range(1,7):
        info = text[i]
        info = str(info)
        info = info[8:-9]
        ausgabe = text2[i+1]
        ausgabe = str(ausgabe)
        ausgabe = ausgabe[:-4]
        ausgabe = ausgabe.split("/strong>")
        ausgabe = [item.strip() for item in ausgabe]
        ausgabe = ausgabe[1]
        st.write(f"*{info}* {ausgabe}\n")
        
    st.subheader("Saisoninformationen:")
    
    st.write("Saison: 2023 - 2024")
    
    # Saisoninformationen scrapen
    response = requests.get(BASE_URL + f"teams/{team_kurz}/2024.html")
    
    if response.status_code == 200:
        data = response.text
    else:
        print(f"Fehler bei der Anfrage: {response.status_code}")
        
    data = BeautifulSoup(data, 'html.parser')
        
    text3 = data.find_all("p")
    
    for i,e in enumerate(text3):
        if i in [2, 4, 5, 6, 11]:
            if i == 4:
                ausgabe2 = e.get_text()[:-7]
                st.write(f"{ausgabe2}\n")
            else:
                ausgabe2 = e.get_text()
                st.write(f"{ausgabe2}\n")

# Spalte 2 für die Streamlit-Homepage konfiguieren
with col2:
    
    st.subheader("Ligadurchschnitt:")
    
    # URL der Webseite mit den Per Game Stats
    url = "https://www.basketball-reference.com/leagues/NBA_2024.html#all_per_game_team-opponent"

    # Die Seite herunterladen
    response = requests.get(url)

    # BeautifulSoup verwenden, um den HTML-Inhalt zu analysieren
    soup = BeautifulSoup(response.content, "html.parser")

    # Die Tabelle mit den Per Game Stats finden
    table = soup.find("table", {"id": "per_game-team"})

    # Die Zeilen der Tabelle durchgehen und die Daten extrahieren
    for row in table.find_all("tr")[-1:]:
        columns = row.find_all("td")
        team_name = columns[0].text
        field_goals = columns[3].text
        field_goal_attemps = columns[4].text
        field_goald_percentage = columns[5].text
        three_point_field_goals = columns[6].text
        three_point_field_goal_attemps = columns[7].text
        three_point_field_goald_percentage = columns[8].text
        two_point_field_goals = columns[9].text
        two_point_field_goal_attemps = columns[10].text
        two_point_field_goald_percentage = columns[11].text
        free_throws = columns[12].text
        free_throw_attemps = columns[13].text
        free_throw_percentage = columns[14].text
        offensive_rebounds = columns[15].text
        defensive_rebounds = columns[16].text
        total_rebounds = columns[17].text
        assists = columns[18].text
        steals = columns[19].text
        blocks = columns[20].text
        turnovers = columns[21].text
        fouls = columns[22].text
        punkte = columns[23].text

        st.write(f"{team_name}")
        st.write(f"Field Goals: {field_goals}   Field Goals Attemps: {field_goal_attemps}   Field Goals Percentage: {field_goald_percentage}")
        st.write(f"3-Point Field Goals: {three_point_field_goals}   3-Point Field Goal Attemps: {three_point_field_goal_attemps}    3-Point Field Goal Percentage: {three_point_field_goald_percentage}")
        st.write(f"2-Point Field Goals: {two_point_field_goals}   2-Point Field Goal Attemps: {two_point_field_goal_attemps}    2-Point Field Goal Percentage: {two_point_field_goald_percentage}")
        st.write(f"Free Throws: {free_throws}   Free Throws Attemps: {free_throw_attemps}   Free Throw Percentage: {free_throw_percentage}")
        st.write(f"Offensive Rebounds: {offensive_rebounds}    Defensive Rebounds: {defensive_rebounds}    Total Rebounds: {total_rebounds}")
        st.write(f"Assists: {assists}   Steals: {steals}    Blocks: {blocks}")
        st.write(f"Turnovers: {turnovers}   Fouls: {fouls}")
        st.write(f"Punkte: {punkte}")

    st.subheader("Saisondurchschnitt:")
    st.info("Offensive")
        
    # Die Tabelle mit den Per Game Stats finden (Offensive)
    table = soup.find("table", {"id": "per_game-team"})

    # Die Zeilen der Tabelle durchgehen und die Daten extrahieren
    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        if team in columns[0].text:
            team_name = columns[0].text
            field_goals = columns[3].text
            field_goal_attemps = columns[4].text
            field_goald_percentage = columns[5].text
            three_point_field_goals = columns[6].text
            three_point_field_goal_attemps = columns[7].text
            three_point_field_goald_percentage = columns[8].text
            two_point_field_goals = columns[9].text
            two_point_field_goal_attemps = columns[10].text
            two_point_field_goald_percentage = columns[11].text
            free_throws = columns[12].text
            free_throw_attemps = columns[13].text
            free_throw_percentage = columns[14].text
            offensive_rebounds = columns[15].text
            defensive_rebounds = columns[16].text
            total_rebounds = columns[17].text
            assists = columns[18].text
            steals = columns[19].text
            blocks = columns[20].text
            turnovers = columns[21].text
            fouls = columns[22].text
            punkte = columns[23].text

            st.write(f"Team: {team_name}")
            st.write(f"Field Goals: {field_goals}   Field Goals Attemps: {field_goal_attemps}   Field Goals Percentage: {field_goald_percentage}")
            st.write(f"3-Point Field Goals: {three_point_field_goals}   3-Point Field Goal Attemps: {three_point_field_goal_attemps}    3-Point Field Goal Percentage: {three_point_field_goald_percentage}")
            st.write(f"2-Point Field Goals: {two_point_field_goals}     2-Point Field Goal Attemps: {two_point_field_goal_attemps}      2-Point Field Goal Percentage: {two_point_field_goald_percentage}")
            st.write(f"Free Throws: {free_throws}   Free Throws Attemps: {free_throw_attemps}   Free Throw Percentage: {free_throw_percentage}")
            st.write(f"Offensive Rebounds: {offensive_rebounds}     Defensive Rebounds: {defensive_rebounds}    Total Rebounds: {total_rebounds}")
            st.write(f"Assists: {assists}   Steals: {steals}    Blocks: {blocks}")
            st.write(f"Turnovers: {turnovers}   Fouls: {fouls}")
            st.write(f"Punkte: {punkte}")
        
    st.info("Defensive")
        
    # Die Tabelle mit den Per Game Stats finden (Defensive)
    table = soup.find("table", {"id": "per_game-opponent"})

    # Die Zeilen der Tabelle durchgehen und die Daten extrahieren
    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        if team in columns[0].text:
            team_name = columns[0].text
            field_goals = columns[3].text
            field_goal_attemps = columns[4].text
            field_goald_percentage = columns[5].text
            three_point_field_goals = columns[6].text
            three_point_field_goal_attemps = columns[7].text
            three_point_field_goald_percentage = columns[8].text
            two_point_field_goals = columns[9].text
            two_point_field_goal_attemps = columns[10].text
            two_point_field_goald_percentage = columns[11].text
            free_throws = columns[12].text
            free_throw_attemps = columns[13].text
            free_throw_percentage = columns[14].text
            offensive_rebounds = columns[15].text
            defensive_rebounds = columns[16].text
            total_rebounds = columns[17].text
            assists = columns[18].text
            steals = columns[19].text
            blocks = columns[20].text
            turnovers = columns[21].text
            fouls = columns[22].text
            punkte = columns[23].text

            st.write(f"Team: {team_name}")
            st.write(f"Field Goals: {field_goals}   Field Goals Attemps: {field_goal_attemps}   Field Goals Percentage: {field_goald_percentage}")
            st.write(f"3-Point Field Goals: {three_point_field_goals}   3-Point Field Goal Attemps: {three_point_field_goal_attemps}    3-Point Field Goal Percentage: {three_point_field_goald_percentage}")
            st.write(f"2-Point Field Goals: {two_point_field_goals}     2-Point Field Goal Attemps: {two_point_field_goal_attemps}      2-Point Field Goal Percentage: {two_point_field_goald_percentage}")
            st.write(f"Free Throws: {free_throws}   Free Throws Attemps: {free_throw_attemps}   Free Throw Percentage: {free_throw_percentage}")
            st.write(f"Offensive Rebounds: {offensive_rebounds}     Defensive Rebounds: {defensive_rebounds}    Total Rebounds: {total_rebounds}")
            st.write(f"Assists: {assists}   Steals: {steals}    Blocks: {blocks}")
            st.write(f"Turnovers: {turnovers}   Fouls: {fouls}")
            st.write(f"Punkte: {punkte}")        