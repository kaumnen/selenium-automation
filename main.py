from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from dotenv import load_dotenv
load_dotenv()


PATH = 'C:\Program Files (x86)\chromedriver.exe'

EMAIL_CW = os.getenv('codewars_email')
USER_CW = os.getenv('codewars_username')
PASSW_CW = os.getenv('codewars_password')

EMAIL_GH = os.getenv('github_email')
USER_GH = os.getenv('github_username')
PASSW_GH = os.getenv('github_password')
REPO_NAME = os.getenv('github_repository_name')

driver = webdriver.Chrome(PATH)

##############
### singning in CODEWARS
##############

#opening signin page
driver.get('https://www.codewars.com/users/sign_in')

#finding email field and pasting yours into
email_typein = driver.find_element_by_id('user_email')
email_typein.send_keys(EMAIL_CW)

#finding password field and pasting yours into
passw_typein = driver.find_element_by_id('user_password')
passw_typein.send_keys(PASSW_CW)

email_typein.send_keys(Keys.RETURN)

#going to the user solutions
driver.get('https://www.codewars.com/users/' + USER_CW + '/completed_solutions')

#copying first code in solutions
program_code = driver.find_element_by_class_name('mb-5px')
programm = program_code.text
programm_split_by_nl = programm.split('\n')

#getting full name of kata
kata_kyu = driver.find_element_by_class_name('inner-small-hex')
kata_text = driver.find_element_by_link_text('String repeat')

kata_name_for_github = f'[{kata_kyu.text}] {kata_text.text}.py'

##############
### singning in GITHUB
##############

#opening github
driver.get('https://github.com/login')

#finding email field and pasting yours into
email_typein = driver.find_element_by_id('login_field')
email_typein.send_keys(EMAIL_GH)

#finding password field and pasting yours into
passw_typein = driver.find_element_by_id('password')
passw_typein.send_keys(PASSW_CW)

email_typein.send_keys(Keys.RETURN)

#going to user repo
driver.get('https://github.com/' + USER_GH + '/' + REPO_NAME + '/new/master')

#pasting kata name
filename = driver.find_element_by_name('filename')
filename.send_keys(kata_name_for_github)

#pasting code inside github
code_area = driver.find_element_by_class_name('CodeMirror-code')
#code_area.send_keys(programm)
#ActionChains(driver).move_to_element(code_area).click(code_area)
for i in programm_split_by_nl:
    code_area.send_keys(i)
    code_area.send_keys('\n')

#submitting code to repo
commit_button = driver.find_element_by_id('submit-file')
commit_button.click()

print("thats it, thanks for using me! :)")

##############
### testing
##############

#driver.get("https://www.pastebin.com")
#textt = driver.find_element_by_id('postform-text')
#for i in programm_test:
#    textt.send_keys(i)
#    textt.send_keys('\n')