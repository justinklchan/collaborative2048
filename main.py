import thread
import time

def main():
    try:
        m = thread.start_new_thread(killable_input, tuple())
        # s = raw_input("input:")
        while 1:
            time.sleep(0.1) 
    except KeyboardInterrupt:
        print "exception" 
    print "exit main"

def killable_input():
    w = thread.start_new_thread(normal_input, tuple())
    i = thread.start_new_thread(wait_sometime, tuple())


def normal_input():
    s = raw_input("input:")


def wait_sometime():
    time.sleep(4) # or any other condition to kill the thread
    print "too slow, killing imput"
    thread.interrupt_main()

main()