import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialog,QMainWindow,QMessageBox,QPushButton,QFileDialog,QTableWidgetItem,QLabel,QStyledItemDelegate
from PyQt5.QtGui import QPixmap,QImage
from login import Ui_Form_Login
from signup import Ui_Form_Signup
from MainMenu import Ui_MainWindow
from admin import Ui_Admin
import requests
import json
import time
loginUrl = 'https://shopapiptithcm.azurewebsites.net/api/login'
data_test = requests.get("https://shopapiptithcm.azurewebsites.net/api/getitems").text
data = json.loads(data_test)

rq = requests.get("https://shopapiptithcm.azurewebsites.net/api/getorder").text
dataOrder = json.loads(rq)
UserName  = ""
password = ''
tempCart = {}
phone = ""
idtemp = []
tempstatus = ""
idOrder = ""
priceSP = ""
tempOrderUser = []
print(type(data))

# Trang dang nhap
class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        self.uic = Ui_Form_Login()
        self.uic.setupUi(self)
        self.uic.id.setText("admin")
        self.uic.password.setText("123")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Nut Bam
        self.uic.button_exit.clicked.connect(self.close)
        self.uic.button_login.clicked.connect(self.checkAcc)
        self.uic.button_signup.clicked.connect(self.gotoCreate)
        # kiem tra Tai khoan
    def checkAcc(self):
        global UserName
        UserName = self.uic.id.text()
        password = self.uic.password.text()
        response = requests.post('https://shopapiptithcm.azurewebsites.net/api/login',
                                 json={'id': UserName, 'Pass': password})

        if response.text == "0":
            QMessageBox.information(self, "Loi", "Sai ten tai khoan hoac mat khau")
        elif response.text == "13":
            QMessageBox.information(self,'','tai khoan da bi khoa')
        elif response.text =="12":
            re = requests.post("https://shopapiptithcm.azurewebsites.net/api/getadminphone",json= {"id":UserName}).text
            global phone
            phone = re
            self.gotoadmin()
        elif response.text == "11":
            print(UserName)
            print(password)

            return self.gotoScreenUser()

    def gotoadmin(self):
        main_win.close()
        screenadmin.show()

    # Chuyen sang trang chu
    def gotoScreenUser(self):
        main_win.close()
        screencart.show()
        print("gio hang hien tai")
        crt = requests.post("https://shopapiptithcm.azurewebsites.net/api/findcart", json={"id": UserName}).text
        temp = json.loads(crt)
        print(temp)
    # Chuyen sang trang dang ki
    def gotoCreate(self):
        main_win.close()
        createacc.show()

# dang ki tai khoan
class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        #loadUi("signup.ui",self)
        self.uic = Ui_Form_Signup()
        self.uic.setupUi(self)
        self.uic.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # nnut bam
        self.uic.button_signup.clicked.connect(self.createaccfunction)
        self.uic.button_back.clicked.connect(self.gotoLogin)
        self.uic.button_exit.clicked.connect(self.close)

# tao tai khoan
    def createaccfunction(self):
        idUser = self.uic.id.text()
        email = self.uic.email.text()
        password = self.uic.password.text()
        confirmpass = self.uic.confirmPassword.text()
        responseId = requests.post('https://shopapiptithcm.azurewebsites.net/api/create/checkid',
                                 json={'id': idUser, 'Pass': password})
        responseEmail = requests.post('https://shopapiptithcm.azurewebsites.net/api/create/checkemail',
                                      json={"Email": email})

        print(responseId.text)

        print(responseEmail.text)
        if responseId.text == "1":
            QMessageBox.information(self,"","tai khoan da co nguoi su dung")
        elif responseEmail.text =="1":
            QMessageBox.information(self,"","Email da co nguoi su dung")
        elif password != confirmpass:
            QMessageBox.information(self,"loi","mat khau xac thuc khong dung")
        else:
            rq =requests.post("https://shopapiptithcm.azurewebsites.net/api/createuser",
                                           json={'id': idUser, 'Pass': password, "Type": "USER", "Email": email}).text
            r = json.loads(rq)
            if r['code'] == 1:
                QMessageBox.information(self,'chúc mung','dang kí thành công')
                return self.gotoLogin()
            else:
                QMessageBox.information(self,"","dang ki that bai")

    # Chuyen sang trang dang nhap
    def gotoLogin(self):
        createacc.close()
        main_win.show()

