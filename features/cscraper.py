from requests import get
try: 
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    if input(f"BeautifulSoup4 is required to run this program, execute pip install bs4? (Y): ").lower().strip() in ["", "y"]:
        import os
        os.system(f"pip install bs4")
    else:
        exit()
import json

#Static solution TODO: make dynamic
def CScraper(MODE="RTX3080"):
    SNAPSHOT = False
    with open("searches.json", "r") as jFile:
        queries = json.load(jFile)

    #Use snapshots instead of querying Carousell while in development as it is more ethical 
    if SNAPSHOT:
        htmlStr = ""
        with open("rtx3080_body.html", "r", encoding='utf-8') as snapshotF:
            for line in snapshotF:
                htmlStr += line
        soup = BeautifulSoup(htmlStr)
    else:
        bHTML = get(queries[MODE], headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'
        }) #Might break if they ever add more validation for scraping in headers
        soup = BeautifulSoup(bHTML.content, 'html5lib')

    #Parse
    output = []
    PREFIX = "https://www.carousell.sg"
    for product in soup.find_all('div', class_='D_rl D_BU'):
        title = product.find('p', class_='D_pw M_kN D_ov M_jO D_px M_kO D_pA M_kS D_pE M_kV D_pH M_kY D_pJ M_la D_pF M_kW D_pN')
        price = product.find('p', class_='D_pw M_kN D_ov M_jO D_px M_kO D_pA M_kS D_pC M_kU D_pH M_kY D_pK M_lb D_pM')
        image = product.img #No class required, therefore the syntax allows, assume there is only one img tag
        urlList = product.find_all(class_='D_qF')
        for element in urlList:
            url = element["href"]
            if url[:2] == "/p":
                url = PREFIX + url
        if not image:
            video = product.find('video') #Class is D_aEk in case there are unreleated videos breaking, assume there is only 1 in the card
            if video:
                try: 
                    mediaOutput = "[Video]({})".format(video['src'])
                except KeyError:
                    mediaOutput = "Video is present but src is not found"
            else:
                mediaOutput = "No media found"
        else:
            mediaOutput = "[Image]({})".format(image['src'])
        output.append([title.get_text() if title else "Title not found", url, "\nPrice: {}\n{}".format("$0" if not price else price.get_text(), mediaOutput)])

    return output

if __name__ == "__main__":
    print(CScraper())