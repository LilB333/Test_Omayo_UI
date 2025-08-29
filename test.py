import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

#Настройки Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox") #без этой настройки страница виснет на подгрузке
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service(ChromeDriverManager().install())

#Инициализируем драйвер
driver = webdriver.Chrome(service=service, options=chrome_options)

#Устанавливаем таймаут для загрузки страницы
driver.set_page_load_timeout(3)

base_url = 'https://omayo.blogspot.com/'

#Открываем сайт с обработкой таймаута
try:
    driver.get(base_url)
except Exception as e:
    driver.execute_script("window.stop();")  # Останавливаем загрузку
driver.maximize_window()

#Создаем ActionChains
actions = ActionChains(driver)

#Создаем переменную time_sleep для удобства проверки работы автотеста
time_sleep = 5

#ПРОВЕРЯЕМ ЧЕК-БОКС ORANGE
checkbox_element_1 = driver.find_element(By.XPATH, "//input[@id='checkbox1' and @value='orange']")
#Скроллим чуть чекбокса
driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});"  
        "window.scrollBy(0, 50);",  #Опускаем на 50px вниз
        checkbox_element_1
)
assert checkbox_element_1.is_selected()
print('Чек-бокс Orange заполнен')

time.sleep(time_sleep)

#ЗАПОЛНЯЕМ ЧЕК-БОКС BLUE
checkbox_element_2 = driver.find_element(By.XPATH, "//input[@id='checkbox2' and @value='blue']")
checkbox_element_2.click()
assert checkbox_element_2.is_selected()
print('Чек-бокс Blue заполнен')

time.sleep(time_sleep)

#КЛИКАЕМ НА ССЫЛКУ Open a popup window
link_element =  driver.find_element(By.XPATH, "//a[contains(text(), 'Open a popup window')]")
base_window = driver.current_window_handle
windows_before_click = driver.window_handles
link_element.click()

time.sleep(time_sleep)

#ПРОВЕРЯЕМ ОТОБРАЖЕНИЕ НОВОГО ОКНА
WebDriverWait(driver, 10).until(lambda x: len(x.window_handles) > len(windows_before_click))
current_windows = driver.window_handles
new_window = current_windows[-1]
#Переключаемся на новое окно
driver.switch_to.window(new_window)
assert driver.current_url != base_url
print("Открыто новое окно")

time.sleep(time_sleep)

#ЗАКРЫВАЕМ ОКНО
driver.close()
print("Окно закрыто")
#Переключаемся на главное окно
driver.switch_to.window(base_window)

time.sleep(time_sleep)

#КЛИКАЕМ ДВАЖДЫ НА КНОПКУ Double-click
double_click_element = driver.find_element(By.XPATH, "//p[@id='testdoubleclick']")
actions.double_click(double_click_element).perform()
context_menu = driver.find_element(By.XPATH, "//div[@class='dropdown-content show']")
#Скроллим чуть ниже контекстного меню
driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});"  
        "window.scrollBy(0, 50);",  #Опускаем на 50px вниз
        context_menu
)
assert context_menu.is_displayed()
print("Отображается контекстное меню")

time.sleep(time_sleep)

#КЛИКАЕМ НА Gmail В КОНТЕКСТНОМ МЕНЮ
gmail_button = driver.find_element(By.XPATH, "//a[contains(text(),'Gmail')]")
try:
    gmail_button.click()
except Exception as e:
    driver.execute_script("window.stop();")  # Останавливаем загрузку
assert driver.current_url != base_url
print("Открыта новая страница")

time.sleep(time_sleep)

#ВОЗВРАЩАЕМСЯ ОБРАТНО НА СТРАНИЦУ https://omayo.blogspot.com/
try:
    driver.back()
except Exception as e:
    driver.execute_script("window.stop();")  # Останавливаем загрузку
assert driver.current_url == base_url
print("Вернулись обратно на https://omayo.blogspot.com/")

time.sleep(time_sleep)

driver.quit()