#Trang chu
class Cart(QMainWindow):
    def __init__(self):
        super(Cart,self).__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.loadTableCart()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Chinh size table
        self.uic.tableWidget.setColumnWidth(0,200)
        self.uic.tableWidget.setColumnWidth(1,350)
        self.uic.tableWidget.setColumnWidth(2,335)
        self.uic.tableWidget.setColumnWidth(3,100)
        self.uic.tableWidget_2.setColumnWidth(0, 250)
        self.uic.tableWidget_2.setColumnWidth(1, 320)
        self.uic.tableWidget_2.setColumnWidth(2, 320)
        self.uic.tableWidget_2.setColumnWidth(3, 100)
        self.uic.tableWidget_3.setColumnWidth(0, 100)
        self.uic.tableWidget_3.setColumnWidth(1, 200)
        self.uic.tableWidget_3.setColumnWidth(2, 100)
        self.uic.tableWidget_3.setColumnWidth(4, 300)
        self.uic.tableWidget_3.setColumnWidth(3, 130)
        self.uic.tableWidget_3.setColumnWidth(5, 100)
        self.uic.tableWidget_3.setColumnWidth(6, 55)
        self.uic.frame_3.hide()
        self.uic.frame_25.hide()
        #Loai hinh thanh toan

        self.uic.comboBox.addItems(['COD','MOMO','ATM'])

        self.uic.stackedWidget.setCurrentWidget(self.uic.page_home)
        # nut bam
        self.uic.exitButton.clicked.connect(self.close)
        self.uic.hideButton.clicked.connect(self.showMinimized)
        self.uic.addtoCart.clicked.connect(self.checkAmount)
        self.uic.cartButton.clicked.connect(self.gotoCart)
        self.uic.homeButton.clicked.connect(self.gotoHome)
        self.uic.SoLuong.valueChanged.connect(self.vlChange)
        self.uic.buyButton.clicked.connect(self.checkInfo)
        self.uic.profileButton.clicked.connect(self.gotoProfile)
        self.uic.orderbutton.clicked.connect(self.gotoordered)


    def gotoordered(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page)
        self.ordered()


    def ordered(self):
        crt = requests.post("https://shopapiptithcm.azurewebsites.net/api/findorder", json={"buyer": UserName}).text
        temp = json.loads(crt)
        row = 0
        total = 0
        self.uic.tableWidget_3.setRowCount(len(temp))
        for items in temp:
            self.uic.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(items["phone"]))
            self.uic.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(items["status"]))
            self.uic.tableWidget_3.setItem(row, 2, QtWidgets.QTableWidgetItem(items["payment"]))
            self.uic.tableWidget_3.setItem(row, 3, QtWidgets.QTableWidgetItem(items["address"]))
            self.uic.tableWidget_3.setItem(row, 4, QtWidgets.QTableWidgetItem(items["date"]))
            self.uic.tableWidget_3.setItem(row, 5, QtWidgets.QTableWidgetItem(str(items["total"])))

            btn = QPushButton("edit".format(row))

            self.uic.tableWidget_3.setCellWidget(row, 6, btn)
            btn.setStyleSheet(
                "background-color: rgb(85, 170, 255);border-bottom-left-radius:0px;border-bottom-right-radius:0px;")

            btn.clicked.connect(self.updateOrderUser)
            row += 1



    def updateOrderUser(self):
        self.uic.frame_25.show()
        button = self.sender()
        index = self.uic.tableWidget_3.indexAt(button.pos())
        self.uic.changeadress.setText(self.uic.tableWidget_3.item(index.row(),3).text())
        self.uic.changephone.setText(self.uic.tableWidget_3.item(index.row(),0).text())
        self.uic.update.clicked.connect(self.updateOrder)
        crt = requests.post("https://shopapiptithcm.azurewebsites.net/api/findorder", json={"buyer": UserName}).text
        temp = json.loads(crt)
        global  tempOrderUser
        tempOrderUser = temp[index.row()]

    def updateOrder(self):
        if len(self.uic.changephone.text()) < 10 or self.uic.changeadress.text() == '':
            QMessageBox.information(self,'','vui long nhap chinh xac thong tin')
        else:
            global tempOrderUser
            tempOrderUser['address'] = self.uic.changeadress.text()
            tempOrderUser['phone'] = self.uic.changephone.text()
            print(tempOrderUser)
            request = requests.put("https://shopapiptithcm.azurewebsites.net/api/updateorder",json=tempOrderUser)

            QMessageBox.information(self,'','Thanh cong')









    #Trang Profile
    def gotoProfile(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.pageUser)
        self.uic.id.setText(UserName)
        request = requests.post("https://shopapiptithcm.azurewebsites.net/api/userorders",json={"buyer":UserName}).text
        response = json.loads(request)
        self.uic.done.setText(str(response['code']))
        self.uic.change.hide()
        self.uic.confirm.hide()
        self.uic.label_14.hide()
        self.uic.label_15.hide()
        self.uic.accept.hide()
        self.uic.changePass.clicked.connect(self.changepass)
        self.uic.logOut.clicked.connect(self.gotologin)


    def changepass(self):
        self.uic.changePass.hide()
        self.uic.label_14.show()
        self.uic.label_15.show()
        self.uic.change.show()
        self.uic.confirm.show()
        self.uic.accept.show()
        self.uic.accept.clicked.connect(self.change)



    def change(self):
        if self.uic.change.text() != self.uic.confirm.text():
            QMessageBox.information(self,'','mat khau xac nhan khong dung')
        else:
            re = requests.get("https://shopapiptithcm.azurewebsites.net/api/getalluser").text
            rsp = json.loads(re)
            temp ={}
            for i in rsp:
                if i['id'] == UserName:
                    print(i)
                    if i['pass'] == self.uic.change.text():
                        QMessageBox.information(self,'','mat khau trung voi mat khau cu')
                    else:

                        i['pass'] = self.uic.confirm.text()
                        temp = i
                        break
            request = requests.put("https://shopapiptithcm.azurewebsites.net/api/updateuseradmin", json=i).text
            res = json.loads(request)
            if res['code'] ==1:
                QMessageBox.information(self,'','doi mat khau thanh cong')
            else:
                QMessageBox.information(self, '', 'doi mat khau that bai')







    def gotologin(self):
        screencart.close()
        main_win.show()


    #Trang mua hang
    def gotoHome(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_home)
    #chuyen Trang gio hang
    def gotoCart(self):
        rq_cart = requests.post("https://shopapiptithcm.azurewebsites.net/api/findcart",
                                json={"id": UserName}).text
        global tempCart
        tempCart = json.loads(rq_cart)

        if tempCart['items'] == None:
            QMessageBox.information(self,'','Gio hang chua co hang')
        else:
            self.uic.stackedWidget.setCurrentWidget(self.uic.page_2)
            self.cart()

