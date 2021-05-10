from flask import Flask
from flask import Flask, render_template, request, jsonify
import json
from colour import Color
from flask_wtf import FlaskForm
from wtforms import SelectField
import os
import pandas as pd
import mysql.connector

app = Flask(__name__)

yr=0




@app.route('/', methods=["POST", "GET"])
def hello_world():

    if request.method == "POST":

        global yr
        yr = request.form.get('selectie')
        gemlist = color_map(yr)
        return render_template("index.html", gemeenten=gemlist, year=yr)

    else:
        yr = 2020
        gemlist = color_map(yr)
        return render_template("index.html", gemeenten=gemlist, year=yr)


def match_color(gem):

    colors = [['dannyvera-rollercoaster', '#FF7373'], ['queen-bohemianrhapsody', '#654EF2'], ['edestaal-hethetnognooitzodonkerwest', '#F2B727'], ["neetoétlottum-haldmich'svas", '#008040'], ['rowwenhèze-november', '#26004D'], ['eagles-hotelcalifornia', '#C8A2CB'], ['normaal-deboerdatisdekeerl', '#439981'],
              ['billyjoel-pianoman', '#8B5A2B'], ['boudewijndegroot-avond', '#e303fc'], ['ledzeppelin-stairwaytoheaven', '#00c206'], ['pearljam-black', '#000000'], ['guusmeeuwis-brabant', '#ffb700'], ['pinkfloyd-wishyouwerehere', '#250759'], ['bløfft.geike-zoutelande', '#56824f'], ['geendata', '#898c88']]

    for color in colors:
        if gem[2] == color[0]:
            return color[1]


def color_map(yr):

    gemlist = []

    f = open(
        "C:\\Users\\braml\\Desktop\\Projectjes\\top2000statistieken.nl\\Interactive\\static\\gemeenten alfabetisch 2020.csv",
        "r")
    for line in f:
        temp = []
        list = line.split(',')
        temp.append(list[2])
        temp.append(list[1])
        gemlist.append(temp)
        # print(gemlist)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="top2000"
    )

    mycursor = mydb.cursor()
    for gem in gemlist:

        sql = "SELECT num1, pct1 FROM stemlijst WHERE jaar= %s AND gemeente = %s"
        mycursor.execute(sql, (yr, gem[0]))

        myresult = mycursor.fetchall()

        for res in myresult:
            gem.append(res[0])
            gem.append(res[1])
            gem.append(match_color(gem))

    return gemlist


def get_music_attr():
    return 1


@app.route("/<gemeente>/<jaar>", methods=["POST", "GET"])
def gemeente_rapport(gemeente, jaar):

    rapport = ["", 0,"", 0,"", 0,"", 0,"", 0,"", 0,"", 0,"", 0,"", 0,"", 0,]
    print(gemeente, jaar)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="top2000"
    )

    mycursor = mydb.cursor()

    rapport = []

    sql = "SELECT * FROM stemlijst inner join gemeenten on stemlijst.id=gemeenten.stemlijst inner join nummers n on stemlijst.num1=n.id inner join nummers n2 on stemlijst.num2=n2.id inner join nummers n3 on stemlijst.num3=n3.id inner join nummers n4 on stemlijst.num4=n4.id inner join nummers n5 on stemlijst.num5=n5.id inner join nummers n6 on stemlijst.num6=n6.id inner join nummers n7 on stemlijst.num7=n7.id inner join nummers n8 on stemlijst.num8=n8.id inner join nummers n9 on stemlijst.num9=n9.id inner join nummers n10 on stemlijst.num10=n10.id WHERE jaar= %s AND gemeente = %s limit 1"
    mycursor.execute(sql, (yr, gemeente))

    myresult = mycursor.fetchall()
    print(myresult)


    chart = str(myresult)

    _chart = chart.split(",")
    print(_chart)

    for c in _chart:
        print(c)

    gemeente = _chart[2].replace("'", '')
    rapport.append([_chart[27].replace("'", ''), _chart[28].replace("'", ''), int(_chart[4].replace("'", '')), 1])
    rapport.append([_chart[30].replace("'", ''), _chart[31].replace("'", ''), int(_chart[6].replace("'", '')), 2])
    rapport.append([_chart[33].replace("'", ''), _chart[34].replace("'", ''), int(_chart[8].replace("'", '')), 3])
    rapport.append([_chart[36].replace("'", ''), _chart[37].replace("'", ''), int(_chart[10].replace("'", '')), 4])
    rapport.append([_chart[39].replace("'", ''), _chart[40].replace("'", ''), int(_chart[12].replace("'", '')), 5])
    rapport.append([_chart[42].replace("'", ''), _chart[43].replace("'", ''), int(_chart[14].replace("'", '')), 6])
    rapport.append([_chart[45].replace("'", ''), _chart[46].replace("'", ''), int(_chart[16].replace("'", '')), 7])
    rapport.append([_chart[48].replace("'", ''), _chart[49].replace("'", ''), int(_chart[18].replace("'", '')), 8])
    rapport.append([_chart[51].replace("'", ''), _chart[52].replace("'", ''), int(_chart[20].replace("'", '')), 9])
    rapport.append([_chart[54].replace("'", ''), _chart[55].replace("'", '').replace(")]", ''), int(_chart[22].replace("'", '')), 10])


    gemlist = color_map(jaar)
    return render_template("index.html", year=yr, chart = rapport, gemeente=gemeente, gemeenten = gemlist)



if __name__ == '__main__':
    app.run()
