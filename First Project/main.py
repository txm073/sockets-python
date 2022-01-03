import time
while True:
    try:
        import GUI
    except ConnectionAbortedError:
        time.sleep(1)
        continue
    break