#Danh sach san pham

    def loadTableCart(self):
        row = 0
        self.uic.tableWidget.setRowCount(len(data))
        for items in data:
            self.uic.tableWidget.setItem(row, 0,QtWidgets.QTableWidgetItem(items["id"]))
            self.uic.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(items["price"])))
            self.uic.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(items["brand"]))

# ADD image to QtableWidget




         #   self.uic.tableWidget.setCellWidget(row, 3, w)
            btn = QPushButton("Buy".format(row))
            btn.clicked.connect(self.clickBuy)
            self.uic.tableWidget.setCellWidget(row, 3, btn)
            btn.setStyleSheet("background-color: rgb(85, 170, 255);border-bottom-left-radius:0px;border-bottom-right-radius:0px;")
            row+=1

#Kiem tra so luong san pham mua > 0
    def checkAmount(self):
        amount = self.uic.SoLuong.value()
        if amount == 0:
            QMessageBox.information(self,"Loi","So luong phai lon hon 0")
        else:
            self.checkRemain()
#Check so luong san pham con lai
    def checkRemain(self):
        for items in data:
            if self.uic.idSP.text() == items['id']:
                if items['remain'] <= 0:
                    QMessageBox.information(self,'Loi','san pham da het hang')
                else:
                    self.addtoCart()

    # click nut Mua
    def clickBuy(self):
        self.uic.frame_3.show()
        self.uic.SoLuong.clear()
        button = self.sender()
        index = self.uic.tableWidget.indexAt(button.pos())
        self.uic.total.hide()
        self.uic.idSP.setText(self.uic.tableWidget.item(index.row(),0).text())
        global priceSP
        priceSP = self.uic.tableWidget.item(index.row(),1).text()
       # self.price = int(priceSP)


        templist = data[index.row()]
        zdi2 = templist["image"]
        r = requests.get(zdi2, stream=True)
        assert r.status_code == 200
        img = QImage()
        assert img.loadFromData(r.content)
        w = QLabel()
        pixmap = QPixmap.fromImage(img)
        #  w.setPixmap(QPixmap.fromImage(img))
        # w.setPixmap(pixmap)
        pixmap.scaled(200,200)
        self.uic.image.setPixmap(pixmap)
        self.uic.image.setMaximumSize(485,312)
      # self.uic.image.resize(pixmap.width(), pixmap.height())

    #Tinh gia tien san pham da chon
    def vlChange(self):
        global priceSP
        price = int(priceSP)
            # tinh tien san pham
        totalPrice = self.uic.SoLuong.value() * price
        self.uic.total.setText(str(totalPrice))
        self.uic.total.show()

