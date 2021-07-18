import json





class READ_WRITE:

    def READ_JSON(FILE_DIR):
        """FILE_DIR에는 데이터를 읽어올 JSON데이터 파일 디렉토리를 입력해주세요.

        리턴
        --------
        READ_JSON(FILE_DIR = :func:`JSON_DIR`)\n
        ==> READ_USER_DATA[:func:`"KEY"`]
        """
        
        with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
            READ_USER_DATA = json.load(READ_USER_PROFILE)
            READ_USER_PROFILE.close()
        
        return READ_USER_DATA #READ_USER_DATA타입 = DICT
    
    def WRITE_JSON(FILE_DIR, JSON_DATA):
        """FILE_DIR에는 수정할 JSON데이터 파일 디렉토리\n
        JSON_DATA에는 수정할 데이터와 값을 :func:`DICT`로 넣기\n
        만약 2개 이상이면 :func:`LIST`안에 :func:`DICT`를 넣는 방식으로 해주세요.\n

        그리고 JSON의 KEY가 어떤 키안에 종속되어 있을 경우
        
        예시 1번
        --------
            수정 데이터 2개 이상 일시 예시:\n
            NUM1_JSON_KEY = "EXAM1"\n
            NUM1_JSON_VAL = "1000"\n
            NUM2_JSON_KEY = "EXAM1"\n
            NUM2_JSON_VAL = "2000"\n

            JSON_DATA 입력 값
            --------
                ==>DATA = [{"KEY": "EXAM1", "VALUE": "1000"}, {"KEY": "EXAM2", "VALUE": "2000"}]\n
                DATA[0] ==> {"KEY": "EXAM1", "VALUE": "1000"}\n
                DATA[1] ==> {"KEY": "EXAM2", "VALUE": "2000"}\n
                이때 DATA의 타입은 tuple 혹은 list여야함\n


        예시 2번
        --------
            수정 데이터의 JSON의 키가 2개 이상의 키를 거쳐야 할때 예시:\n
            DATA = [{"KEY": ["EXAM1-1", "EXAM1-2], "VALUE": "1000"}]\n
            ==> KEY = 부모키, ["EXAM1-1", "EXAM1-2] = 자식키 1번, 2번\n
        
            JSON_KEY 값
            --------
            DATA[0]["KEY"][0] ==> EXAM1-1\n
            DATA[0]["KEY"][1] ==> EXAM1-2\n
        """
        JSON_DATA_LIST = JSON_DATA
        JSON_DATA_LIST_COUNTER = len(JSON_DATA_LIST)
        JSON_DATA_KEY_COUNTER = len(JSON_DATA_LIST)

       
        #with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
        for COUNT in range(JSON_DATA_LIST_COUNTER):
            JSON_DATA_KEY_COUNTER = len(JSON_DATA_LIST[COUNT]["KEY"])
            if JSON_DATA_KEY_COUNTER == 1:
                KEY1 = JSON_DATA_LIST[COUNT]["KEY"][0]
                JSON_VALUE = JSON_DATA_LIST[COUNT]["VALUE"]
                #READ_USER_DATA[f"{JSON_KEY}"] = [f"{JSON_VALUE}"]
                try:
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()

                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)

                except:
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_FIRST_USER_PROFILE:
                        FIRST_WRITE_DATA = {f"{KEY1}": ""}
                        json.dump(FIRST_WRITE_DATA, WRITE_FIRST_USER_PROFILE, indent = 4)
                    
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()
                    
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)
                
            elif JSON_DATA_KEY_COUNTER == 2:
                KEY1 = JSON_DATA_LIST[COUNT]["KEY"][0]
                KEY2 = JSON_DATA_LIST[COUNT]["KEY"][1]
                JSON_VALUE = JSON_DATA_LIST[COUNT]["VALUE"]
                #JSON_KEY = JSON_DATA_LIST[COUNT][f"{KEY1}"][f"{KEY2}"]
                try:
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()

                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1][KEY2] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)

                except:
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_FIRST_USER_PROFILE:
                        FIRST_WRITE_DATA = {f"{KEY1}": {f"{KEY2}": ""}}
                        json.dump(FIRST_WRITE_DATA, WRITE_FIRST_USER_PROFILE, indent = 4)
                    
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()
                    
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1][KEY2] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)

            elif JSON_DATA_KEY_COUNTER == 3:
                KEY1 = JSON_DATA_LIST[COUNT]["KEY"][0]
                KEY2 = JSON_DATA_LIST[COUNT]["KEY"][1]
                KEY3 = JSON_DATA_LIST[COUNT]["KEY"][2]
                JSON_VALUE = JSON_DATA_LIST[COUNT]["VALUE"]
                #READ_USER_DATA[KEY1][KEY2][KEY3] = [JSON_VALUE]



                try:
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()

                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1][KEY2][KEY3] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)

                except:
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_FIRST_USER_PROFILE:
                        FIRST_WRITE_DATA = {f"{KEY1}": {f"{KEY2}": {f"{KEY3}": ""}}}
                        json.dump(FIRST_WRITE_DATA, WRITE_FIRST_USER_PROFILE, indent = 4)
                    
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()
                    
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1][KEY2][KEY3] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)
            
            elif JSON_DATA_KEY_COUNTER == 4:
                KEY1 = JSON_DATA_LIST[COUNT]["KEY"][0]
                KEY2 = JSON_DATA_LIST[COUNT]["KEY"][1]
                KEY3 = JSON_DATA_LIST[COUNT]["KEY"][2]
                KEY4 = JSON_DATA_LIST[COUNT]["KEY"][3]
                JSON_VALUE = JSON_DATA_LIST[COUNT]["VALUE"]
                #READ_USER_DATA[KEY1][KEY2][KEY3] = [JSON_VALUE]



                try:
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()

                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1][KEY2][KEY3][KEY4] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)

                except:
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_FIRST_USER_PROFILE:
                        FIRST_WRITE_DATA = {f"{KEY1}": {f"{KEY2}": {f"{KEY3}": {f"{KEY4}": ""}}}}
                        json.dump(FIRST_WRITE_DATA, WRITE_FIRST_USER_PROFILE, indent = 4)
                    
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()
                    
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1][KEY2][KEY3][KEY4] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)

            elif JSON_DATA_KEY_COUNTER == 5:
                KEY1 = JSON_DATA_LIST[COUNT]["KEY"][0]
                KEY2 = JSON_DATA_LIST[COUNT]["KEY"][1]
                KEY3 = JSON_DATA_LIST[COUNT]["KEY"][2]
                KEY4 = JSON_DATA_LIST[COUNT]["KEY"][3]
                KEY5 = JSON_DATA_LIST[COUNT]["KEY"][4]
                JSON_VALUE = JSON_DATA_LIST[COUNT]["VALUE"]
                #READ_USER_DATA[KEY1][KEY2][KEY3] = [JSON_VALUE]



                try:
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()

                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1][KEY2][KEY3][KEY4][KEY5] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)

                except:
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_FIRST_USER_PROFILE:
                        FIRST_WRITE_DATA = {f"{KEY1}": {f"{KEY2}": {f"{KEY3}": {f"{KEY4}": {f"{KEY5}": ""}}}}}
                        json.dump(FIRST_WRITE_DATA, WRITE_FIRST_USER_PROFILE, indent = 4)
                    
                    with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
                        READ_USER_DATA = json.load(READ_USER_PROFILE)
                        READ_USER_PROFILE.close()
                    
                    with open(f"{FILE_DIR}", "w", encoding = "utf-8") as WRITE_USER_PROFILE:
                        READ_USER_DATA[KEY1][KEY2][KEY3][KEY4][KEY5] = JSON_VALUE
                        json.dump(READ_USER_DATA, WRITE_USER_PROFILE, indent = 4)

            else:
                print(f"JSON_KEY를 5개 이상 받을수 없습니다")
"""
    def REWRITE_JSON(FILE_DIR, F_KEY, JSON_DATA):
        
        
        #이 함수의 JSON_DATA는 WRITE_JSON함수의 JSON_DATA형식과 다르게 입력해야합니다.\n JSON_DATA는 DICT의 형식으로 입력해야합니다.
        
        with open(f"{FILE_DIR}", "r", encoding = "utf-8") as READ_USER_PROFILE:
            READ_USER_DATA = json.load(READ_USER_PROFILE)
            READ_USER_PROFILE.close()
        
        DATA_KEY_LIST = [KEYS for KEYS in READ_USER_DATA]
        COUNTER = len(DATA_KEY_LIST) - 1

        DATA = READ_USER_DATA[f"{DATA_KEY_LIST[COUNTER]}"]

        with open(f"{FILE_DIR}", "w", encoding = "utf-8") as REWRITE_USER_PROFILE:
            REWRITE_JSON_DATA = {f"{DATA_KEY_LIST[0]}": DATA, f"{F_KEY}": JSON_DATA}
            print(REWRITE_JSON_DATA)
            json.dump(REWRITE_JSON_DATA, REWRITE_USER_PROFILE, indent = 4)
"""