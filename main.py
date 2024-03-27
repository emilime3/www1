import requests
from bs4 import BeautifulSoup
import os
from googlesearch import search
import subprocess

def process_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    section = soup.find('div', class_='rich-text-2 tablecontent w-richtext')
    tiktokers = []
    for item in section.find_all('li'):
        tiktoker = item.text.strip()
        if tiktoker:
            tiktokers.append(tiktoker)

    with open('tiktokers_list.md', 'w', encoding='utf-8') as file:
        file.write("# Lista TikTokerów\n\n")
        for tiktoker in tiktokers:
            file.write(f"- [{tiktoker}](tiktokers/{tiktoker.replace(' ', '_')}.md)\n")

    os.makedirs('tiktokers', exist_ok=True)

    for tiktoker in tiktokers:
        # Próba wyodrębnienia tylko imienia i nazwiska TikTokera
        name_only = tiktoker.split('-')[0].split('.')[1].strip()  # Przykładowe przetworzenie
        tiktoker_file_path = os.path.join('tiktokers', f"{name_only.replace(' ', '_')}.md")
        with open(tiktoker_file_path, 'w', encoding='utf-8') as file:
            file.write(f"# {name_only}\n\n")

            query = f"{name_only} TikToker site:tiktok.com"
            tiktok_profile_url = next(search(query, num=1, stop=1, pause=2), None)
            if tiktok_profile_url:
                file.write(f"\nOdwiedź profil na TikToku: [{tiktok_profile_url}]({tiktok_profile_url})\n")

    with open('index.md', 'w', encoding='utf-8') as file:
        file.write("# Witryna poświęcona TikTokerom\n\n")
        file.write("TUTAJ ZNAJDZIESZ NAJLEPSZYCH TIKTOKERÓW NA ŚWIECIE - [Lista TikTokerów](tiktokers_list.md)\n")

    with open('_config.yml', 'w', encoding='utf-8') as file:
        file.write("theme: minima\n")

    print("Zakończono generowanie witryny.")

def generate_site_with_jekyll():
    # Wywołanie Jekyll build
    subprocess.run(["bundle", "exec", "jekyll", "build"], check=True, shell=True)

    print("Strona wygenerowana za pomocą Jekylla.")

# Adres strony do scrapowania
url = 'https://www.favikon.com/blog/the-20-most-famous-tiktok-influencers-in-the-world'

# Przetwarzanie strony
#process_page(url)

generate_site_with_jekyll()