# them san pham vao gio hang
    def addtoCart(self):
        amount = self.uic.SoLuong.value()
        id = self.uic.idSP.text()
        price = int(self.uic.total.text())
        rq_cart = requests.post("https://shopapiptithcm.azurewebsites.net/api/findcart",
                         json = {"id": UserName}).text
        tempCart = json.loads(rq_cart)
        if tempCart["items"] != None:

            tempCart['items']+=[{"id": id,"amount": amount,"price": price}]
            tempCart['total'] += price

        else:
            requests.post("https://shopapiptithcm.azurewebsites.net/api/createcart", json={"id": UserName})
            tempCart = {
                "id":UserName,'total':price,'items':[{"id": id,"amount": amount,"price": price}]}
            print('gio hang moi tao')
        requests.put("https://shopapiptithcm.azurewebsites.net/api/updatecart", json=tempCart)
        print('gio hang tam')
        print(tempCart)
        QMessageBox.information(self,"Chúc mung","Thêm san pham thành công")
#Trang gio hang
    def cart(self):
        crt = requests.post("https://shopapiptithcm.azurewebsites.net/api/findcart", json={"id": UserName}).text
        temp= json.loads(crt)
        row = 0
        total = 0
        self.uic.tableWidget_2.setRowCount(len(temp['items']))
        for items in temp['items']:
            self.uic.tableWidget_2.setItem(row, 0,QtWidgets.QTableWidgetItem(items["id"]))
            self.uic.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(items["amount"])))
            self.uic.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(items["price"])))
            total += items['price']
            btn = QPushButton("Delete".format(row))

            self.uic.tableWidget_2.setCellWidget(row, 3, btn)
            btn.setStyleSheet(
                "background-color: rgb(85, 170, 255);border-bottom-left-radius:0px;border-bottom-right-radius:0px;")

            btn.clicked.connect(self.deleteCart)
            row+=1
        self.uic.total_2.setText(str(total))


