import swaybarclient

import psutil

class Module(swaybarclient.Module):
    def Init(self):
        self.color = '000000'

        self.background = '4040FF'
        self.border = '4040FF'

        self.border_left = 1
        self.border_right = 1

        self.separator = False
        self.sep_block_width = 0

    def Update(self):
        cpu_percent = str(round(psutil.cpu_percent()))

        self.full_text = f'cpu: {cpu_percent}%'
