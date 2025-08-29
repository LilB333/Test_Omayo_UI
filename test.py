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

url = 'https://omayo.blogspot.com/'

#Открываем сайт с обработкой таймаута
try:
    driver.get(url)
except Exception as e:
    driver.execute_script("window.stop();")  # Останавливаем загрузку

# Создаем ActionChains
actions = ActionChains(driver)

#ПРОВЕРЯЕМ ЧЕК-БОКС ORANGE
checkbox = driver.find_element(By.XPATH, "//h2[@class='title' and contains(text(),'By Default Selected Check Box option')]")
checkbox_element = driver.find_element(By.XPATH, "//input[@id='checkbox1' and @value='orange']")
assert checkbox_element.is_selected()
print('Чек-бокс Orange заполнен')

#ЗАПОЛНЯЕМ ЧЕК-БОКС BLUE
checkbox_element_2 = driver.find_element(By.XPATH, "//input[@id='checkbox2' and @value='blue']")
checkbox_element_2.click()
assert checkbox_element_2.is_selected()
print('Чек-бокс Blue заполнен')

#КЛИКАЕМ НА ССЫЛКУ Open a popup window
link_element =  driver.find_element(By.XPATH, "//a[contains(text(), 'Open a popup window')]")
base_window = driver.current_window_handle
windows_before_click = driver.window_handles
link_element.click()

#ПРОВЕРЯЕМ ОТОБРАЖЕНИЕ НОВОГО ОКНА
WebDriverWait(driver, 10).until(lambda x: len(x.window_handles) > len(windows_before_click))
current_windows = driver.window_handles
new_window = current_windows[-1]
#Переключаемся на новое окно
driver.switch_to.window(new_window)
assert driver.current_url != url
print("Открыто новое окно")

#ЗАКРЫВАЕМ ОКНО
driver.close()
print("Окно закрыто")
#Переключаемся на главное окно
driver.switch_to.window(base_window)

#КЛИКАЕМ ДВАЖДЫ НА КНОПКУ Double-click
double_click_element = driver.find_element(By.XPATH, "//p[@id='testdoubleclick']")
actions.double_click(double_click_element).perform()
assert driver.find_element(By.XPATH, "//div[@class='dropdown-content show']")
print("Отображается контекстное меню")

#КЛИКАЕМ НА Gmail В КОНТЕКСТНОМ МЕНЮ
gmail_button = driver.find_element(By.XPATH, "//a[contains(text(),'Gmail')]")
try:
    gmail_button.click()
except Exception as e:
    driver.execute_script("window.stop();")  # Останавливаем загрузку
assert driver.current_url != url
print("Открыта новая страница")

#ВОЗВРАЩАЕМСЯ ОБРАТНО НА СТРАНИЦУ https://omayo.blogspot.com/
try:
    driver.back()
except Exception as e:
    driver.execute_script("window.stop();")  # Останавливаем загрузку
print("Вернулись обратно на https://omayo.blogspot.com/")
driver.quit()
