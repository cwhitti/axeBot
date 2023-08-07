from class_lookup import *
from classes import name_list
import time

for subject in name_list:
    url_list = get_urls(subject, "")
    print(subject, len(url_list))
    time.sleep(5)
