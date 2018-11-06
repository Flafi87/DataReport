import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matplotlib.dates as mdates
pd.options.mode.chained_assignment = None #default='warn'
import time
import schedule
from pathlib import Path
import tkinter.messagebox
import traceback
import subprocess

exchange_rate_huf = 320
exchange_rate_pln = 4.26
exchange_rate_czk = 25.63

directory = ''

target_hun = 0
target_pl = 0
target_cz = 0
target_ee = 0
interval = 20000
chartRefresh = 15



def update_target_rate():
    global exchange_rate_huf
    global exchange_rate_pln
    global exchange_rate_czk
    global target
    global target_ee
    global target_hun
    global target_pl
    global target_cz

    try:
        df_target = pd.read_excel(directory /'target.xls', header=0)
        target_hun = df_target.iloc[0]['TARGET(EUR)']
        target_pl = df_target.iloc[1]['TARGET(EUR)']
        target_cz = df_target.iloc[2]['TARGET(EUR)']
        target_ee = df_target.iloc[3]['TARGET(EUR)']
        exchange_rate_huf = df_target.iloc[0]['RATE']
        exchange_rate_pln = df_target.iloc[1]['RATE']
        exchange_rate_czk = df_target.iloc[2]['RATE']
    except Exception as e:
        tkinter.messagebox.showinfo('Error', e)
        print(traceback.print_exc())
        print(e)

def makeachart():
    pd.options.mode.chained_assignment = None  # default='warn'
    global exchange_rate_huf
    global exchange_rate_pln
    global exchange_rate_czk
    # report file location
    global sales_report
    global quotes
    global target_hun
    global target_pl
    global target_cz
    global target_ee
    global photo

    # reading report file and target file changed to root
    try:
        df = pd.read_csv('report.dat', sep='\t', decimal=",")


        df['Time'] = df['Time'] = (pd.to_datetime(df['Time'])).dt.tz_localize('UTC').dt.tz_convert('Europe/Warsaw')
        df['Time'] = (df['Time'].dt.tz_localize(None))


        is_hun = df.loc[:, 'SOrg.'] == 'HU01'
        is_pl = df.loc[:, 'SOrg.'] == 'PL01'
        is_cz = df.loc[:, 'SOrg.'] == 'CZ01'

        df_hungary = df[is_hun]
        df_poland = df[is_pl]
        df_czech = df[is_cz]

        df_hungary['sales_eur'] = np.where(df_hungary['Curr.'] == 'HUF', df_hungary['Net value'] / exchange_rate_huf,
                                           df_hungary['Net value'])

        df_poland['sales_eur'] = np.where(df_poland['Curr.'] == 'PLN', df_poland['Net value'] / exchange_rate_pln,
                                          df_poland['Net value'])

        df_czech['sales_eur'] = np.where(df_czech['Curr.'] == 'CZK', df_czech['Net value'] / exchange_rate_czk,
                                         df_czech['Net value'])

        df_hungary
        df_euro = (df_hungary, df_poland, df_czech)
        df_euro = pd.concat(df_euro)

        df_euro = df_euro.sort_values('Time')
        df_cumsum = df_euro.sales_eur.cumsum()
        df_euro['cumsum'] = df_cumsum
        df_euro['target'] = target_ee

        #Create json file from the data
        df_euro.to_json(path_or_buf = 'data.json')

        global sales
        sales = df_cumsum.tail(1)
        print(round(float(sales),2))

        x = df_euro['Time']
        y = df_euro['cumsum']



        fig = plt.figure()
        fig.set_size_inches(16,9)

        font = {'weight' : 'bold',
            'size'   : 50}
        ax = plt.axes()
        ax.grid(True)
        axa = plt.gca().get_xaxis()
        # format major xtick label
        axa.set_major_formatter(mdates.DateFormatter('%H:%M'))

        plt.ylabel('Sales (EUR)', fontsize = 30)
        #plt.title('Daily Sales', fontsize = 30)

        plt.rc('font',**font)
        plt.style.use('seaborn-whitegrid')
        plt.plot(x,y,linewidth = 5, color = '#5f259f')
        plt.axhline(y=target_ee,linewidth=4, color='r')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.tight_layout() ##experiment
        plt.savefig('cumsum.png')
        photo = '''<div id='sales' class='slides'>
                        <div><h2>DAILY SALES EE</h2></div>
                        <img class="cumsum" src="cumsum.png">
                    </div>'''
        print('I made chart')

    except Exception as e:
        tkinter.messagebox.showinfo('Error', e)
        print(traceback.print_exc())
        print(e)

