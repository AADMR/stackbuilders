#!/usr/bin/python
import sys
import datetime
import time
import re

in_plate_validate=in_date_validate=in_time_validate=valid=option=False
again=True

class Road:
    def __init__(self,name):#Constructor
        self.name=name
        self.format=["xxx999","xxx9999","31-12-9999","23-59"]# format of data inputs
        self.law_plate=["1-2","3-4","5-6","7-8","0-9"]# pos 0 = Monday, 1=Tuesday, 2=Wednesday...
        self.law_day=[0,1,2,3,4]# pos 0 = Monday, 1=Tuesday, 2=Wednesday... (days when Pico y Placa applies)
        self.law_time=["7:00-9:30","16:00-19:30"]# It can be added or removed different ranges (range of times)
        self.plate_actual="0"
        self.time_actual="0"
        self.date_actual="0"
    def __del__(self):#Destructor
        print ('Objeto "'+str(self.name)+'" destruido')

    def input_detection(self,characters,types):#Method # 1
        model=self.format[types]
        pos=0

        if len(characters)>len(model):
            return "1"#error longitud grande
        valid=True if re.match("^[a-zA-Z0-9-]*$", characters) else False

        for char in model:
            model_type=char.isalpha()
            try:
                chartypeactual=(characters[pos].isalpha())
            except:
                return "2"#error longitud pequena
            if (str(chartypeactual) == str(model_type)) and (str(valid)=="True"):
                pos += 1
            else:
                return "3"#error format model

        return 0

    def predictor(self):#Method # 2 (This method doesn't check if the data inputs are correct because the methond "input_detection" does it.)
        sts_1=0 #inside of the weekday
        sts_2=0 #which day
        sts_3=0 #hour
        d,m,y=self.date_actual.split("-")#it depends on the format "31-12-9999"
        com_num_day=(datetime.date(int(y), int(m), int(d))).weekday()
        com_dig_plate = (self.plate_actual[6]) if (len(self.plate_actual)==7) else (self.plate_actual[5])#it depends on the format "xxx999","xxx9999"
        val=(self.time_actual).split("-")
        com_h_time=val[0]#it depends on the format "23-59"
        com_m_time=val[1]#it depends on the format "23-59"

        for a in self.law_day:#for status 1
            if int(a) == int(com_num_day):
                sts_1=1
                break
            else:
                sts_1=0

        try:#for status 2
            num_1, num_2 = (self.law_plate[int(com_num_day)]).split("-")#it depends on the format "["1-2","3-4","5-6","7-8","9-0"]"
            sts_2 = 1 if ((int(com_dig_plate)==int(num_1))or(int(com_dig_plate)==int(num_2))) else 0
        except:
            sts_2=0


        for a in range (0,len(self.law_time)):#for status 3 (It depends on format "7:00-9:30")
            hour_ini,hour_end = (self.law_time[a]).split("-")
            hour_ini_hour,hour_ini_min=hour_ini.split(":")
            hour_end_hour,hour_end_min=hour_end.split(":")

            if (int(com_h_time)>=int(hour_ini_hour) and int(com_m_time)>=int(hour_ini_min)) and (int(com_h_time)<int(hour_end_hour) or ((int(com_h_time)==int(hour_end_hour))and(int(com_m_time)<=int(hour_end_min)))):
                sts_3=1
                break
            else:
                sts_3=0

        if (sts_1==0 or sts_2==0 or sts_3==0):#Summary of states
            return "Circulacion <LIBRE>"
        else:
            return "Circulacion <PROHIBIDA>"


try:
    while again:
        road=Road("Quito")
        while in_plate_validate==False:# PLATE input
            in_characters = input("(Formato: XXX879 o XXX9876)  Ingresar Placa: ")

            in_det_p1=road.input_detection(in_characters,0) #"0" for plate1
            in_det_p2=road.input_detection(in_characters,1) #"1" for plate2

            in_plate_validate = True if ((int(in_det_p1)==0)or(int(in_det_p2)==0)) else False

            print ("**************ERROR al ingresar PLACA**************") if (str(in_plate_validate)=="False") else (print ("Placa = "+str(in_characters)))
            print ("")

            road.plate_actual=in_characters

        while in_date_validate==False:# DATE input
            in_characters = input("(Formato: dd-mm-yyyy) Ingresar Fecha: ")

            in_det_date=road.input_detection(in_characters,2) #"2" date

            in_date_validate = True if ((int(in_det_date)==0)) else False

            print ("**************ERROR al ingresar FECHA**************") if (str(in_date_validate)=="False") else (print ("Fecha = "+str(in_characters)))
            print ("")

            if in_date_validate:
                try:
                    d,m,y=in_characters.split("-")
                    datetime.datetime(year=int(y),month=int(m),day=int(d))
                except ValueError:
                    print ("**************ERROR no existe FECHA**************")
                    print ("Fecha = "+str(in_characters))
                    print ("")
                    in_date_validate = False

            road.date_actual=in_characters

        while in_time_validate==False:# TIME input
            in_characters = input("(Formato: hh-mm) Ingresar Hora: ")

            in_det_date=road.input_detection(in_characters,3) #"3" for time

            in_time_validate = True if ((int(in_det_date)==0)) else False

            print ("**************ERROR al ingresar HORA**************") if (str(in_time_validate)=="False") else (print ("Fecha = "+str(in_characters)))
            print ("")

            if in_time_validate:
                try:
                    h,m=in_characters.split("-")
                    datetime.datetime(year=2018,month=5,day=29,hour=int(h),minute=int(m))
                except ValueError:
                    print ("**************ERROR no existe HORA**************")
                    print ("Hora = "+str(in_characters))
                    print ("")
                    in_time_validate = False

            road.time_actual=in_characters

        print ("##########Informacion##############")
        print ("Placa = "+str(road.plate_actual))
        print ("Fecha = "+str(road.date_actual))
        print (" Hora = "+str(road.time_actual))
        print ("###################################")
        print ("")

        prediction=road.predictor()
        print ("########################")
        print (str(prediction))
        print ("########################")

        while option==False:
            print ("")
            in_characters = input("(s=repetir n=terminar) Desea Consultar de nuevo: ")
            try:
                if str(in_characters)=="s" or str(in_characters)=="s":
                    in_plate_validate=in_date_validate=in_time_validate=valid=option=False
                    again=True
                    break
                elif str(in_characters)=="n" or str(in_characters)=="n":
                    option=True
                    again=False
            except:
                option=False

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print ("Force closing")
    del road
