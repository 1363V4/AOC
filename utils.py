import time

# Get your input


def read_data() -> list:
    '''
    Returns a list with all the lines from data.txt as separate string entries
    '''
    with open("input.txt", "r") as f:
        return [i.strip() for i in f.readlines()]

# Time your code


class Clock:
    '''
    Initiate Clock at the start of the code
    Call Clock.tic() at the beginning
    Call Clock.toc() at the end to get time since tic
    You can add a custom message to toc
    '''
    def tic(self) -> None:
        self.start_time = time.time()

    def toc(self, msg: str = "") -> None:
        end = time.time()
        time_since_tic = ((end - self.start_time)*1000) // 1
        output_string = f"{msg:.^20}" + f"Done in {time_since_tic}ms"
        print(output_string)
