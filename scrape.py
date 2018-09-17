import requests
from bs4 import BeautifulSoup
from csv import writer, reader
STATUS_SUCCESS = 200
FILES_ENCODING = "utf-8"

def main():
    """Main function runs on startup"""
    choosen_url = input("Paste in a full url (including http/s): ")
    site_data = request_site(choosen_url)
    domain_name = name_gen(choosen_url)
    images_list = write_csv(site_data, domain_name)
    activate_gen = input("Generate images list to HTML? (y/n): ")
    if activate_gen[0] == 'y':
        gen_html(domain_name, images_list)


def name_gen(url_string):
    """Return a website name"""
    domain_name = url_string.split('/')[2]
    return domain_name


def write_csv(url_data, domain_name):
    """parses the data back a .CSV file"""
    with open(f'./csv/{domain_name}.csv', 'w', encoding=FILES_ENCODING) as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(["Index", "Url"])
        soup = BeautifulSoup(url_data.content, "html.parser")
        img_tags = soup.find_all("img", {"src": True})
        images_list = []
        for i, img in enumerate(img_tags):
            row_data = i, img["src"]
            csv_writer.writerow([row_data])
            images_list.append(row_data)
        print(f"Done scraping, closing {domain_name}.csv file")
        return images_list


def request_site(url):
    """Scraper sends a request to site"""
    get_result = requests.get(url)
    print(f"Got status response: {get_result.status_code}")
    if get_result.status_code is not STATUS_SUCCESS:
        raise Exception(f"ERROR: Failed to parse the given url")
    return get_result


def gen_html(domain_name, images_list):
    """Optional function turns the images_list file into an .HTML file"""
    with open(f'./html/{domain_name}.html', 'w') as html_file:
        html_file.write("<body>\n")
        [html_file.write(f"<img src={item[1]}>\n") for item in images_list if len(item) > 1]
        html_file.write("</body>")
    print(f"Done, {domain_name}.html was created")


main()
