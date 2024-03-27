from loguru import logger
from minicv import Images
from minidevice import MiniDevice
from pygamescript.template import Template, ImageTemplate
from typing import Optional
import numpy as np
from pygamescript.algo import CurveGenerate, RandomPointGenerate
import random


class GameScript(MiniDevice):
    def __init__(self, serial=None, capMethod=None, touchMethod=None, screenshotTimeout=30) -> None:
        super().__init__(serial, capMethod, touchMethod, screenshotTimeout)
        self.__current_screenshot = self.screenshot()

    def screenshot(self):
        """get cv2.Mat format image"""
        return Images.bytes2opencv(self.screenshot_raw())

    def saveScreenshot(self, path: str = './screenshot.png'):
        """save screenshot to path"""
        with open(path, 'wb') as file:
            file.write(self.screenshot_raw())

    def find(self, template: Template, isColor: bool = False, colorThreshold: int = 4):
        """find template on the device's screen

        Args:
            template (Template): 模板 ImageTemplate ColorsTemplate OcrTemplate
            isColor  (bool): 是否找色 Default to False. 仅在ImageTemplate中有效
            colorThreshold (int): 颜色相似度 0~255 Default to 4. 仅在ImageTemplate中有效

        Returns:
            result: 是否匹配到
        """
        screenshot = self.screenshot()
        if isinstance(template, ImageTemplate):
            result = template.match_color(screenshot, colorThreshold) if isColor else template.match(screenshot)
        else:
            result = template.match(screenshot)

        if result:
            logger.debug(f"success find {template}")
        return result

    def findAndOperate(self, template: Template, operate, operateParams: Optional[dict] = None, isColor: bool = False,
                       colorThreshold: int = 4):
        """find template on the device's screen ,operate the device

        Args:
            template (Template): 模板
            operate (function): 操作方法
            operateParams: 操作方法参数 默认{”result“ : result} 当然你可以设置自定义result

        Returns:
            result: 是否找到模板 会传递给operate函数
        """
        result = self.find(template, isColor, colorThreshold)
        if result:
            operateParams = operateParams or {}
            operateParams.setdefault("result", result)
            operate(**operateParams)
        return result

    def rangeRandomClick(self, result: tuple | list, duration=None,
                         randomPointGenerateAlgo=RandomPointGenerate.normalDistribution):
        if len(result) == 2:
            x, y = result
        elif len(result) == 4:
            x, y = randomPointGenerateAlgo(result)
        else:
            raise ValueError(f"{result} is No Correct Value")
        if duration is None:
            randomI = round(np.random.normal(0, 30))
            duration = random.randint(200, 350) if randomI > 80 else random.randint(80, 120)
        self.click(x, y, duration)

    def curveSwipe(self, startX, startY, endX, endY, duration, curveGenerateAlgo=CurveGenerate.BezierCurve):
        points = curveGenerateAlgo(startX, startY, endX, endY, duration)
        self.swipe(points, duration)

    def findAndClick(self, template: Template, result: tuple | list = None, duration=None, randomPointGenerateAlgo=None,
                     isColor: bool = False, colorThreshold: int = 4):
        clickParams = {}
        if result:
            clickParams["result"] = result
        if randomPointGenerateAlgo:
            clickParams["randomPointGenerateAlgo"] = randomPointGenerateAlgo
        if duration:
            clickParams["duration"] = duration
        return self.findAndOperate(template, self.rangeRandomClick, clickParams, isColor=isColor,
                                   colorThreshold=colorThreshold)
