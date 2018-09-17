import requests
from bs4 import BeautifulSoup
from csv import writer, reader


def init():
    """Main init function runs on startup"""
    choosen_url = input("Paste in a full url (including http/s): ")
    site_data = scan_site_images(choosen_url)
    name = name_gen(choosen_url)
    write_csv(site_data, name)
    activae_gen = input("Generate CSV to HTML? (y/n): ")
    if activae_gen[0] == 'y':
        gen_html(choosen_url, name)


def name_gen(url_string):
    """Return a website name"""
    name = url_string.split('/')[2]
    return name


def write_csv(url_data, name):
    """parses the data back a .CSV file"""
    with open(f'./csv/{name}.csv', 'w', encoding="utf-8") as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(["Index", "Url"])
        soup = BeautifulSoup(url_data.content, "html.parser")
        img_tags = soup.find_all("img", {"src": True})
        for i, img in enumerate(img_tags):
            src = img["src"]
            csv_writer.writerow([i, src])
        print(f"Done scraping, closing {name}.csv file")


def scan_site_images(url):
    """Scraper sends a request to site"""
    STATUS_SUCCESS = 200
    get_result = requests.get(url)
    print(f"Got status response: {get_result.status_code}")
    if get_result.status_code is not STATUS_SUCCESS:
        raise Exception(f"ERROR: Failed to parse the given url")
    return get_result


def gen_html(url, name):
    """Optional function turns the .CSV file into an .HTML file"""
    with open(f'./csv/{name}.csv', 'r', encoding="utf-8") as csv_file:
        csv_reader = reader(csv_file)
        items = list(csv_reader)
        with open(f'./html/{name}.html', 'w') as html_file:
            html_file.write("<body>\n")
            for item in items:
                if item:
                    html_file.write(f"<img src={item[1]}>\n")
            html_file.write("</body>")
        print(f"Done, {name}.html was created")


init()
