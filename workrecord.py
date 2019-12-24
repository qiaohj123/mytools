# -*- coding:utf-8 -*-
import wx
import time
from time import sleep
import math
import wx.grid
import pymysql
from selenium import webdriver
# from workdata.zentao.zentao import Zentao
'''
全局变量
login_name 登录系统用户名
now_time 系统默认当前日期
zenuser 禅道用户名
zenpasswd 禅道密码
realdate 项目工时日期
project  项目工时名称
protime  项目工时时长
'''
login_name = None
zenuser = None
zenpasswd = None
realdate = None
project = None
protime = None
now_time = time.strftime('%Y-%m-%d')




class Sql_operations(object):
    def __init__(self):
        self.db = pymysql.connect(host='192.169.3.9', user='root', password='123456', db='qhj001', port=3306, charset='utf8')
        self.cursor = self.db.cursor()

    def Select_usr(self,table):
        self.tablename = table
        sql = "select * from %s order by id DESC"%self.tablename
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception as err:
            print('查询失败，语句错误')

    def Select_data(self,table):
        self.tab = table
        sql = "select * from %s where name = '%s' order by id desc"%(self.tab,login_name)
        # sql = "select * from %s order by id DESC"%self.tab
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception as err:
            print('查询失败，语句错误')

    def Insert_data(self,table,name,proname,workdate,timenum):
        self.tablename = table
        self.name = name
        self.proname = proname
        self.workdate = workdate
        self.timenum = timenum
        sql = "insert into %s(name, proname, workdate, timenum) VALUES('%s','%s','%s','%s')"%(self.tablename,self.name,self.proname,self.workdate,self.timenum)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            self.db.rollback()
            print('提交工时数据失败%s'%(err))

    def Insert_bugdata(self,table,name,proname,bugtime,fatal,serious,common,suggestion):
        self.tablename = table
        self.name = name
        self.proname = proname
        self.bugtime = bugtime
        self.fatal = fatal
        self.serious = serious
        self.common = common
        self.suggestion = suggestion
        sql = "insert into %s(name, proname, bugtime, fatal, serious, Common, suggestion) VALUES('%s','%s','%s','%s','%s','%s','%s')"%(self.tablename,self.name,self.proname,self.bugtime,self.fatal,self.serious,self.common,self.suggestion)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            self.db.rollback()
            print('提交工时数据失败%s'%(err))

    def Select_condition(self,table,name,date,proname):
        self.table = table
        self.name = name
        self.date = date
        self.proname = proname
        sql = "select * from %s where name = '%s' AND workdate = '%s' AND proname = '%s'"%(self.table,self.name,self.date,self.proname)
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            print(data)
            return data
        except Exception as err:
            print('查询失败，语句错误')

    def User_mapping(self, loginname):
        global zenuser
        global zenpasswd
        self.logins_name = loginname
        sql = "select * from mapping where username = '%s'"%self.logins_name
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            zenuser = data[2]
            zenpasswd = data[3]
        except Exception as e:
            print('查询失败，语句错误')

    def __close__(self):
        self.db.close()


