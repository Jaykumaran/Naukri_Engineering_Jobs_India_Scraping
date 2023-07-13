import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_naukri_engineering_jobs(count):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)

    try:
        driver.get("https://www.naukri.com/engineering-jobs")

        csv_file = open('Naukri_scrape_all_details.csv', 'w', encoding="utf-8", newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Job Title', 'Company', 'Experience', 'Salary', 'Location', 'Description', 'Skills'])

        current_page = 1
        while current_page <= count:
            job_articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article.jobTuple')))
            for article in job_articles:
                try:
                    job_title = article.find_element(By.CSS_SELECTOR, 'a.title.ellipsis').text
                    company = article.find_element(By.CSS_SELECTOR, 'a.subTitle.ellipsis').text
                    experience = article.find_element(By.CSS_SELECTOR, 'li.experience span').text
                    salary = article.find_element(By.CSS_SELECTOR, 'li.salary span').text
                    location = article.find_element(By.CSS_SELECTOR, 'li.location span').text
                    description = article.find_element(By.CSS_SELECTOR, 'div.ellipsis.job-description').text
                    tags = [tag.text for tag in article.find_elements(By.CSS_SELECTOR, 'ul.tags li')]

                    csv_writer.writerow([job_title, company, experience, salary, location, description, ', '.join(tags)])
                    print('Job Title:', job_title)
                    print('Company:', company)
                    print('Experience:', experience)
                    print('Salary:', salary)
                    print('Location:', location)
                    print('Description:', description)
                    print('Skills:', tags)
                    print('-----------------------------------------')
                except Exception as e:
                    print('Error occurred while scraping job details:', str(e))

            try:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text() = "Next"]')))
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                driver.execute_script("window.scrollBy(0, -150);")
                next_button.click()
                current_page += 1
            except Exception as e:
                print('Error occurred while clicking next button:', str(e))
                break

        csv_file.close()
    except Exception as e:
        print('Error occurred during scraping:', str(e))
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_naukri_engineering_jobs(500)
