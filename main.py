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


class Windows(QWidget, Ui_Form):  # Windows 类，继承自 FramelessWindow 和 Ui_Form
    def __init__(self):
        super(Windows, self).__init__()  # 父类初始化
        self.setupUi(self)  # 设置UI
        self.basic_tools = HandWrite_settings()  # 实例化基础设置
        self.generator_engine = HandWrite_generator()  # 创建一个转换模板
        self.params = self.generator_engine.template_params  # 获取默认参数
        self.preview_image_dict = {}  # 预览图片字典

        # 设置默认启动项
        self.set_default()
        self.connect_signal()

    def img_show_func(self, img_path):  # 负责将图片显示在 img_preview 上
        frame = QImage(str(img_path), "PNG")
        frame = frame.scaled(
            667,
            945,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        pix = QPixmap.fromImage(frame)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()
        scene.addItem(item)
        self.img_preview.setScene(scene)
        self.img_preview.horizontalScrollBar().setValue(1)  # 设置滚动条初始位置
        self.img_preview.verticalScrollBar().setValue(1)  # 设置滚动条初始位置

    def page_number_change(self):  # 当 page_number 改变时，调用 img_show_func
        if self.page_number.currentText() != "":
            self.img_show_func(
                self.preview_image_dict[int(self.page_number.currentText())]
            )

    def connect_signal(self):  # 连接信号
        self.page_number.currentIndexChanged.connect(self.page_number_change)
        self.pushButton_export.clicked.connect(self.export)
        self.pushButton_theme.clicked.connect(self.generate_theme)

    def set_default(self):  # 通过默认模板来设置页面默认值
        # 设置宽度高度
        self.lineEdit_width.setText(str(self.params["default_paper_x"]))
        self.lineEdit_height.setText(str(self.params["default_paper_y"]))

        # 设置默认字体和候选字体
        self.ttf_selector.addItems(self.basic_tools.get_ttf_file_path()[0])
        self.ttf_selector.setCurrentIndex(0)

        # 设置字体大小，行距，字距
        self.lineEdit_font_size.setText(str(self.params["default_font_size"]))
        self.lineEdit_line_spacing.setText(str(self.params["default_line_spacing"]))
        self.lineEdit_char_distance.setText(str(self.params["default_word_spacing"]))

        # 设置留白
        self.lineEdit_margin_top.setText(str(self.params["default_top_margin"]))
        self.lineEdit_margin_bottom.setText(str(self.params["default_bottom_margin"]))
        self.lineEdit_margin_left.setText(str(self.params["default_left_margin"]))
        self.lineEdit_margin_right.setText(str(self.params["default_right_margin"]))

        # 设置默认字体颜色, 背景颜色
        self.comboBox_char_color.addItems(self.basic_tools.font_color_dict.keys())
        self.comboBox_char_color.setCurrentIndex(0)
        self.comboBox_background_color.addItems(
            self.basic_tools.background_color_dict.keys()
        )
        self.comboBox_background_color.setCurrentIndex(0)

        # 设置扰动参数
        self.lineEdit_line_spacing_sigma.setText(
            str(self.params["default_line_spacing_sigma"])
        )
        self.lineEdit_font_size_sigma.setText(
            str(self.params["default_font_size_sigma"])
        )
        self.lineEdit_word_spacing_sigma.setText(
            str(self.params["default_word_spacing_sigma"])
        )
        self.lineEdit_perturb_x_sigma.setText(
            str(self.params["default_perturb_x_sigma"])
        )
        self.lineEdit_perturb_y_sigma.setText(
            str(self.params["default_perturb_y_sigma"])
        )
        self.lineEdit_perturb_theta_sigma.setText(
            str(self.params["default_perturb_theta_sigma"])
        )

        # 设置默认文本
        default_text = "使用 Qt6 编写的手写字体生成器，旨在帮助用户自动完成一些无用的手写作业任务。\n 项目提供了丰富的设置选项，包括字体、字号、行距、字距、颜色、背景、倍率、扰动等。\n 项目还提供了一个随机文章生成器，可以帮助用户生成一些无用的文章。"
        self.textEdit_main.setPlainText(default_text)

        # 设置默认倍率
        self.comboBox_resolution.addItems(self.basic_tools.default_rate_dict.keys())
        self.comboBox_resolution.setCurrentIndex(2)

        # 设置默认预览
        self.generator_engine.modify_template_params(
            default_background=(255, 255, 255, 255)
        )
        # 生成默认预览图片
        preview_image_dict = self.generator_engine.generate_image(default_text)
        self.img_show_func(preview_image_dict[0])
        # 设置 page 列表
        self.page_number.addItems([str(i) for i in preview_image_dict])

    # 读取填写信息
    def get_info_from_form(self):
        self.params["default_paper_x"] = int(float(self.lineEdit_width.text()))
        self.params["default_paper_y"] = int(float(self.lineEdit_height.text()))
        self.params["default_font"] = self.basic_tools.get_ttf_file_path()[1][
            self.ttf_selector.currentIndex()
        ]
        self.params["default_font_size"] = int(float(self.lineEdit_font_size.text()))
        self.params["default_line_spacing"] = int(
            float(self.lineEdit_line_spacing.text())
        )
        self.params["default_word_spacing"] = int(
            float(self.lineEdit_char_distance.text())
        )
        self.params["default_top_margin"] = int(float(self.lineEdit_margin_top.text()))
        self.params["default_bottom_margin"] = int(
            float(self.lineEdit_margin_bottom.text())
        )
        self.params["default_left_margin"] = int(
            float(self.lineEdit_margin_left.text())
        )
        self.params["default_right_margin"] = int(
            float(self.lineEdit_margin_right.text())
        )
        self.params["default_fill"] = self.basic_tools.font_color_dict[
            self.comboBox_char_color.currentText()
        ]
        self.params["default_background"] = self.basic_tools.background_color_dict[
            self.comboBox_background_color.currentText()
        ]
        self.params["rate"] = self.basic_tools.default_rate_dict[
            self.comboBox_resolution.currentText()
        ]
        self.params["default_line_spacing_sigma"] = float(
            self.lineEdit_line_spacing_sigma.text()
        )
        self.params["default_font_size_sigma"] = float(
            self.lineEdit_font_size_sigma.text()
        )
        self.params["default_word_spacing_sigma"] = float(
            self.lineEdit_word_spacing_sigma.text()
        )
        self.params["default_perturb_x_sigma"] = float(
            self.lineEdit_perturb_x_sigma.text()
        )
        self.params["default_perturb_y_sigma"] = float(
            self.lineEdit_perturb_y_sigma.text()
        )
        self.params["default_perturb_theta_sigma"] = float(
            self.lineEdit_perturb_theta_sigma.text()
        )

    def get_text_from_textedit_main(self):
        return self.textEdit_main.toPlainText()

    def get_theme_from_lineEdit_theme(self):
        return self.lineEdit_theme.text()

    def get_count_from_lineEdit_word_count(self):
        return self.lineEdit_word_count.text()

    # 获取主题，并生成文章
    def generate_theme(self):
        theme = self.get_theme_from_lineEdit_theme()
        count = self.get_count_from_lineEdit_word_count()
        if theme == "":
            self.textEdit_main.setPlainText("请输入主题")
            return
        if count == "":
            self.textEdit_main.setPlainText("请输入字数")
            return
        if not count.isdigit():
            self.textEdit_main.setPlainText("字数必须为整数")
            return
        generated_article = BullshitGenerator(theme, int(count))
        self.textEdit_main.setPlainText(generated_article)

    # 导出
    def export(self):
        folder_path = "outputs"
        if os.path.exists(folder_path):
            # 遍历目录中的所有文件和子目录
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"无法删除文件 '{file_path}': {e}")
        else:
            print(f"目录 '{folder_path}' 不存在。")

        # 清空 page_number
        self.page_number.clear()
        # 读取填写信息
        self.get_info_from_form()
        # 修改模板参数
        self.generator_engine.modify_template_params(**self.params)
        # 生成模板
        self.generator_engine.generate_template()
        # 生成图片
        self.preview_image_dict = self.generator_engine.generate_image(
            self.get_text_from_textedit_main()
        )
        # 显示图片
        self.img_show_func(self.preview_image_dict[0])
        # 设置 page 列表
        self.page_number.addItems([str(i) for i in self.preview_image_dict])


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("QT_GUI/icon.jpg"))
    window = Windows()
    window.show()
    sys.exit(app.exec())
