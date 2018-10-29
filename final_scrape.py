import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

import string
from itertools import permutations

from threading import Lock
import multiprocessing
from functools import partial

import os

'''Global variables.'''
result_directory = os.path.join(os.getcwd(), 'files')
wait_time = 10
result = set()

'''
Uniqnames can only have a length from 3 to 8 and only include
lowercase letters. 
'''

def is_student(row):
	'''Check if row is a student.'''
	second = row.find_elements_by_tag_name('td')[1]
	titles = second.find_elements_by_class_name('titles')[0]
	first = 'Student' in titles.text
	second = 'Student Life' not in titles.text
	return first and second

def get_uniqname(row):
	'''Return uniqname of row.'''
	first = row.find_elements_by_tag_name('td')[0]
	uniqname = row.find_elements_by_class_name('uniqname')[0]
	return uniqname.text

def return_uniqnames(table):
	'''Given a table, return the uniqnames.'''
	for row in table:
		if is_student(row):
			result.add(get_uniqname(row))

def add_failed_name(name):
	write_to_file('FAILED' + name, [name])

def get_new_uniqnames(search, checked):
	'''Return a list of uniqnames given a search query.'''
	search = ''.join(search)
	if search in result:
		return
	if search in checked:
		return
	path = os.path.join(os.getcwd(), 'chromedriver.exe')
	browser = webdriver.Chrome(executable_path=path) #replace with .Firefox(), or with the browser of your choice
	url = 'https://mcommunity.umich.edu/#search:' + search

	try:
		browser.get(url) #navigate to the page

		wait(browser, wait_time).until(EC.presence_of_element_located((By.ID, 'peopleContent')))
		people = browser.find_elements_by_id('peopleContent')[0]

		wait(people, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchResults')))
		searchResults = people.find_elements_by_class_name('searchResults')[0]

		wait(searchResults, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
		tbody = searchResults.find_elements_by_tag_name('tbody')[0]

		table = tbody.find_elements_by_tag_name('tr')
		try:
			wait(tbody, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
			table = tbody.find_elements_by_tag_name('tr')
		except selenium.common.exceptions.TimeoutException:
			return

		if len(table) == 0:
			# check for errors
			return
		else:
			return_uniqnames(table)
			write_to_file(search, result)
	except Exception:
		add_failed_name(search)
	finally:
		browser.quit()


def insert_into_result(results):
	result.add(results)

def write_to_file(search, result):
	'''Create file.'''
	f = open(os.path.join(result_directory, '{}.txt'.format(search)), 'w+')
	f.write(str(result))
	f.close()

def get_already_checked(directory):
	'''Get the queries that have already been searched.'''
	filenames = os.listdir(directory)
	ret = set()
	for filename in filenames:
		query = ''
		if 'FAILED' in filename:
			filename = filename.replace('FAILED', '')
		query = filename.split('.')[0]
		ret.add(query)
	return ret

def main():
	'''Run program.'''

	'''This will be the length of the uniqname you want to search!'''
	uniqname_length = 3

	'''Check if the output directory is already made. Create if not already.'''
	if not os.path.isdir(result_directory):
		os.mkdir(result_directory)

	'''Get the searches that have already been checked.'''
	checked = get_already_checked(result_directory)

	'''Generate all the permutations of uniqname searches.'''
	possible = permutations(string.ascii_lowercase, r=uniqname_length)
	with multiprocessing.Pool() as pool:
		pool.map(partial(get_new_uniqnames, checked=checked), possible)

main()
