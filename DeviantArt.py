"""Author : Ahmed Limam
u/Infreezy

Note : Apparently it only works if default browser is Chrome.
Error : requests.exceptions.SSLError: HTTPSConnectionPool(host='www.deviantart.com', port=443): Max retries exceeded with url: /infreezy/art/Yare-Yare-795900546 (Caused by SSLError(SSLZeroReturnError(6, 'TLS/SSL connection has been closed (EOF) (_ssl.c:1076)')))"""
# TODO : fix SSLError & Timeouts
import requests,bs4,os
page=1
search = input('>')
template = f"https://www.deviantart.com/search/deviations?page={page}&q={search}"
r1 = requests.get(template)
r1.raise_for_status()
soup1 = bs4.BeautifulSoup(r1.text, 'lxml')
body1 = soup1.body
about_results_number = body1.select("span._4pI41")[0].text
if "No results" in about_results_number:
    print(f"{about_results_number}.")
    exit()
else:
    print(f"About {about_results_number} for \"{search}\".")
results_number = about_results_number[:about_results_number.index(' results')]
if results_number[-1] == "K":
    continue_question = input('Warning too many files to download.\nContinue anyway? (yes/no)\n>').lower()
    if continue_question == "no" or continue_question == "n":
        exit()
if results_number[-1] == "M":
    continue_question = input('Warning too many files to download.\nContinue anyway? (yes/no)\n>').lower()
    if continue_question == "no" or continue_question == "n":
        exit()
while True:
    template = f"https://www.deviantart.com/search/deviations?page={page}&q={search}"
    r1 = requests.get(template)
    r1.raise_for_status()
    soup1 = bs4.BeautifulSoup(r1.text, 'lxml')
    body1 = soup1.body
    print("\nCurrently on page",page)
    try :
        for i in range(0,24):
            imgs_bloc = body1.select("a._5sgHw")[i]
            img_link =imgs_bloc["href"]
            print("Loading "+img_link)
            try :
                r2 = requests.get(img_link)
            except requests.exceptions.SSLError:
                i+=1
                continue
            soup2 = bs4.BeautifulSoup(r2.text,'lxml')
            try:
                final_bloc = soup2.select('div._1LGGs div img')[0]["src"]
            except Exception:
                i+=1
            try:
                os.mkdir("imgs")
            except FileExistsError:
                pass
            r3 = requests.get(final_bloc)
            file = open(os.path.join("imgs",os.path.basename(img_link))+".png","wb")
            print(f"\tDownloading {final_bloc}")
            for chunk in r3.iter_content(100000):
                file.write(chunk)
        page+=1
        try:
            check = body1.select("a._5sgHw")[0]
        except Exception:
            pass
    except IndexError:
        print("Done.")
        break
