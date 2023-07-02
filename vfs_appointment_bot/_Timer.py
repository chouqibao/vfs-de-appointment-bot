import time


def countdown(t):
    while t > -1:
        # timer = 'Retry after {:02d} seconds'.format(t)
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        timer = 'Retry after %02d:%02d:%02d' % (h, m, s)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
