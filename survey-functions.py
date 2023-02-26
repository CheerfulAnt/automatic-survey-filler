import json
from datetime import datetime, date
from random import randrange, uniform, shuffle, choice
from math import ceil
from selenium.webdriver.common.by import By

def button_click(button_id_in, driver_in):
    button_in = driver_in.find_element(By.ID, button_id_in)
    driver_in.execute_script("arguments[0].click();", button_in)

def bill_nr_generator(last_run_date_in, date_format_in, days_back_in, purchase_days_back_in, bill_last_nr_in,                                                                                                       bill_daily_in):

    today_minus_last_run_date = date.today() - datetime.strptime(last_run_date_in, date_format_in).date()
    days_from_last_run = (today_minus_last_run_date).days

    bill_current_nr = bill_last_nr_in + (days_from_last_run * bill_daily_in)

    bill_current_nr_range_stop = bill_current_nr - ( days_back_in * bill_daily_in)

    bill_current_nr_range_start = bill_current_nr - (purchase_days_back_in * bill_daily_in)

    bill_random_nr = randrange(bill_current_nr_range_start, bill_current_nr_range_stop)

    bills_numbers_tuple = (bill_random_nr, bill_current_nr)

    return bills_numbers_tuple

def ratings_generator(elements_qty_in, stars_qty_in, rating_in='very_good'):

    if stars_qty_in < 5:
        return 1

    ratings_list_in = []

    if rating_in == 'max':
        ratings_list_in = [stars_qty_in for _ in range(elements_qty_in) ]

    elif rating_in == 'very_good':
        for x in range(elements_qty_in):
            if x < ceil(round(uniform(0.6, 0.9), 1) * elements_qty_in ):
                ratings_list_in.append(stars_qty_in)
            else:
                ratings_list_in.append(stars_qty_in - 1)

    elif rating_in == 'reasonably_well':
        ratings_reasonably_well_in = ceil((stars_qty_in / 2))
        ratings_list_in  = [randrange(ratings_reasonably_well_in, stars_qty_in) for _ in range(elements_qty_in)]

    elif rating_in == 'hopeless':
        ratings_hopeless_in = ceil((stars_qty_in / 2))
        ratings_list_in_in = [randrange(1, ratings_hopeless_in) for _ in range(elements_qty_in)]

    shuffle(ratings_list_in)

    rate_min_in = min(ratings_list_in)
    rate_max_in = max(ratings_list_in)

    rate_min_index_in = ratings_list_in.index(rate_min_in)
    rate_max_index_in = ratings_list_in.index(rate_max_in)

    if rate_max_index_in:
        ratings_list_in[rate_min_index_in], ratings_list_in[rate_max_index_in] =\
                                        ratings_list_in[rate_max_index_in], ratings_list_in[rate_min_index_in]

    return ratings_list_in

def button_star_click(page_in, button_star_dictionary_in, ratings_generator_in, stars_qty_in, driver_in,
                                                                                            rating_in = 'very_good'):

    button_star_dictionary_in_len = len(button_star_dictionary_in[page_in])

    ratings_list_in = ratings_generator_in(button_star_dictionary_in_len, stars_qty_in, rating_in)

    counter_loop = 0

    for value_in in button_star_dictionary_in[page_in].values():
        button_star_in = driver_in.find_element(By.XPATH, value_in.format(ratings_list_in[counter_loop]))
        driver_in.execute_script("arguments[0].click();", button_star_in)
        counter_loop += 1

def select_comment(j_data_in, shop_nr_in):

    rating_satisfaction_keys_list = list(j_data_in['text_answers']['rating_satisfaction'].keys())

    rating_satisfaction_used_keys_list = list(j_data_in['shop_nr'][shop_nr_in]["text_answer_used_rating_satisfaction"]
                                                                                                                .keys())

    rating_satisfaction_list_for_choice = list(set(rating_satisfaction_keys_list) -
                                                                                set(rating_satisfaction_used_keys_list))

    rating_satisfaction_choice = choice(rating_satisfaction_list_for_choice)

    if rating_satisfaction_choice != '1':

        new_dict = {rating_satisfaction_choice : str(date.today())}

        with open('topSurveyData.json', 'r+', encoding="utf-8") as j_file:
            j_data_in['shop_nr'][shop_nr_in]['text_answer_used_rating_satisfaction'].update(new_dict)
            j_file.seek(0)
            json.dump(j_data_in, j_file, indent=4)
            j_file.truncate()

    return j_data_in['text_answers']['rating_satisfaction'][rating_satisfaction_choice]
