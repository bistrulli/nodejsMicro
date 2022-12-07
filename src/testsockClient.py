from Client import clientProcess_sock
import time

if __name__ == '__main__':
    u=clientProcess_sock(500.0,1)
    u.start()
    time.sleep(30)
    u.terminate()
    u.join()
    print("exited")