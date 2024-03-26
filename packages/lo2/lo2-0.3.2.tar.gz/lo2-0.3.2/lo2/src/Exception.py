ANSI_RED = "\033[1;31m"
ANSI_YELLOW = "\033[0;33m"
ANSI_GREEN = "\033[0;32m"
ANSI_NORMAL = "\033[0m"


def __color_warp__(color, text):
    return f"{color}{text}{ANSI_NORMAL}"


class SyntaxError(Exception):
    def __init__(self, message=""):
        # 获取当前调用位置的文件名和行号
        try:
            raise Exception
        except Exception as e:
            frame = e.__traceback__.tb_frame.f_back

        file_name = frame.f_code.co_filename
        line_number = frame.f_lineno

        self.message = __color_warp__(ANSI_RED, f" {message}\n")
        self.message += "File: " + __color_warp__(
            ANSI_RED, f"{file_name}:{line_number}"
        )
        super().__init__(self.message)

    def __str__(self):
        print("-" * 20)
        return self.message


class RuntimeError(Exception):
    def __init__(self, message=""):
        # 获取当前调用位置的文件名和行号
        try:
            raise Exception
        except Exception as e:
            frame = e.__traceback__.tb_frame.f_back

        file_name = frame.f_code.co_filename
        line_number = frame.f_lineno

        self.message = __color_warp__(ANSI_RED, f" {message}\n")
        self.message += "File: " + __color_warp__(
            ANSI_RED, f"{file_name}:{line_number}"
        )
        super().__init__(self.message)

    def __str__(self):
        print("-" * 20)
        return self.message
