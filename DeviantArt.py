import requests,bs4,os,urllib3
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
}
urllib3.disable_warnings()
page=1
search = input('Searching for : ')
template = f"https://www.deviantart.com/search/deviations?page={page}&q={search}"
session = requests.session()
r1 = session.get(template,headers=headers)
soup1 = bs4.BeautifulSoup(r1.text, 'lxml')
body1 = soup1.body
about_results_number = body1.select("span._4pI41")[0].text
if "No results" in about_results_number:
    print(f"{about_results_number}.")
    exit()
else:
    print(f"About {about_results_number} for \"{search}\".")
results_number = about_results_number[:about_results_number.index(' results')]
continue_question = input('Download? y/n :').lower()
if 'n' in continue_question:
    exit()
continue_question = input('Download? y/n :').lower()
if 'y' in continue_question:
    pass
elif 'n' in continue_question:
    exit()
while True:
    template = f"https://www.deviantart.com/search/deviations?page={page}&q={search}"
    session = requests.session()
    r1 = session.get(template, headers=headers)
    soup1 = bs4.BeautifulSoup(r1.text, 'lxml')
    body1 = soup1.body
    print("\nCurrently on page",page)
    try :
        for i in range(0,24):
            imgs_bloc = body1.select("a._5sgHw")[i]
            img_link =imgs_bloc["href"]
            print("Loading "+img_link)
            try :
                r2 = session.get(img_link, headers=headers)
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
            r3 = session.get(final_bloc, headers=headers)
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
        print("\nDone.")
        break
