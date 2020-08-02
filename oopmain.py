from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from dotenv import load_dotenv
import sys
import time
load_dotenv()

PATH = 'C:\Program Files (x86)\chromedriver.exe'

driver = webdriver.Chrome(PATH)

class User:
    def __init__(self):
        user_choice = input("Do you want to: \n1. write your credentials here \n2.use .env file? \nwrite number 1 or 2: ")

        if user_choice.isdigit() and 0 < int(user_choice) < 3:
            user_choice = int(user_choice)

        else:
            self.closing_program()

        if user_choice == 1:

            self.EMAIL_CW = input("write your codewars email: ")
            if '@' not in self.EMAIL_CW:
                self.closing_program()
            self.USER_CW = input("write your codewars username: ")
            self.PASSW_CW = input("write your codewars password: ")

            self.EMAIL_GH = input("write your github email: ")
            if '@' not in self.EMAIL_GH:
                self.closing_program()
            self.USER_GH = input("write your github username: ")
            self.PASSW_GH = input("write your github password: ")
            self.REPO_NAME = input("write your exact github repo name: ")

        else:
            self.EMAIL_CW = os.getenv('codewars_email')
            self.USER_CW = os.getenv('codewars_username')
            self.PASSW_CW = os.getenv('codewars_password')

            self.EMAIL_GH = os.getenv('github_email')
            self.USER_GH = os.getenv('github_username')
            self.PASSW_GH = os.getenv('github_password')
            self.REPO_NAME = os.getenv('github_repository_name')

    #if something is not right, method which closes active program
    def closing_program(self):
        print("\nwrong input. closing program.")
        time.sleep(3)
        sys.exit()

    def site_opening(self, website):
        driver.get(website)

    def codewars_github_login(self):
        github_login_icon = driver.find_element_by_class_name('btn')
        github_login_icon.click()
        self.github_login()

    def codewars_normal_login(self):
        #finding email field and pasting yours into
        email_typein = driver.find_element_by_id('user_email')
        email_typein.send_keys(self.EMAIL_CW)

        #finding password field and pasting yours into
        passw_typein = driver.find_element_by_id('user_password')
        passw_typein.send_keys(self.PASSW_CW)

        email_typein.send_keys(Keys.RETURN)

    def codewars_copying(self):
        #going to the user solutions
        driver.get('https://www.codewars.com/users/' + self.USER_CW + '/completed_solutions')

        #copying first code in solutions
        program_code = driver.find_element_by_class_name('mb-5px')
        program_split_by_nl = program_code.text.split('\n')

        #getting full name of kata
        kata_kyu = driver.find_element_by_class_name('item-title')
        kata_prep = kata_kyu.text.split('\n')
        kata_name_for_github = f'[{kata_prep[0]}] {kata_prep[1]}.py'

        return [kata_name_for_github, program_split_by_nl]

    def github_login(self):
        #finding email field and pasting yours into
        email_typein = driver.find_element_by_id('login_field')
        email_typein.send_keys(self.EMAIL_GH)

        #finding password field and pasting yours into
        passw_typein = driver.find_element_by_id('password')
        passw_typein.send_keys(self.PASSW_CW)
        
        email_typein.send_keys(Keys.RETURN)

    def github_code_submission(self, kata_name, program_code):
        #going to user repo
        driver.get('https://github.com/' + self.USER_GH + '/' + self.REPO_NAME + '/new/master')

        #pasting kata name
        filename = driver.find_element_by_name('filename')
        filename.send_keys(kata_name)

        #pasting code inside github
        code_area = driver.find_element_by_class_name('CodeMirror-code')
        #code_area.send_keys(programm)
        #ActionChains(driver).move_to_element(code_area).click(code_area)
        for i in program_code:
            code_area.send_keys(i)
            code_area.send_keys('\n')

        #submitting code to repo
        commit_button = driver.find_element_by_id('submit-file')
        commit_button.click()

test = User()

test.site_opening('https://www.codewars.com/users/sign_in') #site opening

try:
    codewars_login_type = int(input("Do you login to codewars with: \n1. email/password\n2. github\nWrite number (1 or 2): ")) #checking if user if loging in with github or not
except:
    test.closing_program()

if codewars_login_type == 1:
    test.codewars_normal_login()
    codewars_data = test.codewars_copying()
    
else:
    test.codewars_github_login()
    codewars_data = test.codewars_copying()


test.site_opening('https://github.com/login')
if codewars_login_type == 1:
    test.github_login()
test.github_code_submission(codewars_data[0], codewars_data[1])