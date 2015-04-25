import os, sys
sys.path.append(os.path.join('../myo-python/'))

from Tkinter import *
import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_
import random

myo.init()

SHOW_OUTPUT_CHANCE = 0.01
r"""
There can be a lot of output from certain data like acceleration and orientation.
This parameter controls the percent of times that data is shown.
"""

class Listener(myo.DeviceListener):
    # return False from any method to stop the Hub

    def __init__(self, canvas, width, height):
        self.width = width
        self.height = height
        self.canvas = canvas
        self.colors = ["red","orange","yellow","green","cyan","blue","purple","black"]
        self.color = "black"
        self.r = 10
        self.fist = False
        self.timerDelay = 10

        self.position = [self.width/4, self.height/4]
        self.prevAcceleration = None
        self.prevOrientation = None
        self.accelAmountCap = 21

    def on_connect(self, myo, timestamp):
        print_("Connected to Myo")
        myo.vibrate('short')
        myo.request_rssi()

    def on_rssi(self, myo, timestamp, rssi):
        pass

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        r""" Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        print_('Paired')
        print_("If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")
        print_("Double tap enables EMG.")
        print_("Spreading fingers disables EMG.\n")

    def on_disconnect(self, myo, timestamp):
        print_('on_disconnect')

    def on_pose(self, myo, timestamp, pose):
        print_('on_pose', pose)
        if pose == pose_t.double_tap:
            print_("Enabling EMG")
            print_("Spreading fingers disables EMG.")
            print_("=" * 80)
            myo.set_stream_emg(stream_emg.enabled)
        elif pose == pose_t.fingers_spread:
            print_("=" * 80)
            print_("Disabling EMG")
            myo.set_stream_emg(stream_emg.disabled)
            self.fist = False
        elif pose == pose_t.fist:
            self.fist = True

    def on_orientation_data(self, myo, timestamp, orientation):
        self.position = [self.width/4, self.height/4]
        if self.prevOrientation:
            dx =  orientation[0] - self.prevOrientation[0]
            dy =  orientation[1] - self.prevOrientation[1]

            xscale = 5000
            yscale = 2000
            self.position[0] = self.position[0] + dx*xscale
            self.position[1] = self.position[1] + dy*yscale

        self.prevOrientation = orientation
        print self.position

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        #if self.prevAcceleration:
            #dx =  acceleration[0] - self.prevAcceleration[0]
            #dy =  acceleration[1] - self.prevOrientation[1]

            #xscale = 2
            #yscale = 2
            #self.position[0] = self.position[0] + dx*xscale
            #self.position[1] = self.position[1] + dy*yscale

        #self.prevAcceleration = acceleration
        pass


    #def on_gyroscope_data(self, myo, timestamp, gyroscope):
        #show_output('gyroscope', gyroscope)

    def on_unlock(self, myo, timestamp):
        print_('unlocked')

    def on_lock(self, myo, timestamp):
        print_('locked')

    def on_sync(self, myo, timestamp, arm, x_direction):
        print_('synced', arm, x_direction)

    def on_unsync(self, myo, timestamp):
        print_('unsynced')

    #def on_emg(self, myo, timestamp, emg):
        #show_output('emg', emg)

    def onTimerFired(self):
        if self.fist == True:
            self.canvas.create_oval(self.position[0], self.position[1], self.position[0] + self.r, self.position[1] + self.r, fill = self.color)

    def onTimerFiredWrapper(self):
        self.onTimerFired()
        self.canvas.after(self.timerDelay, self.onTimerFiredWrapper)

def show_output(message, data):
    if random.random() < SHOW_OUTPUT_CHANCE:
        print_(message + ':' + str(data))

def main():
    width = 1900
    height = 800

    timerDelay = 500
    root = Tk()
    root.resizable(True, True)
    backgroundColor = "white"
    drawing_area = Canvas(root, width=width, height=height, background=backgroundColor)
    drawing_area.pack()
    drawing_area.after(timerDelay, myo.time.sleep(.2))
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)
    listener = Listener(drawing_area, width, height)
    hub.run(1000, listener)
    def terminate():
        root.destroy()
        hub.stop()
    root.protocol('WM_DELETE_WINDOW', terminate)

    listener.onTimerFiredWrapper()

    root.mainloop()

if __name__ == '__main__':
    main()
