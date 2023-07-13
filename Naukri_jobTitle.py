import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_naukri_engineering_jobs( count):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.naukri.com/engineering-jobs")

    csv_file = open('Naukri_scrape_Title.csv', 'w', encoding="utf-8", newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Job Title'])

    current_page = 1
    while current_page <= count:
        job_titles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.title.ellipsis')))
        for title in job_titles:
                csv_writer.writerow([title.text])
                print(title.text)

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text() = "Next"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        driver.execute_script("window.scrollBy(0, -150);")
        next_button.click()
        current_page += 1

    csv_file.close()
    driver.quit()

if __name__ == "__main__":
    scrape_naukri_engineering_jobs(500)
