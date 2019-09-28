from target import TargetType
from cv import UIMatcher
import uiautomator2 as u2

import time


class Automator:
    def __init__(self, device: str, targets: dict):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect(device)
        self.targets = targets

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        while True:
            # 判断是否出现货物。
            for target in TargetType:
                self._match_target(target)
                break

            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 当然，也可以使用图像探测的模式。
            self.d.click(550, 1650)

            # 滑动屏幕，收割金币。
            self._swipe()

    def _swipe(self):
        """
        滑动屏幕，收割金币。
        """
        for i in range(3):
            # 横向滑动，共 3 次。
            sx, sy = self._get_position(i * 3 + 1)
            ex, ey = self._get_position(i * 3 + 3)
            self.d.swipe(sx, sy, ex, ey)

    @staticmethod
    def _get_position(key):
        """
        获取指定建筑的屏幕位置。
        """
        positions = {
            1: (294, 1184),
            2: (551, 1061),
            3: (807, 961),
            4: (275, 935),
            5: (535, 810),
            6: (799, 687),
            7: (304, 681),
            8: (541, 568),
            9: (787, 407)
        }
        return positions.get(key)

    def _get_target_position(self, target: TargetType):
        """
        获取货物要移动到的屏幕位置。
        """
        return self._get_position(self.targets.get(target))

    def _match_target(self, target: TargetType):
        """
        探测货物，并搬运货物。
        """
        cargoPos = [[660, 1640],[0.771*1080, 0.815*1920],[0.895*1080, 0.77*1920]]
        for cargo in cargoPos:
            screen = self.d.screenshot(format="opencv")
            result = UIMatcher.match(screen)
            if result is None:
                return

                # 获取当前屏幕快照
                # 由于 OpenCV 的模板匹配有时会智障，故我们探测次数实现冗余。

                # 使用 OpenCV 探测货物。

                # 若无探测到，终止对该货物的探测。
                # 实现冗余的原因：返回的货物屏幕位置与实际位置存在偏差，导致移动失效

            for i in range(3):
                sx, sy = cargo
                for cnt in range(9):
                    ex, ey = self._get_position(cnt+1)
                    time.sleep(.3)
                    self.d.swipe(sx, sy, ex, ey)
                # sx, sy = result
                # 获取货物目的地的屏幕位置。
                # ex, ey = self._get_target_position(target)

                # 搬运货物。
                # self.d.swipe(sx, sy, ex, ey)
