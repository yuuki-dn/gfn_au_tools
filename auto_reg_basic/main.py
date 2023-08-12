############################################################
#             TOOL TẠO TÀI KHOẢN AU - GFN BASIC            #
#          Phát triển bởi: June8th a.k.a Lumine <3         #
#       Facebook: https://www.facebook.com/june8th.dan/    #
#           Github: https://github.com/june8th-dan         #
############################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random, re, time, string, datetime
from colorama import Fore,Style

# Thiết lập
mail_prefix = "iceb" # Đầu mail, được tự động đặt khi tạo ngẫu nhiên
verbose = True # Hỗ trợ việc theo dõi quá trình tạo

# Thẻ reg
with open("cardlist.txt") as list_card_file:
    list_card = list_card_file.readlines()
    list_card_file.close()
def random_card():
    card = random.sample(list_card,1)[0]
    if verbose: print(Fore.MAGENTA, f"Đang sử dụng thẻ {card}")
    card = card.split("|")
    return {
        "ccNo": card[0],
        "expMonth": card[1],
        "expYear": card[2],
        "cvv": card[3]
    }

# Chế độ
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--lang=jp')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
chrome_options.add_argument('window-size=800,600')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
prefs = {
         # 'profile.managed_default_content_settings.images': 2,
         'profile.managed_default_content_settings.media_stream': 2,
         'profile.managed_default_content_settings.media': 2
}
chrome_options.add_experimental_option('prefs', prefs)

session = None

