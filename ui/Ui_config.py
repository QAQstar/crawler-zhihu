# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Code\Python\crawler\ui\config.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.gridWidget = QtWidgets.QWidget(Dialog)
        self.gridWidget.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setHorizontalSpacing(50)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalWidget = QtWidgets.QWidget(self.gridWidget)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_15.setContentsMargins(1, -1, -1, -1)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_8 = QtWidgets.QLabel(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_15.addWidget(self.label_8)
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber_2.sizePolicy().hasHeightForWidth())
        self.lcdNumber_2.setSizePolicy(sizePolicy)
        self.lcdNumber_2.setDigitCount(2)
        self.lcdNumber_2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_2.setProperty("value", 5.0)
        self.lcdNumber_2.setProperty("intValue", 5)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.horizontalLayout_15.addWidget(self.lcdNumber_2)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_2.setSizePolicy(sizePolicy)
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(10)
        self.horizontalSlider_2.setSingleStep(1)
        self.horizontalSlider_2.setPageStep(1)
        self.horizontalSlider_2.setProperty("value", 5)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalLayout_15.addWidget(self.horizontalSlider_2)
        self.gridLayout.addWidget(self.horizontalWidget, 1, 1, 1, 1)
        self.horizontalWidget1 = QtWidgets.QWidget(self.gridWidget)
        self.horizontalWidget1.setObjectName("horizontalWidget1")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.horizontalWidget1)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_9 = QtWidgets.QLabel(self.horizontalWidget1)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_16.addWidget(self.label_9)
        self.spinBox_4 = QtWidgets.QSpinBox(self.horizontalWidget1)
        self.spinBox_4.setMinimum(1)
        self.spinBox_4.setMaximum(500)
        self.spinBox_4.setSingleStep(10)
        self.spinBox_4.setProperty("value", 5)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_16.addWidget(self.spinBox_4)
        self.gridLayout.addWidget(self.horizontalWidget1, 2, 1, 1, 1)
        self.horizontalWidget2 = QtWidgets.QWidget(self.gridWidget)
        self.horizontalWidget2.setObjectName("horizontalWidget2")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.horizontalWidget2)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.horizontalWidget3 = QtWidgets.QWidget(self.horizontalWidget2)
        self.horizontalWidget3.setObjectName("horizontalWidget3")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.horizontalWidget3)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_5 = QtWidgets.QLabel(self.horizontalWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_14.addWidget(self.label_5)
        self.lcdNumber = QtWidgets.QLCDNumber(self.horizontalWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy)
        self.lcdNumber.setDigitCount(3)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setProperty("intValue", 50)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout_14.addWidget(self.lcdNumber)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(500)
        self.horizontalSlider.setSingleStep(10)
        self.horizontalSlider.setPageStep(50)
        self.horizontalSlider.setProperty("value", 50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_14.addWidget(self.horizontalSlider)
        self.horizontalLayout_12.addWidget(self.horizontalWidget3)
        self.gridLayout.addWidget(self.horizontalWidget2, 1, 0, 1, 1)
        self.horizontalWidget_2 = QtWidgets.QWidget(self.gridWidget)
        self.horizontalWidget_2.setObjectName("horizontalWidget_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_6 = QtWidgets.QLabel(self.horizontalWidget_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_9.addWidget(self.label_6)
        self.spinBox_3 = QtWidgets.QSpinBox(self.horizontalWidget_2)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(50)
        self.spinBox_3.setProperty("value", 5)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_9.addWidget(self.spinBox_3)
        self.gridLayout.addWidget(self.horizontalWidget_2, 2, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.gridWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox.setMinimum(0.5)
        self.doubleSpinBox.setMaximum(10.0)
        self.doubleSpinBox.setSingleStep(0.5)
        self.doubleSpinBox.setProperty("value", 5.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_4.addWidget(self.doubleSpinBox)
        self.gridLayout.addWidget(self.widget, 4, 0, 1, 1)
        self.horizontalWidget_5 = QtWidgets.QWidget(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget_5.sizePolicy().hasHeightForWidth())
        self.horizontalWidget_5.setSizePolicy(sizePolicy)
        self.horizontalWidget_5.setObjectName("horizontalWidget_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalWidget_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.horizontalWidget_5)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.horizontalWidget_5)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(50)
        self.spinBox.setProperty("value", 5)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_3.addWidget(self.spinBox)
        self.gridLayout.addWidget(self.horizontalWidget_5, 0, 0, 1, 1)
        self.horizontalWidget4 = QtWidgets.QWidget(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget4.sizePolicy().hasHeightForWidth())
        self.horizontalWidget4.setSizePolicy(sizePolicy)
        self.horizontalWidget4.setObjectName("horizontalWidget4")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.horizontalWidget4)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_7 = QtWidgets.QLabel(self.horizontalWidget4)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_17.addWidget(self.label_7)
        self.verticalWidget = QtWidgets.QWidget(self.horizontalWidget4)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.verticalWidget)
        self.radioButton.setChecked(False)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalWidget)
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_2.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.verticalWidget)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_2.addWidget(self.radioButton_3)
        self.horizontalLayout_17.addWidget(self.verticalWidget)
        self.gridLayout.addWidget(self.horizontalWidget4, 3, 1, 1, 1)
        self.horizontalWidget_4 = QtWidgets.QWidget(self.gridWidget)
        self.horizontalWidget_4.setObjectName("horizontalWidget_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.horizontalWidget_4)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_2 = QtWidgets.QLabel(self.horizontalWidget_4)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_11.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.horizontalWidget_4)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(50)
        self.spinBox_2.setProperty("value", 10)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_11.addWidget(self.spinBox_2)
        self.gridLayout.addWidget(self.horizontalWidget_4, 0, 1, 1, 1)
        self.horizontalWidget5 = QtWidgets.QWidget(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget5.sizePolicy().hasHeightForWidth())
        self.horizontalWidget5.setSizePolicy(sizePolicy)
        self.horizontalWidget5.setObjectName("horizontalWidget5")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.horizontalWidget5)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_4 = QtWidgets.QLabel(self.horizontalWidget5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_10.addWidget(self.label_4)
        self.textEdit = QtWidgets.QTextEdit(self.horizontalWidget5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 50))
        self.textEdit.setToolTip("")
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_10.addWidget(self.textEdit)
        self.gridLayout.addWidget(self.horizontalWidget5, 3, 0, 1, 1)
        self.horizontalWidget6 = QtWidgets.QWidget(self.gridWidget)
        self.horizontalWidget6.setObjectName("horizontalWidget6")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalWidget6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalWidget6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addWidget(self.horizontalWidget6, 5, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "设置"))
        self.label_8.setText(_translate("Dialog", "情感分析训练轮数"))
        self.label_9.setText(_translate("Dialog", "模糊搜索结果限制"))
        self.label_5.setText(_translate("Dialog", "爬取回答数"))
        self.label_6.setText(_translate("Dialog", "搜索线程数"))
        self.label_3.setText(_translate("Dialog", "分析图x轴缩放比例"))
        self.label.setText(_translate("Dialog", "解析热榜线程数"))
        self.label_7.setText(_translate("Dialog", "清理缓存间隔"))
        self.radioButton.setText(_translate("Dialog", "1天"))
        self.radioButton_2.setText(_translate("Dialog", "7天"))
        self.radioButton_3.setText(_translate("Dialog", "30天"))
        self.label_2.setText(_translate("Dialog", "爬取回答线程数"))
        self.label_4.setText(_translate("Dialog", "答案敏感词过滤"))
        self.textEdit.setPlaceholderText(_translate("Dialog", "请在此输入需要过滤的敏感词，以空格分隔"))
        self.pushButton.setText(_translate("Dialog", "恢复默认"))
        self.pushButton_2.setText(_translate("Dialog", "应用设置"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

