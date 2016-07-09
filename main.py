try:
    import tkinter
except ImportError:
    import Tkinter as tkinter
try:
    import win32api
    import time
except ImportError as e:
    print("Failed import! Check for any dependency errors!")
    print("Error: <{0}>".format(e))
    input("Press any key to exit...")
    exit()


class MainWindow:
    def __init__(self):
        # objects within the main window
        self.timer = CustomTimer()

        # window creation
        self.window = tkinter.Tk()
        self.window.title("WAZZAP")
        # self.window.geometry("320x240")

        # object population
        self.timeLabel = tkinter.Label(self.window, text="")
        self.lbl = tkinter.Label(self.window, text="Hi there!")
        self.timerMiscLabel = tkinter.Label(self.window, text="Timer:")
        self.timerLabel = tkinter.Label(self.window, text="Not set")

        # self.splitPanedWindow = tkinter.PanedWindow(orient="VERTICAL")
        self.hourField = tkinter.Entry(self.window)
        self.minuteField = tkinter.Entry(self.window)

        self.loginButton = tkinter.Button(self.window, text="Print!", command=self.loginButton_clicked)
        # self.consoleText = tkinter.Text(self.window)

        # window population/packing
        self.timeLabel.pack()
        self.lbl.pack()
        self.timerMiscLabel.pack()
        self.timerLabel.pack()
        # self.consoleText.pack()
        self.loginButton.pack(side=tkinter.BOTTOM)
        self.hourField.pack(side=tkinter.LEFT)
        self.minuteField.pack(side=tkinter.RIGHT)


        self.tick()
        self.window.mainloop()

    # event handlers
    def loginButton_clicked(self):
        try:
            self.set_timer()
        except AssertionError:
            print("Invalid input... Retry again")

        print(str(self.hourField.get()) + ":" + str(self.minuteField.get()))

    # main tick of the program
    def tick(self):
        self.window.after(1000, self.tick)
        self.update_gui()
        self.timer.tick()

    # auxiliary methods
    def update_gui(self):
        now = time.strftime("%H:%M:%S")
        self.timeLabel.configure(text=now)
        if self.timer.is_active():
            self.timerLabel.configure(text=(str(self.timer.get_target_hour()) + ":" +
                                            str(self.timer.get_target_minute())))
        else:
            self.timerLabel.configure(text="Not set")

    def set_timer(self):
        try:
            self.timer.set_timer(self.hourField.get(), self.minuteField.get())
        except AssertionError as e:
            print("Error: <{0}>".format(e))
        self.hourField.configure(text="")
        self.minuteField.configure(text="")


class WindowMessage:
    def __init__(self, message):
        self.window = tkinter.Tk()
        self.messageLabel = tkinter.Label(self.window, text="Timer Set!")


class CustomTimer:
    def __init__(self):
        self.target_hour = None
        self.target_minute = None
        self.active = False

    # getters and setters
    def is_active(self):
        return self.active

    def get_target_hour(self):
        return self.target_hour

    def get_target_minute(self):
        return self.target_minute

    # timer core methods
    def set_timer(self, target_hour, target_minute):
        try:
            target_hour = int(target_hour)
            target_minute = int(target_minute)
        except ValueError:
            raise AssertionError("target_hour/target_minute is in incorrect format!")
        assert 0 <= target_hour <= 24, "target_hour not within range (0-24)!"
        assert 0 <= target_minute <= 60, "target_minute not within range(0-60)"
        self.target_hour = target_hour
        self.target_minute = target_minute
        self.active = True

    def timer_trigger(self):
        playpause()

    def tick(self):
        if self.is_active():
            self.check_timer()

    def check_timer(self):
        now = time.strftime("%H:%M")
        hour, minute = now.split(":")
        if int(hour) == self.target_hour and int(minute) == self.target_minute:
            self.timer_trigger()
            self.active = False


def playpause():
    VK_MEDIA_PLAY_PAUSE = 0xB3
    hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)


if __name__ == "__main__":
    window = MainWindow()