#Xoa san pham trong gio hang
    def deleteCart(self):
        button = self.sender()
        index = self.uic.tableWidget_2.indexAt(button.pos())
        list = tempCart['items']
        list.pop(index.row())
        tempCart['items'] = list
        requests.put("https://shopapiptithcm.azurewebsites.net/api/updatecart", json=tempCart)
        QMessageBox.information(self,'','xoa thanh cong vui long reset gio hang')


#Kiem tra thong tin thanh toan
    def checkInfo(self):
        linephone = self.uic.linePhone.text()
        if len(linephone) < 10 or self.uic.lineAdress.text() == '':
            QMessageBox.information(self,'','Vui long nhap chinh xac thong tin de thanh toan')
        else:
            self.CreateOrder()



# Tao Order
    def CreateOrder(self):
        tempOrder = {
            "id":None,
            "buyer": UserName,
            "phone": self.uic.linePhone.text(),
            "status": "pending",
            "payment": self.uic.comboBox.currentText(),
            "address": self.uic.lineAdress.text(),
            "date": time.asctime(time.localtime(time.time())),
            "total":int(self.uic.total_2.text()),
            "items": tempCart['items'],
            "admins": [],
        }

        print(tempOrder)
        re = requests.post("https://shopapiptithcm.azurewebsites.net/api/createp",json=tempOrder).text
        r =json.loads(re)

        if r["code"] == 1:
            QMessageBox.information(self,"","dat hang thanh cong")
        else:
            QMessageBox.information(self,"","dat hang that bai")