def create_acc_basic():
    # Email & Mật khẩu ngẫu nhiên
    email = f"{mail_prefix}_{''.join(random.sample(string.ascii_lowercase + string.digits, 8))}@mailforspam.com"
    password = ["A","b","1","@"] + list(random.sample(string.ascii_letters + "@#$%&!()*-+=_`~" + string.digits, 8))
    random.shuffle(password)
    password = "".join(password)
    if verbose: print(Fore.YELLOW, f"Đang thử với {email} | {password}", Fore.RED)
    # Khởi tạo phiên
    global session
    session = webdriver.Chrome(options=chrome_options)
    if verbose: print(Fore.YELLOW, "Selenium đã bắt đầu", Fore.RED)
    # Load trang đăng kí tài khoản
    session.get("https://connect.auone.jp/net/vw/cca_eu_net/cca?ID=ENET0510")
    # Step 1
    if verbose: print(Fore.YELLOW, "Đăng kí bước 1...", Fore.RED)
    session.find_element(By.XPATH, '//input[@id="wowAliasIdEmail"]').send_keys(email)
    session.find_element(By.XPATH, '//button[@class="idk-button-primary idk-margin"]').click()
    # Step 2
    WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "confirmcode")))
    if verbose: print(Fore.YELLOW, "Đăng kí bước 2...", Fore.RED)
    # Mở mailforspam.com lấy code
    time.sleep(15)
    session.execute_script(f'window.open("https://mailforspam.com/mail/{email.split("@")[0]}/1","_blank");')
    session.switch_to.window(session.window_handles[1])
    mail_content = session.find_element(By.XPATH, '//p[@id="messagebody"]').text
    code = re.search(r'\b\d{6}\b', mail_content).group()
    if verbose: print(Fore.YELLOW, "Lấy OTP thành công!", Fore.RED)
    session.close()
    session.switch_to.window(session.window_handles[0])
    session.find_element(By.XPATH, '//input[@id="confirmcode"]').send_keys(code)
    session.find_element(By.XPATH, '//button[@class="idk-button-primary idk-margin"]').click()
    # Step 3
    WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "password")))
    if verbose: print(Fore.YELLOW, "Đăng kí bước 3...", Fore.RED)
    session.find_element(By.XPATH, '//input[@id="password"]').send_keys(password)
    session.find_element(By.XPATH, '//input[@id="csBirthdayYYYY"]').send_keys(str(random.randint(1980,2000)))
    dropdown = session.find_element(By.XPATH, '//select[@id="csBirthdayMM" and @name="csBirthdayMM"]')
    dropdown.find_element(By.XPATH, '//option[@value="{}"]'.format(str(random.randint(1,12)).zfill(2))).click()
    session.find_element(By.XPATH, '//input[@id="csBirthdayDD"]').send_keys(str(random.randint(10,28)))
    session.find_element(By.XPATH, '//label[@class="idk-text-16-bold-no-lh radio-gender" and @data-bind="d_eMail1"]').click()
    session.find_element(By.XPATH, '//button[@name="btn_cmp" and @id="btn_cmp"]').click()
    if verbose: print(Fore.YELLOW, "Đăng kí hoàn tất", Fore.RED)
    # Thêm thông tin & địa chỉ
    WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "returnBtnArea")))
    if verbose: print(Fore.YELLOW, "Đang thêm địa chỉ...", Fore.RED)
    session.get("https://id.auone.jp/id/userinfo/cinfo_set.html")
    session.find_element(By.XPATH, '//input[@name="nameKanji" and @id="nameKanji"]').send_keys("Abc Defgh")
    session.find_element(By.XPATH, '//input[@name="nameKana" and @id="nameKana"]').send_keys("フリ ガナ")
    session.find_element(By.XPATH, '//input[@name="zip" and @id="zip"]').send_keys("1040001")
    session.find_element(By.XPATH, '//input[@name="addr1" and @id="addr1"]').send_keys("123Abcdef")
    session.find_element(By.XPATH, '//input[@name="tel" and @id="tel"]').send_keys("0987654321")
    session.find_element(By.XPATH, '//div[@class="btn_box"]/a[2]/img').click()
    session.find_element(By.XPATH, '//div[@class="btn_box"]/a[2]/img').click()
    # Xác nhận mật khẩu
    WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "auonePwd")))
    session.find_element(By.XPATH, '//input[@name="auonePwd" and @id="auonePwd"]').send_keys(password)
    session.find_element(By.XPATH, '//button[@id="btn_pwdLogin" and @name="btn_login"]').click()
    if verbose: print(Fore.YELLOW, "Thêm địa chỉ hoàn tất", Fore.RED)
    # Kích hoạt basic
    session.get("https://pass.auone.jp/gate/allocate?rid=SP5G2010SGFN&ru=https%3A%2F%2Fmy.au.com%2Frd%2Fgfbentry?nm=1&pru=1")
    session.find_element(By.XPATH, '//div[@class="p-w-fill u-center p-bg--white u-pvxxl"]/span[@class="p-shiny__btn p-bg--white"]/a').click()
    session.find_element(By.XPATH, '//div[@id="btn-area"]/div[@class="douibtn"]/a[1]').click()
    if verbose: print(Fore.YELLOW, "Đang đăng kí au Smart Pass...", Fore.RED)
    # Add thẻ
    WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "creditNo")))
    reg_card = random_card()
    session.find_element(By.XPATH, '//input[@name="creditNo" and @id="creditNo"]').send_keys(reg_card["ccNo"])
    dropdown = session.find_element(By.XPATH, '//select[@id="creditEffTimlmtMonth" and @name="creditEffTimlmtMonth"]')
    dropdown.find_element(By.XPATH, '//option[@value="{}"]'.format(reg_card["expMonth"])).click()
    dropdown = session.find_element(By.XPATH, '//select[@id="creditEffTimlmtYear" and @name="creditEffTimlmtYear"]')
    dropdown.find_element(By.XPATH, '//option[@value="{}"]'.format(reg_card["expYear"])).click()
    session.find_element(By.XPATH, '//input[@name="secrtyCd" and @id="secrtyCd"]').send_keys(reg_card["cvv"])
    session.find_element(By.XPATH, '//a[@id="btn_register" and @name="btn_register"]').click()
    if verbose: print(Fore.YELLOW, "Đang xác thực thẻ...", Fore.RED)
    # Kích hoạt GFN
    WebDriverWait(session, 30).until(EC.url_to_be("https://pass.auone.jp/permission/app/premium"))
    if verbose: print(Fore.YELLOW, "Xác thực thành công. Đang kích hoạt Geforce Now...", Fore.RED)
    WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "btn-area")))
    session.find_element(By.XPATH, '//div[@id="btn-area"]/div[@class="douibtn"]/a').click()
    WebDriverWait(session, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "label-agree")))
    session.find_element(By.XPATH, '//input[@name="agree" and @value="agree" and @class="checkbox-agree"]').click()
    session.find_element(By.XPATH, '//div[@class="btns"]/button[@class="btn-primary js-btn-agree js-btn-modal"]').click()
    session.find_element(By.XPATH, '//div[@class="btns-primary"]/button[@class="btn-primary"]').click()
    WebDriverWait(session, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
    if verbose: print(Fore.YELLOW, "Kích hoạt thành công", Fore.RED)
    ###########
    session.quit()
    return {"email": email, "password": password}


print(Fore.RED,   " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n",
      Fore.YELLOW, "┃          TOOL TẠO TÀI KHOẢN AU - GFN BASIC  v1.5         ┃\n",
      Fore.GREEN,  "┃          Phát triển bởi: June8th a.k.a Lumine <3         ┃\n",
      Fore.CYAN,   "┃       Facebook: https://www.facebook.com/june8th.dan/    ┃\n",
      Fore.BLUE,   "┃           Github: https://github.com/june8th-dan         ┃\n",
      Fore.MAGENTA,"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n",
      Style.RESET_ALL, "\n")

acc_quantity = int(input("Nhập số lượng acc cần tạo: "))
for i in range(acc_quantity):
    print(Fore.RED, f"\n>>> Đang tạo tài khoản thứ {i + 1}")
    try:
        result = create_acc_basic()
    except: continue
    if verbose: print(Style.RESET_ALL, "------------------------------------------------",
          Fore.GREEN, f"\nTạo tài khoản thành công! {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", Style.RESET_ALL,
          "\nTài khoản:", Fore.CYAN, result["email"], Style.RESET_ALL,
          "\nMật khẩu: ", Fore.YELLOW, result["password"], Style.RESET_ALL,
          "\n ------------------------------------------------")
    with open("output.txt","a") as File:
        File.write(f'{result["email"]} | {result["password"]} | {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}\n')
        File.close()