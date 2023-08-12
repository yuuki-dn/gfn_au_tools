from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random, re, time, string, datetime, json
from colorama import Fore,Style
from os import system

with open("config.json", "r") as f:
    config = json.loads(f.read())
    verbose = config["verbose"]
    f.close()

class _card():
    def __init__(self) -> None:
        self.list_card = []
        self.current_card = -1
        self.add()
    
    def add(self):
        with open("card.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                split = line.strip().split("|")
                if len(split) == 4:
                    self.list_card.append({
                        "no": split[0],
                        "month": split[1],
                        "year": split[2] if len(split[2]) == 4 else "20" + split[2],
                        "cvv": split[3],
                        "state": "unchecked"
                    })
                elif len(split) == 5 and split[4] in ["unchecked", "allowed"]:
                    self.list_card.append({
                        "no": split[0],
                        "month": split[1],
                        "year": split[2] if len(split[2]) == 4 else "20" + split[2],
                        "cvv": split[3],
                        "state": split[4]
                    })
            f.close()
    
    def get(self):
        self.current_card += 1
        if self.current_card == len(self.list_card):
            print("Hết thẻ")
            exit()
        return self.list_card[self.current_card]
    
    def state(self, state):
        self.list_card[self.current_card]["state"] = state
    
    def save(self):
        with open("card.txt", "w", encoding="utf-8") as f:
            for card in self.list_card:
                f.write(f"{card['no']}|{card['month']}|{card['year']}|{card['cvv']}|{card['state']}\n")
            f.close()

card = _card()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--lang=jp')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
chrome_options.add_argument('window-size=800,600')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
prefs = {
        #  'profile.managed_default_content_settings.images': 2,
         'profile.managed_default_content_settings.media_stream': 2,
         'profile.managed_default_content_settings.media': 2
}
chrome_options.add_experimental_option('prefs', prefs)

class instance:
    def __init__(self, instanceid) -> None:
        self.instancename = f"{Fore.BLUE}[Instance {instanceid}]{Style.RESET_ALL}"
        self.isworking = True
        self.__failattempt__ = 0
        self.driver = webdriver.Chrome(options=chrome_options)
        self.email = None
        self.password = None
        self.create_account(self.driver)
        self.main()

    def reset_session(self):
        self.driver.quit()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.create_account(self.driver)
    
    def create_account(self, session):
        self.email = f"{''.join(random.sample(string.ascii_lowercase + string.digits, 6))}_{''.join(random.sample(string.ascii_lowercase + string.digits, 8))}@mailforspam.com"
        self.password = ["A","b","1","@"] + list(random.sample(string.ascii_letters + "@#$%&!~" + string.digits, 8))
        random.shuffle(self.password)
        self.password = "".join(self.password)
        if verbose: print(self.instancename, Fore.YELLOW, f"Đang thử với {self.email} | {self.password}", Fore.RED)
        session.get("https://connect.auone.jp/net/vw/cca_eu_net/cca?ID=ENET0510")
        # Step 1
        if verbose: print(self.instancename, Fore.YELLOW, "Đăng kí bước 1...", Fore.RED)
        session.find_element(By.XPATH, '//input[@id="wowAliasIdEmail"]').send_keys(self.email)
        session.find_element(By.XPATH, '//button[@class="idk-button-primary idk-margin"]').click()
        # Step 2
        WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "confirmcode")))
        if verbose: print(self.instancename, Fore.YELLOW, "Đăng kí bước 2...", Fore.RED)
        # Mở mailforspam.com lấy code
        time.sleep(6)
        session.execute_script(f'window.open("https://mailforspam.com/mail/{self.email.split("@")[0]}/1","_blank");')
        session.switch_to.window(session.window_handles[1])
        mail_content = session.find_element(By.XPATH, '//p[@id="messagebody"]').text
        code = re.search(r'\b\d{6}\b', mail_content).group()
        if verbose: print(self.instancename, Fore.YELLOW, "Lấy OTP thành công!", Fore.RED)
        session.close()
        session.switch_to.window(session.window_handles[0])
        session.find_element(By.XPATH, '//input[@id="confirmcode"]').send_keys(code)
        session.find_element(By.XPATH, '//button[@class="idk-button-primary idk-margin"]').click()
        # Step 3
        WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "password")))
        if verbose: print(self.instancename, Fore.YELLOW, "Đăng kí bước 3...", Fore.RED)
        session.find_element(By.XPATH, '//input[@id="password"]').send_keys(self.password)
        session.find_element(By.XPATH, '//input[@id="csBirthdayYYYY"]').send_keys(str(random.randint(1980,2000)))
        dropdown = session.find_element(By.XPATH, '//select[@id="csBirthdayMM" and @name="csBirthdayMM"]')
        dropdown.find_element(By.XPATH, '//option[@value="{}"]'.format(str(random.randint(1,12)).zfill(2))).click()
        session.find_element(By.XPATH, '//input[@id="csBirthdayDD"]').send_keys(str(random.randint(10,28)))
        session.find_element(By.XPATH, '//label[@class="idk-text-16-bold-no-lh radio-gender" and @data-bind="d_eMail1"]').click()
        session.find_element(By.XPATH, '//button[@name="btn_cmp" and @id="btn_cmp"]').click()
        if verbose: print(self.instancename, Fore.YELLOW, "Đăng kí hoàn tất", Fore.RED)
        # Thêm thông tin & địa chỉ
        WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "returnBtnArea")))
        if verbose: print(self.instancename, Fore.YELLOW, "Đang thêm địa chỉ...", Fore.RED)
        session.get("https://id.auone.jp/id/userinfo/cinfo_set.html")
        session.find_element(By.XPATH, '//input[@name="nameKanji" and @id="nameKanji"]').send_keys(f"{''.join(random.sample(string.ascii_lowercase + string.digits, 3))} {''.join(random.sample(string.ascii_lowercase + string.digits, 3))}")
        session.find_element(By.XPATH, '//input[@name="nameKana" and @id="nameKana"]').send_keys("フリ ガナ")
        session.find_element(By.XPATH, '//input[@name="zip" and @id="zip"]').send_keys("1040001")
        session.find_element(By.XPATH, '//input[@name="addr1" and @id="addr1"]').send_keys(f"{''.join(random.sample(string.ascii_lowercase + string.digits, 6))}")
        session.find_element(By.XPATH, '//input[@name="tel" and @id="tel"]').send_keys(f"09{random.randint(10000000,99999999)}")
        session.find_element(By.XPATH, '//div[@class="btn_box"]/a[2]/img').click()
        session.find_element(By.XPATH, '//div[@class="btn_box"]/a[2]/img').click()
        # Xác nhận mật khẩu
        WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "auonePwd")))
        session.find_element(By.XPATH, '//input[@name="auonePwd" and @id="auonePwd"]').send_keys(self.password)
        session.find_element(By.XPATH, '//button[@id="btn_pwdLogin" and @name="btn_login"]').click()
        if verbose: print(self.instancename, Fore.YELLOW, "Thêm địa chỉ hoàn tất", Fore.RED)
        self.__failattempt__ = 3

    def add_card(self, session, card):
        session.get("https://id.auone.jp/id/userinfo/creditcard_set.html")
        if verbose: print(self.instancename, Fore.YELLOW, f"Đang thử thêm thẻ {card['no']}|{card['month']}|{card['year']}|{card['cvv']}", Fore.RED)
        try:
            WebDriverWait(session, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-orange")))
            session.find_element(By.XPATH, '//div[@id="btnarea"]/a[@href="javascript:void(0);"]').click()
        except: pass
        WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "cardNo")))
        session.find_element(By.XPATH, '//input[@id="cardNumber" and @name="card_num"]').send_keys(card["no"])
        dropdown = session.find_element(By.XPATH, '//select[@id="cardExpirationMonth" and @name="limitMonth"]')
        dropdown.find_element(By.XPATH, '//option[@value="{}"]'.format(card["month"])).click()
        dropdown = session.find_element(By.XPATH, '//select[@id="cardExpirationYear" and @name="limitYear"]')
        dropdown.find_element(By.XPATH, '//option[@value="{}"]'.format(card["year"])).click()
        session.find_element(By.XPATH, '//input[@id="securityCode" and @name="securityCode"]').send_keys(card["cvv"])
        session.find_element(By.XPATH, '//div[@class="btn_box"]/a[2]/img').click()
        session.find_element(By.XPATH, '//div[@class="btn_box"]/a[2]/img').click()
        try:
            pass
        except:
            self.__failattempt__ -= 1
            return {
                "status": "error",
                "message": session.find_element(By.XPATH, '//div[@id="error"]').text
            }
        
    def check_basic(self, card):
        session = self.driver
        session.get("https://pass.auone.jp/gate/allocate?rid=SP5G2010SGFN&ru=https%3A%2F%2Fmy.au.com%2Frd%2Fgfbentry?nm=1&pru=1")
        session.find_element(By.XPATH, '//div[@class="p-w-fill u-center p-bg--white u-pvxxl"]/span[@class="p-shiny__btn p-bg--white"]/a').click()
        session.find_element(By.XPATH, '//div[@id="btn-area"]/div[@class="douibtn"]/a[1]').click()
        if verbose: print(self.instancename, Fore.YELLOW, "Đang đăng kí au Smart Pass...", Fore.RED)
        # Add thẻ
        WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "creditNo")))
        session.find_element(By.XPATH, '//input[@name="creditNo" and @id="creditNo"]').send_keys(card["no"])
        dropdown = session.find_element(By.XPATH, '//select[@id="creditEffTimlmtMonth" and @name="creditEffTimlmtMonth"]')
        dropdown.find_element(By.XPATH, '//option[@value="{}"]'.format(card["month"])).click()
        dropdown = session.find_element(By.XPATH, '//select[@id="creditEffTimlmtYear" and @name="creditEffTimlmtYear"]')
        dropdown.find_element(By.XPATH, '//option[@value="{}"]'.format(card["year"])).click()
        session.find_element(By.XPATH, '//input[@name="secrtyCd" and @id="secrtyCd"]').send_keys(card["cvv"])
        session.find_element(By.XPATH, '//a[@id="btn_register" and @name="btn_register"]').click()
        if verbose: print(self.instancename, Fore.YELLOW, "Đang xác thực thẻ...", Fore.RED)
        # Kích hoạt GFN
        try:
            WebDriverWait(session, 20).until(EC.url_to_be("https://pass.auone.jp/permission/app/premium"))
            if verbose: print(self.instancename, Fore.YELLOW, "Xác thực thành công. Đang kích hoạt Geforce Now...", Fore.RED)
            WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "btn-area")))
            session.find_element(By.XPATH, '//div[@id="btn-area"]/div[@class="douibtn"]/a').click()
            WebDriverWait(session, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "label-agree")))
            session.find_element(By.XPATH, '//input[@name="agree" and @value="agree" and @class="checkbox-agree"]').click()
            session.find_element(By.XPATH, '//div[@class="btns"]/button[@class="btn-primary js-btn-agree js-btn-modal"]').click()
            session.find_element(By.XPATH, '//div[@class="btns-primary"]/button[@class="btn-primary"]').click()
            WebDriverWait(session, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
            if verbose: print(self.instancename, Fore.YELLOW, "Kích hoạt thành công", Fore.RED)
            session.get("https://id.auone.jp/id/userinfo/creditcard_set.html")
            if verbose: print(self.instancename, Fore.YELLOW, "Đang gỡ thẻ...", Fore.RED)
            WebDriverWait(session, 30).until(EC.presence_of_element_located((By.ID, "btnarea")))
            session.find_element(By.XPATH, '//div[@id="btnarea"]/a[@href="javascript:void(0);"]').click()
            WebDriverWait(session, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "creditcard_info_container")))
            session.find_element(By.XPATH, '//div[@class="creditcard_info_container"]/a[@class="btn_creditcard_info_delete"]').click()
            WebDriverWait(session, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "btn_box")))
            session.find_element(By.XPATH, '//div[@class="btn_box"]/a[@href="javascript:void(0);"]').click()
            WebDriverWait(session, 30).until(EC.url_to_be("https://id.auone.jp/id/userinfo/creditcarddel_comp.html"))
            if verbose: print(self.instancename, Fore.YELLOW, "Gỡ thẻ thành công", Fore.RED)

            self.reset_session()

            return {
                "status": "success",
                "email": self.email,
                "password": self.password,
            }
        
        except:
            try:
                error_line = session.find_element(By.XPATH, "//*[contains(text(), 'MPLE')]").text
                self.__failattempt__ -= 1
                if self.__failattempt__ == 0:
                    self.reset_session()
                return {
                    "status": "error",
                    "message": error_line
                }
            except:
                self.__failattempt__ -= 1
                if self.__failattempt__ == 0:
                    self.reset_session()
                return {
                    "status": "error",
                    "message": "3ds"
                }
    
    def main(self):
        while True:
            check_card = card.get()
            if check_card["state"] != "success":
                print(self.instancename, f"Đang kiểm tra thẻ {check_card['no']}")
                result = self.check_basic(check_card)
                if result["status"] == "success":
                    print(self.instancename, f"Thẻ {check_card['no']} hợp lệ")
                    card.state("success")
                    with open("output.txt","a") as File:
                        File.write(f'{result["email"]} | {result["password"]} | {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}\n')
                        File.close()
                else:
                    print(self.instancename, f"Thẻ {check_card['no']} không hợp lệ | {result['message']}")
                    card.state(result["message"])
            card.save()

inst = instance("instance1")