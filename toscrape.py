import json
from helper_methods import *


def get_book_links(driver, css_selector):
    return driver.find_elements_by_css_selector(css_selector)


url = 'https://books.toscrape.com/catalogue/page-1.html'
root = 'https://books.toscrape.com/catalogue/'
list_of_all_links = []
driver = start_chrome_browser(driver_exe_file_path='chromedriver.exe', url=url, headless=True)
total_pages = int(str(driver.find_element_by_class_name("current").text).split(' ')[-1])
link_selector = '.product_pod .image_container a'
results = []

for page in range(1, total_pages + 1):
    print(f"page : {page}")
    links = get_book_links(driver, link_selector)
    for i in range(len(links)):
        links = get_book_links(driver, link_selector)
        print(links[i].get_attribute("href"))
        product_link = links[i].get_attribute("href")
        links[i].click()
        product_title = driver.find_element_by_css_selector('.product_main h1').text
        product_information = driver.find_element_by_css_selector(".table-striped tbody")
        soup_content = convert_web_element_to_bs4_object(product_information)
        info_rows = soup_content.find_all("tr")
        product_data = {"title": product_title, "link": product_link}
        print(product_title)
        for row in info_rows:
            print(f"{row.th.text} : {row.td.text}")
            product_data[str(row.th.text).strip(" ")] = row.td.text
        results.append(product_data)
        driver.back()
    if page == total_pages:
        break
    next_page = driver.find_element(By.CSS_SELECTOR, '.next a')
    next_page.click()

with open("books_bookstoscrape.json", 'w') as file:
    json.dump(results, file)
print(len(results))
driver.quit()
