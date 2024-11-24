# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtGui, QtWidgets

# -*- coding: utf-8 -*-
# 导入依赖
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QApplication, QWidget

from QT_GUI.qt_gui import *  # GUI
from HandWrite.HandWrite_generator import HandWrite_generator  # 手写转换
from HandWrite.HandWrite_settings import HandWrite_settings  # 基础设置
from BullshitGenerator.BullshitGenerator import BullshitGenerator  # 文章生成器


class Ui_Form(object):
    def setupUi(self, Form):
        #  主窗口标识与大小
        Form.setObjectName("Form")
        Form.resize(1200, 800)

        # 主窗口布局
        self.mainLayout = QtWidgets.QHBoxLayout(
            Form
        )  # 主窗口水平布局，从左到右添加控件
        self.mainLayout.setObjectName("mainLayout")

        ## 显示区域：图片预览，扰动参数
        self.displayLayout = (
            QtWidgets.QVBoxLayout()
        )  # 显示区域垂直布局，从上到下添加控件
        self.displayLayout.setObjectName("displayLayout")

        ### 图片预览
        self.img_preview = QtWidgets.QGraphicsView(Form)  # 图片预览组件
        self.img_preview.setObjectName("img_preview")
        self.displayLayout.addWidget(self.img_preview)  # 添加图片预览组件

        ### 页数选择
        self.pageLayout = QtWidgets.QHBoxLayout()
        self.pageLayout.setObjectName("pageLayout")
        #### 页数标签
        self.page_label = QtWidgets.QLabel(Form)
        self.page_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.page_label.setObjectName("page_label")
        self.pageLayout.addWidget(self.page_label)
        #### 页数选择框
        self.page_number = QtWidgets.QComboBox(Form)
        self.page_number.setObjectName("page_number")
        self.pageLayout.addWidget(self.page_number)
        self.pageLayout.setStretch(0, 1)
        self.pageLayout.setStretch(1, 8)

        page_font_width = self.page_label.fontMetrics().boundingRect("页码:").width()
        self.page_label.setFixedWidth(page_font_width)
        self.displayLayout.addLayout(self.pageLayout)  # 添加页数选择

        self.mainLayout.addLayout(self.displayLayout)  # 添加显示区域

        ## 信息区域：宽高，字体，字体大小，行距，字距，留白，颜色，文本，分辨率，导出
        self.infoLayout = QtWidgets.QVBoxLayout()
        self.infoLayout.setObjectName("infoLayout")
        self.line = QtWidgets.QLabel()
        ## 页面设置提示标签：包括页面宽高和留白
        self.label_info_page = QtWidgets.QLabel(Form)
        self.label_info_page.setObjectName("label_info_page")
        self.infoLayout.addWidget(self.label_info_page)
        ### 宽高
        #### 宽高标签
        self.pageSettingsLayout = QtWidgets.QHBoxLayout()
        self.pageSettingsLayout.setObjectName("pageSettingsLayout")
        ##### 宽度标签
        self.label_width = QtWidgets.QLabel(Form)
        self.label_width.setObjectName("label_width")
        self.pageSettingsLayout.addWidget(self.label_width)
        ##### 高度标签
        self.label_height = QtWidgets.QLabel(Form)
        self.label_height.setObjectName("label_height")
        self.pageSettingsLayout.addWidget(self.label_height)

        self.infoLayout.addLayout(self.pageSettingsLayout)  # 添加宽高标签

        #### 宽高输入框
        self.pageInputsLayout = QtWidgets.QHBoxLayout()
        self.pageInputsLayout.setObjectName("pageInputsLayout")
        ##### 宽度输入框
        self.lineEdit_width = QtWidgets.QLineEdit(Form)
        self.lineEdit_width.setObjectName("lineEdit_width")
        self.pageInputsLayout.addWidget(self.lineEdit_width)
        ##### X 标签
        self.resolution_x = QtWidgets.QLabel(Form)
        self.resolution_x.setObjectName("resolution_x")
        self.pageInputsLayout.addWidget(self.resolution_x)
        ##### 高度输入框
        self.lineEdit_height = QtWidgets.QLineEdit(Form)
        self.lineEdit_height.setObjectName("lineEdit_height")
        self.pageInputsLayout.addWidget(self.lineEdit_height)

        self.infoLayout.addLayout(self.pageInputsLayout)  # 添加宽高输入框
        ### 留白
        self.marginLayout = QtWidgets.QHBoxLayout()
        self.marginLayout.setObjectName("marginLayout")
        #### 留白标签
        self.label_margin = QtWidgets.QLabel(Form)
        self.label_margin.setObjectName("label_margin")
        self.marginLayout.addWidget(self.label_margin)

        self.infoLayout.addLayout(self.marginLayout)  # 添加留白标签

        #### 留白输入框
        self.marginInputsLayout = QtWidgets.QHBoxLayout()
        self.marginInputsLayout.setObjectName("marginInputsLayout")
        ##### 上留白输入框
        self.lineEdit_margin_top = QtWidgets.QLineEdit(Form)
        self.lineEdit_margin_top.setObjectName("lineEdit_margin_top")
        self.marginInputsLayout.addWidget(self.lineEdit_margin_top)
        ##### 下留白输入框
        self.lineEdit_margin_bottom = QtWidgets.QLineEdit(Form)
        self.lineEdit_margin_bottom.setObjectName("lineEdit_margin_bottom")
        self.marginInputsLayout.addWidget(self.lineEdit_margin_bottom)
        ##### 左留白输入框
        self.lineEdit_margin_left = QtWidgets.QLineEdit(Form)
        self.lineEdit_margin_left.setObjectName("lineEdit_margin_left")
        self.marginInputsLayout.addWidget(self.lineEdit_margin_left)
        ##### 右留白输入框
        self.lineEdit_margin_right = QtWidgets.QLineEdit(Form)
        self.lineEdit_margin_right.setObjectName("lineEdit_margin_right")
        self.marginInputsLayout.addWidget(self.lineEdit_margin_right)

        self.infoLayout.addLayout(self.marginInputsLayout)  # 添加留白输入框
        self.infoLayout.addWidget(self.line)  # 添加分隔线

        ## 格式设置提示标签：包括字体，字体大小，行距，字距，字体色，背景色
        self.label_info_format = QtWidgets.QLabel(Form)
        self.label_info_format.setObjectName("label_info_format")
        self.infoLayout.addWidget(self.label_info_format)

        ### 字体，字体大小，行距，字距
        #### 字体
        self.fontSettingsLayout = QtWidgets.QHBoxLayout()
        self.fontSettingsLayout.setObjectName("fontSettingsLayout")
        ##### 字体标签
        self.label_font = QtWidgets.QLabel(Form)
        self.label_font.setObjectName("label_font")
        self.fontSettingsLayout.addWidget(self.label_font)
        #### 字体选择框
        self.ttf_selector = QtWidgets.QComboBox(Form)
        self.ttf_selector.setObjectName("ttf_selector")
        self.fontSettingsLayout.addWidget(self.ttf_selector)

        label_font_width = self.label_font.fontMetrics().boundingRect("字体:").width()
        self.label_font.setFixedWidth(label_font_width)
        self.infoLayout.addLayout(self.fontSettingsLayout)  # 添加字体选择框

        #### 字体大小，行距，字距标签
        self.fontParamsLayout = QtWidgets.QHBoxLayout()
        self.fontParamsLayout.setObjectName("fontParamsLayout")
        self.label_font_size = QtWidgets.QLabel(Form)
        ##### 字体大小标签
        self.label_font_size.setObjectName("label_font_size")
        self.fontParamsLayout.addWidget(self.label_font_size)
        self.label_line_spacing = QtWidgets.QLabel(Form)
        ##### 行距标签
        self.label_line_spacing.setObjectName("label_line_spacing")
        self.fontParamsLayout.addWidget(self.label_line_spacing)
        self.label_char_distance = QtWidgets.QLabel(Form)
        ##### 字距标签
        self.label_char_distance.setObjectName("label_char_distance")
        self.fontParamsLayout.addWidget(self.label_char_distance)

        self.infoLayout.addLayout(self.fontParamsLayout)  # 添加字体大小，行距，字距标签

        #### 字体大小，行距，字距输入框
        self.fontInputsLayout = QtWidgets.QHBoxLayout()
        self.fontInputsLayout.setObjectName("fontInputsLayout")
        self.lineEdit_font_size = QtWidgets.QLineEdit(Form)
        ##### 字体大小输入框
        self.lineEdit_font_size.setObjectName("lineEdit_font_size")
        self.fontInputsLayout.addWidget(self.lineEdit_font_size)
        self.lineEdit_line_spacing = QtWidgets.QLineEdit(Form)
        ##### 行距输入框
        self.lineEdit_line_spacing.setObjectName("lineEdit_line_spacing")
        self.fontInputsLayout.addWidget(self.lineEdit_line_spacing)
        self.lineEdit_char_distance = QtWidgets.QLineEdit(Form)
        ##### 字距输入框
        self.lineEdit_char_distance.setObjectName("lineEdit_char_distance")
        self.fontInputsLayout.addWidget(self.lineEdit_char_distance)

        self.infoLayout.addLayout(
            self.fontInputsLayout
        )  # 添加字体大小，行距，字距输入框

        ### 颜色
        self.colorLayout = QtWidgets.QHBoxLayout()
        self.colorLayout.setObjectName("colorLayout")
        #### 字体色标签
        self.label_char_color = QtWidgets.QLabel(Form)
        self.label_char_color.setObjectName("label_char_color")
        self.colorLayout.addWidget(self.label_char_color)
        #### 背景色标签
        self.label_background_color = QtWidgets.QLabel(Form)
        self.label_background_color.setObjectName("label_background_color")
        self.colorLayout.addWidget(self.label_background_color)

        self.infoLayout.addLayout(self.colorLayout)  # 添加颜色标签

        #### 颜色选择框
        self.colorInputsLayout = QtWidgets.QHBoxLayout()
        self.colorInputsLayout.setObjectName("colorInputsLayout")
        ##### 字体色选择框
        self.comboBox_char_color = QtWidgets.QComboBox(Form)
        self.comboBox_char_color.setObjectName("comboBox_char_color")
        self.colorInputsLayout.addWidget(self.comboBox_char_color)
        ##### 背景色选择框
        self.comboBox_background_color = QtWidgets.QComboBox(Form)
        self.comboBox_background_color.setObjectName("comboBox_background_color")
        self.colorInputsLayout.addWidget(self.comboBox_background_color)

        self.infoLayout.addLayout(self.colorInputsLayout)  # 添加颜色选择框
        self.infoLayout.addWidget(self.line)  # 添加分隔线

        ### 扰动设置标签
        self.label_perturb = QtWidgets.QLabel(Form)
        self.label_perturb.setObjectName("label_perturb")
        self.infoLayout.addWidget(self.label_perturb)

        ### 扰动参数 1
        #### 扰动参数 1 标签
        self.perturbParams1Layout = (
            QtWidgets.QHBoxLayout()
        )  # 扰动参数水平布局，从左到右添加控件
        self.perturbParams1Layout.setObjectName("perturbParams1Layout")
        ##### 行间距扰动标签
        self.label_line_spacing_sigma = QtWidgets.QLabel(Form)
        self.label_line_spacing_sigma.setObjectName("label_line_spacing_sigma")
        self.perturbParams1Layout.addWidget(self.label_line_spacing_sigma)
        ##### 字体大小扰动标签
        self.label_font_size_sigma = QtWidgets.QLabel(Form)
        self.label_font_size_sigma.setObjectName("label_font_size_sigma")
        self.perturbParams1Layout.addWidget(self.label_font_size_sigma)
        ##### 字间距扰动标签
        self.label_word_spacing_sigma = QtWidgets.QLabel(Form)
        self.label_word_spacing_sigma.setObjectName("label_word_spacing_sigma")
        self.perturbParams1Layout.addWidget(self.label_word_spacing_sigma)

        self.infoLayout.addLayout(self.perturbParams1Layout)  # 添加扰动参数 1 标签

        #### 扰动参数 1 输入框
        self.perturbInputs1Layout = QtWidgets.QHBoxLayout()
        self.perturbInputs1Layout.setObjectName("perturbInputs1Layout")
        #### 行间距扰动输入框
        self.lineEdit_line_spacing_sigma = QtWidgets.QLineEdit(Form)
        self.lineEdit_line_spacing_sigma.setObjectName("lineEdit_line_spacing_sigma")
        self.perturbInputs1Layout.addWidget(self.lineEdit_line_spacing_sigma)
        #### 字体大小扰动输入框
        self.lineEdit_font_size_sigma = QtWidgets.QLineEdit(Form)
        self.lineEdit_font_size_sigma.setObjectName("lineEdit_font_size_sigma")
        self.perturbInputs1Layout.addWidget(self.lineEdit_font_size_sigma)
        #### 字间距扰动输入框
        self.lineEdit_word_spacing_sigma = QtWidgets.QLineEdit(Form)
        self.lineEdit_word_spacing_sigma.setObjectName("lineEdit_word_spacing_sigma")
        self.perturbInputs1Layout.addWidget(self.lineEdit_word_spacing_sigma)

        self.infoLayout.addLayout(self.perturbInputs1Layout)  # 添加扰动参数 1 输入框

        ### 扰动参数 2
        #### 扰动参数 2 标签
        self.perturbParams2Layout = (
            QtWidgets.QHBoxLayout()
        )  # 扰动参数水平布局，从左到右添加控件
        self.perturbParams2Layout.setObjectName("perturbParams2Layout")
        #### 横向笔画扰动标签
        self.label_perturb_x_sigma = QtWidgets.QLabel(Form)
        self.label_perturb_x_sigma.setObjectName("label_perturb_x_sigma")
        self.perturbParams2Layout.addWidget(self.label_perturb_x_sigma)
        #### 纵向笔画扰动标签
        self.label_perturb_y_sigma = QtWidgets.QLabel(Form)
        self.label_perturb_y_sigma.setObjectName("label_perturb_y_sigma")
        self.perturbParams2Layout.addWidget(self.label_perturb_y_sigma)
        #### 旋转笔画扰动标签
        self.label_perturb_theta_sigma = QtWidgets.QLabel(Form)
        self.label_perturb_theta_sigma.setObjectName("label_perturb_theta_sigma")
        self.perturbParams2Layout.addWidget(self.label_perturb_theta_sigma)

        self.infoLayout.addLayout(self.perturbParams2Layout)  # 添加扰动参数 2 标签

        #### 扰动参数 2 输入框
        self.perturbInputs2Layout = QtWidgets.QHBoxLayout()
        self.perturbInputs2Layout.setObjectName("perturbInputs2Layout")
        #### 横向笔画扰动输入框
        self.lineEdit_perturb_x_sigma = QtWidgets.QLineEdit(Form)
        self.lineEdit_perturb_x_sigma.setObjectName("lineEdit_perturb_x_sigma")
        self.perturbInputs2Layout.addWidget(self.lineEdit_perturb_x_sigma)
        #### 纵向笔画扰动输入框
        self.lineEdit_perturb_y_sigma = QtWidgets.QLineEdit(Form)
        self.lineEdit_perturb_y_sigma.setObjectName("lineEdit_perturb_y_sigma")
        self.perturbInputs2Layout.addWidget(self.lineEdit_perturb_y_sigma)
        #### 旋转笔画扰动输入框
        self.lineEdit_perturb_theta_sigma = QtWidgets.QLineEdit(Form)
        self.lineEdit_perturb_theta_sigma.setObjectName("lineEdit_perturb_theta_sigma")
        self.perturbInputs2Layout.addWidget(self.lineEdit_perturb_theta_sigma)

        self.infoLayout.addLayout(self.perturbInputs2Layout)  # 添加扰动参数 2 输入框
        self.infoLayout.addWidget(self.line)  # 添加分隔线

        ### 文本设置标签
        self.label_text = QtWidgets.QLabel(Form)
        self.label_text.setObjectName("label_text")
        self.infoLayout.addWidget(self.label_text)

        ### 主题
        self.themeLayout = QtWidgets.QHBoxLayout()
        self.themeLayout.setObjectName("themeLayout")
        #### 主题标签
        self.label_theme = QtWidgets.QLabel(Form)
        self.label_theme.setObjectName("label_theme")
        self.themeLayout.addWidget(self.label_theme)
        #### 主题输入框
        self.lineEdit_theme = QtWidgets.QLineEdit(Form)
        self.lineEdit_theme.setObjectName("lineEdit_theme")
        self.themeLayout.addWidget(self.lineEdit_theme)
        ### 字数
        #### 字数标签
        self.label_word_count = QtWidgets.QLabel(Form)
        self.label_word_count.setObjectName("label_word_count")
        self.themeLayout.addWidget(self.label_word_count)
        #### 字数输入框
        self.lineEdit_word_count = QtWidgets.QLineEdit(Form)
        self.lineEdit_word_count.setObjectName("lineEdit_word_count")
        self.themeLayout.addWidget(self.lineEdit_word_count)
        #### 确认按钮
        self.pushButton_theme = QtWidgets.QPushButton(Form)
        self.pushButton_theme.setObjectName("pushButton_theme")
        self.themeLayout.addWidget(self.pushButton_theme)

        self.infoLayout.addLayout(self.themeLayout)  # 添加主题

        ### 文本
        self.textEdit_main = QtWidgets.QTextEdit(Form)
        self.textEdit_main.setObjectName("textEdit_main")

        self.infoLayout.addWidget(self.textEdit_main)  # 添加文本输入框
        self.infoLayout.addWidget(self.line)  # 添加分隔线

        ### 导出设置标签
        self.label_export = QtWidgets.QLabel(Form)
        self.label_export.setObjectName("label_export")
        self.infoLayout.addWidget(self.label_export)

        ### 渲染精度，导出
        self.exportLayout = QtWidgets.QHBoxLayout()
        self.exportLayout.setObjectName("exportLayout")
        #### 渲染精度标签
        self.comboBox_resolution_info = QtWidgets.QLabel(Form)
        self.comboBox_resolution_info.setObjectName("comboBox_resolution_info")
        self.exportLayout.addWidget(self.comboBox_resolution_info)
        #### 渲染精度选择框
        self.comboBox_resolution = QtWidgets.QComboBox(Form)
        self.comboBox_resolution.setObjectName("comboBox_resolution")
        self.exportLayout.addWidget(self.comboBox_resolution)
        #### 导出按钮
        self.pushButton_export = QtWidgets.QPushButton(Form)
        self.pushButton_export.setObjectName("pushButton_export")
        self.exportLayout.addWidget(self.pushButton_export)

        self.exportLayout.setStretch(1, 1)  # 设置渲染精度选择框的拉伸比例
        self.exportLayout.setStretch(2, 5)  # 设置导出按钮的拉伸比例
        self.infoLayout.addLayout(self.exportLayout)  # 添加渲染精度选择框和导出按钮

        ### 导出提示信息
        self.label_info = QtWidgets.QLabel(Form)
        self.label_info.setObjectName("label_info")
        self.infoLayout.addWidget(self.label_info)
        self.infoLayout.addWidget(self.line)  # 添加分隔线

        ### 作者信息
        self.authorLayout = QtWidgets.QHBoxLayout()
        self.authorLayout.setObjectName("authorLayout")
        self.label_author = QtWidgets.QLabel(Form)
        self.label_author.setObjectName("label_author")
        self.authorLayout.addStretch()
        self.authorLayout.addWidget(self.label_author)
        self.infoLayout.addStretch()
        self.infoLayout.addLayout(self.authorLayout)  # 添加作者信息

        self.mainLayout.addLayout(self.infoLayout)  # 添加信息区域

        self.retranslateUi(Form)  # 窗口初始化
        QtCore.QMetaObject.connectSlotsByName(Form)  # 连接信号与槽

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "自动手写生成器"))
        self.label_line_spacing_sigma.setText(_translate("Form", "行间距扰动"))
        self.label_font_size_sigma.setText(_translate("Form", "字体大小扰动"))
        self.label_word_spacing_sigma.setText(_translate("Form", "字间距扰动"))
        self.label_perturb_x_sigma.setText(_translate("Form", "横向笔画扰动"))
        self.label_perturb_y_sigma.setText(_translate("Form", "纵向笔画扰动"))
        self.label_perturb_theta_sigma.setText(_translate("Form", "旋转笔画扰动"))
        self.page_label.setText(_translate("Form", "页码:"))
        self.label_width.setText(_translate("Form", "宽度"))
        self.label_height.setText(_translate("Form", "高度"))
        self.resolution_x.setText(_translate("Form", "x"))
        self.label_font_size.setText(_translate("Form", "字体大小"))
        self.label_line_spacing.setText(_translate("Form", "行距"))
        self.label_char_distance.setText(_translate("Form", "字距"))
        self.label_margin.setText(_translate("Form", "留白(上,下,左,右)"))
        self.label_char_color.setText(_translate("Form", "字体色"))
        self.label_background_color.setText(_translate("Form", "背景色"))
        self.pushButton_export.setText(_translate("Form", "导出"))
        self.label_theme.setText(_translate("Form", "主题:"))
        self.pushButton_theme.setText(_translate("Form", "生成"))
        self.label_word_count.setText(_translate("Form", "字数:"))
        self.comboBox_resolution_info.setText(_translate("Form", "渲染精度:"))
        self.label_info_page.setText(
            _translate("Form", "<span style='font-size: 18px;'><b>页面设置</b></span>")
        )
        self.label_info_format.setText(
            _translate("Form", "<span style='font-size: 18px;'><b>格式设置</b></span>")
        )
        self.label_font.setText(_translate("Form", "字体:"))
        self.label_perturb.setText(
            _translate("Form", "<span style='font-size: 18px;'><b>扰动设置</b></span>")
        )
        self.label_text.setText(
            _translate("Form", "<span style='font-size: 18px;'><b>文本设置</b></span>")
        )
        self.label_export.setText(
            _translate("Form", "<span style='font-size: 18px;'><b>导出设置</b></span>")
        )
        self.line.setText(_translate("Form", " "))
        self.label_info.setText(
            _translate(
                "Form",
                "注意当字数太多时，请调低渲染精度，否则可能会花费较长时间生成图片",
            )
        )
        self.label_author.setText(
            _translate("Form", "CaoBoyu_SZU  © 2077 Arasaka, Inc.\n")
        )

        self.label_author.setStyleSheet("color: rgb(80, 80, 80);")
        self.label_author.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_author.setWordWrap(True)
        self.label_author.setFont(QtGui.QFont("Microsoft YaHei UI", 10))
