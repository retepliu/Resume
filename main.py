# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:14:02 2021

@author: liu
"""

import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
import os,time,re,sqlite3
import pandas as pd
from myTools import get_soup
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import rate_count


# pd.set_option('display.max_rows', None)


class MainMenu():
    def __init__(self):
        self.df1=[]
        self.df2=[]
        self.num=[]
        self.datas=[]
        
        
        self.title_label()
        self.label()
        self.button()
        self.optionmenu()
        self.text()
    
        
    def title_label(self):
        self.label0=tk.Label(frame1,text='台灣銀行匯率看板：',font=('Arial',12),bg='black',fg='white',anchor='w')
        self.label0.pack(fill='x')
        
        
    def label(self):
        self.label_left=tk.Label(frame3,text=self.df1,anchor='w',bg='yellow',justify='left')
        self.label_right=tk.Label(frame3,text=self.df2,anchor='w',bg='yellow',justify='left')
        
        self.label_right.grid(row=1,column=1,padx=5,pady=5,sticky='nswe')
        self.label_left.grid(row=1,column=0,padx=5,pady=5,sticky='nswe')
        

    
    def optionmenu(self):
        global head
        self.varCash=tk.StringVar()
        self.varMonth=tk.StringVar()
        self.varChoice=tk.StringVar()
        self.varMonth_2=tk.StringVar()
        
        self.num=['美金(USD)','港幣(HKD)','英鎊(GBP)','澳幣(AUD)','加拿大幣(CAD)','新加坡幣(SGD)','瑞士法郎(CHF)',
                '日圓(JPY)','南非幣(ZAR)','瑞典幣(SEK)','紐元(NZD)','泰幣(THB)','菲國比索(PHP)','印尼幣(IDR)',
                '歐元(EUR)','韓元(KRW)','越南盾(VND)','馬來幣(MYR)','人民幣(CNY)']
        
        month=['三個月','六個月']
        choice=['歷史匯率.csv檔','歷史匯率.db檔']
        head='請選擇'
        
        
        self.om=ttk.OptionMenu(frame4, self.varCash, head, *self.num, direction='below',command=self.save)
        self.om.grid(row=1,column=0,padx=5,pady=10,sticky='nw')
        self.om.config(width=12)
        
        self.omChoice=ttk.OptionMenu(frame4, self.varChoice, head, *choice, direction='below',command=self.saveChoice)
        self.omChoice.grid(row=0,column=1,padx=5,pady=10,sticky='ne')
        self.omChoice.config(width=18)
        
        self.omMonth=ttk.OptionMenu(frame4, self.varMonth, head, *month, direction='below',command=self.saveMonth)
        self.omMonth.grid(row=0,column=0,padx=5,pady=10,sticky='e')
        self.omMonth.config(width=5)
        
        self.omMonth_2=ttk.OptionMenu(frame4, self.varMonth_2, head, *month, direction='below', command=self.saveMonth_2)
        self.omMonth_2.grid(row=1,column=1,padx=5,pady=10,sticky='w')
        self.omMonth_2.config(width=5)
        
        
    def button(self):
        self.btn_link=tk.Button(frame2,text='連結',font=(10),command=self.link)
        self.btn_link.grid(row=0,column=0,padx=10,pady=5,sticky='nw')
        
        self.btn_close=tk.Button(frame2,text='結束',font=(10),command=win.destroy)
        self.btn_close.grid(row=0,column=1,padx=10,pady=5,sticky='nw')
        
        self.btn_bank_info=ttk.Button(frame4,text='下載',width=10,command=self.select)
        self.btn_bank_info.grid(row=0,column=2,padx=20,pady=10,sticky='nw')
        
        self.btn_send=ttk.Button(frame4,text='歷史匯率',width=10,command=self.get_rate)
        self.btn_send.grid(row=1,column=1,padx=5,pady=10,sticky='ne')
        
        self.btn_plt=ttk.Button(frame4,text='匯率折線圖',width=10,command=self.get_plt)
        self.btn_plt.grid(row=1,column=2,padx=20,pady=10,sticky='e')
        
        self.btn_rate_count=ttk.Button(frame2,text='匯率試算',width=10,command=self.open_rate)
        self.btn_rate_count.grid(row=0,column=2,padx=170,pady=10,sticky='e')
        
        
        self.btn_clr=ttk.Button(frame4,text='清除',width=5,command=self.clear)
        self.btn_clr.grid(row=0,column=0,padx=10,pady=10,sticky='w')
        
    
    def clear(self):
        self.varMonth.set(head)
        self.varChoice.set(head)
        self.varCash.set(head)
        self.varMonth_2.set(head)
    
    
    def select(self):
        
        if self.varMonth.get() != head and self.varChoice.get() != head:
            if monthNum != '' and choiceNum != '':
                try:
                    if monthNum == '三個月' and choiceNum == '歷史匯率.csv檔':
                        self.get_bank_infos()
                        
                    elif monthNum == '六個月' and choiceNum == '歷史匯率.csv檔':
                        self.get_bank_infos_6m()
                    
                    elif monthNum == '三個月' and choiceNum == '歷史匯率.db檔':
                        self.tosql()
                        
                    elif monthNum == '六個月' and choiceNum == '歷史匯率.db檔':
                        self.tosql_6m()
                
                except Exception as e:
                    tk.messagebox.showwarning(title='Warning',message=e)
                
            
        elif self.varChoice.get() != head and self.varMonth.get() == head:
            tk.messagebox.showwarning(title='Warning',message='尚未選擇[期間]！')
        
        elif self.varMonth.get() != head and self.varChoice.get() == head:
            tk.messagebox.showwarning(title='Warning',message='尚未選擇[檔案類型]！')
            
        else:
            tk.messagebox.showwarning(title='Warning',message='尚未選擇！')
                
            
        
    def open_rate(self):
        rate_count.App(win)
        

    def text(self):
        self.t=tkst.ScrolledText(frame5)
        self.t.pack()
        
        
    def tosql(self):
        self.t.delete(1.0,'end')
       
        url='https://rate.bot.com.tw/xrt/history/USD?Lang=zh-TW'
    
        soup=get_soup(url)
    
        names=[]
        for option in soup.find(class_='input-medium').find_all('option'):
            names.append(option.text.strip())
    
        dollars=[]
        for name in names:
            i=''.join(re.findall(r'[A-Z]',name))
            dollars.append(i)
    
        for i in dollars:
            time.sleep(2)
            info_url=f'https://rate.bot.com.tw/xrt/quote/ltm/{i}'
            soup=get_soup(info_url)
            table=soup.find('table',class_='table table-striped table-bordered table-condensed table-hover')
            # print(info_url)
            columns=[]
            for tr in table.find('thead').find_all('tr'):
                column=[th.text.strip() for th in tr.find_all('th')]
                columns.append(list(filter(None,column)))
    
            nums=['date']+['rate']+['cash_buy']+['cash_sold']+['spot_buy']+['spot_sold']
    
            datas=[]
            for tr in table.find('tbody').find_all('tr'):
                tds=[td.text.strip() for td in tr.find_all('td')]
                tds=[td.replace('\n',' ').replace('\r',' ').replace(' ','') for td in tds]
                datas.append(tds)
    
            df=pd.DataFrame(datas,columns=nums)
            
            
            path='bank_sql/'
            name=i+'.db'
            filename=os.path.join(path, name)
            
            sqlstr='''
                create table if not exists data(
                    id integer primary key autoincrement,
                    date text,
                    rate text,
                    cash_buy interger,
                    cash_sold integer,
                    spot_buy integer,
                    spot_sold integer
                );
                '''
                  
            if not os.path.exists(path):
                os.mkdir(path)  
                
            if os.path.exists(filename):
                os.remove(filename)
                        
            with sqlite3.connect(filename) as connect:
                connect=sqlite3.connect(filename)
                cursor=connect.cursor()
                cursor.execute(sqlstr)
                connect.commit()
                # print(i+':建立資料庫(表)成功!')   
                
                with sqlite3.connect(filename) as connect:
                    df.to_sql('data',connect,if_exists='append',index=False)
    
            self.t.insert('insert',f'已儲存{i}.db\n')
            self.t.yview_moveto(1)
            self.t.update()
             
        self.t.insert('insert','下載完畢!')  
        
        
    def tosql_6m(self):
        self.t.delete(1.0,'end')
       
        url='https://rate.bot.com.tw/xrt/history/USD?Lang=zh-TW'
    
        soup=get_soup(url)
    
        names=[]
        for option in soup.find(class_='input-medium').find_all('option'):
            names.append(option.text.strip())
    
        dollars=[]
        for name in names:
            i=''.join(re.findall(r'[A-Z]',name))
            dollars.append(i)
    
        for i in dollars:
            time.sleep(2)
            info_url=f'https://rate.bot.com.tw/xrt/quote/l6m/{i}'
            soup=get_soup(info_url)
            table=soup.find('table',class_='table table-striped table-bordered table-condensed table-hover')
            # print(info_url)
            columns=[]
            for tr in table.find('thead').find_all('tr'):
                column=[th.text.strip() for th in tr.find_all('th')]
                columns.append(list(filter(None,column)))
    
            nums=['date']+['rate']+['cash_buy']+['cash_sold']+['spot_buy']+['spot_sold']
    
            datas=[]
            for tr in table.find('tbody').find_all('tr'):
                tds=[td.text.strip() for td in tr.find_all('td')]
                tds=[td.replace('\n',' ').replace('\r',' ').replace(' ','') for td in tds]
                datas.append(tds)
    
            df=pd.DataFrame(datas,columns=nums)
            
            
            path='bank_sql_6m/'
            name=i+'_6m.db'
            filename=os.path.join(path, name)
            
            sqlstr='''
                create table if not exists data(
                    id integer primary key autoincrement,
                    date text,
                    rate text,
                    cash_buy interger,
                    cash_sold integer,
                    spot_buy integer,
                    spot_sold integer
                );
                '''
                  
            if not os.path.exists(path):
                os.mkdir(path)  
                
            if os.path.exists(filename):
                os.remove(filename)
                        
            with sqlite3.connect(filename) as connect:
                connect=sqlite3.connect(filename)
                cursor=connect.cursor()
                cursor.execute(sqlstr)
                connect.commit()
                # print(i+':建立資料庫(表)成功!')   
                
                with sqlite3.connect(filename) as connect:
                    df.to_sql('data',connect,if_exists='append',index=False)
    
            self.t.insert('insert',f'已儲存{i}_6m.db\n')
            self.t.yview_moveto(1)
            self.t.update()
             
        self.t.insert('insert','下載完畢!')


    def link(self):

        url='https://rate.bot.com.tw/xrt?Lang=zh-TW'
    
        soup=get_soup(url)
        
        if soup != None:
        
            table = soup.find('table',class_='table table-striped table-bordered table-condensed table-hover')
            
            columns=[]
            for tr in table.find('thead').find_all('tr'):
                column=[th.text.strip() for th in tr.find_all('th')]
                columns.append(list(filter(None,column)))
                
            # columns_sec=[columns[1][0]]+[columns[1][1]]+[columns[1][2]]+[columns[1][3]]
            
            self.datas=[]
            for tr in table.find('tbody').find_all('tr'):
                tds=[td.text.strip() for td in tr.find_all('td')]
                tds=[td.replace('\n',' ').replace('\r',' ').replace(' ','') for td in tds]
                self.datas.append(tds)
                
            
                
            df=pd.DataFrame(self.datas,columns=['0','1','2','3','4','5','6','7','8','9','10'])
            
            df['0']=self.num
            
            df.drop(columns=['5','6','7','8','9','10'],inplace=True)
            
            c=['A','B','C','D']
            
            df.columns=[columns[0][0]]+c
        
            df1=df[['幣別','A','B']]
            df1.rename(columns={'A':'本行買入','B':'本行賣出'},inplace=True)
            self.df1=df1.set_index('幣別')
            
            df2=df[['幣別','C','D']]
            df2.rename(columns={'C':'本行買入','D':'本行賣出'},inplace=True)
            self.df2=df2.set_index('幣別')
            # print(self.num,self.df1,self.df2)
            
            time=soup.find('div',id='ie11andabove')
            newest_time=time.find('span',class_='time')
            newest_time=newest_time.text.strip()
            
            self.label0.config(text=f'台灣銀行匯率看板：{newest_time}',fg='red')
             
            self.label1=tk.Label(frame3,text='現金匯率',font=(10),anchor='e',fg='red',bg='yellow')
            self.label2=tk.Label(frame3,text='即期匯率',font=(10),anchor='w',fg='red',bg='yellow')
            
            self.label1.grid(row=0,column=0,padx=65,pady=5,sticky='nswe')
            self.label2.grid(row=0,column=1,padx=60,pady=5,sticky='nswe')
            
            self.label()

        else:
            return None
        
        
    def save(self, option):
        global rate
        rate=self.varCash.get()
        
    def saveChoice(self, option):
        global choiceNum
        choiceNum=self.varChoice.get()
        
    def saveMonth(self, option):
        global monthNum
        monthNum=self.varMonth.get()
        
    def saveMonth_2(self, option):
        global monthNum_2
        monthNum_2=self.varMonth_2.get()
        
  
    def get_rate(self):
        pd.set_option('display.max_rows', None)
        # print(rate)
        if self.varCash.get() != head and self.varMonth_2.get() != head:
            if rate != '' and monthNum_2 == '三個月':
                i=''.join(re.findall(r'[A-Z]',rate))
                path='bank/'
                try:
                    df=pd.read_csv(f'{path}/{i}.csv',encoding='utf-8-sig',index_col=0)
                    df.set_index('掛牌日期',inplace=True)
                    # df=df.iloc[::-1]
                
                    cash_rate=df[['幣別','現金本行買入','現金本行賣出']]
                    cash_rate.rename(columns={'現金本行買入':'本行買入','現金本行賣出':'本行賣出'},inplace=True)
                    
                    spot_rate=df[['幣別','即期本行買入','即期本行賣出']]
                    spot_rate.rename(columns={'即期本行買入':'本行買入','即期本行賣出':'本行賣出'},inplace=True)
                    
                    top=tk.Toplevel(win)
                    top.title(f'{i}歷史匯率')
                    top.geometry('500x350')
                    
                    canvas=tk.Canvas(top)
                    
                    scrollbar=tk.Scrollbar(top,orient='vertical',command=canvas.yview)
                    
                    frame=tk.Frame(canvas)
 
                    cash_title=tk.Label(frame,text='現金匯率',anchor='center',fg='red')
                    cash_title.grid(row=0,column=0,padx=5,pady=5,sticky='nswe')
                    cash_label=tk.Label(frame,text=cash_rate,anchor='center')
                    cash_label.grid(row=1,column=0,padx=5,pady=5,sticky='nswe')
                    
                    spot_title=tk.Label(frame,text='即期匯率',anchor='center',fg='red')
                    spot_title.grid(row=0,column=1,padx=5,pady=5,sticky='nswe')
                    spot_label=tk.Label(frame,text=spot_rate,anchor='center')
                    spot_label.grid(row=1,column=1,padx=5,pady=5,sticky='nswe')
                    
                    canvas.create_window(0, 0, anchor='nw', window=frame)
                    canvas.update_idletasks()
                    canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scrollbar.set)
                    
                    canvas.pack(side='left',fill='both',expand=True)
                    scrollbar.pack(side='right',fill='y')
                
                except Exception as e:
                    tk.messagebox.showwarning(title='Warning',message=e)
                
            elif rate != '' and monthNum_2 == '六個月':
                i=''.join(re.findall(r'[A-Z]',rate))
                path='bank_6m/'
                try:
                    df=pd.read_csv(f'{path}/{i}_6m.csv',encoding='utf-8-sig',index_col=0)
                    df.set_index('掛牌日期',inplace=True)
                    # df=df.iloc[::-1]
                
                    cash_rate=df[['幣別','現金本行買入','現金本行賣出']]
                    cash_rate.rename(columns={'現金本行買入':'本行買入','現金本行賣出':'本行賣出'},inplace=True)
                    
                    spot_rate=df[['幣別','即期本行買入','即期本行賣出']]
                    spot_rate.rename(columns={'即期本行買入':'本行買入','即期本行賣出':'本行賣出'},inplace=True)
                    
                    top=tk.Toplevel(win)
                    top.title(f'{i}歷史匯率')
                    top.geometry('500x350')
                    
                    canvas=tk.Canvas(top)
                    
                    scrollbar=tk.Scrollbar(top,orient='vertical',command=canvas.yview)
                    
                    frame=tk.Frame(canvas)
 
                    cash_title=tk.Label(frame,text='現金匯率',anchor='center',fg='red')
                    cash_title.grid(row=0,column=0,padx=5,pady=5,sticky='nswe')
                    cash_label=tk.Label(frame,text=cash_rate,anchor='center')
                    cash_label.grid(row=1,column=0,padx=5,pady=5,sticky='nswe')
                    
                    spot_title=tk.Label(frame,text='即期匯率',anchor='center',fg='red')
                    spot_title.grid(row=0,column=1,padx=5,pady=5,sticky='nswe')
                    spot_label=tk.Label(frame,text=spot_rate,anchor='center')
                    spot_label.grid(row=1,column=1,padx=5,pady=5,sticky='nswe')
                    
                    canvas.create_window(0, 0, anchor='nw', window=frame)
                    canvas.update_idletasks()
                    canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scrollbar.set)
                    
                    canvas.pack(side='left',fill='both',expand=True)
                    scrollbar.pack(side='right',fill='y')
                
                except Exception as e:
                    tk.messagebox.showwarning(title='Warning',message=e)
                    
                    
        elif self.varCash.get() != head and self.varMonth_2.get() == head:
            tk.messagebox.showwarning(title='Warning',message='請選擇期間！')
            
        elif self.varCash.get() == head and self.varMonth_2.get() != head:
            tk.messagebox.showwarning(title='Warning',message='請選擇幣別！')
                
        else:
            tk.messagebox.showwarning(title='Warning',message='請選擇幣別＆期間！')
                
                
                
    def get_plt(self):
        
        if self.varCash.get() != head and self.varMonth_2.get() != head:
            if rate != '' and monthNum_2 == '三個月':
                i=''.join(re.findall(r'[A-Z]',rate))
                path='bank/'
                try:
                    df=pd.read_csv(f'{path}/{i}.csv',encoding='utf-8-sig',index_col=0)
                    df.set_index('掛牌日期',inplace=True)
                    df=df.iloc[::-1]
                
                    cash_rate=df[['幣別','現金本行買入','現金本行賣出']]
                    cash_rate.rename(columns={'現金本行買入':'本行買入','現金本行賣出':'本行賣出'},inplace=True)
                    
                    spot_rate=df[['幣別','即期本行買入','即期本行賣出']]
                    spot_rate.rename(columns={'即期本行買入':'本行買入','即期本行賣出':'本行賣出'},inplace=True)
                    
                    
                    top_plt=tk.Toplevel(win)
                    top_plt.title(f'{i}匯率折線圖')
                    top_plt.geometry('1500x800')
                    
                    
                    canvas_plt=tk.Canvas(top_plt)
                    
                    scrollbar_plt=tk.Scrollbar(top_plt,orient='vertical',command=canvas_plt.yview)
                    
                    frame_plt=tk.Frame(canvas_plt)
                    
                    fig1=plt.figure(figsize=(20,12))
                    # fg1=fig1.add_subplot(111)
        
                    plt.title(f'{i}現金匯率',fontsize=16,pad=5)
                    plt.xlabel('日期',fontsize=14,labelpad=10)
                    plt.ylabel('匯率',fontsize=14,labelpad=20,rotation=0)
                
                    plt.grid(axis='y')
                    plt.plot(cash_rate.index,cash_rate['本行買入'],color='red',label='本行買入')
                
                    plt.plot(cash_rate.index,cash_rate['本行賣出'],color='blue',label='本行賣出')
                
                    plt.xticks(range(0,len(cash_rate.index),5),rotation=45)
                
                    plt.legend()
                    plt.show()
                
                    fig2=plt.figure(figsize=(20,12))
                    # fg2=fig2.add_subplot(111)
                
                    plt.title(f'{i}即期匯率',fontsize=16,pad=5)
                    plt.xlabel('日期',fontsize=14,labelpad=10)
                    plt.ylabel('匯率',fontsize=14,labelpad=20,rotation=0)
                
                    plt.grid(axis='y')
                    plt.plot(spot_rate.index,spot_rate['本行買入'],color='red',label='本行買入')
                
                    plt.plot(spot_rate.index,spot_rate['本行賣出'],color='blue',label='本行賣出')
                
                    plt.xticks(range(0,len(cash_rate.index),5),rotation=45)
                
                    plt.legend()
                    plt.show()
                    
                                    
                    canvas1=FigureCanvasTkAgg(fig1,frame_plt)
                    # canvas1.show()
                    canvas1.get_tk_widget().grid(row=0)
                    
                    canvas2=FigureCanvasTkAgg(fig2,frame_plt)
                    # canvas2.show()
                    canvas2.get_tk_widget().grid(row=1)
                    
                    
                    canvas_plt.create_window(0, 0, anchor='nw', window=frame_plt)
                    canvas_plt.update_idletasks()
                    canvas_plt.configure(scrollregion=canvas_plt.bbox('all'),yscrollcommand=scrollbar_plt.set)
                    
                    canvas_plt.pack(side='left',fill='both',expand=True)
                    scrollbar_plt.pack(side='right',fill='y')
                    
                except Exception as e:
                    tk.messagebox.showwarning(title='Warning',message=e)
                
            elif rate != '' and monthNum_2 == '六個月':
                i=''.join(re.findall(r'[A-Z]',rate))
                path='bank_6m/'
                try:
                    df=pd.read_csv(f'{path}/{i}_6m.csv',encoding='utf-8-sig',index_col=0)
                    df.set_index('掛牌日期',inplace=True)
                    df=df.iloc[::-1]
                
                    cash_rate=df[['幣別','現金本行買入','現金本行賣出']]
                    cash_rate.rename(columns={'現金本行買入':'本行買入','現金本行賣出':'本行賣出'},inplace=True)
                    
                    spot_rate=df[['幣別','即期本行買入','即期本行賣出']]
                    spot_rate.rename(columns={'即期本行買入':'本行買入','即期本行賣出':'本行賣出'},inplace=True)
                    
                    
                    top_plt=tk.Toplevel(win)
                    top_plt.title(f'{i}匯率折線圖')
                    top_plt.geometry('1500x800')
                    
                    
                    canvas_plt=tk.Canvas(top_plt)
                    
                    scrollbar_plt=tk.Scrollbar(top_plt,orient='vertical',command=canvas_plt.yview)
                    
                    frame_plt=tk.Frame(canvas_plt)
                    
                    fig1=plt.figure(figsize=(20,12))
                    # fg1=fig1.add_subplot(111)
        
                    plt.title(f'{i}現金匯率',fontsize=16,pad=5)
                    plt.xlabel('日期',fontsize=14,labelpad=10)
                    plt.ylabel('匯率',fontsize=14,labelpad=20,rotation=0)
                
                    plt.grid(axis='y')
                    plt.plot(cash_rate.index,cash_rate['本行買入'],color='red',label='本行買入')
                
                    plt.plot(cash_rate.index,cash_rate['本行賣出'],color='blue',label='本行賣出')
                
                    plt.xticks(range(0,len(cash_rate.index),5),rotation=45)
                
                    plt.legend()
                    plt.show()
                
                    fig2=plt.figure(figsize=(20,12))
                    # fg2=fig2.add_subplot(111)
                
                    plt.title(f'{i}即期匯率',fontsize=16,pad=5)
                    plt.xlabel('日期',fontsize=14,labelpad=10)
                    plt.ylabel('匯率',fontsize=14,labelpad=20,rotation=0)
                
                    plt.grid(axis='y')
                    plt.plot(spot_rate.index,spot_rate['本行買入'],color='red',label='本行買入')
                
                    plt.plot(spot_rate.index,spot_rate['本行賣出'],color='blue',label='本行賣出')
                
                    plt.xticks(range(0,len(cash_rate.index),5),rotation=45)
                
                    plt.legend()
                    plt.show()
                    
                                    
                    canvas1=FigureCanvasTkAgg(fig1,frame_plt)
                    # canvas1.show()
                    canvas1.get_tk_widget().grid(row=0)
                    
                    canvas2=FigureCanvasTkAgg(fig2,frame_plt)
                    # canvas2.show()
                    canvas2.get_tk_widget().grid(row=1)
                    
                    
                    canvas_plt.create_window(0, 0, anchor='nw', window=frame_plt)
                    canvas_plt.update_idletasks()
                    canvas_plt.configure(scrollregion=canvas_plt.bbox('all'),yscrollcommand=scrollbar_plt.set)
                    
                    canvas_plt.pack(side='left',fill='both',expand=True)
                    scrollbar_plt.pack(side='right',fill='y')
                    
                except Exception as e:
                    tk.messagebox.showwarning(title='Warning',message=e)
                    
                    
        elif self.varCash.get() != head and self.varMonth_2.get() == head:
            tk.messagebox.showwarning(title='Warning',message='請選擇期間！')
            
        elif self.varCash.get() == head and self.varMonth_2.get() != head:
            tk.messagebox.showwarning(title='Warning',message='請選擇幣別！')
            
        else:
            tk.messagebox.showwarning(title='Warning',message='請選擇幣別＆期間！')
        
       
    
    def get_bank_infos(self):
        
        self.t.delete(1.0,'end')
       
        url='https://rate.bot.com.tw/xrt/history/USD?Lang=zh-TW'
    
        soup=get_soup(url)
    
        names=[]
        for option in soup.find(class_='input-medium').find_all('option'):
            names.append(option.text.strip())
    
        dollars=[]
        for name in names:
            i=''.join(re.findall(r'[A-Z]',name))
            dollars.append(i)
    
        for i in dollars:
            time.sleep(2)
            info_url=f'https://rate.bot.com.tw/xrt/quote/ltm/{i}'
            soup=get_soup(info_url)
            table=soup.find('table',class_='table table-striped table-bordered table-condensed table-hover')
            # print(info_url)
            columns=[]
            for tr in table.find('thead').find_all('tr'):
                column=[th.text.strip() for th in tr.find_all('th')]
                columns.append(list(filter(None,column)))
    
            nums=[columns[0][0]]+[columns[0][2]]+['現金本行買入']+['現金本行賣出']+['即期本行買入']+['即期本行賣出']
    
            datas=[]
            for tr in table.find('tbody').find_all('tr'):
                tds=[td.text.strip() for td in tr.find_all('td')]
                tds=[td.replace('\n',' ').replace('\r',' ').replace(' ','') for td in tds]
                datas.append(tds)
    
            df=pd.DataFrame(datas,columns=nums)
            
            path='bank/'
    
            if not os.path.exists(path):
                os.mkdir(path)
    
            df.to_csv(f'{path}{i}.csv',encoding='utf-8-sig')
    
            self.t.insert('insert',f'已儲存{i}.csv\n')
            self.t.yview_moveto(1)
            self.t.update()
             
        self.t.insert('insert','下載完畢!')  
        
        
    def get_bank_infos_6m(self):
        self.t.delete(1.0,'end')
       
        url='https://rate.bot.com.tw/xrt/history/USD?Lang=zh-TW'
    
        soup=get_soup(url)
    
        names=[]
        for option in soup.find(class_='input-medium').find_all('option'):
            names.append(option.text.strip())
    
        dollars=[]
        for name in names:
            i=''.join(re.findall(r'[A-Z]',name))
            dollars.append(i)
    
        for i in dollars:
            time.sleep(2)
            info_url=f'https://rate.bot.com.tw/xrt/quote/l6m/{i}'
            soup=get_soup(info_url)
            table=soup.find('table',class_='table table-striped table-bordered table-condensed table-hover')
            # print(info_url)
            columns=[]
            for tr in table.find('thead').find_all('tr'):
                column=[th.text.strip() for th in tr.find_all('th')]
                columns.append(list(filter(None,column)))
    
            nums=[columns[0][0]]+[columns[0][2]]+['現金本行買入']+['現金本行賣出']+['即期本行買入']+['即期本行賣出']
    
            datas=[]
            for tr in table.find('tbody').find_all('tr'):
                tds=[td.text.strip() for td in tr.find_all('td')]
                tds=[td.replace('\n',' ').replace('\r',' ').replace(' ','') for td in tds]
                datas.append(tds)
    
            df=pd.DataFrame(datas,columns=nums)
            
            path='bank_6m/'
    
            if not os.path.exists(path):
                os.mkdir(path)
    
            df.to_csv(f'{path}{i}_6m.csv',encoding='utf-8-sig')
    
            self.t.insert('insert',f'已儲存{i}_6m.csv\n')
            self.t.yview_moveto(1)
            self.t.update()
             
        self.t.insert('insert','下載完畢!')  
        
        


if __name__ == '__main__':
    
    win = tk.Tk()
    win.title('匯率查詢')
    win.geometry('400x700')
    
    frame1=tk.Frame(win)
    frame2=tk.Frame(win,bg='yellow')
    frame3=tk.Frame(win,width=400,height=400,bg='yellow')
    frame4=tk.Frame(win,width=400,height=150)
    frame5=tk.Frame(win,width=400,height=78)
    
    
    frame1.pack(side='top',fill='x')
    
    frame2.pack(fill='x')
    # frame2.grid_propagate(0)
    frame3.pack(fill='x')
    frame3.grid_propagate(0)
    frame4.pack(fill='x')
    frame4.grid_propagate(0)
    frame5.pack(side='bottom',fill='x')
    frame5.grid_propagate(0)


    MainMenu()
    win.mainloop()