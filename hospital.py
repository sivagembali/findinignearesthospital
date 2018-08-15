'''arguments = cgi.FieldStorage()
for i in arguments.keys():
    if(i == 'dist'):
        dist_name = arguments[i].value
    if(i == 'latt'):
        latitude = float(arguments[i].value)
    if(i == 'lon'):
        longitude = float(arguments[i].value)'''
from flask import Flask,request,current_app
from math import radians, sin, cos, acos
import os
app = Flask(__name__)

#method to calculate distance between source and destination which return the distance between two points
def distance_two_latlongs(slatlon,dlatlon1):
    dist = 6371.01 * acos(sin(slatlon[0])*sin(dlatlon1[0]) + cos(slatlon[0])*cos(dlatlon1[0])*cos(slatlon[1] - dlatlon1[1]))
    return dist
@app.route('/')
def homepage():
    return current_app.send_static_file('index.html')


@app.route('/getLocation',methods=['POST'])
def findnearesthospital():
    #longitude = round(float(request.form['log']),3)
    longitude = float(request.form['log'])
    #latitude = round(float(request.form['lat']),3)
    latitude =  float(request.form['lat'])
    dist_name = request.form['dist_name'].title()
    distance_list = []
    health_center = { }

    #External file accessing and storing the data in a dictionary 
    file_access = open('geocode_health_centre.csv','r')
    file_raw_data = file_access.read() # the whole data in the file is stored in file_raw_data
    file_data_lines_list = file_raw_data.split("\n") #splitted the data by new line character
    for each_line in range(len(file_data_lines_list)-1):
        file_each_line_data = file_data_lines_list[each_line].split(',')  #each line again splitted with ','
        key_dist = file_each_line_data[1]
        li_temp =[]

        if(file_each_line_data[1] not in health_center.keys()):

            health_center[file_each_line_data[1]] = []
            li_temp.append(file_each_line_data[4])
            li_temp.append(file_each_line_data[6])
            li_temp.append(file_each_line_data[7])
            health_center[key_dist].append(li_temp)       
        else:

            li_temp.append(file_each_line_data[4])
            li_temp.append(file_each_line_data[6])
            li_temp.append(file_each_line_data[7])
            health_center[key_dist].append(li_temp)
    #User interaction part
    try:
        #dist_name = arguments[0].value
        #input("Enter district name: ").title()
        #print(dist_name)
        #input("Enter Latitude: ")
        #input("Enter Longitude: ")
        if(dist_name in health_center.keys()):
            #latitude = float(arguments[1].value)
            #longitude = float(arguments[2].value)
            slatlon = [latitude,longitude]
            hospital_list = health_center[dist_name]
            for i in range(len(hospital_list)):
                try:
                    lat = float(hospital_list[i][1])
                    lon = float(hospital_list[i][2])
                except ValueError:
                    continue
                dlatlon1 = [lat,lon]
                distance = distance_two_latlongs(slatlon,dlatlon1)
                distance_list.append(distance)

            minimum = min(distance_list)

            min_index = distance_list.index(minimum)
            #print(len(distance_list),minimum,min_index)
            #print("Nearest Hospital: ",hospital_list[min_index][0],hospital_list[min_index][1],hospital_list[min_index][2])
            return hospital_list[min_index][0]
        else:
            #print("district name not found")
            return "District name not found"
        #print(hospital_list[i])
    except Exception as inst:
        pass
        #print("Exception: ",type(inst),inst)
    else:
        pass
        #print("Thank you")
    finally:
        file_access.close()
    #print(health_center)
    return ""
if __name__== '__main__':
    app.run(debug=False)