import multiprocessing
from mirobot import *
from oak_d_lite import *

if __name__ == '__main__':
    queue = multiprocessing.Queue()

    mirobot_p = multiprocessing.Process(target=mirobot_control, args=(queue,))
    mirobot_p.start()

    oak_d_lite_p = multiprocessing.Process(target=oak_d_lite_control, args=(queue,))
    oak_d_lite_p.start()
    # queue.put(MyFancyClass('Fancy Dan'))

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    mirobot_p.join()
    oak_d_lite_p.join()
