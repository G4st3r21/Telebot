from aiogram.utils.helper import Helper, HelperMode, ListItem


class RewriteStates(Helper):
    mode = HelperMode.snake_case

    STATE_NEWCLASS = ListItem()
    STATE_IM_TEXT1 = ListItem()
    STATE_IM_TEXT2 = ListItem()
    STATE_GET_TEXT = ListItem()
    STATE_DELETE = ListItem()
    STATE_SET_TIMER1 = ListItem()
    STATE_SET_TIMER2 = ListItem()
