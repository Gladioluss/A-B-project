import csv
import yandexConnect
import Employee
import wx


from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


URL_SKYPE = "https://signup.live.com/signup?lcid=1033&wa=wsignin1.0&rpsnv=13&ct=1641639151&rver=7.1.6819.0&wp=MBI_SSL&wreply=https%3a%2f%2flw.skype.com%2flogin%2foauth%2fproxy%3fclient_id%3d578134%26redirect_uri%3dhttps%253A%252F%252Fweb.skype.com%26source%3dscomnav%26form%3dmicrosoft_registration%26fl%3dphone2&lc=1033&id=293290&mkt=ru-RU&psi=skype&lw=1&cobrandid=2befc4b5-19e3-46e8-8347-77317a16a5a5&client_flight=ReservedFlight33%2CReservedFligh&fl=phone2&lic=1&uaid=fcd3780cd25e4b33a6b479494d96d2d7"
URL_JIRA = "https://id.atlassian.com/signup?continue=https%3A%2F%2Fstart.atlassian.com%2F"
URL_YANDEX_MAIL = "https://passport.yandex.ru/auth/add?retpath=https%3A%2F%2Fconnect.yandex.ru%2Fportal%2Fhome%3Fncrnd%3D631640%26status%3Dok"


def find_element_and_send_keys(driver, xpath, key):
    return driver.find_element_by_xpath(xpath).send_keys(key)


def find_element_and_click(driver, xpath):
    return driver.find_element_by_xpath(xpath).click()


def register_skype_account(driver, URL, employee):
    driver.get(URL)
    sleep(1.5)
    logi = find_element_and_click(driver, '//*[@id="easiSwitch"]')
    sleep(1.5)

    login_btn = find_element_and_send_keys(driver, '//*[@id="MemberName"]', employee.get_emailAddress())
    p = find_element_and_click(driver, '//*[@id="iSignupAction"]')
    sleep(1.5)
    p = find_element_and_send_keys(driver, '//*[@id="PasswordInput"]', employee.get_password())
    l = find_element_and_click(driver, '//*[@id="iSignupAction"]')
    sleep(1.5)
    user_name = employee.get_fullname().split(' ')
    l = find_element_and_send_keys(driver, '//*[@id="LastName"]', user_name[0])
    l = find_element_and_send_keys(driver, '//*[@id="FirstName"]', user_name[1])
    sleep(1.5)
    a = find_element_and_click(driver, '//*[@id="iSignupAction"]')
    sleep(1.5)


def register_jira_account(driver, URL, employee):
    driver.get(URL)
    login = find_element_and_send_keys(driver, '//*[@id="email"]', employee.get_emailAddress())
    employee_fullname = employee.get_fullname()
    fullname = find_element_and_send_keys(driver, '//*[@id="displayName"]', employee_fullname)
    sleep(1.5)
    register = find_element_and_click(driver, '//*[@id="signup-submit"]/span')
    sleep(2)
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')


def register_yandex_mail_account(driver, URL, employee):
    driver.get(URL)
    login = find_element_and_send_keys(driver, '//*[@id="passp-field-login"]', employee.get_emailAddress())
    sleep(1.5)
    next = find_element_and_click(driver, '//*[@id="passp:sign-in"]')
    sleep(1.5)
    password = find_element_and_send_keys(driver, '//*[@id="passp-field-passwd"]', employee.get_password())
    sleep(1.5)
    next = find_element_and_click(driver, '//*[@id="passp:sign-in"]')
    sleep(1.5)
    reg = find_element_and_click(driver, '//*[@id="nb-1"]/body/div/div[1]/form/div[2]/button')

class registerFrame(wx.Frame):

    EMPLOYEE = None

    def __init__(self, parent, title, employee):
        super().__init__(parent, title=title, size=(300, 300))
        global EMPLOYEE
        EMPLOYEE = employee
        panel = wx.Panel(self, wx.ID_ANY)

        btn_yandex = wx.Button(panel, wx.ID_ANY, "Создать аккаунт Яндекс", (10, 20))
        self.Bind(wx.EVT_BUTTON, self.onButtonYandex, id=btn_yandex.GetId())

        btn_skype = wx.Button(panel, wx.ID_ANY, "Создать аккаунт Skype", (10, 50))
        self.Bind(wx.EVT_BUTTON, self.onButtonSkype, id=btn_skype.GetId())

        btn_jira = wx.Button(panel, wx.ID_ANY, "Создать аккаунт Jira", (10, 80))
        self.Bind(wx.EVT_BUTTON, self.onButtonJira, id=btn_jira.GetId())



    def onButtonYandex(self, event):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        register_yandex_mail_account(driver, URL_YANDEX_MAIL, EMPLOYEE)

    def onButtonSkype(self, event):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        register_skype_account(driver, URL_SKYPE, EMPLOYEE)

    def onButtonJira(self, event):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        register_jira_account(driver, URL_JIRA, EMPLOYEE)


def load_user(filename):
    with open(filename, 'r') as csvfile:
        row = csv.DictReader(csvfile)
        for r in row:
            return {
                'fullname': r['fullname'],
                'password': r['password'],
                'emailAddress': r['emailAddress']
            }


def main(filename):
    fullname = load_user(filename)
    employee = Employee.Employee(fullname['fullname'], fullname['password'], fullname['emailAddress'])

    app = wx.App()
    frame = registerFrame(None, title='Регистрация', employee=employee)
    frame.Show()
    frame.Center()
    app.MainLoop()


if __name__ == '__main__':
    yandexConnect.pars_token_and_domain()
    yandexConnect.create_users('passwords.csv')
    main('passwords.csv')
