from aiogram.utils.helper import Helper, HelperMode, ListItem


class AllStates(Helper):
    mode = HelperMode.snake_case

    MAILING_STATE = ListItem()
