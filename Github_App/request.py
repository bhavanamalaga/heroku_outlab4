import requests
from datetime import datetime
import calendar


def time():
    current_time = datetime.now()
    date_time = current_time.strftime("%m %d %Y %H %M")  
    return date_time

def convert_time():
    tim = time()
    list = tim.split(" ")
    list[0] = calendar.month_abbr[int(list[0])]
    if(list[3] == '12'):
       list.append('p.m.')

    
    elif(int(list[3])//12 ==0):
        list.append('a.m.')
    
    else:
        list.append('p.m.')
        list[3] = str(int(list[3])%12)
    
    string = ''+list[0]+". "+list[1]+", "+list[2]+", "+list[3]+':'+list[4]+" "+list[5]
    return string
    
