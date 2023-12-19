from tkinter import *
import tkinter.messagebox
import hashlib
import time
import pymysql

LOG_LINE_NUM = 0
CNAME_LIST = [[],[]]
COU_FILES = []
COU_BTM = []

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #設置視窗畫面以及顯示的東西
    def set_init_window(self):
        self.init_window_name.title("中興大學匿名聊天室")           #視窗名稱
        #self.init_window_name.geometry('320x160+10+10')                         #前面為視窗大小，+10 +10 打開時的位置
        self.init_window_name.geometry('1068x681+100+10')
        #self.init_window_name["bg"] = "pink"                                    #背景色，其他背景色：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #透明度，值越小虚化程度越高
        #標籤
        self.init_data_label1 = Label(self.init_window_name, text="帳號")
        self.init_data_label1.place(x =20 ,y =20 )
        self.init_data_label2 = Label(self.init_window_name, text="密碼")
        self.init_data_label2.place(x =20 ,y =60)

        self.onemessage_label = Label(self.init_window_name, text="訊息展開處")
        self.manymessage_label = Label(self.init_window_name, text="課程名稱")

        #打訊息框
        self.init_data_Entry1 = Entry(self.init_window_name,show=None, font=('Arial', 12))  #打帳號的框
        self.init_data_Entry1.place(x =70,y =20 )
        self.init_data_Entry2 = Entry(self.init_window_name,show = "*", font=('Arial', 12))  #打密碼的框
        self.init_data_Entry2.place(x =70,y =60 )
        self.onemessage_Text = Text(self.init_window_name, width=60, height=40)  #訊息展開處
        self.onemessage_Text.bind("<Key>", lambda a: "break")  #只能讀取不能修改 但是也不能複製
        self.typemessage_Text = Text(self.init_window_name, width=50, height=4) #輸入要打的訊息的地方

        #按钮
        self.str_login_button = Button(self.init_window_name, text="登入", bg="white", width=10,command=self.login) 
        self.str_login_button.place(x=20, y=100)
        self.str_enter_button = Button(self.init_window_name, text="送出訊息", bg="white", width=8,command=self.addword)
        self.str_logout_button = Button(self.init_window_name, text="登出", bg="white", width=8,command=self.logout)

    #需要比對帳密
    def login(self):    #登入def 進入資料庫尋找帳密是否正確
        src = self.init_data_Entry1.get()#.encode()
        src2 = self.init_data_Entry2.get()
        if self.use_sql_aco('account_student', 'name',src) == "sqlnotfound": #判斷與資料庫是不是對的(先判斷帳號有沒有註冊過) if 沒註冊過
            tkinter.messagebox.showinfo(title='訊息', message='帳號不存在，請重新登入。')
            self.init_data_Entry2.delete(0,"end")
        elif self.use_sql_aco('account_student', 'name',src,2) != src2: #判斷資料庫對應的密碼是否正確 if 註冊過但是不符
            tkinter.messagebox.showinfo(title='訊息', message='密碼錯誤，請重新登入。')
            self.init_data_Entry2.delete(0,"end")
        else:
            tkinter.messagebox.showinfo(title='訊息', message='登入成功')
            self.init_data_label1.place_forget()
            self.init_data_label2.place_forget()
            self.str_login_button.place_forget()
            self.init_data_Entry1.place_forget()
            self.init_data_Entry2.place_forget()

            self.onemessage_label.place(x=500 ,y=20)
            self.manymessage_label.place(x =20,y = 20)
            self.onemessage_Text.place(x =500 ,y=60) 
            self.typemessage_Text.place(x = 500,y = 600)
            self.str_enter_button.place(x = 860,y = 615)
            self.str_logout_button.place(x = 20,y = 635)
            self.show_button() #要在右邊顯示按鈕們
            #成功登入的動作

