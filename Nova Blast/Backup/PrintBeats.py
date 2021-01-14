import threading
import time


class PrintBeats(threading.Thread):
    def __init__(self, beatsTime):
        threading.Thread.__init__(self)
        self.beatsTime = beatsTime

    def run(self):
        print("Print Start")
        playStartTime = time.time()
        nextBeatTime = self.beatsTime[0]
        index = 1
        while True:
            if (time.time() - playStartTime) >= nextBeatTime:
                print(index)
                nextBeatTime = self.beatsTime[index]
                index += 1
                if index >= self.beatsTime.shape[0]:
                    break
