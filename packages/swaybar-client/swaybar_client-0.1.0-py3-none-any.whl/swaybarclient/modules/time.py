import datetime

import swaybarclient

class Module(swaybarclient.Module):
    def Init(self):
        self.color = '000000'

        self.background = '600060'
        self.border = '600060'

        self.border_left = 1
        self.border_right = 1

        self.separator = False
        self.sep_block_width = 0

    def Update(self):
        now = datetime.datetime.now()

        second = str(now.second).zfill(2)
        minute = str(now.minute).zfill(2)
        hour = str(now.hour).zfill(2)


        self.full_text = f'{hour}:{minute}:{second}'
