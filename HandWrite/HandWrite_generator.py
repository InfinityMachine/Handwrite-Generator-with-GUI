# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageFont
from handright import Template, handwrite

from HandWrite.HandWrite_settings import HandWrite_settings


class HandWrite_generator(object):
    def __init__(self):
        self.template_params = {
            "rate": 4,  # 图片缩放比例
            "default_paper_x": 667,  # 默认纸张宽度 px
            "default_paper_y": 945,  # 默认纸张高度 px
            "default_font": HandWrite_settings.get_ttf_file_path()[1][
                0
            ],  # 默认字体文件路径
            "default_img_output_path": "outputs",  # 默认图片输出路径
            "default_font_size": 30,  # 默认字体大小
            "default_line_spacing": 70,  # 默认行间距 px
            "default_top_margin": 10,  # 默认顶部留白 px
            "default_bottom_margin": 10,  # 默认底部留白 px
            "default_left_margin": 10,  # 默认左边留白 px
            "default_right_margin": 10,  # 默认右边留白 px
            "default_word_spacing": 1,  # 默认字间距 px
            "default_line_spacing_sigma": 1,  # 默认行间距随机扰动 px
            "default_font_size_sigma": 1,  # 默认字体大小随机扰动 px
            "default_word_spacing_sigma": 1,  # 默认字间距随机扰动 px
            "default_perturb_x_sigma": 1,  # 默认笔画横向偏移随机扰动 px
            "default_perturb_y_sigma": 1,  # 默认笔画纵向偏移随机扰动 px
            "default_perturb_theta_sigma": 0.05,  # 默认笔画旋转偏移随机扰动 rad
            "default_start_chars": "“（[<",  # 特定字符提前换行，防止出现在行尾
            "default_end_chars": "，。",  # 防止特定字符因排版算法的自动换行而出现在行首
            "default_background": (0, 0, 0, 0),  # 默认背景颜色 (透明)
            "default_fill": (0, 0, 0, 255),  # 默认字体填充颜色 (黑色)
        }
        self.template = None  # 模板

    def modify_template_params(self, **kwargs):  # 修改模板参数
        for key, value in kwargs.items():
            self.template_params[key] = value
        self.generate_template()

    def generate_template(self):  # 生成模板
        rate = self.template_params["rate"]
        self.template = Template(
            background=Image.new(
                mode="RGBA",
                size=(
                    self.template_params["default_paper_x"] * rate,
                    self.template_params["default_paper_y"] * rate,
                ),
                color=self.template_params["default_background"],
            ),
            font=ImageFont.truetype(
                self.template_params["default_font"],
                size=self.template_params["default_font_size"] * rate,
            ),
            line_spacing=self.template_params["default_line_spacing"] * rate,
            fill=self.template_params["default_fill"],
            left_margin=self.template_params["default_left_margin"] * rate,
            top_margin=self.template_params["default_top_margin"] * rate,
            right_margin=self.template_params["default_right_margin"] * rate,
            bottom_margin=self.template_params["default_bottom_margin"] * rate,
            word_spacing=self.template_params["default_word_spacing"] * rate,
            line_spacing_sigma=self.template_params["default_line_spacing_sigma"]
            * rate,
            font_size_sigma=self.template_params["default_font_size_sigma"] * rate,
            word_spacing_sigma=self.template_params["default_word_spacing_sigma"]
            * rate,
            start_chars=self.template_params["default_start_chars"],
            end_chars=self.template_params["default_end_chars"],
            perturb_x_sigma=self.template_params["default_perturb_x_sigma"],
            perturb_y_sigma=self.template_params["default_perturb_y_sigma"],
            perturb_theta_sigma=self.template_params["default_perturb_theta_sigma"],
        )

    def generate_image(self, text):  # 生成图片
        temp_file_path_dict = {}

        if self.template is None:  # 如果模板为空
            self.generate_template()

        images = handwrite(
            text, self.template, "outpus"
        )  # 生成手写图片，如果文本较长，则分成多张图像

        for i, im in enumerate(
            images
        ):  # 保存图片，enumerate() 函数用于将一个可遍历的数据对象组合为一个索引序列，同时列出数据和数据下标
            assert isinstance(im, Image.Image)  # 判断是否为 Image.Image 类型
            save_path = Path("outputs").joinpath(f"{i}.png")  # 保存路径
            temp_file_path_dict[i] = save_path
            im.save(save_path)  # 保存图片到指定路径
        return temp_file_path_dict  # 返回图片路径
