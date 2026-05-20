from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

def convert_persian_numbers(text, mode):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹,،"
    english_digits = "0123456789,,"

    translation_table = str.maketrans(persian_digits, english_digits)
    if mode == "price":
        converted = text.translate(translation_table)
        return converted.replace(",", "")
    
    elif mode == "year":
        converted = text.translate(translation_table)
        return converted.split(" - ")[1]
    
    elif mode == "mileage":
        converted = text.translate(translation_table)
        return converted
    
    else:
        raise ValueError("Invalid mode")

def scraper(page_counter):
    price = []
    year = []
    color = []
    mileage = []
    urls = []

    with sync_playwright() as p:
        for pagenumb in range(page_counter):
            browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)
            page = browser.new_page()
            page.goto(f"https://divar.ir/s/tehran/car/peugeot/207i?page={pagenumb}")
            page.wait_for_selector("div")
            content = page.content()

            soup = BeautifulSoup(content, "html.parser")

            allcars = soup.find_all("a", attrs={"class":"kt-post-card__action"})
            allcars_description = soup.find_all("div", attrs= {"class": "kt-post-card__description"})

            for i in range(len(allcars)): 
                try:
                    selected_url = 'https://divar.ir' + allcars[i]['href']
                    page.goto(selected_url)
                    page.wait_for_selector("td")
                    selected_car_content = page.content()

                    soup = BeautifulSoup(selected_car_content, "html.parser")
                    selected_car = soup.find_all('td' , attrs={"class":"kt-group-row-item kt-group-row-item__value kt-group-row-item--info-row"})
                    
                    # Extract and validate car price    
                    selected_price = allcars_description[(2*i)+1].text.split(" ")[0]
                    int_selected_price = int(convert_persian_numbers(selected_price, "price"))
                    if  300000000 < int_selected_price and len(selected_car)==3:   # Filter out invalid/fake listings based on price
                        price.append(convert_persian_numbers(selected_price, "price"))
                        
                        # Extract car manufacture year
                        selected_model = selected_car[1].text
                        year.append(convert_persian_numbers(selected_model, "year"))

                        # Normalize car color to English
                        if "سفید" in selected_car[2].text:
                            color.append("White")
                            
                        elif "مشکی" in selected_car[2].text:
                            color.append("Black")
                            
                        elif "خاکستری" in selected_car[2].text:
                            color.append("Gray")
                        else:
                            color.append("Other")
                        
                        # Extract car mileage
                        selected_kilometer = selected_car[0].text
                        mileage.append(convert_persian_numbers(selected_kilometer, "mileage"))

                        # Store car page URL
                        urls.append(selected_url)
                except Exception as e:
                    print(f"Error loading ad: {e}")
            soup.decompose()    
            browser.close()
    
    seen = set()  # Load existing rows to prevent duplicates

    try:
        with open("csvfile.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                seen.add(tuple(row))
    except FileNotFoundError:
        pass

    with open("csvfile.csv", "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        for p, m, k, c, u in zip(price, year, mileage, color, urls):
            row = (p, m, k, c, u)

            if row not in seen:           # Append only new unique rows
                writer.writerow(row)
                seen.add(row)

if __name__ == "__main__":
    scraper(1)   # Specify the number of pages to scrape for example scraper(5)