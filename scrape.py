import requests as req
from bs4 import BeautifulSoup
from csv import writer, reader


def init():
    """Main init function runs on startup"""
    user_input = input("Paste in a full url (including http/s): ")
    scrape_site(user_input)
    activae_gen = input("Generate CSV to HTML? (y/n): ")
    if activae_gen[0] == 'y':
        gen_html(user_input)


def scrape_site(url):
    """Scraper sends a request and parses the data back to a .CSV file"""
    incoming = req.get(url)
    print(f"Got status response: {incoming.status_code}")
    if incoming.status_code == 200:
        name = url.split('.')[1]
        with open(f'./csv/{name}.csv', 'w', encoding="utf-8") as csv_file:
            csv_writer = writer(csv_file)
            csv_writer.writerow(["Index", "Url", "Alt"])
            soup = BeautifulSoup(incoming.content, "html.parser")
            img_tags = soup.find_all("img", {"src": True})
            for i, img in enumerate(img_tags):
                alt = img["alt"]
                src = img["src"]
                csv_writer.writerow([i, src, alt])
        print(f"Done scraping, closing {name}.csv file")


def gen_html(url):
    """Optional function turns the .CSV file into an .HTML file"""
    name = url.split('.')[1]
    with open(f'./csv/{name}.csv', 'r', encoding="utf-8") as csv_file:
        csv_reader = reader(csv_file)
        items = list(csv_reader)
        with open(f'./html/{name}.html', 'w') as html_file:
            html_file.write("<body>\n")
            for item in items:
                if item:
                    html_file.write(f"<img src={item[1]} alt={item[2]}>\n")
            html_file.write("</body>")
        print(f"Done, {name}.html was created")


init()
