import requests
from bs4 import BeautifulSoup

def GetGameInfo(GameName):
    try:
        url = 'https://store.steampowered.com/search/?term='
        url2 = 'https://store.steampowered.com/app/'
        url3 = 'https://steamcharts.com/app/' #'https://steamcharts.com/search/?q='
        #url2 = 'https://steamdb.info/search/?a=all&q=%2F'
        #url3 = "https://steamdb.info/app/1721470/charts/"
        response = requests.get(url + GameName)
        emoticons_dictionary = {
            "Overwhelmingly Positive": " :star_struck:",
            "Very Positive": " :heart_eyes:",
            "Positive": " :smile:",
            "Mostly Positive": " :slight_smile:",
            "Mixed": " :neutral_face:",
            "Mostly Negative": " :confused:",
            "Negative": " :scream:",
            "Very Negative": " :rage:",
            "Overwhelmingly Negative": " :skull:"
        }

        if response.status_code != 200:
            #print('Nie udało się otrzymać danych')
            return "Error"
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            games = soup.find_all("a", class_ = 'search_result_row')
            #print(games[0].get('data-ds-appid'))
            app_ids = [] #games.get('data-ds-appid')
            app_names = []
            app_id = None
            
            app_names = [game.find('span', attrs={'class':'title'}).text.strip() for game in games if game.find('span', attrs={'class':'title'})]
            app_ids = [ids.get("data-ds-appid") for ids in games]
            
            #print(app_names, app_ids)

            for i in range(len(app_names)):
                if app_names[i].lower() == GameName.lower():
                    app_id = app_ids[i]
                    break
            if app_id == None:
                app_id = app_ids[0]
            
            #print(f"{app_id} -----------------------------------------------------")

            if app_id != None:
                #print('\n----------znaleziono grę-------------\n')
                response = requests.get(url2 + app_id)

                if response.status_code != 200:
                    #print('Nie udało się otrzymać danych')
                    return "Error"
                else:
                    soup = BeautifulSoup(response.content, "html.parser")

                    name = soup.find('div', attrs={"id": "appHubAppName", "class": "apphub_AppName"}).text.strip()
                    try:
                        price = soup.find('div', attrs={"class": "game_purchase_price price"}).text.strip()
                        before_price = ""
                        price_procent = ""
                    except:
                        try:
                            price = soup.find('div', attrs={"class": "discount_final_price"}).text.strip()
                            before_price = soup.find('div', attrs={"class": "discount_original_price"}).text.strip()
                            price_procent = soup.find('div', attrs={"class": "discount_pct"}).text.strip()
                        except:
                            price = "This game has no set price :("
                            before_price = ""
                            price_procent = ""
                    try:
                        description = soup.find('div', attrs={"class": "game_description_snippet"}).text.strip()
                    except:
                        description = f"Couldn't find description about {name} :("
                    try:
                        release_date = soup.find('div', attrs={'class': 'date'}).text.strip()
                    except:
                        release_date = "There is no release date for this game :("
                    try:
                        studio = soup.find('div', attrs={'class': 'summary column', 'id': 'developers_list'}).find('a').text.strip()
                    except:
                        studio = "There is no producer found :("
                    try:
                        image = soup.find('img', attrs={'class': 'game_header_image_full'}).get("src")
                    except:
                        image = 'https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png'
                    try:
                        opinion = soup.find('span', attrs={'itemprop': 'description'}).text.strip()
                        opinion = opinion + emoticons_dictionary[opinion]
                    except:
                        opinion = "This game don't have any opinion yet :("
                    try:
                        response = requests.get(url3 + app_id)
                        if response.status_code != 200:
                            players_online = "Couldn't find online players"
                        else:
                            soup = BeautifulSoup(response.content, "html.parser")
                            players_online = soup.find('span', attrs={'class': 'num'}).text.strip()
                            players_online = format(int(players_online), ',').replace(',', ' ')
                    except:
                        players_online = "Couldn't find online players"
                    #print(f"{name}\n{price}\n{before_price}\n{description}\n{release_date}\n{studio}\n{image}\n{opinion}\n\n{url2+app_id}")
                    
                    return [name, description, price, before_price, release_date, studio, opinion, image, url2+app_id, price_procent, players_online]
                    

            else:
                #print('nie znaleziono gier')
                return "Game not found"
            
            #print("\n----------------------------------------\n")

            #print(games)
            #print(f"AppIds: {app_ids}")
    except:
        return "Error"
        
while False:
    x = input("Game: ")
    print(GetGameInfo(x))
#<div class="_1n_4-zvf0n4aqGEksbgW9N">Counter-Strike 2</div>