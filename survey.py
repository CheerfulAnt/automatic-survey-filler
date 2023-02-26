#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import topSurveyFunctions as tSF
from datetime import date, datetime, timedelta
from random import randrange, choice, choices
import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

with open('topSurveyData.json', 'r', encoding="utf-8") as j_file:
    j_data = json.load(j_file)

shop_nr = 12345

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(j_data['driver_url'] + shop_nr)
driver.maximize_window()

bills_numbers_tuple = tSF.bill_nr_generator(j_data['last_run_date'], j_data['date_format'], j_data['days_back'],
    j_data['purchase_days_back'], j_data['shop_nr'][shop_nr]['bill_last_nr'], j_data['shop_nr'][shop_nr]['bill_daily'])

driver.find_element(By.ID, j_data['input_ID']['bill_number']).send_keys(bills_numbers_tuple[0])

dropdown_click = driver.find_element(By.XPATH, j_data['dropdown_options']['age_XPATH']
                        .format(choices(list(j_data['dropdown_options']['age_dict'].keys()),
                        weights=list(j_data['dropdown_options']['age_dict'].values()))[0]))
driver.execute_script("arguments[0].click();", dropdown_click)

tSF.button_click('buttonNext', driver)

tSF.button_star_click('page03', j_data['button_star_XPATH'], tSF.ratings_generator, j_data['survey_stars'],
                                                                            driver, rating_in=j_data['survey_rating'])

driver.find_element(By.ID, j_data['text_answers']['rating_satisfaction_ID']).send_keys(
                                                        "" if choice([0 ,1]) else tSF.select_comment(j_data, shop_nr))

if j_data['product_missing'] == 1:

    radio_click = driver.find_element(By.ID, j_data['radio_buttons']['product_missing_ID']
                        .format(j_data['product_missing']))
    driver.execute_script("arguments[0].click();", radio_click)

    driver.find_element(By.ID, j_data['text_answers']['product_missing_ID']).send_keys(
            j_data['text_answers']['product_missing'][randrange(len(j_data['text_answers']['product_missing']))])

else:

    radio_click = driver.find_element(By.ID, j_data['radio_buttons']['product_missing_ID']
                        .format(j_data['product_missing']))
    driver.execute_script("arguments[0].click();", radio_click)

tSF.button_click('buttonNext', driver)


tSF.button_star_click('page06', j_data['button_star_XPATH'], tSF.ratings_generator, j_data['survey_stars'],
                                                                            driver, rating_in=j_data['survey_rating'])

tSF.button_click('buttonNext', driver)

tSF.button_star_click('page07', j_data['button_star_XPATH'], tSF.ratings_generator, j_data['survey_stars'],
                                                                            driver, rating_in=j_data['survey_rating'])

tSF.button_click('buttonNext', driver)

tSF.button_star_click('page08', j_data['button_star_XPATH'], tSF.ratings_generator, j_data['survey_stars'],
                                                                            driver, rating_in=j_data['survey_rating'])

yes_no_choices_list = [1, 2]
yes_no_choices = choices(yes_no_choices_list, weights=(25, 50))[0]

if yes_no_choices == 1:

    radio_click = driver.find_element(By.ID, "id")
    driver.execute_script("arguments[0].click();", radio_click)

    radio_click = driver.find_element(By.ID, "id")
    driver.execute_script("arguments[0].click();", radio_click)

    radio_click = driver.find_element(By.ID, "id")
    driver.execute_script("arguments[0].click();", radio_click)

else:

    radio_click = driver.find_element(By.ID, "id")
    driver.execute_script("arguments[0].click();", radio_click)

tSF.button_click('buttonNext', driver)

tSF.button_star_click('page09', j_data['button_star_XPATH'], tSF.ratings_generator, j_data['survey_stars'],
                                                                            driver, rating_in=j_data['survey_rating'])

radio_click = driver.find_element(By.ID, "id")
driver.execute_script("arguments[0].click();", radio_click)

tSF.button_click('buttonNext', driver)

tSF.button_star_click('page10', j_data['button_star_XPATH'], tSF.ratings_generator, choice([9,10]), driver,
                                                                                    rating_in=j_data['survey_rating'])

tSF.button_click('buttonNext', driver)

dropdown_click = driver.find_element(By.XPATH, j_data['dropdown_options']['purchase_price_XPATH']
                        .format(choices(list(j_data['dropdown_options']['purchase_price_dict']
                        .keys()), weights=list(j_data['dropdown_options']['purchase_price_dict'].values()))[0]))
driver.execute_script("arguments[0].click();", dropdown_click)

purchase_date_days_from_run = math.floor((bills_numbers_tuple[1] - bills_numbers_tuple[0])
                                                                        / j_data['shop_nr'][shop_nr]['bill_daily'])

purchase_date = date.today() - timedelta(days=purchase_date_days_from_run)

purchase_date_converted_to_survey_format = datetime.strftime(datetime.combine(purchase_date, datetime.min.time()),
                                                                                        j_data['date_format_survey'])

driver.find_element(By.ID, "id_").send_keys(purchase_date_converted_to_survey_format)

dropdown_click = driver.find_element(By.XPATH, j_data['dropdown_options']['purchase_time_XPATH']
                       .format(choices(list(j_data['dropdown_options']['purchase_time_dict']
                       .keys()), weights=list(j_data['dropdown_options']['purchase_time_dict'].values()))[0]))
driver.execute_script("arguments[0].click();", dropdown_click)


dropdown_click = driver.find_element(By.XPATH, j_data['dropdown_options']['purchase_frequency_XPATH']
                       .format(choices(list(j_data['dropdown_options']['purchase_frequency_dict']
                       .keys()), weights=list(j_data['dropdown_options']['purchase_frequency_dict'].values()))[0]))
driver.execute_script("arguments[0].click();", dropdown_click)

radio_click = driver.find_element(By.ID, "id_{}".format(choice(list(j_data['gender'].values()))))
driver.execute_script("arguments[0].click();", radio_click)

tSF.button_click('buttonNext', driver)

radio_click = driver.find_element(By.ID, "id_{}".format(choice([0, 1])))
driver.execute_script("arguments[0].click();", radio_click)

time.sleep(2)

tSF.button_click('buttonFinish', driver)

delete_text_before_data = datetime.strptime(j_data['last_run_date'], j_data['date_format']).date() - timedelta(days=
                                                                                j_data['remove_used_answer_after_days'])

keys_to_remove = []

for keys, values in j_data['shop_nr'][shop_nr]['text_answer_used_rating_satisfaction'].items():
    if delete_text_before_data > datetime.strptime(values, '%Y-%m-%d').date():
        keys_to_remove.append(keys)

for key in keys_to_remove:
    j_data['shop_nr'][shop_nr]['text_answer_used_rating_satisfaction'].pop(key)

j_data['last_run_date'] = str(date.today())
j_data['remove_used_answer_last_date'] = str(date.today())
j_data['shop_nr'][shop_nr]['bill_last_nr'] = bills_numbers_tuple[1]
j_data['shop_nr'][shop_nr]['surveys_filled_all'] += 1
j_data['shop_nr'][shop_nr]['surveys_filled_daily'] += 1

with open('topSurveyData.json', 'r+', encoding="utf-8") as j_file:
    j_file.seek(0)
    json.dump(j_data, j_file, indent=4)
    j_file.truncate()

driver.quit()
