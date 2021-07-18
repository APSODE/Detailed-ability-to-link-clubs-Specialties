from Class.USER_JSON_RW.RW_JSON import READ_WRITE
from selenium import webdriver
import discord
import time
import datetime
import json

CONFIG_DIR = ".\\Class\\COVID_FINDER\\COVID_FINDER_CONFIG\\COVID_FINDER_CONFIG.json"

class INTERNAL_FUNC:
    def Del(Second):
        time.sleep(Second)
        return Second

    def Driver_Get_X_Path(XPath, DRIVER):
        time.sleep(1)
        driver = DRIVER
        dgxp = driver.find_element_by_xpath(XPath)
        return dgxp
    def Driver_Get_Class(ClassName, driver):
        try:
            dgc = driver.find_element_by_class_name(ClassName)
            return dgc
        except:
            del_sec = 1.5
            time.sleep(del_sec + 5.5) #로딩이 느려 예외가 발생했을 경우 5초 delay를 주어 대기후 다시 코드 시작
            dgc = driver.find_element_by_class_name(ClassName)
            return dgc

class COVID:
    def TIME_CHECK():
        TODAY = datetime.datetime.today()
        TD_HOUR = TODAY.hour
        TD_MIN = TODAY.minute
        TD_SEC = TODAY.second
        READ_CONFIG_DATA = READ_WRITE.READ_JSON(CONFIG_DIR)
        BASETME_HOUR = READ_CONFIG_DATA["TIME_CONFIG"]["BASETIME_HOUR"]
        BASETME_MIN = READ_CONFIG_DATA["TIME_CONFIG"]["BASETIME_MIN"]
        BASETME_SEC = READ_CONFIG_DATA["TIME_CONFIG"]["BASETIME_SEC"]
        #if BASETME_HOUR != NULL:
        if (TD_MIN % BASETME_MIN) == 0:
            if TD_SEC == 0:
                return True
            else:
                return False    
        else:
            return False


    def REFRESH_DATA(TIME_CHECK):
        if TIME_CHECK == True:
            READ_CONFIG_DATA = READ_WRITE.READ_JSON(CONFIG_DIR)
            KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["CITY_NUM"]]
            OPTION = webdriver.ChromeOptions()
            OPTION.add_argument("headless")
            #driver = webdriver.Chrome(chromedriver_dir, options = options)
            DIR = ".\\Driver\\chromedriver_win32\\chromedriver.exe"
            #DRIVER = webdriver.Chrome(DIR, options = options)
            DRIVER = webdriver.Chrome(DIR, options = OPTION)
            for KEY_NAME in KEY_LIST:
                RESULT = []
                CITY_NAME = KEY_NAME
                CITY_NUM = READ_CONFIG_DATA["CITY_NUM"][f"{KEY_NAME}"]
                CITY_URL = READ_CONFIG_DATA["URL"]["OPTION"]["EACH_REGION"] + f"{CITY_NUM}"
                DRIVER.get(CITY_URL)
        
                for COUNT in range(2):
                    NUM = COUNT + 1
                    BASIC_X_PATH = f"/html/body/div[@id='root']/div[@class='sc-AxjAm hKkiMb sc-AxirZ idrxEV sc-AxhCb eSwYtm sc-AxgMl cVmQYF']/div[@class='sc-AxjAm bRuiNy sc-AxirZ fZVwIW sc-AxiKw eSbheu']/div[@class='sc-AxjAm jItFqW sc-AxirZ duVOLM sc-AxhCb eSwYtm'][{NUM}]/div[@class='sc-AxjAm fiWmrI sc-AxirZ heBhHx sc-AxiKw eSbheu']/div[@class='sc-AxjAm hQNuxH sc-AxirZ idrxEV sc-AxiKw eSbheu']/div[@class='sc-AxjAm dhEPlC']/span"
                    INTERNAL_FUNC.Del(1)
                    READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(BASIC_X_PATH, DRIVER).text
                    RESULT.append(READ_DATA)

                with open(CONFIG_DIR, "w", encoding = "utf-8") as WRITE_CONFIG_PROFILE:
                    READ_CONFIG_DATA["SAVE_DATA"][f"{CITY_NAME}"] = {}
                    READ_CONFIG_DATA["SAVE_DATA"][f"{CITY_NAME}"][f"TOTAL_AMOUNT"] = RESULT[0]
                    READ_CONFIG_DATA["SAVE_DATA"][f"{CITY_NAME}"][f"TODAY_AMOUNT"] = RESULT[1]
                    json.dump(READ_CONFIG_DATA, WRITE_CONFIG_PROFILE, indent = 4)
            DRIVER.quit()

            READ_CONFIG_DATA = READ_WRITE.READ_JSON(CONFIG_DIR)
            F_KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["X_PATH"]] #X_PATH키의 값에 속해 있는 키들을 리스트의 형식으로 받아옴
            URL = READ_CONFIG_DATA["URL"]["BASIC_URL"]
            OPTION = webdriver.ChromeOptions()
            OPTION.add_argument("headless")
            #driver = webdriver.Chrome(chromedriver_dir, options = options)
            DIR = ".\\Driver\\chromedriver_win32\\chromedriver.exe"
            DRIVER = webdriver.Chrome(DIR, options = OPTION)
            DRIVER.get(URL)
            CLOSE_BTN_X_PATH_1 = "/html/body/div[@id='root-portal']/div[@class='Layout__SBox-dxfASU lfSkfB Layout__SFlex-dGOlJW Xdeos Layout__SCol-cKWydp iDqTgD Modal__ModalContainer-cejTIT ifdjuG']/button[@class='Button-dtvKLW giplLf']"
            CLOSE_BTN_X_PATH_2 = "/html/body/div[@id='root-portal']/div[@class='Layout__SBox-dxfASU inRbsl Layout__SFlex-dGOlJW Xdeos Layout__SCol-cKWydp iDqTgD Modal__ModalContainer-cejTIT kRiNlL']/button[@class='Button-dtvKLW giplLf']"
            try:
                INTERNAL_FUNC.Driver_Get_X_Path(CLOSE_BTN_X_PATH_1, DRIVER).click()
                try:
                    INTERNAL_FUNC.Driver_Get_X_Path(CLOSE_BTN_X_PATH_2, DRIVER).click()
                except:
                    pass
            except:
                pass

            #DRIVER = webdriver.Chrome(DIR)
            with open(CONFIG_DIR, "w", encoding = "utf-8") as WRITE_SAVE_PROFILE:
                READ_CONFIG_DATA["SAVE_DATA"]["TOTAL_VALUE"] = {}
                json.dump(READ_CONFIG_DATA, WRITE_SAVE_PROFILE, indent = 4)

            for F_NOW_KEY_NAME in F_KEY_LIST:#F_NOW_KEY_NAME 데이터 종류 (확진자, 사망자, 완치자)
                S_KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["X_PATH"][f"{F_NOW_KEY_NAME}"]]

                if F_NOW_KEY_NAME == "CONFIRMED_CASE":
                    CASE_NAME = "확진자"
                elif F_NOW_KEY_NAME == "COMPLETE_HEALER":
                    CASE_NAME = "완치자"
                elif F_NOW_KEY_NAME == "DEAD_COUNT":
                    CASE_NAME = "사망자"

                with open(CONFIG_DIR, "w", encoding = "utf-8") as WRITE_SAVE_PROFILE:
                    READ_CONFIG_DATA["SAVE_DATA"]["TOTAL_VALUE"][f"{CASE_NAME}"] = {}
                    json.dump(READ_CONFIG_DATA, WRITE_SAVE_PROFILE, indent = 4)
                        
                for S_NOW_KEY_NAME in S_KEY_LIST:#S_NOW_KEY_NAME 데이터 종류 (확진자에 한해 당일 확진자값도 존재 / 나머지는 총합 / 전일대비)
                    if S_NOW_KEY_NAME == "TOTAL_NATIONWIDE":
                        VALUE_NAME = "총합"
                    elif S_NOW_KEY_NAME == "TOTAL_INCREASE_AMOUNT":
                        VALUE_NAME = "전일 대비 증가"
                    elif S_NOW_KEY_NAME == "TODAY_INCREASE_AMOUNT":
                        VALUE_NAME = "당일 증가"
                    X_PATH_DATA = READ_CONFIG_DATA["X_PATH"][f"{F_NOW_KEY_NAME}"][f"{S_NOW_KEY_NAME}"]
                    if type(X_PATH_DATA) == list:
                        try:
                            X_PATH = X_PATH_DATA[0]
                            READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
                        except:
                            try:
                                X_PATH = X_PATH_DATA[1]
                                READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
                            except:
                                READ_DATA = "NULL"
                    else:
                        try:
                            X_PATH = X_PATH_DATA
                            READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
                        except:
                            READ_DATA = "NULL"
                        
                    with open(CONFIG_DIR, "w", encoding = "utf-8") as WRITE_SAVE_PROFILE:
                        if "명" in READ_DATA:
                            READ_DATA = READ_DATA.split("명")[0]
                        READ_CONFIG_DATA["SAVE_DATA"]["TOTAL_VALUE"][f"{CASE_NAME}"][f"{VALUE_NAME}"] = READ_DATA
                        json.dump(READ_CONFIG_DATA, WRITE_SAVE_PROFILE, indent = 4)

                      


    def COVID_CHECK(REGION):
        if REGION != None:
            READ_CONFIG_DATA = READ_WRITE.READ_JSON(CONFIG_DIR)
            KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["CITY_NUM"]]

            for COUNT in range(len(KEY_LIST)):
                if KEY_LIST[COUNT] in REGION:
                    CITY_NAME = KEY_LIST[COUNT]
                    TOTAL_AMOUNT = READ_CONFIG_DATA["SAVE_DATA"][f"{CITY_NAME}"]["TOTAL_AMOUNT"]
                    TODAY_AMOUNT = READ_CONFIG_DATA["SAVE_DATA"][f"{CITY_NAME}"]["TODAY_AMOUNT"]

                    RT_EMBED = discord.Embed(title = f":mag: {CITY_NAME} :mag_right:", description = f"")
                    RT_EMBED.add_field(name = f"**총합 확진자**", value = f"**`{TOTAL_AMOUNT}명`**", inline = True)
                    RT_EMBED.add_field(name = f"**당일 확진자**", value = f"**`{TODAY_AMOUNT}명`**", inline = True)

                    return RT_EMBED
            
        elif REGION == None:
            READ_CONFIG_DATA = READ_WRITE.READ_JSON(CONFIG_DIR)
            RT_EMBED = discord.Embed(title = f":mag: 전국 코로나19 현황 :mag_right:", description = f"")
            F_KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["X_PATH"]] #X_PATH키의 값에 속해 있는 키들을 리스트의 형식으로 받아옴

            for F_NOW_KEY_NAME in F_KEY_LIST:
                S_KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["X_PATH"][f"{F_NOW_KEY_NAME}"]]

                if F_NOW_KEY_NAME == "CONFIRMED_CASE":
                    CASE_NAME = "확진자"
                elif F_NOW_KEY_NAME == "COMPLETE_HEALER":
                    CASE_NAME = "완치자"
                elif F_NOW_KEY_NAME == "DEAD_COUNT":
                    CASE_NAME = "사망자"

                for S_NOW_KEY_NAME in S_KEY_LIST:
                    if S_NOW_KEY_NAME == "TOTAL_NATIONWIDE":
                        VALUE_NAME = "총합"
                    elif S_NOW_KEY_NAME == "TOTAL_INCREASE_AMOUNT":
                        VALUE_NAME = "전일 대비 증가"
                    elif S_NOW_KEY_NAME == "TODAY_INCREASE_AMOUNT":
                        VALUE_NAME = "당일 증가"
                    
                    READ_DATA = READ_CONFIG_DATA["SAVE_DATA"]["TOTAL_VALUE"][f"{CASE_NAME}"][f"{VALUE_NAME}"]

                    if CASE_NAME == "확진자":
                        PRINT_TEXT = f'```fix\n{READ_DATA}\n```'
                    elif CASE_NAME == "완치자":
                        PRINT_TEXT = f'```css\n{READ_DATA}\n```'
                    elif CASE_NAME == "사망자":
                        PRINT_TEXT = f"```bf\n{READ_DATA}\n```"

                    if READ_DATA != "NULL":
                        RT_EMBED.add_field(name = f"**{VALUE_NAME} {CASE_NAME}**", value = f"**{PRINT_TEXT}**", inline = False)
                    elif READ_DATA == "NULL":
                        RT_EMBED.add_field(name = f"**{VALUE_NAME} {CASE_NAME}**", value = f"**`집계중`**", inline = False)     

            return RT_EMBED
                    
                
            # READ_CONFIG_DATA = READ_WRITE.READ_JSON(CONFIG_DIR)
            # RT_EMBED = discord.Embed(title = f":mag: 전국 코로나19 현황 :mag_right:", description = f"")
            # F_KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["X_PATH"]] #X_PATH키의 값에 속해 있는 키들을 리스트의 형식으로 받아옴
            # URL = READ_CONFIG_DATA["URL"]["BASIC_URL"]
            # OPTION = webdriver.ChromeOptions()
            # OPTION.add_argument("headless")
            # #driver = webdriver.Chrome(chromedriver_dir, options = options)
            # DIR = ".\\Driver\\chromedriver_win32\\chromedriver.exe"
            # DRIVER = webdriver.Chrome(DIR, options = OPTION)
            # DRIVER.get(URL)
            # CLOSE_BTN_X_PATH_1 = "/html/body/div[@id='root-portal']/div[@class='Layout__SBox-dxfASU lfSkfB Layout__SFlex-dGOlJW Xdeos Layout__SCol-cKWydp iDqTgD Modal__ModalContainer-cejTIT ifdjuG']/button[@class='Button-dtvKLW giplLf']"
            # CLOSE_BTN_X_PATH_2 = "/html/body/div[@id='root-portal']/div[@class='Layout__SBox-dxfASU inRbsl Layout__SFlex-dGOlJW Xdeos Layout__SCol-cKWydp iDqTgD Modal__ModalContainer-cejTIT kRiNlL']/button[@class='Button-dtvKLW giplLf']"
            # try:
            #     INTERNAL_FUNC.Driver_Get_X_Path(CLOSE_BTN_X_PATH_1, DRIVER).click()
            #     try:
            #         INTERNAL_FUNC.Driver_Get_X_Path(CLOSE_BTN_X_PATH_2, DRIVER).click()
            #     except:
            #         pass
            # except:
            #     pass

            # #DRIVER = webdriver.Chrome(DIR)
            # with open(CONFIG_DIR, "w", encoding = "utf-8") as WRITE_SAVE_PROFILE:
            #     READ_CONFIG_DATA["SAVE_DATA"]["TOTAL_VALUE"] = {}
            #     json.dump(READ_CONFIG_DATA, WRITE_SAVE_PROFILE, indent = 4)

            # for F_NOW_KEY_NAME in F_KEY_LIST:#F_NOW_KEY_NAME 데이터 종류 (확진자, 사망자, 완치자)
            #     S_KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["X_PATH"][f"{F_NOW_KEY_NAME}"]]

            #     if F_NOW_KEY_NAME == "CONFIRMED_CASE":
            #         CASE_NAME = "확진자"
            #     elif F_NOW_KEY_NAME == "COMPLETE_HEALER":
            #         CASE_NAME = "완치자"
            #     elif F_NOW_KEY_NAME == "DEAD_COUNT":
            #         CASE_NAME = "사망자"

            #     with open(CONFIG_DIR, "w", encoding = "utf-8") as WRITE_SAVE_PROFILE:
            #         READ_CONFIG_DATA["SAVE_DATA"]["TOTAL_VALUE"][f"{CASE_NAME}"] = {}
            #         json.dump(READ_CONFIG_DATA, WRITE_SAVE_PROFILE, indent = 4)
                        
            #     for S_NOW_KEY_NAME in S_KEY_LIST:#S_NOW_KEY_NAME 데이터 종류 (확진자에 한해 당일 확진자값도 존재 / 나머지는 총합 / 전일대비)
            #         if S_NOW_KEY_NAME == "TOTAL_NATIONWIDE":
            #             VALUE_NAME = "총합"
            #         elif S_NOW_KEY_NAME == "TOTAL_INCREASE_AMOUNT":
            #             VALUE_NAME = "전일 대비 증가"
            #         elif S_NOW_KEY_NAME == "TODAY_INCREASE_AMOUNT":
            #             VALUE_NAME = "당일 증가"
            #         X_PATH_DATA = READ_CONFIG_DATA["X_PATH"][f"{F_NOW_KEY_NAME}"][f"{S_NOW_KEY_NAME}"]
            #         if type(X_PATH_DATA) == list:
            #             try:
            #                 X_PATH = X_PATH_DATA[0]
            #                 READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
            #             except:
            #                 try:
            #                     X_PATH = X_PATH_DATA[1]
            #                     READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
            #                 except:
            #                     READ_DATA = "NULL"
            #         else:
            #             try:
            #                 X_PATH = X_PATH_DATA
            #                 READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
            #             except:
            #                 READ_DATA = "NULL"
                        
            #         with open(CONFIG_DIR, "w", encoding = "utf-8") as WRITE_SAVE_PROFILE:
            #             READ_CONFIG_DATA["SAVE_DATA"]["TOTAL_VALUE"][f"{CASE_NAME}"][f"{VALUE_NAME}"] = READ_DATA
            #             json.dump(READ_CONFIG_DATA, WRITE_SAVE_PROFILE, indent = 4)
            #         if CASE_NAME == "확진자":
            #             PRINT_TEXT = f'```fix\n{READ_DATA}\n```'
            #         elif CASE_NAME == "완치자":
            #             PRINT_TEXT = f'```css\n{READ_DATA}\n```'
            #         elif CASE_NAME == "사망자":
            #             PRINT_TEXT = f"```bf\n{READ_DATA}\n```"

            #         print(READ_DATA)
            #         if READ_DATA != "NULL":
            #             RT_EMBED.add_field(name = f"**{VALUE_NAME} {CASE_NAME}**", value = f"**{PRINT_TEXT}**", inline = False)
            #         elif READ_DATA == "NULL":
            #             RT_EMBED.add_field(name = f"**{VALUE_NAME} {CASE_NAME}**", value = f"**`집계중`**", inline = False)     
                    

            # return RT_EMBED
                    
        # elif REGION == None:
        #     RT_EMBED = discord.Embed(title = f":mag: 전국 코로나19 현황 :mag_right:", description = f"")
        #     READ_CONFIG_DATA = READ_WRITE.READ_JSON(CONFIG_DIR)
        #     F_KEY_LIST = [KEY for KEY in READ_CONFIG_DATA["X_PATH"]]
        #     URL = READ_CONFIG_DATA["URL"]["BASIC_URL"]
        #     OPTION = webdriver.ChromeOptions()
        #     OPTION.add_argument("headless")
        #     #driver = webdriver.Chrome(chromedriver_dir, options = options)
        #     DIR = ".\\Driver\\chromedriver_win32\\chromedriver.exe"
        #     DRIVER = webdriver.Chrome(DIR, options = OPTION)
        #     #DRIVER = webdriver.Chrome(DIR)
        #     DRIVER.get(URL)
        #     INTERNAL_FUNC.Del(2)

        #     for COUNT in range(len(F_KEY_LIST)):
        #         if F_KEY_LIST[COUNT] == "CONFIRMED_CASE":
        #             CASE_NAME = "확진자"
        #         elif F_KEY_LIST[COUNT] == "COMPLETE_HEALER":
        #             CASE_NAME = "완치자"
        #         elif F_KEY_LIST[COUNT] == "DEAD_COUNT":
        #             CASE_NAME = "사망자"
                
        #         for KEY_NAME in [KEY for KEY in READ_CONFIG_DATA["X_PATH"][f"{F_KEY_LIST[COUNT]}"]]:
        #             X_PATH = READ_CONFIG_DATA["X_PATH"][f"{F_KEY_LIST[COUNT]}"][f"{KEY_NAME}"]
        #             try:
        #                 if type(X_PATH) == list:
        #                     try:
        #                         X_PATH = X_PATH[0]
        #                         READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text   
        #                     except:
        #                         X_PATH = X_PATH[1]
        #                         READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text   
        #                 else:
        #                     READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
        #             except:
        #                 try:
        #                     CLOSE_BTN_X_PATH_1 = "/html/body/div[@id='root-portal']/div[@class='Layout__SBox-dxfASU lfSkfB Layout__SFlex-dGOlJW Xdeos Layout__SCol-cKWydp iDqTgD Modal__ModalContainer-cejTIT ifdjuG']/button[@class='Button-dtvKLW giplLf']"
        #                     CLOSE_BTN_X_PATH_2 = "/html/body/div[@id='root-portal']/div[@class='Layout__SBox-dxfASU inRbsl Layout__SFlex-dGOlJW Xdeos Layout__SCol-cKWydp iDqTgD Modal__ModalContainer-cejTIT kRiNlL']/button[@class='Button-dtvKLW giplLf']"
        #                     READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(CLOSE_BTN_X_PATH_1, DRIVER).click()
        #                     READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(CLOSE_BTN_X_PATH_2, DRIVER).click()
                            
        #                     if type(X_PATH) == list:
        #                         try:
        #                             X_PATH = X_PATH[0]
        #                             READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text   
        #                         except:
        #                             X_PATH = X_PATH[1]
        #                             READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text   
        #                     else:
        #                         READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
                            
        #                 except:
        #                     try:
        #                         if type(X_PATH) == list:
        #                             try:
        #                                 X_PATH = X_PATH[0]
        #                                 READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text   
        #                             except:
        #                                 X_PATH = X_PATH[1]
        #                                 READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text   
        #                         else:
        #                             READ_DATA = INTERNAL_FUNC.Driver_Get_X_Path(X_PATH, DRIVER).text
        #                     except:
        #                         READ_DATA = "NULL"


        #             print(READ_DATA)
        #             if KEY_NAME == "TOTAL_NATIONWIDE":
        #                 VALUE_NAME = "총합"
        #             elif KEY_NAME == "TOTAL_INCREASE_AMOUNT":
        #                 VALUE_NAME = "전일 대비 증가"
        #             elif KEY_NAME == "TODAY_INCREASE_AMOUNT":
        #                 VALUE_NAME = "당일 증가"
                    
        #             if READ_DATA != "NULL":
        #                 RT_EMBED.add_field(name = f"**{VALUE_NAME} {CASE_NAME}**", value = f"**`{READ_DATA}명`**", inline = False)
        #             elif READ_DATA == "NULL":
        #                 RT_EMBED.add_field(name = f"**{VALUE_NAME} {CASE_NAME}**", value = f"**`집계중`**", inline = False)
        #     DRIVER.quit()
        #     return RT_EMBED
            