#jerry@mail.nchu.edu.tw
#jerry123456789

    def logout(self): #初始化
        res = tkinter.messagebox.askquestion(title='訊息', message='確認登出?')
        if res == 'yes':

            self.init_data_label1.place(x =20 ,y =20)
            self.init_data_label2.place(x =20 ,y =60)
            self.str_login_button.place(x=20, y=100)
            self.init_data_Entry1.place(x =70,y =20)
            self.init_data_Entry2.place(x =70,y =60)

            self.onemessage_label.place_forget()
            self.onemessage_label = Label(self.init_window_name, text="訊息展開處")
            self.manymessage_label.place_forget()
            self.onemessage_Text.place_forget() 
            self.typemessage_Text.place_forget()
            self.str_enter_button.place_forget()
            self.str_logout_button.place_forget()
            self.close_button()
            self.init_data_Entry1.delete(0,"end")
            self.init_data_Entry2.delete(0,"end")
            self.typemessage_Text.delete(1.0,"end")
            self.onemessage_Text.delete(1.0,"end")

    #按完登入後來的
    def show_button(self): #顯示按鈕出來
        global COU_BTM
        global COU_FILES
        src = self.init_data_Entry1.get()
        sql_stu_cou = self.use_sql_cou('student_course','name',src)
        COU_FILES=[]      #為了放課程名稱
        COU_BTM=[]        #為了存放各種按鈕
        for i in range(len(sql_stu_cou)):
            COU_FILES.append(sql_stu_cou[i][2])

        #for i in range(10): #range10 改成課程名稱
        #    files.append("Button"+str(i))

        for i in range(len(COU_FILES)): 
            COU_BTM.append(Button(self.init_window_name, text=COU_FILES[i], width=20,command=lambda c=i: self.show_alone_msg(COU_BTM[c].cget("text")))) #text內放課程名稱
            COU_BTM[i].place(x =20,y = 60+i*30) #按鈕們顯示出來放旁邊 

    def close_button(self): #初始化的其中一個步驟
        global COU_BTM
        global COU_FILES
        for i in range(len(COU_FILES)):
            COU_BTM[i].place_forget()
        src,src2='',''
        CNAME_LIST = [[],[]]
        COU_FILES = []
        COU_BTM = []

    #從show_button來的
    def show_alone_msg(self,course_name): #按鈕按下去之後 執行的東西 搜尋課程名稱 將文檔顯示在右邊方塊
        self.onemessage_label.place_forget()
        self.onemessage_label = Label(self.init_window_name, text=course_name)
        self.onemessage_label.place(x=500 ,y=20)
        self.onemessage_Text.delete(1.0,"end")
        self.codename_list(course_name) #把所有名字跟代碼存在global變數內
        course_msg = self.use_sql_course_msg(course_name)   #抓取課堂相對應的資料
        course_msg_real = ''
        for i in range(len(course_msg)):
            course_msg_real = course_msg_real + course_msg[i][2]+ ' ' + self.change_name(course_msg[i][1]) + ': ' + course_msg[i][3] + '\n'
        self.onemessage_Text.insert(END, course_msg_real)