def makeQuoteTable():
    try:
        global quotes
        df_quote = pd.read_excel(directory / 'Sales Quotes.xlsx', sheet_name='High Value Quotes', header=3, converters={'Contact Person':str})
        filtered_table = df_quote[
            ['Employee responsible for', 'Sales Organisation', 'Sold To Portfolio', 'Sold To Name', 'Contact Person', 'Quote Ref', 'Quote Status', 'Value of Quotes', 'Quote Margin %']].copy()
        filtered_table = filtered_table.round({'Quote Margin %' : 2})
        tablehtml = filtered_table.to_html(index = False)
        print('I made table quotes')
        return tablehtml

    except Exception as e:
        tkinter.messagebox.showinfo('Error', e)
        print(traceback.print_exc())
        print(e)

def runScript():
    try:
        #subprocess.call(['cscript.exe',os.getcwd() + '/data/script.vbs'])
        subprocess.call(['cscript.exe',os.getcwd() + '/script.vbs'])
        print('I ran the script')

    except Exception as e:
        tkinter.messagebox.showinfo('Error', e)
        print(traceback.print_exc())
        print(e)


# def scheduler():
#     schedule.every(10).seconds.do(runScript)
#     schedule.every(20).seconds.do(makeachart)
#     schedule.every(30).seconds.do(makeQuoteTable)
#     schedule.every(30).seconds.do(make_index)
#     while True:
#          schedule.run_pending()
#          time.sleep(1)



def imgMaker(imgList):
    global photo
    i=0
    while i < len(imgList):
        photom= '''<img class = "slides" src="{file}{image}">'''
        photo += photom.format(file = "file:///", image = str(Path(imgList[i])))
        i+=1


def make_index():
    tablehtml = makeQuoteTable()
    global photo
    global interval
    indexhtml = '''<!DOCTYPE html>
                <html lang="">
                <link rel="stylesheet" href="style.css">
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">

                    <title></title>
                </head>

                <body>
                   <div id='presentation-box'>
                         <div id='holder'>
                           <div id='nps' class = 'slides'>
                           <div><h2>NPS & First Choice</h2></div>
                           <img src="{file}{NPS}"><img src="{file}{FC}"></div>
                           <div id='quotes' class='slides'><h2>HIGH VALUE QUOTES</h2>
                                {Table}
                            </div>
                           {Photos}
                         </div>
                         <div id = 'time'></div>
                   </div>
                </body>
                </html>
                <script src="script.js"></script>'''
    finalIndex = indexhtml.format(file = "file:///", FC = directory / "fc.png",NPS = directory / "nps.png", Table = tablehtml, Photos = photo)
    f = open('index.html','w+')
    f.write(finalIndex)
    f.close()
    print('I made index')

    javascript = '''let interval = {interv} ;
                    let chartinterval = {chartrefresh}*60000;
                    
                    
                    
                    
                    function startTime() {{
                        let today = new Date();
                        let h = today.getHours();
                        let m = today.getMinutes();
                        let s = today.getSeconds();
                        let M = today.getMonth()+1;
                        let D = today.getDate();
                        let Y = today.getFullYear();
                        
                        m = checkTime(m);
                        s = checkTime(s);
                        document.getElementById('time').innerHTML =
                        `${{D}}.${{M}}.${{Y}} ${{h}}:${{m}}`
                        let t = setTimeout(startTime, 1000);
                    }}
                    function checkTime(i) {{
                        if (i < 10) {{i = "0" + i}};  // add zero in front of numbers < 10
                        return i;
                    }}
                    
                    startTime()
                    
                    function fade(indexname){{
                        indexname.classList.add = 'active'
                    }}
                    
                    let myIndex = 0;
                    const repeat = chartinterval / interval;
                    let repeated = 0;
                    function slideShow() {{
                        restart = 1;
                        x = document.getElementsByClassName('slides');
                            for (i = 0; i < x.length; i++){{
                            x[i].style.display = 'none';
                            x[myIndex].classList.remove("active");
                            x[myIndex].style.display = 'inline-block';
                            }}
                        setTimeout(function() {{
                            x[myIndex].classList.add('active');
                            myIndex++;
                            repeated++;
                            if(repeated >= repeat && (myIndex+1) == x.length){{
                                setTimeout(location.reload(true),interval - 2000)
                            }}
                            if (myIndex == x.length) {{ myIndex = 0; }}
                        }},interval-2000);
                        setTimeout(slideShow, interval);
                    }}
                    slideShow();'''
    intervalString = str(interval*1000)
    finalJavascript = javascript.format(interv = intervalString, chartrefresh = chartRefresh)
    f = open('script.js','w+')
    f.write(finalJavascript)
    f.close()
    print('I made javascript')


def ThreadExample():
    global chartRefresh
    if chartRefresh <= 1:
        chartRefresh = 2
    schedule.every(chartRefresh-1).minutes.do(runScript).tag('job')
    schedule.every(chartRefresh).minutes.do(makeachart).tag('job')
    schedule.every().day.at("08:59").do(update_target_rate).tag('job')
    schedule.every().day.at("09:00").do(make_index).tag('job')

    while True:
        schedule.run_pending()
        time.sleep(1)

