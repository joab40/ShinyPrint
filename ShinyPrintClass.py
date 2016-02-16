#!/produkter/gnu/python/bin/python
# specfile='JCMJAVA.spec'

# import sys
# sys.path.append("/usr/lib64/python2.6/site-packages")
#import rpm
import os.path
import os
import curses
import time
import multiprocessing


class ShitMsg:
    def shit(self, msgs=None, msgstatus=None, msginput=None):
        # self.mypadsy, self.mypadsx = self.mypads.getyx()
        if msgstatus == "ok" and msgs == None:
            self.ok()
            self.mypadsy += 1
        elif msgstatus == "wait":
            if msginput != None:
                self.input(msginput)
            self.mypads.addstr(self.mypadsy, self.mypadsx, msgs, self.color_white)

        elif msgstatus == "ok" or msgs == "ok":
            if msgs != "ok":
                self.mypads.addstr(self.mypadsy, self.mypadsx, msgs, self.color_white)
            if msginput != None:
                self.input(msginput)
            self.ok()
            self.mypadsy += 1

        elif msgstatus == "failed" or msgs == "failed":
            if msgs != "failed":
                self.mypads.addstr(self.mypadsy, self.mypadsx, msgs, self.color_white)
            if msginput != None:
                self.input(msginput)
            self.failed()
            self.mypadsy += 1

        elif msgstatus == "warning" and msgs == None:
            self.warning()
            self.mypadsy += 1
        elif msgstatus == "warning":
            self.mypads.addstr(self.mypadsy, self.mypadsx, msgs, self.color_white)
            self.warning()
            self.mypadsy += 1

        else:
            if msgs == None:
                msgs = '\n'
            else:
                msgs += '\n'

            # print ("msgs: ",msgs)
            self.mypads.addstr(self.mypadsy, self.mypadsx, msgs, self.color_white)
            self.mypadsy += 1

    def input(self, msgin):
        self.mypads.addstr(self.mypadsy, 40, "(" + msgin + ")", self.color_white)

    def ok(self):
        # Print with correct position [OK] Colors green
        # self.mypadsy, self.mypadsx = self.mypads.getyx()
        self.mypads.addstr(self.mypadsy, 80, "[", self.color_white)
        self.mypads.addstr(self.mypadsy, 81, "OK", self.color_green)
        self.mypads.addstr(self.mypadsy, 83, "]", self.color_white)
        self.mypads.addstr(self.mypadsy, 84, "\n", self.color_white)

    def warning(self):
        # Print with correct position [OK] Colors green
        # self.mypadsy, self.mypadsx = self.mypads.getyx()
        self.mypads.addstr(self.mypadsy, 80, "[", self.color_white)
        self.mypads.addstr(self.mypadsy, 81, "WARNING", self.color_yellow)
        self.mypads.addstr(self.mypadsy, 88, "]", self.color_white)
        self.mypads.addstr(self.mypadsy, 89, "\n", self.color_white)

    def failed(self):
        # Print with correct position [OK] Colors green
        # self.mypadsy, self.mypadsx = self.mypads.getyx()
        self.mypads.addstr(self.mypadsy, 80, "[", self.color_white)
        self.mypads.addstr(self.mypadsy, 81, "FAILED", self.color_red)
        self.mypads.addstr(self.mypadsy, 87, "]", self.color_white)
        self.mypads.addstr(self.mypadsy, 88, "\n", self.color_white)

    def rotate(self, running):
        # self.mypadsy, self.mypadsx = self.mypads.getyx()
        self.mypads.addstr(self.mypadsy, 80, "[", self.color_white)
        self.mypads.addstr(self.mypadsy, 82, "]", self.color_white)
        while (running.is_set() == False):
            self.mypads.addstr(self.mypadsy, 81, "|", self.color_yellow)
            time.sleep(0.2)
            self.mypads.addstr(self.mypadsy, 81, "/", self.color_yellow)
            time.sleep(0.2)
            self.mypads.addstr(self.mypadsy, 81, "-", self.color_yellow)
            time.sleep(0.2)
            self.mypads.addstr(self.mypadsy, 81, "\\", self.color_yellow)
            # Try read event call = to exit
            running.wait(0.2)

    def exit(self):
        curses.curs_set(1)
        curses.endwin()

    def __init__(self, border=True, progress=False):
        # Startup
        self.screen = curses.initscr()
        self.height, self.width = self.screen.getmaxyx()
        if self.width < 90:
            Print("Terminal Width is to small: ", self.width, " Try larger then 90")
            exit()
            sys.exit(1)
        self.screen = curses.start_color()

        # COLORS
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.color_yellow = curses.color_pair(1)
        self.color_white = curses.color_pair(2)
        self.color_red = curses.color_pair(3)
        self.color_green = curses.color_pair(4)

        # Create window and subpad
        self.body = curses.newwin(self.height - progress, 0, 0, 0)
        self.body.immedok(True)
        if border is True:
            self.body.border(0)
        self.mypads = self.body.subpad(self.height - 2 - progress, self.width - 2 - progress, 1, 1)
        self.mypads.immedok(True)
        self.mypads.scrollok(1)
        self.mypads.idlok(1)
        self.mypadsy, self.mypadsx = self.mypads.getyx()
        if progress is True:
            self.progressprecent = 5
            self.safewidth = self.width - 6
            self.cursesprogresspresent = 0
            self.myprogress = curses.newwin(1, self.width, self.height - 1, 1)
            self.myprogress.immedok(True)

    def start(self, shitmsg, inputcall=None):
        self.shit(shitmsg, "wait", inputcall)
        self.num = multiprocessing.Event()
        self.P = multiprocessing.Process(target=self.rotate, args=(self.num,))
        self.P.start()

    def stop(self, shitdone="ok", inputerror=None):
        # Send stop to subproc
        self.num.set()
        self.P.join()
        self.shit("", shitdone, inputerror)

    def done(self):
        # Ending pause
        curses.curs_set(1)
        self.body.getch()
        self.exit()

    def progress(self, percent=100):
        self.pregressy, self.progressx = self.myprogress.getyx()
        self.cursesprogresspresent = percent * 0.01 * self.width
        while self.progressprecent < self.cursesprogresspresent:
            # self.procentcounter
            self.progressprecent += 1
            self.realprecent = round(float(self.progressprecent) / float(self.width) * 100.0)
            counter = "-(" + str(self.realprecent) + "%)--"
            self.myprogress.addstr(self.pregressy, 0, "[")
            self.myprogress.addstr(self.pregressy, self.width - 3, "]")
            self.myprogress.addstr(self.pregressy, 1, counter)
            self.myprogress.refresh()
            if self.progressprecent <= self.safewidth:
                self.myprogress.addstr(self.pregressy, self.progressprecent, "-->")
                self.myprogress.refresh()
                time.sleep(0.02)
        if percent == 100:
            self.myprogress.addstr(self.pregressy, 1, '-(Done! Press Enter to Exit)-')

# EXAMPLE
testar="SPECFILE_a01"
console = ShitMsg(border=True,progress=True)
# console.progress(5)
# console.start("Shit is starting","Kor med filen: " + testar)
console.start("Shit is starting")
# time.sleep(1)
console.stop("ok")
#console.stop("failed","Gick inte" + testar)
# console.progress(20)
# time.sleep(1)
console.start("subproctest")
console.stop("warning")
# console.progress(30)
console.shit("SkaBaraSkrivaOK","ok","variable" + testar)
# console.shit("KorTestMedWaitOK","wait")
# time.sleep(1)
# console.shit("ok")


# console.shit("testarFAILED")
# console.shit("failed")
# console.shit("FAILEDwaitFAILED","wait")
# time.sleep(1)
# console.shit("failed","failed","pga shit in")
# console.progress(50)
# console.progress(100)
# console.shit("Det har gar failed direkt","failed")
# console.shit("Det har gar ok direkt","ok","hurra")
# console.shit("Om java eller weblogic uppdaterats, .ndra p. wikin : http://mw.sfa.se:16080/wiki/index.php/Installations_best%C3%A4llningar_Middleware")
console.done()
