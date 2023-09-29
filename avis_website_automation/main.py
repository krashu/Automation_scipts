from create_booking import create_reservation
from booking_cancellation import cancel
from datetime import datetime
import time
import os


try:
    email = input("Email: ")
    email = email if len(email) else 'appdev682@gmail.com'
    domain = 'https://www.avis.co.uk/'  # input("Avis website Link: ").strip().upper()
    print()

    start = time.time()
    # Folder name and create
    today = datetime.now()
    folder = r'screenshots\\' + today.strftime("%Y-%m-%d %H-%M-%S")
    os.mkdir(folder)

    try:
        print('#' * 40)

        reservation_id = create_reservation(domain=domain, folder=folder, email=email)
        if reservation_id:
            status = cancel(domain, reservation_id, folder, email)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open(f'{folder}\\Reservation_logs.csv', 'a') as file:
                file.write(dt_string + ',' + domain + ',' + reservation_id + ',' + status + '\n')
        else:
            raise Exception("Error while creating reservation for ", domain)
    except Exception as e:
        print(e)
        print('~' * 50)
        # print()
        # print()
        # print(domain + ' not worked')
    finally:
        print('-' * 40)
        print()
    end = time.time() - start
    print(f'Script completed in {round(end, 2)} seconds')
    time.sleep(30)
except KeyboardInterrupt:
    print()
    print("Exiting Script.........")