class Manager(QMainWindow):
    def __init__(self):
        super(Manager,self).__init__()
        #loadUi("signup.ui",self)
        self.uic = Ui_Admin()
        self.uic.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.product()
        self.uic.tableWidget.setColumnWidth(0, 200)
        self.uic.tableWidget.setColumnWidth(1, 300)
        self.uic.tableWidget.setColumnWidth(2, 300)
        self.uic.tableWidget.setColumnWidth(3, 100)
        self.uic.tableWidget.setColumnWidth(4,85)
        self.uic.tableWidget_3.setColumnWidth(0, 100)
        self.uic.tableWidget_3.setColumnWidth(1, 200)
        self.uic.tableWidget_3.setColumnWidth(2, 100)
        self.uic.tableWidget_3.setColumnWidth(3, 300)
        self.uic.tableWidget_3.setColumnWidth(4, 130)
        self.uic.tableWidget_3.setColumnWidth(5, 100)
        self.uic.tableWidget_3.setColumnWidth(6, 55)
        self.uic.tableWidget_2.setColumnWidth(0, 100)
        self.uic.tableWidget_2.setColumnWidth(1, 200)
        self.uic.tableWidget_2.setColumnWidth(2, 100)
        self.uic.tableWidget_2.setColumnWidth(3, 100)
        self.uic.tableWidget_2.setColumnWidth(4, 200)
        self.uic.tableWidget_2.setColumnWidth(5, 150)
        self.uic.tableWidget_2.setColumnWidth(6, 105)

        self.uic.comboBox.addItems(['','banned', 'ok'])
        self.uic.comboBox_2.addItems(["","pending","canceled","packaging","delivering","done"])

        self.uic.exitButton.clicked.connect(self.close)
        self.uic.hideButton.clicked.connect(self.showMinimized)
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_home)
        self.uic.homeButton.clicked.connect(self.gotoproduct)
        self.uic.editSP.clicked.connect(self.updateSP)
        self.uic.profileButton.clicked.connect(self.gotouser)
        self.uic.cartButton.clicked.connect(self.gotoorder)
        self.uic.addSP.clicked.connect(self.addsp)



    def gotoorder(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_2)
        self.order()

    def gotouser(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page)
        self.user()

    def gotoproduct(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_home)


    def product(self):
        data_test = requests.get("https://shopapiptithcm.azurewebsites.net/api/getitems").text
        data_2 = json.loads(data_test)
        row = 0
        self.uic.tableWidget.setRowCount(len(data_2))
        for items in data_2:
            self.uic.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(items["id"]))
            self.uic.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(items["price"])))
            self.uic.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(items["brand"]))
            self.uic.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(items["remain"])))
            btn = QPushButton("Edit".format(row))
            self.uic.tableWidget.setCellWidget(row, 4, btn)
            btn.setStyleSheet(
                "background-color: rgb(85, 170, 255);border-bottom-left-radius:0px;border-bottom-right-radius:0px;")
            row += 1
            btn.clicked.connect(self.detailSP)


    def detailSP(self):
        button = self.sender()
        index = self.uic.tableWidget.indexAt(button.pos())

        self.uic.tenSP.setText(self.uic.tableWidget.item(index.row(), 0).text())
        self.uic.brandSP.setText(self.uic.tableWidget.item(index.row(), 2).text())
        self.uic.priceSP.setText(self.uic.tableWidget.item(index.row(), 1).text())
        self.uic.amountSP.setText(self.uic.tableWidget.item(index.row(), 3).text())
        tempImage = data[index.row()]
        self.uic.imageSP.setText(str(tempImage['image']))
        self.uic.videoSP.setText(str(tempImage['url']))

    def updateSP(self):
        tempprice = int(self.uic.priceSP.text())
        tempremain = int(self.uic.amountSP.text())
        tempSP = {
            "id": self.uic.tenSP.text(),
            "brand": self.uic.brandSP.text(),
            "price": tempprice,
            "remain": tempremain,
            "image": self.uic.imageSP.text(),
            "url": self.uic.videoSP.text()
        }

        request = requests.put("https://shopapiptithcm.azurewebsites.net/api/updateitem",json=tempSP).text
        respone = json.loads(request)
        print(respone)
        if respone['code'] == 1:
            QMessageBox.information(self, "", "Thanh cong")
        else:
            QMessageBox.information(self, "", "That bai")

    def addsp(self):
        tempprice = int(self.uic.priceSP.text())
        tempremain = int(self.uic.amountSP.text())
        tempsp = {
            "id": self.uic.tenSP.text(),
            "brand": self.uic.brandSP.text(),
            "price": tempprice,
            "remain": tempremain,
            "image": self.uic.imageSP.text(),
            "url": self.uic.videoSP.text()

        }
        request = requests.post("https://shopapiptithcm.azurewebsites.net/api/createitem",json=tempsp).text
        response = json.loads(request)
        if response['code'] == 1:
            QMessageBox.information(self,'','thanh cong')
        else:
            QMessageBox.information(self,'','that bai')
    def user(self):
        rq = requests.get("https://shopapiptithcm.azurewebsites.net/api/getalluser").text
        data = json.loads(rq)
        print(data)
        row = 0
        self.uic.tableWidget_3.setRowCount(len(data))
        for items in data:
            self.uic.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(items["id"]))
            self.uic.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(items["pass"]))
            self.uic.tableWidget_3.setItem(row, 2, QtWidgets.QTableWidgetItem(items["type"]))
            self.uic.tableWidget_3.setItem(row, 3, QtWidgets.QTableWidgetItem(items["email"]))
            self.uic.tableWidget_3.setItem(row, 4, QtWidgets.QTableWidgetItem(items["phone"]))
            self.uic.tableWidget_3.setItem(row, 5, QtWidgets.QTableWidgetItem(items["status"]))
            btn = QPushButton("Edit".format(row))
            self.uic.tableWidget_3.setCellWidget(row, 6, btn)
            btn.setStyleSheet(
                "background-color: rgb(85, 170, 255);border-bottom-left-radius:0px;border-bottom-right-radius:0px;")
            row += 1
            btn.clicked.connect(self.detailUser)


    def detailUser(self):
        button = self.sender()
        index = self.uic.tableWidget_3.indexAt(button.pos())
        self.uic.idU.setText(self.uic.tableWidget_3.item(index.row(), 0).text())
        self.uic.passU.setText(self.uic.tableWidget_3.item(index.row(), 1).text())
        self.uic.emailU.setText(self.uic.tableWidget_3.item(index.row(), 3).text())
        self.uic.comboBox.setCurrentText(self.uic.tableWidget_3.item(index.row(), 5).text())
        self.uic.updateU.clicked.connect(self.updateuser)
        global tempstatus
        tempstatus = self.uic.tableWidget_3.item(index.row(), 5).text()



    def updateuser(self):
        tempUser = {
                "id": self.uic.idU.text(),
                "pass": self.uic.passU.text(),
                "type": "USER",
                "email": self.uic.emailU.text(),
                "phone": None,
                "status": self.uic.comboBox.currentText()
        }
        request = requests.put("https://shopapiptithcm.azurewebsites.net/api/updateuseradmin",json=tempUser).text
        response = json.loads(request)
        if response['code'] == 1:
            QMessageBox.information(self,"","Thanh cong")
        else:
            QMessageBox.information(self,"","That bai")

    def order(self):
        rq = requests.get("https://shopapiptithcm.azurewebsites.net/api/getorder").text
        data_2 = json.loads(rq)
        row = 0
        self.uic.tableWidget_2.setRowCount(len(data_2))
        for items in data_2:
            self.uic.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(items["phone"]))
            self.uic.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(items["status"]))
            self.uic.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(items["payment"]))
            self.uic.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(items["address"]))
            self.uic.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(items["date"]))
            self.uic.tableWidget_2.setItem(row, 5, QtWidgets.QTableWidgetItem(str(items["total"])))
            btn = QPushButton("Edit".format(row))
            self.uic.tableWidget_2.setCellWidget(row, 6, btn)
            btn.setStyleSheet(
                "background-color: rgb(85, 170, 255);border-bottom-left-radius:0px;border-bottom-right-radius:0px;")
            row += 1
            btn.clicked.connect(self.detailOrder)


    def detailOrder(self):

        button = self.sender()
        index = self.uic.tableWidget_2.indexAt(button.pos())
        self.uic.comboBox_2.setCurrentText(self.uic.tableWidget_2.item(index.row(),1).text())
        self.uic.paymentOD.setText(self.uic.tableWidget_2.item(index.row(), 2).text())
        self.uic.addressOD.setText(self.uic.tableWidget_2.item(index.row(), 3).text())
        self.uic.phoneOD.setText(self.uic.tableWidget_2.item(index.row(), 0).text())
        self.uic.updateOD.clicked.connect(self.updateorder)
        global idtemp
        idtemp= dataOrder[index.row()]


    def updateorder(self):
        if idtemp =="done":
            QMessageBox.information(self,'','khong the chinh sua don da hoan thanh')
        else:
            idtemp2 = idtemp
            print(idtemp2)
            idtemp2['status'] = self.uic.comboBox_2.currentText()
            idtemp2['payment'] = self.uic.paymentOD.text()
            idtemp2['adress'] = self.uic.addressOD.text()
            idtemp2['phone'] = self.uic.phoneOD.text()
            request = requests.put("https://shopapiptithcm.azurewebsites.net/api/updateorderadmin",json=idtemp2).text
            re = json.loads(request)
            if re['code'] == 1:
                QMessageBox.information(self,'','thanh cong')
            else:
                QMessageBox.information(self,'','that bai')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_win = Login()
    screenadmin = Manager()
    createacc = CreateAcc()
    screencart = Cart()
    main_win.show()
    sys.exit(app.exec_())