class UserLogin(wx.Frame):
    '''
    登录界面
    '''

    # 初始化登录界面
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(UserLogin, self).__init__(*args, **kw)
        # 设置窗口屏幕居中
        self.Center()
        # 创建窗口
        self.pnl = wx.Panel(self)
        # 调用登录界面函数
        self.LoginInterface()

    def LoginInterface(self):
        # 创建垂直方向box布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        #################################################################################
        # 创建logo静态文本，设置字体属性
        logo = wx.StaticText(self.pnl, label="测试二部工作记录")
        font = logo.GetFont()
        font.PointSize += 30
        font = font.Bold()
        logo.SetFont(font)
        # 添加logo静态文本到vbox布局管理器
        vbox.Add(logo, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=150)
        #################################################################################
        # 创建静态框
        sb_username = wx.StaticBox(self.pnl, label="用户名")
        sb_password = wx.StaticBox(self.pnl, label="密  码")
        # 创建水平方向box布局管理器
        hsbox_username = wx.StaticBoxSizer(sb_username, wx.HORIZONTAL)
        hsbox_password = wx.StaticBoxSizer(sb_password, wx.HORIZONTAL)
        # 创建用户名、密码输入框
        self.user_name = wx.TextCtrl(self.pnl, size=(210, 25))
        self.user_password = wx.TextCtrl(self.pnl, style = wx.TE_PASSWORD,size=(210, 25))
        # 添加用户名和密码输入框到hsbox布局管理器
        hsbox_username.Add(self.user_name, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_password.Add(self.user_password, 0, wx.EXPAND | wx.BOTTOM, 5)
        # 将水平box添加到垂直box
        vbox.Add(hsbox_username, proportion=0, flag=wx.CENTER | wx.TOP, border=30)
        vbox.Add(hsbox_password, proportion=0, flag=wx.CENTER)
        #################################################################################
        # 创建水平方向box布局管理器
        hbox = wx.BoxSizer()
        # 创建登录按钮、绑定事件处理
        login_button = wx.Button(self.pnl, label="登录", size=(80, 25))
        login_button.Bind(wx.EVT_BUTTON, self.LoginButton)
        # 添加登录按钮到hbox布局管理器
        hbox.Add(login_button, 0, flag=wx.EXPAND | wx.TOP, border=5)
        # 将水平box添加到垂直box
        vbox.Add(hbox, proportion=0, flag=wx.CENTER)
        #################################################################################
        # 设置面板的布局管理器vbox
        self.pnl.SetSizer(vbox)

    def LoginButton(self, event):
        global login_name
        op = Sql_operations()
        # 获取users表中的用户名和密码信息，返回为二维元组
        data = op.Select_usr("userdata")
        login_sign = ''
        # 匹配用户名和密码
        for i in data:
            if (i[1] == self.user_name.GetValue()) and (i[2] == self.user_password.GetValue()):
                login_sign = 1
                break
        if login_sign != 1:
            print("用户名或密码错误！")
        elif login_sign == 1:
            print("登录成功！")
            login_name = self.user_name.GetValue()
            operation = UserOperation(None, title="测试二部工作记录", size=(1024, 768))
            operation.Show()
            self.Close(True)


class UserOperation(wx.Frame):
    def __init__(self, *args, **kw):
        super(UserOperation, self).__init__(*args, **kw)
        # 设置窗口屏幕居中
        self.Center()
        # 创建窗口
        self.pnl = wx.Panel(self)
        # 调用操作界面函数
        self.OperationInterface()

    def OperationInterface(self):
        # 创建垂直方向box布局管理器
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        #################################################################################
        # 创建logo静态文本，设置字体属性
        logo = wx.StaticText(self.pnl, label="测试二部工作记录")
        font = logo.GetFont()
        font.PointSize += 30
        font = font.Bold()
        logo.SetFont(font)
        # 添加logo静态文本到vbox布局管理器
        self.vbox.Add(logo, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=5)
        #################################################################################
        # 创建静态框
        sb_button = wx.StaticBox(self.pnl, label="选择操作")
        # 创建垂直方向box布局管理器
        vsbox_button = wx.StaticBoxSizer(sb_button, wx.VERTICAL)
        # vsbox_button = wx.StaticBoxSizer(wx.VERTICAL)
        # vsbox_button.Add(sb_button,0, wx.EXPAND | wx.RIGHT, border=5)
        # 创建操作按钮、绑定事件处理
        workdate_button = wx.Button(self.pnl, id=10, label="工时登记", size=(150, 50))   # 查看信息
        bug_button = wx.Button(self.pnl, id=11, label="bug记录", size=(150, 50))     # 添加信息
        sum_button = wx.Button(self.pnl, id=12, label="工时统计", size=(150, 50))  # 删除信息
        quit_button = wx.Button(self.pnl, id=13, label="退出系统", size=(150, 50))        # 退出系统
        self.Bind(wx.EVT_BUTTON, self.ClickButton, id=10, id2=13)
        # 添加操作按钮到vsbox布局管理器
        vsbox_button.Add(workdate_button, 0, wx.EXPAND | wx.BOTTOM | wx.CENTER, 40)
        vsbox_button.Add(bug_button, 0, wx.EXPAND | wx.BOTTOM, 40)
        vsbox_button.Add(sum_button, 0, wx.EXPAND | wx.BOTTOM, 40)
        vsbox_button.Add(quit_button, 0, wx.EXPAND | wx.BOTTOM, 200)
        # 创建静态框
        sb_show_operation = wx.StaticBox(self.pnl, label="显示/操作窗口", size=(800, 500))
        # 创建垂直方向box布局管理器
        self.vsbox_show_operation = wx.StaticBoxSizer(sb_show_operation, wx.VERTICAL)
        # 创建水平方向box布局管理器
        hbox = wx.BoxSizer()
        hbox.Add(vsbox_button, 0, wx.EXPAND | wx.BOTTOM, 5)
        hbox.Add(self.vsbox_show_operation, 0, wx.EXPAND | wx.BOTTOM, 5)
        # 将hbox添加到垂直box
        self.vbox.Add(hbox, proportion=0, flag=wx.CENTER)
        #################################################################################
        self.pnl.SetSizer(self.vbox)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("工时登记操作！")
            inquire_button = AddOp(None, title="测试二部", size=(1024, 668))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("bug登记操作！")
            add_button = AddOpBug(None, title="测试二部", size=(1024, 668))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            print("工时统计操作！")
            del_button = InquireOp(None, title="测试二部", size=(1024, 768))
            del_button.Show()
            self.Close(True)
        elif source_id == 13:
            self.Close(True)
#

#继承UserOperation类，实现初始化操作界面
class InquireOp(UserOperation):
    def __init__(self, *args, **kw):
        super(InquireOp, self).__init__(*args, **kw)
        # 创建数据展示网格
        self.stu_grid = self.CreateGrid()
        # self.stu_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelleftClick)
        # 添加到vsbox_show_operation布局管理器
        self.Select_operation()
        self.vsbox_show_operation.Add(self.stu_grid, 0, wx.LEFT | wx.TOP,0)


    def Select_operation(self):
        # 创建水平方向布局管理器
        hbox = wx.BoxSizer()
        # lastpage = wx.Button(self.pnl, label='下一页', size=(80, 25))
        # lastpage2 = wx.Button(self.pnl, label='上一页', size=(80, 25))
        #
        # # 添加登录按钮到hbox布局管理器
        # hbox.Add(lastpage, 0, flag=wx.EXPAND | wx.TOP, border=5)
        # hbox.Add(lastpage2, 0, flag=wx.EXPAND | wx.TOP, border=5)
        # # 将水平box添加到垂直box
        # self.vsbox_show_operation.Add(hbox, 0, wx.LEFT | wx.TOP, 0)

        self.emp_name = wx.TextCtrl(self.pnl, size=(110, 25))
        self.work_date = wx.TextCtrl(self.pnl, size=(110, 25))
        self.pro_name = wx.TextCtrl(self.pnl, size=(110, 25))
        self.select_affirm = wx.Button(self.pnl, id=14, label="查询", size=(80, 25))
        # # 为添加按钮组件绑定事件处理
        self.select_affirm.Bind(wx.EVT_BUTTON, self.ClickButton, id=14)
        # self.sel_grid = self.CreateGrid_cod()
        # self.vsbox_show_operation.Add(self.sel_grid, 0, wx.LEFT | wx.TOP, 0)
        #################################################################################
        # 创建静态框
        sb_name = wx.StaticText(self.pnl, label="姓  名：")
        sb_date = wx.StaticText(self.pnl, label="日期月份：")
        sb_pro = wx.StaticText(self.pnl, label="项目名称：")

        # ## 创建水平方向布局管理
        hbox.Add(sb_name, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(self.emp_name, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(sb_date, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(self.work_date, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(sb_pro, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(self.pro_name, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(self.select_affirm, 0, flag=wx.EXPAND | wx.TOP, border=10)
        # ## 创建水平方向布局管理
        # name_hos = wx.StaticBoxSizer(sb_name, wx.HORIZONTAL)
        # date_hos = wx.StaticBoxSizer(sb_date, wx.HORIZONTAL)
        # pro_hos = wx.StaticBoxSizer(sb_pro, wx.HORIZONTAL)
        # 加入到水平管理布局
        # hbox.Add(self.emp_name, 0, flag=wx.EXPAND | wx.TOP, border=10)
        # hbox.Add(self.pro_name, 0, flag=wx.EXPAND | wx.TOP, border=10)
        # hbox.Add(self.work_date, 0, flag=wx.EXPAND | wx.TOP, border=10)
        #

        # name_hos.Add(self.emp_name, 0, wx.EXPAND | wx.BOTTOM, 5)
        # date_hos.Add(self.pro_name, 0, wx.EXPAND | wx.BOTTOM, 5)
        # pro_hos.Add(self.work_date, 0, wx.EXPAND | wx.BOTTOM, 5)
        self.vsbox_show_operation.Add(hbox, 0, wx.LEFT | wx.TOP, 0)


    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("工时登记操作！")
            inquire_button = AddOp(None, title="测试二部", size=(1024, 668))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("bug登记操作！")
            add_button = AddOpBug(None, title="测试二部", size=(1024, 668))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            print("工时统计操作！")
            del_button = InquireOp(None, title="测试二部", size=(1024, 768))
            del_button.Show()
            self.Close(True)
        elif source_id == 14:
            print("查询统计操作！")
            del_button = SelecOp(None, title="测试二部", size=(1024, 768))
            del_button.Show()
            self.Close(True)
        elif source_id == 13:
            self.Close(True)

    # def CreateGrid(self):
    #     # 连接login_users数据库
    #     op = Sql_operations()
    #     np = op.Select_data("prodata")
    #     column_names = ("姓名", "项目名称", "工时日期", "工时时长(小时)")
    #     stu_grid = wx.grid.Grid(self.pnl)
    #     stu_grid.CreateGrid(len(np), len(np[0])-1)
    #     for row in range(len(np)):
    #         stu_grid.SetRowLabelValue(row, str(np[row][0]))  # 确保网格序列号与数据库id保持一致
    #         for col in range(1, len(np[row])):
    #             stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
    #             stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
    #     stu_grid.AutoSize()
    #     # stu_grid.SetTable(table)
    #     stu_grid.SetColSize(0,50)
    #     stu_grid.SetColSize(1,150)
    #     stu_grid.SetColSize(2,150)
    #     stu_grid.SetColSize(3,100)
    #     return stu_grid
    def CreateGrid(self):
        # 连接login_users数据库
        op = Sql_operations()
        np = op.Select_data("prodata")
        column_names = ("姓名", "项目名称", "工时日期", "工时时长(小时)")
        stu_grid = wx.grid.Grid(self.pnl)
        rows = len(np)
        # stu_grid.CreateGrid(rows, len(np[0])-1)
        if rows <= 20:
            stu_grid.CreateGrid(rows, len(np[0]) - 1)
            for row in range(rows):
                stu_grid.SetRowLabelValue(row, str(row+1))  # 确保网格序列号与数据库id保持一致
                for col in range(1, len(np[row])):
                    stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
                    stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
        else:
            stu_grid.CreateGrid(rows, len(np[0]) - 1)
            for row in range(rows):
                stu_grid.SetRowLabelValue(row, str(row+1))
                for col in range(1, len(np[row])):
                    stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
                    stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
        stu_grid.AutoSize()
        # stu_grid.SetTable(table)
        stu_grid.SetColSize(0,50)
        stu_grid.SetColSize(1,150)
        stu_grid.SetColSize(2,150)
        stu_grid.SetColSize(3,100)
        return stu_grid


    # def CreateGrid_cod(self):              # 条件查询
    #     # 连接login_users数据库
    #     myname = self.emp_name.GetValue()
    #     date = self.work_date.GetValue()
    #     proname = self.pro_name.GetValue()
    #     op = Sql_operations()
    #     np = op.Select_condition("prodata",myname,date,proname)
    #     print(np)
    #     column_names = ("姓名", "项目名称", "工时日期", "工时时长(小时)")
    #     stu_grid = wx.grid.Grid(self.pnl)
    #     rows = len(np)
    #     # stu_grid.CreateGrid(rows, len(np[0])-1)
    #     if rows <= 20:
    #         stu_grid.CreateGrid(rows, len(np[0]) - 1)
    #         for row in range(rows):
    #             stu_grid.SetRowLabelValue(row, str(row+1))  # 确保网格序列号与数据库id保持一致
    #             for col in range(1, len(np[row])):
    #                 stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
    #                 stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
    #     else:
    #         stu_grid.CreateGrid(rows, len(np[0]) - 1)
    #         for row in range(rows):
    #             stu_grid.SetRowLabelValue(row, str(row+1))
    #             for col in range(1, len(np[row])):
    #                 stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
    #                 stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
    #     stu_grid.AutoSize()
    #     # stu_grid.SetTable(table)
    #     stu_grid.SetColSize(0,50)
    #     stu_grid.SetColSize(1,150)
    #     stu_grid.SetColSize(2,150)
    #     stu_grid.SetColSize(3,100)
    #     return stu_grid

    def CreateGrid_cod2(self,event):              # 条件查询
        # 连接login_users数据库
        myname = self.emp_name.GetValue()
        date = self.work_date.GetValue()
        proname = self.pro_name.GetValue()
        op = Sql_operations()
        np = op.Select_condition("prodata",myname,date,proname)
        column_names = ("姓名", "项目名称", "工时日期", "工时时长(小时)")
        stu_grid = wx.grid.Grid(self.pnl)
        rows = len(np)
        # stu_grid.CreateGrid(rows, len(np[0])-1)
        if rows <= 20:
            stu_grid.CreateGrid(rows, len(np[0]) - 1)
            for row in range(rows):
                stu_grid.SetRowLabelValue(row, str(row+1))  # 确保网格序列号与数据库id保持一致
                for col in range(1, len(np[row])):
                    stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
                    stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
        else:
            stu_grid.CreateGrid(rows, len(np[0]) - 1)
            for row in range(rows):
                stu_grid.SetRowLabelValue(row, str(row+1))
                for col in range(1, len(np[row])):
                    stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
                    stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
        stu_grid.AutoSize()
        # stu_grid.SetTable(table)
        stu_grid.SetColSize(0,50)
        stu_grid.SetColSize(1,150)
        stu_grid.SetColSize(2,150)
        stu_grid.SetColSize(3,100)
        return stu_grid


    def Lastpage(self,event):
        op = Sql_operations()
        np = op.Select_data("prodata")
        column_names = ("姓名", "项目名称", "工时日期", "工时时长(小时)")
        stu_grid = wx.grid.Grid(self.pnl)
        rows = len(np)
        pages = math.floor(rows/20)
        if pages > 1:
            for row in range(20):
                stu_grid.SetRowLabelValue(row, str(row + 1))
                for col in range(1, len(np[row])):
                    stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
                    stu_grid.SetCellValue(row, col - 1, str(np[row+20][col]))
        stu_grid.AutoSize()
        # stu_grid.SetColSize(0, 50)
        # stu_grid.SetColSize(1, 150)
        # stu_grid.SetColSize(2, 150)
        # stu_grid.SetColSize(3, 100)
        return stu_grid

    def OnLabelleftClick(self, event):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        # 获取users表中的用户名和密码信息，返回为二维元组
        np = op.FindAll("stu_info")
        print("RowIdx: {0}".format(event.GetRow()))
        print("ColIdx: {0}".format(event.GetRow()))
        print(np[event.GetRow()])
        event.Skip()

class SelecOp(UserOperation):
    def __init__(self, *args, **kw):
        super(SelecOp, self).__init__(*args, **kw)
        # 创建数据展示网格
        self.stus_grid = self.CreateGrid_cod()
        # self.stu_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelleftClick)
        # 添加到vsbox_show_operation布局管理器
        self.vsbox_show_operation.Add(self.stus_grid, 0,)

    def CreateGrid_cod(self):  # 条件查询
        hbox = wx.BoxSizer()
        self.emps_name = wx.TextCtrl(self.pnl, size=(110, 25))
        self.works_date = wx.TextCtrl(self.pnl, size=(110, 25))
        self.pros_name = wx.TextCtrl(self.pnl, size=(110, 25))
        self.selects_affirm = wx.Button(self.pnl, id=14, label="查询", size=(80, 25))
        # # 为添加按钮组件绑定事件处理
        self.selects_affirm.Bind(wx.EVT_BUTTON, self.ClickButton, id=14)

        # 创建静态框
        sb_name = wx.StaticText(self.pnl, label="姓  名：")
        sb_date = wx.StaticText(self.pnl, label="日期月份：")
        sb_pro = wx.StaticText(self.pnl, label="项目名称：")

        # ## 创建水平方向布局管理
        hbox.Add(sb_name, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(self.emps_name, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(sb_date, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(self.works_date, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(sb_pro, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(self.pros_name, 0, flag=wx.EXPAND | wx.TOP, border=10)
        hbox.Add(self.selects_affirm, 0, flag=wx.EXPAND | wx.TOP, border=10)
        self.vsbox_show_operation.Add(hbox, 0, wx.LEFT | wx.TOP, 0)

        # 连接login_users数据库
        # inop = InquireOp()
        # myname = inop.emp_name.GetValue()
        # date = inop.work_date.GetValue()
        # proname = inop.pro_name.GetValue()


        myname = self.emps_name.GetValue()
        date = self.works_date.GetValue()
        proname = self.pros_name.GetValue()
        op = Sql_operations()
        np = op.Select_condition("prodata", myname, date, proname)
        column_names = ("姓名", "项目名称", "工时日期", "工时时长(小时)")
        stus_grid = wx.grid.Grid(self.pnl)
        rows = len(np)
        if rows == 0:
            return stus_grid
        else:
            # stu_grid.CreateGrid(rows, len(np[0])-1)
            if rows <= 20:
                stus_grid.CreateGrid(rows, len(np[0]) - 1)
                for row in range(rows):
                    stus_grid.SetRowLabelValue(row, str(row + 1))  # 确保网格序列号与数据库id保持一致
                    for col in range(1, len(np[row])):
                        stus_grid.SetColLabelValue(col - 1, column_names[col - 1])
                        stus_grid.SetCellValue(row, col - 1, str(np[row][col]))
            else:
                stus_grid.CreateGrid(rows, len(np[0]) - 1)
                for row in range(rows):
                    stus_grid.SetRowLabelValue(row, str(row + 1))
                    for col in range(1, len(np[row])):
                        stus_grid.SetColLabelValue(col - 1, column_names[col - 1])
                        stus_grid.SetCellValue(row, col - 1, str(np[row][col]))
            stus_grid.AutoSize()
            # stu_grid.SetTable(table)
            stus_grid.SetColSize(0, 50)
            stus_grid.SetColSize(1, 150)
            stus_grid.SetColSize(2, 150)
            stus_grid.SetColSize(3, 100)
            return stus_grid


# 继承UserOperation类，实现初始化操作界面
class AddOp(UserOperation):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(AddOp, self).__init__(*args, **kw)
        # 创
        self.emp_name = wx.TextCtrl(self.pnl, size=(210, 25),style = wx.TE_READONLY)
        self.pro_name = wx.TextCtrl(self.pnl, size=(210, 25))
        self.work_date = wx.TextCtrl(self.pnl, size=(210, 25))
        self.work_time = wx.TextCtrl(self.pnl, size=(210, 25))
        self.add_affirm = wx.Button(self.pnl, label="提交保存", size=(80, 25))

        self.emp_name.SetValue(login_name)
        self.work_date.SetValue(now_time)
        # 为添加按钮组件绑定事件处理
        self.add_affirm.Bind(wx.EVT_BUTTON, self.AddAffirm)
        #################################################################################
        # 创建静态框
        sb_name = wx.StaticBox(self.pnl, label="姓  名")
        sb_pro = wx.StaticBox(self.pnl, label="项目名称")
        sb_date = wx.StaticBox(self.pnl, label="工时日期")
        sb_time = wx.StaticBox(self.pnl, label="工时时长（小时）")
        # 创建水平方向box布局管理器
        hsbox_name = wx.StaticBoxSizer(sb_name, wx.HORIZONTAL)
        hsbox_pro = wx.StaticBoxSizer(sb_pro, wx.HORIZONTAL)
        hsbox_date = wx.StaticBoxSizer(sb_date, wx.HORIZONTAL)
        hsbox_time = wx.StaticBoxSizer(sb_time, wx.HORIZONTAL)
        # 添加到hsbox布局管理器
        hsbox_name.Add(self.emp_name, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_pro.Add(self.pro_name, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_date.Add(self.work_date, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_time.Add(self.work_time, 0, wx.EXPAND | wx.BOTTOM, 5)
        #################################################################################
        # 添加到vsbox_show_operation布局管理器
        self.vsbox_show_operation.Add(hsbox_name, 0, wx.LEFT | wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_pro, 0, wx.LEFT |  wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_date, 0, wx.LEFT | wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_time, 0, wx.LEFT |  wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(self.add_affirm, 0, wx.LEFT |  wx.FIXED_MINSIZE, 50)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("工时登记操作！")
            inquire_button = AddOp(None, title="测试二部", size=(1024, 668))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("bug登记操作！")
            add_button = AddOpBug(None, title="测试二部", size=(1024, 668))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            print("工时统计操作！")
            del_button = InquireOp(None, title="测试二部", size=(1024, 668))
            del_button.Show()
            self.Close(True)
        elif source_id == 13:
            self.Close(True)

    def Zentao(self,username, passwd, proname, recdate, reclong):
        id = Id()
        name = Name()
        css = Css()
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')  # 设置option
        # dr = webdriver.Chrome(chrome_options=option)  # 调用带参数的谷歌浏览器
        dr = webdriver.Chrome()
        dr.get('http://192.169.2.79/zentao/')
        sleep(2)
        id.by_id_s(dr, 'account', username)
        name.by_name_s(dr, 'password', passwd)
        id.by_id_c(dr, 'submit')
        sleep(3)
        css.by_css_c(dr, 'li[data-id="my"]')
        sleep(2)
        css.by_css_c(dr, 'li[data-id="task"]')
        sleep(2)

        table = id.by_id(dr, 'tasktable')
        table_rows = table.find_elements_by_tag_name('tr')  # 获取表格行数

        for i in range(1, len(table_rows)):
            txt = table_rows[i].find_elements_by_tag_name('td')[2].text
            if proname in txt:
                print(i, txt)
                i = str(i)
                try:
                    dr.find_element_by_xpath('//*[@id="tasktable"]/tbody/tr[' + i + ']/td[13]/a[2]').click()
                except Exception as e:
                    pass
                sleep(4)
                dr.switch_to.frame('iframe-triggerModal')
                id.by_id_s(dr, 'dates[1]', recdate)
                id.by_id_s(dr, 'consumed[1]', reclong)
                id.by_id_s(dr, 'left[1]', '1')
                id.by_id_s(dr, 'work[1]', '功能测试')
                sleep(3)
                id.by_id_c(dr, 'submit')
            else:
                print(txt)
        dr.close()

    def AddAffirm(self, event):
        # 连接login_users数据库
        global login_name
        global realdate
        global project
        global protime
        op = Sql_operations()
        empname = self.emp_name.GetValue()
        project = self.pro_name.GetValue()
        realdate = self.work_date.GetValue()
        protime = self.work_time.GetValue()
        op.Insert_data('prodata',empname, project, realdate, protime)
        # op.User_mapping(login_name)
        # print(project,realdate,protime)
        # Zentao(zenuser,zenpasswd,project,realdate,protime)

        # self.emp_name.Remove(0, 20)
        # self.pro_name.Remove(0, 20)
        # self.work_date.Remove(0, 20)
        self.work_time.Remove(0, 20)
#
# 继承UserOperation类，实现初始化操作界面
class AddOpBug(UserOperation):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(AddOpBug, self).__init__(*args, **kw)

        self.rec_name = wx.TextCtrl(self.pnl, size=(210, 25), style = wx.TE_READONLY)
        self.rec_pro = wx.TextCtrl(self.pnl, size=(210, 25))
        self.rec_date = wx.TextCtrl(self.pnl, size=(210, 25))
        self.rec_fatal = wx.TextCtrl(self.pnl, size=(210, 25))
        self.rec_serious = wx.TextCtrl(self.pnl, size=(210, 25))
        self.rec_common = wx.TextCtrl(self.pnl, size=(210, 25))
        self.rec_suggestion = wx.TextCtrl(self.pnl, size=(210, 25))
        self.add_affirm = wx.Button(self.pnl, label="提交保存", size=(80, 25))
        # 设置默认值
        self.rec_name.SetValue(login_name)
        self.rec_date.SetValue(now_time)
        self.rec_fatal.SetValue('0')
        self.rec_serious.SetValue('0')
        self.rec_common.SetValue('0')
        self.rec_suggestion.SetValue('0')

        # 为添加按钮组件绑定事件处理
        self.add_affirm.Bind(wx.EVT_BUTTON, self.AddAffirm)
        #################################################################################
        # 创建静态框
        sb_name = wx.StaticBox(self.pnl, label="姓  名")
        sb_pro = wx.StaticBox(self.pnl, label="项目名称")
        sb_date = wx.StaticBox(self.pnl, label="bug记录日期")
        sb_fatal = wx.StaticBox(self.pnl, label="致  命")
        sb_serious = wx.StaticBox(self.pnl, label="严  重")
        sb_common = wx.StaticBox(self.pnl, label="一  般")
        sb_suggestion = wx.StaticBox(self.pnl, label="改进建议")
        # 创建水平方向box布局管理器
        hsbox_name = wx.StaticBoxSizer(sb_name, wx.HORIZONTAL)
        hsbox_pro = wx.StaticBoxSizer(sb_pro, wx.HORIZONTAL)
        hsbox_date = wx.StaticBoxSizer(sb_date, wx.HORIZONTAL)
        hsbox_fatal = wx.StaticBoxSizer(sb_fatal, wx.HORIZONTAL)
        hsbox_serious = wx.StaticBoxSizer(sb_serious, wx.HORIZONTAL)
        hsbox_common = wx.StaticBoxSizer(sb_common, wx.HORIZONTAL)
        hsbox_suggestion = wx.StaticBoxSizer(sb_suggestion, wx.HORIZONTAL)
        # 添加到hsbox布局管理器
        hsbox_name.Add(self.rec_name, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_pro.Add(self.rec_pro, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_date.Add(self.rec_date, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_fatal.Add(self.rec_fatal, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_serious.Add(self.rec_serious, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_common.Add(self.rec_common, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_suggestion.Add(self.rec_suggestion, 0, wx.EXPAND | wx.BOTTOM, 5)
        #################################################################################
        # 添加到vsbox_show_operation布局管理器
        self.vsbox_show_operation.Add(hsbox_name, 0, wx.LEFT | wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_pro, 0, wx.LEFT | wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_date, 0, wx.LEFT |wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_fatal, 0, wx.LEFT | wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_serious, 0, wx.LEFT | wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_common, 0, wx.LEFT |wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(hsbox_suggestion, 0, wx.LEFT | wx.FIXED_MINSIZE, 50)
        self.vsbox_show_operation.Add(self.add_affirm, 0, wx.LEFT |  wx.FIXED_MINSIZE, 50)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("工时登记操作！")
            inquire_button = AddOp(None, title="测试二部", size=(1024, 668))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("bug登记操作！")
            add_button = AddOpBug(None, title="测试二部", size=(1024, 668))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            print("工时统计操作！")
            del_button = InquireOp(None, title="测试二部", size=(1024, 668))
            del_button.Show()
            self.Close(True)
        elif source_id == 13:
            self.Close(True)

    def AddAffirm(self, event):
        # 连接login_users数据库
        op = Sql_operations()
        rec_name = self.rec_name.GetValue()
        rec_pro = self.rec_pro.GetValue()
        rec_date = self.rec_date.GetValue()
        rec_fatal = self.rec_fatal.GetValue()
        rec_serious = self.rec_serious.GetValue()
        rec_common = self.rec_common.GetValue()
        rec_suggestion = self.rec_suggestion.GetValue()
        np = op.Insert_bugdata('bugrecord',rec_name, rec_pro, rec_date, rec_fatal,rec_serious,rec_common,rec_suggestion)
        # self.rec_name.Remove(0, 20)
        # self.rec_pro.Remove(0, 20)
        # self.rec_date.Remove(0, 20)
        self.rec_fatal.Remove(0, 20)
        self.rec_serious.Remove(0, 20)
        self.rec_common.Remove(0, 20)
        self.rec_suggestion.Remove(0, 20)




# # 继承InquireOp类，实现初始化操作界面
# class DelOp(InquireOp):
#     def __init__(self, *args, **kw):
#         # ensure the parent's __init__ is called
#         super(DelOp, self).__init__(*args, **kw)
#         # 创建删除学员信息输入框、删除按钮
#         self.del_id = wx.TextCtrl(self.pnl, pos=(407, 78), size=(210, 25))
#         self.del_affirm = wx.Button(self.pnl, label="删除", pos=(625, 78), size=(80, 25))
#         # 为删除按钮组件绑定事件处理
#         self.del_affirm.Bind(wx.EVT_BUTTON, self.DelAffirm)
#         #################################################################################
#         # 创建静态框
#         sb_del = wx.StaticBox(self.pnl, label="请选择需要删除的学生id")
#         # 创建水平方向box布局管理器
#         hsbox_del = wx.StaticBoxSizer(sb_del, wx.HORIZONTAL)
#         # 添加到hsbox_name布局管理器
#         hsbox_del.Add(self.del_id, 0, wx.EXPAND | wx.BOTTOM, 5)
#         # 添加到vsbox_show_operation布局管理器
#         self.vsbox_show_operation.Add(hsbox_del, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
#         self.vsbox_show_operation.Add(self.del_affirm, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
#
#     def ClickButton(self, event):
#         source_id = event.GetId()
#         if source_id == 10:
#             print("查询操作！")
#             inquire_button = InquireOp(None, title="CSDN学生信息管理系统", size=(1024, 668))
#             inquire_button.Show()
#             self.Close(True)
#         elif source_id == 11:
#             print("添加操作！")
#             add_button = AddOp(None, title="", size=(1024, 668))
#             add_button.Show()
#             self.Close(True)
#         elif source_id == 12:
#             pass
#         elif source_id == 13:
#             self.Close(True)
#
#     def DelAffirm(self, event):
#         # 连接login_users数据库
#         op = Sql_operation("login_users")
#         # 向stu_information表添加学生信息
#         del_id = self.del_id.GetValue()
#         print(del_id)
#         np = op.Del(int(del_id))
#
#         del_button = DelOp(None, title="", size=(1024, 668))
#         del_button.Show()
#         self.Close(True)


if __name__ == '__main__':
    app = wx.App()
    login = UserLogin(None, title="测试二部工作记录系统", size=(1024, 668))
    login.Show()
    app.MainLoop()
