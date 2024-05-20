# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 00:55:09 2021

@author: liu
"""

import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
import os,time,re
import pandas as pd
from myTools import get_soup
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App_start:  
    def __init__(self, f1, f2):
        self.f1=f1
        self.f2=f2
        self.num=[]
        self.info=[]
        self.cash=[]
        self.cash_buy=[]
        self.cash_sell=[]
        self.spot_buy=[]
        self.spot_sell=[]
        self.y=''
        self.z=''
        self.rate2=''
        self.entry_num1=''
        self.entry_num2=''
        
        self.button()
        self.entry()
        # self.text()
        self.label()
        self.radio()
        self.optionmenu()
        self.rate_info()
        self.bind()
        
        
    
    def label(self):
        self.la1=tk.Label(self.f1,text='交易種類',font=(16),anchor='center')
        self.la1.grid(row=0,column=0,padx=5,pady=15,sticky='w')
        
        self.la2=tk.Label(self.f1,text='匯率種類',font=(16),anchor='center')
        self.la2.grid(row=1,column=0,padx=5,pady=15,sticky='w')
        
        self.la3=tk.Label(self.f1,text='交易幣別',font=(16),anchor='center')
        self.la3.grid(row=2,column=0,padx=5,pady=15,sticky='w')
        
        self.la4=tk.Label(self.f1,text='交易匯率',font=(16),anchor='center')
        self.la4.grid(row=3,column=0,padx=5,pady=15,sticky='w')
        
        self.laNum=tk.Label(self.f2,text=self.info,font=(12),fg='red',anchor='center')
        self.laNum.grid(row=3,column=1,padx=10,pady=15,sticky='nswe')
        
        self.la5=tk.Label(self.f1,text='新台幣',font=(12),anchor='center')
        self.la5.grid(row=4,column=0,padx=5,pady=15,sticky='w')
        
        self.la6=tk.Label(self.f1,text=self.cash,font=(12),anchor='w')
        self.la6.grid(row=5,column=0,padx=5,pady=15,sticky='nswe')
        
        
    def radio(self):
        self.var=tk.StringVar()
        self.var_rate=tk.StringVar()
        
        self.r1=tk.Radiobutton(self.f2,text='我要買進',font=(12),variable=self.var,value='A',command=self.radio_select)
        self.r1.grid(row=0,column=1,pady=15,sticky='nswe')
        # self.r1.grid_propagate(0)
        
        self.r2=tk.Radiobutton(self.f2,text='我要賣出',font=(12),variable=self.var,value='B',command=self.radio_select)
        self.r2.grid(row=0,column=2,pady=15,sticky='nw')
        # self.r2.grid_propagate(0)
        
        
        self.r3=tk.Radiobutton(self.f2,text='現鈔\t',font=(12),variable=self.var_rate,value='C',command=self.radio_rate_select)
        self.r3.grid(row=1,column=1,padx=5,pady=15,sticky='nswe')
        # self.r3.grid_propagate(0)
        
        self.r4=tk.Radiobutton(self.f2,text='即期',font=(12),variable=self.var_rate,value='D',command=self.radio_rate_select)
        self.r4.grid(row=1,column=2,pady=15,sticky='nw')
        # self.r4.grid_propagate(0)
        
        self.var.set('A')
        self.var_rate.set('C')
    
        self.radio_select()
        self.radio_rate_select()
        
        
    def optionmenu(self):
        global head
        head='請選擇'
        self.varKind=tk.StringVar()

        self.omRate=ttk.OptionMenu(self.f2, self.varKind, head, *self.num, direction='below',command=self.rate_save)
        self.omRate.grid(row=2,column=1,padx=60,pady=15,sticky='nswe')
        self.omRate.config(width=15)
        
        
    def radio_select(self):
        value=self.var.get()
        
        if value == 'A':
            self.y = 1
            
        if value == 'B':
            self.y = 2
           
        self.rate_sum()
        # self.entry1_count()
        # self.entry2_count()
        self.bind()
        
        
    def radio_rate_select(self):
        rate_value=self.var_rate.get()
        
        if rate_value == 'C':
            self.z = 1
            
        if rate_value == 'D':
            self.z = 2
            
        self.rate_sum()
        # self.entry1_count()
        # self.entry2_count()
        self.bind()
            
    # def text(self):
        
    #     self.text1=tk.Text(self.f2,width=30,height=1)
    #     self.text1.grid(row=4,column=1,padx=10,pady=15,sticky='ne')
        
    #     self.text2=tk.Text(self.f2,width=30,height=1)
    #     self.text2.grid(row=5,column=1,padx=10,pady=15,sticky='ne')
        
        
        
    #     a=self.text1.get('1.0','end')
    #     print(a)
    #     self.text2.insert('insert',a*100)
    #     self.text2.update()
    
    def entry(self):
        self.num1=tk.StringVar()
        self.num2=tk.StringVar()
        
        self.ety1=tk.Entry(self.f2,textvariable=self.num1,width=30)
        self.ety1.grid(row=4,column=1,padx=10,pady=15,sticky='ne')
        
        # self.ety1.bind('<KeyRelease>', self.entry1_save)
        
        self.ety2=tk.Entry(self.f2,textvariable=self.num2,width=30)
        self.ety2.grid(row=5,column=1,padx=10,pady=15,sticky='ne')
        
        # self.ety2.bind('<KeyRelease>', self.entry2_save)
        
        # self.ety1.bind('<Return>',self.entry_count)
        
        self.num1.set('1')
        
        
    def button(self):
        btn_clear=tk.Button(self.f2,text='清除',font=(15),command=self.clean)
        btn_clear.grid(row=4,column=2,padx=20,pady=20,sticky='nw')
        
        
    def clean(self):
        self.ety2.delete(0, 'end')
        self.ety2.delete(0, 'end')
        self.num1.set('1')
        
        
    def bind(self):
        self.ety1.bind('<KeyRelease>', self.entry1_save)
        
        self.ety2.bind('<KeyRelease>', self.entry2_save)
        
        
    def entry1_save(self, event):
        # global entry_num1
        # print(self.num1.get())
        self.entry_num1=self.num1.get()
        
        self.entry1_count()
        
        
    def entry2_save(self, event):
        # global entry_num2
        # print(self.num2.get())
        
        self.entry_num2=self.num2.get()
        
        self.entry2_count()
        
        
    def entry1_count(self):
        # print(self.num1.get())
        if self.info != '請選擇幣別':
            if self.num1.get() != '':
                info=eval(self.info)
                num1=eval(self.entry_num1)
                result1=round((num1/info),2)
                
                self.ety1.delete(0, 'end')
                self.ety1.insert(0, self.entry_num1)
                self.ety2.delete(0, 'end')
                self.ety2.insert(0, result1)
                
        else:
            pass
            
            
    def entry2_count(self):
        if self.info != '請選擇幣別':
            if self.num2.get() != '':
                info=eval(self.info)
                num2=eval(self.entry_num2)
                result2=round((info*num2),2)
                
                self.ety2.delete(0, 'end')
                self.ety2.insert(0, self.entry_num2)
                self.ety1.delete(0, 'end')
                self.ety1.insert(0, result2)
                
        else:
            pass
        
        
    def rate_save(self, option):
        # global rate2
        
        self.rate2=self.varKind.get()
        
        if self.rate2 != '':
            self.cash=self.rate2
            
            self.label()
            
        self.rate_sum()
        self.bind()
        
        
    def rate_sum(self):
        global show
        show='請選擇幣別'
        
        if self.rate2 != '':
        
            if self.y == 1 and self.z == 1:
                if self.rate2 in self.num:
                    x=self.num.index(self.rate2)
                    self.info = self.cash_sell[x]
    
            elif self.y == 2 and self.z == 1:
                if self.rate2 in self.num:
                    x=self.num.index(self.rate2)
                    self.info = self.cash_buy[x]
                    
            elif self.y == 1 and self.z == 2:
                if self.rate2 in self.num:
                    x=self.num.index(self.rate2)
                    self.info = self.spot_sell[x]
                    
            elif self.y == 2 and self.z == 2:
                if self.rate2 in self.num:
                    x=self.num.index(self.rate2)
                    self.info = self.spot_buy[x]
                    
        else:
            self.info=show
            
        self.label()
        self.bind()
        
    
    def rate_info(self):
        
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
        
            self.num=['美金(USD)','港幣(HKD)','英鎊(GBP)','澳幣(AUD)','加拿大幣(CAD)','新加坡幣(SGD)','瑞士法郎(CHF)',
                    '日圓(JPY)','南非幣(ZAR)','瑞典幣(SEK)','紐元(NZD)','泰幣(THB)','菲國比索(PHP)','印尼幣(IDR)',
                    '歐元(EUR)','韓元(KRW)','越南盾(VND)','馬來幣(MYR)','人民幣(CNY)']
            
            df=pd.DataFrame(self.datas,columns=['0','1','2','3','4','5','6','7','8','9','10'])
            df['0']=self.num
            df.drop(columns=['5','6','7','8','9','10'],inplace=True)
            
            self.cash_buy=df['1']
            self.cash_sell=df['2']
            
            self.spot_buy=df['3']
            self.spot_sell=df['4']
            
            
            self.label()
            self.optionmenu()
            
            
        # if self.varKind.get() != head:
        #     print(self.varKind)
        #     if rate2 != '':
        #         # for n,i in zip(num, df['1']):
        #         #     if rate2 == n:
        #         #         print(i)
        #         print(rate2)
        
def App(win):   
    
    top_count=tk.Toplevel(win)
    top_count.title('匯率試算')
    top_count.geometry('550x400')
    
    canvas=tk.Canvas(top_count,width=550,height=400)
    canvas.pack()
    f1=tk.Frame(top_count)
    
    f2=tk.Frame(top_count)
    
    canvas.create_window(120, 200, width=250,height=400,  window=f1)
    canvas.create_window(300, 200, width=380,height=400,  window=f2)
    
    App_start(f1,f2)
    
    # top_count.mainloop()
   
if __name__ == '__main__':
    
    win=tk.Tk()
    
    App(win)
    
    win.mainloop()
    