import requests
import threading

URL = "https://lab2container.thankfultree-9626cb78.francecentral.azurecontainerapps.io/employees"

def send_requests():
    for _ in range(150):
        try:
            requests.get(URL, timeout=3)
        except:
            pass

threads = []
for _ in range(100):  
    t = threading.Thread(target=send_requests)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Finished sending requests")