#change name要更改 兩個list(可以放在一起)  [[name],[codename]]一個讀入name 對應的讀入code name


    def codename_list(self,course): #讀入課程名稱 buttton按下會呼叫這個函數內的 List
        global CNAME_LIST 
        CNAME_LIST = [[],[]]
        temp_list = []
        temp_list.append(self.use_sql_name('teacher_course','course_name',course, 2))
        #print(temp_list) #print 出名字
        a = self.use_sql_cou('student_course','course_name',course) #all student name?
        #print(a)
        for i in range(len(a)):
            temp_list.append(a[i][1])
        CNAME_LIST[0]=temp_list
        temp_list=[1]
        #print(CNAME_LIST)
        for i in range(len(a)):
            temp_list.append(self.use_sql_aco('account_student','name',CNAME_LIST[0][i+1],3))
        CNAME_LIST[1]=temp_list
        #print(CNAME_LIST)

    def change_name(self,real_name):
        global CNAME_LIST
        if real_name == CNAME_LIST[0][0]: #可使用 但是要改sql內資料
           return '老師'
        else:
            ni = CNAME_LIST[0].index(real_name)
            if real_name == self.init_data_Entry1.get():
                return CNAME_LIST[1][ni] + '(自己)'
            else:
                return CNAME_LIST[1][ni]
        #另法
        # if real_name == self.init_data_Entry1.get():  
        #   return '自己'
        # elif real_name == CNAME_LIST[0][0]:
        #    return '老師'
        # else:
        #    for i in range(len(CNAME_LIST[0])):
        #        if real_name == CNAME_LIST[0][i]:
        #            return CNAME_LIST[1][i]

    #抓取username 資料存入資料庫內 先判斷是哪個資料要讀入
    def addword(self):
        user_name = self.init_data_Entry1.get() #抓取此使用者姓名
        course_name = self.onemessage_label['text']
        a = self.typemessage_Text.get(1.0,"end")
        if course_name!="訊息展開處":
            if (a != '\n') and (a != '\n\n') :
                self.use_sql_insert_msg(course_name,user_name,str(self.get_current_time()),self.typemessage_Text.get(1.0,"end"))
                add_msg = str(self.get_current_time())+ " " + self.change_name(user_name) + ": " + self.typemessage_Text.get(1.0,"end")
                self.onemessage_Text.insert(END,add_msg)
        self.typemessage_Text.delete(1.0,"end")

    def use_sql_aco(self,table,search,goal,key=0):# 1.table 2.search = goal (ex:id = 5) 3.key(要第幾個值拿出來判斷)
        db_settings = {
            "host":"140.120.108.103",
            "port":3306,
            "user":"user",
            "password":"nchu_8520",
            "db":"account",
            "charset":"utf8"
        }
        try :
            conn = pymysql.connect(**db_settings)
        except Exception as ex :
            print(ex)
        else:
            with conn.cursor() as cursor:
                command = "SELECT * FROM %s where %s ='%s'"
                cursor.execute(command %(table,search,goal))
                result = cursor.fetchall()
                if result == ():
                    print("not found")
                    return "sqlnotfound"
                else:
                    return result[0][key]
                    print(result[0][key]) #account(1帳號2密碼)
                    print(result)
                # conn.commit()

    def use_sql_name(self,table,search,goal,key=0): # change_name使用的東西
        db_settings = {
            "host":"140.120.108.103",
            "port":3306,
            "user":"user",
            "password":"nchu_8520",
            "db":"course",
            "charset":"utf8"
        }
        try :
            conn = pymysql.connect(**db_settings)
        except Exception as ex :
            print(ex)
        else:
            with conn.cursor() as cursor:
                command = "SELECT * FROM %s where %s ='%s'"
                cursor.execute(command %(table,search,goal))
                result = cursor.fetchall()
                if result == ():
                    print("not found")
                    return "sqlnotfound"
                else:
                    return result[0][key] 

    def use_sql_cou(self,table,search,goal,key=0):# 1.table 2.search (id = 5) 3.key(第幾個)
        db_settings = {
            "host":"140.120.108.103",
            "port":3306,
            "user":"user",
            "password":"nchu_8520",
            "db":"course",
            "charset":"utf8"
        }
        try :
            conn = pymysql.connect(**db_settings)
        except Exception as ex :
            print(ex)
        else:
            with conn.cursor() as cursor:
                command = "SELECT * FROM %s where %s ='%s'"
                cursor.execute(command %(table,search,goal))
                result = cursor.fetchall()
                if result == ():
                    print("not found")
                    return "sqlnotfound"
                else:
                    return result
                # conn.commit()

    def use_sql_course_msg(self,classes):# 1.table 2.search (id = 5) 3.key(第幾個)
        db_settings = {
            "host":"140.120.108.103",
            "port":3306,
            "user":"user",
            "password":"nchu_8520",
            "db":"course",
            "charset":"utf8"
        }
        try :
            conn = pymysql.connect(**db_settings)
        except Exception as ex :
            print(ex)
        else:
            with conn.cursor() as cursor:
                command = "SELECT * FROM %s "
                cursor.execute(command %(classes))
                result = cursor.fetchall()
                if result == ():
                    print("not found")
                    return "sqlnotfound"
                else:
                    return result
                # conn.commit()

    def use_sql_insert_msg(self,classes,name,times,msg_content):
        db_settings = {
            "host":"140.120.108.103",
            "port":3306,
            "user":"user",
            "password":"nchu_8520",
            "db":"course",
            "charset":"utf8"
        }
        try :
            conn = pymysql.connect(**db_settings)
        except Exception as ex :
            print(ex)
        else:
            # print(classes)
            # print(name)
            # print(times)
            # print(msg_content)
            with conn.cursor() as cursor:
                command = "INSERT INTO %s(from_name,times,message_content) VALUES('%s','%s','%s')"
                cursor.execute(command %(classes,name,times,msg_content))
                # result = cursor.fetchall()
                conn.commit()

    #獲取當前時間
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #按按鈕就會在另一個框框顯示東西 (這裡沒用到)
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #事件循環 或 保持進行 否則頁面不展示


gui_start()