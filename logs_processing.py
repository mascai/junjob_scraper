import pandas as pd
import datetime, time

df = pd.read_csv("data/user_logs.csv", sep=";")
RES_FILE = "/home/alex/Education/6/cmc/diploma/Notebooks/data/res.csv"

df = pd.read_csv("data/user_logs.csv", sep=";")

def append_to_file(user, file):
    col_names =  ['Name', 'Total_time','Click_vacancy', 'Click_paginate', 'Click_search', 'Click_contact', 'Avg_time_on_vacancy', 'Avg_time_on_action', "Consecutive_num"]
    print("111: ", len(col_names))
    print("222: ", len(user.to_list()))
    if os.path.isfile(file) == 0:
        col_names =  ['Name', 'Total_time','Click_vacancy', 'Click_paginate', 'Click_search', 'Click_contact', 'Avg_time_on_vacancy', 'Avg_time_on_action', "Consecutive_num"]
        df  = pd.DataFrame(columns = col_names)
        
        df.to_csv(file, sep=";")
        
    df = pd.read_csv(file, sep=";")
    a_series = pd.Series(user.to_list(), index = col_names)
    df = df.append(a_series, ignore_index=True)
    
    df.to_csv(file, sep=";", index=False)
      
    
    
    


class User:
    def __init__(self, name, login_time, end_time, click_vacancy, click_paginate, click_search, click_contact, time_on_page, consecutive_num):
        self.name = name
        self.login_time = login_time
        self.end_time = end_time 
        self.click_vacancy = click_vacancy # number of open vacancies
        self.click_paginate = click_paginate # number clicks on next button
        self.click_search = click_search # number of clicks on search button
        self.click_contact = click_contact
        self.time_on_page = time_on_page # number of seconds that user was on the vacancy page
        self.consecutive_num = consecutive_num # number of consecutive vacancy open
    
    def __str__(self):
        return "{};{};{};{};{};{};{}".format(
            self.name, self.login_time, self.end_time, self.click_vacancy, self.click_paginate, self.click_search, self.click_contact, self.time_on_page)
    
    def to_list(self):
        return [self.name, self.time_delta(), self.click_vacancy, self.click_paginate, self.click_search, self.click_contact, self.avg_time_on_vacancy(), self.avg_time_on_action(), self.consecutive_num]
    
    def print(self):
        return """name {}, 
login_time {}, 
end_time {}, 
click_vacancy {}, 
click_paginate {}, 
click_search {},
click_contact {},
time_on_page {}
consecutive_num {}
----Functions----
time_delta {}
avg_time_on_vacancy {}
avg_time_on_action {}
""".format(
            self.name, self.login_time, self.end_time, self.click_vacancy, self.click_paginate, self.click_search, 
            self.click_contact, self.time_on_page, self.consecutive_num, self.time_delta(), self.avg_time_on_vacancy(), self.avg_time_on_action())
        
    
    def time_delta(self):
        """ Total number of seconds on the site"""
        delta = str_to_time(self.end_time) - str_to_time(self.login_time)
        return delta.seconds
    
    def avg_time_on_vacancy(self):
        return self.time_on_page / self.click_vacancy
    
    def avg_time_on_action(self):
        return self.time_delta() / (self.click_vacancy + self.click_paginate + self.click_search + self.click_contact)
        
        

def str_to_time(s):
    return datetime.datetime.strptime(str(s), "%Y-%m-%d %H:%M:%S")
    
    
def create_user(user_name, df):
    df1 = df[df["User"] == user_name]
    login_time = ""
    click_vacancy = 0
    click_paginate = 0
    click_search = 0
    click_contact = 0
    max_consecutive_num = 0
    cur_consecutive_num = 0
    is_first = True
    
    prev = None
    end_time = None
    
    time_on_page = 0 # number of seconds that user was on the vacancy page
    
    for row in df1.iterrows():
        if row[1]["Action"] == "LOGIN":
            login_time = row[1]["Time"]
        elif row[1]["Action"] == "VACANCY":
            click_vacancy += 1
            if prev[1]["Action"] == "VACANCY":
                time_on_page += (str_to_time(row[1]["Time"]) -  str_to_time(prev[1]["Time"])).seconds
                if int(prev[1]["Data1"]) == int(row[1]["Data1"]) + 1:
                    cur_consecutive_num += 1
                    max_consecutive_num = max(max_consecutive_num, cur_consecutive_num)
                else:
                    cur_consecutive_num = 1
                    
        elif row[1]["Action"] == "PAGINATE":
            click_paginate += 1
        elif row[1]["Action"] == "SEARCH":
            click_search += 1
        elif row[1]["Action"] == "CLICK_CONTACT":
            click_contact += 1
        
        end_time = row[1]["Time"]
        prev = row
    
    return User(user_name, login_time, end_time, click_vacancy, click_paginate, click_search, click_contact, time_on_page, max_consecutive_num)


        

res_admin = create_user("admin", df)
res_virus1 = create_user("virus1", df)
print(res_admin.print())
print(res_virus1.print())

append_to_file(res_virus1, RES_FILE)
