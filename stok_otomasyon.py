import os
import sys
import PyQt5
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5 import QtWidgets,QtGui,QtCore,Qt
import sqlite3 as sql
import time

try:
    vt=sql.connect("data.db")
    imlec = vt.cursor()
    imlec.execute("CREATE TABLE IF NOT EXISTS Urunler (urunad text,adet int);")
except:
    print("Baglanti Yok")


class Otomasyon:
    def urunEkle(self,ad,adet):
        sorgu = "Insert into Urunler Values(?,?)"
        sorgu2 = "Select * From urunler where urunad = ?"
        imlec.execute(sorgu2,(ad,))
        kontrol = imlec.fetchall()
        if (len(kontrol) > 0):
            print("Böyle bir ürün zaten var")
        else:
            imlec.execute(sorgu,(ad,adet))
            vt.commit()

    def adetEkle(self,ad,urunadet):
        sorgu = "Select * From Urunler where urunad = ?"
        imlec.execute(sorgu,(ad,))
        urun = imlec.fetchall()
        if(len(urun) == 0):
            print("Böyle bir ürün bulunmuyor...")
        else:
            adet = urun[0][1]
            adet += urunadet
            sorgu2 = "Update Urunler set adet = ? where urunad = ?"
            imlec.execute(sorgu2,(adet,ad))
            vt.commit()
    def satildiCikarildi(self,ad,cikarilacakAdet):
        sorgu = "Select * From Urunler where urunad = ?"
        imlec.execute(sorgu,(ad,))
        urun = imlec.fetchall()
        if(len(urun) == 0):
            print("Böyle bir ürün bulunmuyor...")
        else:
            adet = urun[0][1]
            adet -= cikarilacakAdet
            sorgu2 = "Update Urunler set adet = ? where urunad = ?"
            imlec.execute(sorgu2,(adet,ad))
            vt.commit()
    
    #Urun Sorgulama

    def urunSorgula(self,ad,adetler):
        sorgu = "Select * From Urunler where urunad = ?"
        imlec.execute(sorgu,(ad,))
        urun = imlec.fetchall()
        if(len(urun) == 0):
            print("Böyle bir ürün bulunmuyor.")
        else:
            adet = urun[0][1]
            adetler += str(adet)
            print("Bu üründen",adet,"adet bulunuyor")

    def urunleriGoster(self,liste):
        sorgu = "Select * From Urunler"
        imlec.execute(sorgu)
        urunler = imlec.fetchall()
        liste += urunler
        

otomasyon = Otomasyon()

def Arayuz():
    app = QtWidgets.QApplication(sys.argv)
    pencere = QtWidgets.QWidget()
    pencere.setWindowTitle("Stok Takip Sistemi - cyb3rk Tech.")
    pencere.setGeometry(480,180,1280,260)
    pencere.setFixedSize(1280, 260)

    arkaplan = QtWidgets.QLabel(pencere)
    arkaplan.setPixmap(QtGui.QPixmap("arkaplan.png"))

    mesajbox = QtWidgets.QTextBrowser(pencere)
    mesajbox.move(530,100)
    mesajbox.resize(141,151)
    #Urun Ekleme
    urun_ekleme_urunad = QtWidgets.QLineEdit(pencere)
    urun_ekleme_urunad.move(150,60)
    urun_adet = QtWidgets.QSpinBox(pencere)
    urun_adet.move(290,60)
    urun_ekle_buton = QtWidgets.QPushButton(pencere)
    urun_ekle_buton.move(170,90)
    urun_ekle_buton.setText("Ekle")
    def urun_ekle():
        ueu = urun_ekleme_urunad.text()
        adet = urun_adet.value()
        otomasyon.urunEkle(ueu,adet)
        mesajbox.setText("{} adlı üründen {} tane eklendi !".format(ueu,adet))
    urun_ekle_buton.clicked.connect(urun_ekle)
    
    #Urun Sorgulama
    urun_sorgulama_urunad = QtWidgets.QLineEdit(pencere)
    urun_sorgulama_urunad.move(380,60)
    urun_sorgulama_buton = QtWidgets.QPushButton(pencere)
    urun_sorgulama_buton.move(400,90)
    urun_sorgulama_buton.setText("Sorgula")
    def urunSorgula():
        adetler = []
        ad = urun_sorgulama_urunad.text()
        otomasyon.urunSorgula(ad,adetler)
        mesajbox.setText("Bu üründen {} adet bulunuyor.".format(str(adetler)))
    urun_sorgulama_buton.clicked.connect(urunSorgula)

    #Urun Çıkarma/Satma
    urun_satis_urunad = QtWidgets.QLineEdit(pencere)
    urun_satis_urunad.move(690,60)
    urun_satis_buton = QtWidgets.QPushButton(pencere)
    urun_satis_buton.move(710,90)
    urun_satis_buton.setText("Ürün Satıldı")
    urun_satis_spinbox = QtWidgets.QSpinBox(pencere)
    urun_satis_spinbox.move(830,60)
    def urunSatildi():
        urun = urun_satis_urunad.text()
        adet = urun_satis_spinbox.value()
        otomasyon.satildiCikarildi(urun,adet)
        mesajbox.setText("{} adlı üründen {} adet satıldı/eksildi.".format(urun,adet))
    urun_satis_buton.clicked.connect(urunSatildi)

    #Urun Adet Ekleme 
    urun_adet_ekle = QtWidgets.QLineEdit(pencere)
    urun_adet_ekle.move(920,60)
    urun_adet_ekle_spinbox = QtWidgets.QSpinBox(pencere)
    urun_adet_ekle_spinbox.move(1060,60)
    urun_adet_ekle_buton = QtWidgets.QPushButton(pencere)
    urun_adet_ekle_buton.move(950,90)
    urun_adet_ekle_buton.setText("Adet Ürün Ekle")

    def adetEkle():
        urun = urun_adet_ekle.text()
        adet = urun_adet_ekle_spinbox.value()
        otomasyon.adetEkle(urun,adet)
        mesajbox.setText("{} adlı üründen {} adet eklendi.".format(urun,adet))
    urun_adet_ekle_buton.clicked.connect(adetEkle)

    #Urunleri Goster
    def urunleriGoster():
        liste = []
        otomasyon.urunleriGoster(liste)
        mesajbox.setText(str(liste))


    urunleri_goster = QtWidgets.QPushButton(pencere)
    urunleri_goster.move(523,60)
    urunleri_goster.setText("Ürünlerin Tamamını Göster")
    urunleri_goster.clicked.connect(urunleriGoster)

    myinfo = QtWidgets.QLabel(pencere)
    myinfo.move(1100,150)
    myinfo.resize(190,100)
    myinfo.setFont(QFont('Arial',9))
    myinfo.setText("       created by cyb3rk\n         github/cyb3rk\n         youtube/RAYTAKES")

        
    pencere.show()
    sys.exit(app.exec_())

Arayuz()