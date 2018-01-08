import urllib

import requests, decimal, random, time, string
from time import gmtime, strftime
from geopy.geocoders import Nominatim
import certifi


def uo(args, **kwargs):
    return urllib.request.urlopen(args, cafile=certifi.where(), **kwargs)


class Rapido():

    def __init__(self):
        self.carrier_list = ['!DEA-H', 'Vodafone IN', 'Airtel', 'RELIANCE', 'JIO', 'TATA-DOCOMO', 'AIRCEL']
        self.mobile_manufacturer = ['motorola', 'OnePlus', 'Celkon', 'iball', 'Samsung', 'Nokia', 'Apple', 'Micromax',
                                    'Sony']
        self.manu_models = {
            'motorola': ['Moto X4', 'Moto G5S', 'Moto G5S Plus', 'Moto E4', 'Moto G4', 'Moto X Play', 'Moto X',
                         'XT1068'],
            'OnePlus': ['ONEPLUS A5000', 'ONEPLUS A3000', 'ONEPLUS A3003', 'ONEPLUS A5010'],
            'Celkon': ['Star 4G', 'CliQ', 'AG402', 'A400', 'CT695', 'A15K'],
            'iball': ['Andi5H', 'Andi4.5D', 'Andi5Li', 'Andi4A'],
            'Samsung': ['SM-T280', 'SM-T285', 'SM-A9100', 'SM-A910F', 'SM-J105B', 'J105DS', ' SM-J105F', 'GT-N7452',
                        'SM-C115'],
            'Nokia': ['3310', '150D', 'N6', '230D', 'LUMIA830', 'XL4G'],
            'Apple': ['A1865', 'A1901', 'A1902', 'A1863', 'A1905', 'A1906', 'A1864', 'A1897', 'A1898', 'A1898', 'A1778',
                      'A1661', 'A1633', 'A1634', 'A1549', 'A1522', 'A1662', 'A1453', 'A1507', 'A1428', 'A1431', 'A1349',
                      'A1325', 'A1324', 'A1203'],
            'Micromax': ['YU5010', 'YU5000', 'CANV201', 'Q326', 'Q332'],
            'Sony': ['C6603', 'C5303', 'C5306', 'C5302', 'C6503', 'C6506', 'C6502', 'C6602']}
        self.latitude = str(float(decimal.Decimal(random.randrange(15654785, 38947589)) / 1000000))
        self.longitude = str(float(decimal.Decimal(random.randrange(70452145, 78956585)) / 1000000))
        self.current_datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.firebase = "c9k64oCIoN4:APA91bHGZyiO-pSipx_5f22f365WSe87KuJTABTcEJXWxfr3U8qjMo4UOOdIS3ma9TUh_nyoKIjvsb6ReojPMdSmJwabiiGMqLA0dZ0AsBZKb29gSyAmRoxKARZAzN8g0Q5LGaFDfKU3"
        self.host = 'auth.rapido.bike'

    def generate_deviceid(self, N):
        return ''.join(random.choice(string.digits) for _ in range(N))

    def generate_email(self):
        firstname = ['shubham', 'shubhash', 'sumanyu', 'vikas', 'soubhik', 'rohit', 'bishal', 'avinash', 'saumitra',
                     'krishna', 'sahil', 'sushil', 'robin']
        lastname = ['gupta', 'hardaha', 'soniwal', 'handa', 'saha', 'sood', 'roy', 'topani', 'rawat', 'malhotra',
                    'maggu', 'sharma', 'paruthi']
        domain = ['@gmail.com', '@yahoo.com', '@rediffmail.com', '@hotmail.com', '@yahoo.co.in']
        random_num = self.generate_deviceid(5)
        return firstname[random.randrange(0, len(firstname))] + lastname[
            random.randrange(0, len(lastname))] + random_num + domain[random.randrange(0, len(domain))]

    def create_user(self, mobile):
        device_id = self.generate_deviceid(15)
        url = "https://auth.rapido.bike/auth/local/customer"
        internet = str(random.randrange(0, 15))
        carrier = self.carrier_list[random.randrange(0, len(self.carrier_list))]
        manufacturer = self.mobile_manufacturer[random.randrange(0, len(self.mobile_manufacturer))]
        model = self.manu_models[manufacturer][random.randrange(0, len(self.manu_models[manufacturer]))]
        current_timestamp = int(round(time.time() * 1000))

        payload = "{\"mobile\":\"" + mobile + "\",\"deviceDetails\":{\"deviceId\":\"" + device_id + "\",\"appId\":\"2\",\"internet\":\"" + internet + "\",\"carrier\":\"" + carrier + "\",\"manufacturer\":\"" + manufacturer + "\",\"model\":\"" + model + "\",\"firebaseToken\":\"cQ8bTYANjVE:APA91bGQ5LcZsHxANpKRAFTkXiz1Xn0btXb479CttCKAPNZTUrzCbqkWZoNK2S_shEg6UUio3J2r3bNa4v552mSsC14NLz3e3gxIvTxI7RLy-z8b0fnyVrwpcGS1qghngEoEAsU4BbSf\",\"timeStamp\":" + str(
            current_timestamp) + "},\"smsHashCode\":\"Vku3h7qjnN2\"}"
        headers = {
            'deviceid': device_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'appid': "2",
            'currentdatetime': self.current_datetime,
            'internet': internet,
            'appversion': "72",
            'content-type': "application/json; charset=UTF-8",
            'content-length': "384",
            'host': self.host,
            'connection': "Keep-Alive",
            'accept-encoding': "gzip",
            'user-agent': "okhttp/3.6.0",
            'cache-control': "no-cache"
        }

        response = requests.post(url, data=payload, headers=headers).json()
        message = response['info']["message"]

        print(message)
        cust_id = response['profile']['_id']
        otp = str(input('Enter OTP: '))
        self.verify_otp(otp, device_id, internet, carrier, manufacturer, model, cust_id)

    def verify_otp(self, otp, device_id, internet, carrier, manufacturer, model, cust_id):

        url = "https://auth.rapido.bike/api/users/" + cust_id + "/verifyOtp"
        current_timestamp = int(round(time.time() * 1000))
        payload = "{\"otp\":\"" + otp + "\",\"deviceDetails\":{\"deviceId\":\"" + device_id + "\",\"appId\":\"2\",\"internet\":\"" + internet + "\",\"carrier\":\"" + carrier + "\",\"manufacturer\":\"" + manufacturer + "\",\"model\":\"" + model + "\",\"firebaseToken\":\"cQ8bTYANjVE:APA91bGQ5LcZsHxANpKRAFTkXiz1Xn0btXb479CttCKAPNZTUrzCbqkWZoNK2S_shEg6UUio3J2r3bNa4v552mSsC14NLz3e3gxIvTxI7RLy-z8b0fnyVrwpcGS1qghngEoEAsU4BbSf\",\"timeStamp\":" + str(
            current_timestamp) + "}}"
        headers = {
            'deviceid': device_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'appid': "2",
            'currentdatetime': self.current_datetime,
            'internet': internet,
            'appversion': "72",
            'content-type': "application/json; charset=UTF-8",
            'content-length': "349",
            'host': "auth.rapido.bike",
            'connection': "Keep-Alive",
            'accept-encoding': "gzip",
            'user-agent': "okhttp/3.6.0",
            'cache-control': "no-cache"
        }

        response = requests.put(url, data=payload, headers=headers).json()

        message = response['info']['message']
        print(message)
        # room_id = response['roomId']
        token = response['token']
        self.update_user(device_id, token)
        self.fare_estimate(cust_id, device_id, token)

    def update_user(self, device_id, token):

        url = "https://auth.rapido.bike/api/users/update"
        email = self.generate_email()

        payload = "{\"firstName\":\"Shubham\",\"lastName\":\"Oug\",\"gender\":0,\"email\":\"" + email + "\",\"dateOfBirth\":\"6/1/1986\",\"referralCode\":\"SHUB3HU\"}"
        headers = {
            'deviceid': device_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'appid': "2",
            'currentdatetime': self.current_datetime,
            'internet': "0",
            'appversion': "73",
            'Authorization': "Bearer " + token,
            'Content-Type': "application/json; charset=UTF-8",
            'Content-Length': "131",
            'Host': self.host,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'User-Agent': "okhttp/3.6.0",
            'Cache-Control': "no-cache"
        }

        response = requests.put(url, data=payload, headers=headers)

        print(response.text)

    def fare_estimate(self, cust_id, device_id, token):
        url = "https://auth.rapido.bike/om/api/orders/v2/rideAmount"
        geolocator = Nominatim()
        geolocator.urlopen = uo
        print('Fare Estimate - ')
        pickup_location = ''
        drop_location = ''
        drop = ''
        try:
            while 1:
                pickup = str(input('Enter Pickup: '))
                drop = str(input('Enter Drop: '))
                pickup_location = geolocator.geocode(pickup)
                drop_location = geolocator.geocode(drop)
                #print(pickup_location)
                print(drop_location)
                break
        except:
            print('Exception - ')
            raise
        payload = "{\"pickupLocation\":{\"addressType\":\"\",\"address\":\"" + pickup_location.address.split(',')[
            0] + "\",\"lat\":" + str(pickup_location.latitude) + ",\"lng\":" + str(
            pickup_location.longitude) + ",\"name\":\"\"},\"dropLocation\":{\"addressType\":\"\",\"address\":\"" + \
                  drop_location.address.split(',')[0] + "\",\"lat\":" + str(drop_location.latitude) + ",\"lng\":" + str(
            drop_location.longitude) + ",\"name\":\"" + drop + "\"},\"serviceType\":\"57370b61a6855d70057417d1\",\"customer\":\"" + cust_id + "\",\"couponCode\":\"\",\"paymentType\":\"paytm\"}"
        headers = {
            'deviceid': device_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'appid': "2",
            'currentdatetime': self.current_datetime,
            'internet': "0",
            'appversion': "73",
            'Authorization': "Bearer " + token,
            'Content-Type': "application/json; charset=UTF-8",
            'Content-Length': "501",
            'Host': self.host,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'User-Agent': "okhttp/3.6.0",
            'Cache-Control': "no-cache"
        }

        response = requests.post(url, data=payload, headers=headers).json()
        print(response['info']['message'])
        request_id = response['data']['requestId']
        time_in_min = response['data']['timeInMts']
        quotes = response['data']['quotes']
        service_id = []
        amount_lst = []
        print('Rider is in ' + str(time_in_min) + ' mins.')
        for value in quotes:
            service_idd = value['serviceId']
            service_id.append(service_idd)
            amount = value['amount']
            amount_lst.append(amount)
            print('Service ID : ' + service_idd)
            print('Fare estimated - ' + str(amount))

        print('service id index - 0 or 1 n so on')
        print(service_id)
        print(amount_lst)
        service_user_selection = int(input('Select Service : '))
        final_service_id = service_id[service_user_selection]

        print(response)
        while 1:
            resp = self.book_ride(device_id, token, final_service_id, pickup_location, drop_location, cust_id,
                                  request_id)
            print(resp)
            if resp['info']['status'] == 'success':
                print(resp)
                callback_url = resp['callback_url']
                order_id = resp['data']['_id']
                self.get_details(callback_url, device_id, token)

                yes_or_no = input('Do you want to cancel ride? 1 - Yes | 0 - No ')
                if yes_or_no == 1:
                    self.cancel_booking(order_id, cust_id, token, device_id, pickup_location)
                break

    def book_ride(self, device_id, token, service_id, pickup_location, drop_location, cust_id, request_id):

        url = "https://auth.rapido.bike/rapido/rapido/book"

        payload = "{\"type\":\"booking\",\"userType\":\"customer\",\"serviceType\":\"" + service_id + "\",\"deviceId\":\"" + device_id + "\",\"paymentType\":\"paytm\",\"couponCode\":\"\",\"dropLocation\":{\"lat\":" + str(
            drop_location.latitude) + ",\"lng\":" + str(drop_location.longitude) + ",\"address\":\"" + \
                  drop_location.address.split(',')[0] + "\"},\"pickupLocation\":{\"lat\":" + str(
            pickup_location.latitude) + ",\"lng\":" + str(pickup_location.longitude) + ",\"address\":\"" + \
                  pickup_location.address.split(',')[0] + "\"},\"currentLocation\":{\"lat\":" + str(
            pickup_location.latitude) + ",\"lng\":" + str(
            pickup_location.latitude) + ",\"address\":\"\"},\"userId\":\"" + cust_id + "\",\"requestId\":\"" + request_id + "\"}"
        headers = {
            'deviceid': device_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'appid': "2",
            'currentdatetime': self.current_datetime,
            'internet': "0",
            'appversion': "73",
            'Authorization': "Bearer " + token,
            'Content-Type': "application/json; charset=UTF-8",
            'Content-Length': "615",
            'Host': self.host,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'User-Agent': "okhttp/3.6.0",
            'Cache-Control': "no-cache"
        }

        response = requests.post(url, data=payload, headers=headers).json()

        return response

    def get_details(self, callback_url, device_id, token):

        url = "https://auth.rapido.bike/rapido/rapido" + callback_url

        headers = {
            'deviceid': device_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'appid': "2",
            'currentdatetime': self.current_datetime,
            'internet': "0",
            'appversion': "73",
            'Authorization': "Bearer " + token,
            'Host': self.host,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'User-Agent': "okhttp/3.6.0"
        }

        response = requests.get(url, headers=headers).json()
        driver_number = response['data']['riderObj']['mobile']
        driver_name = response['data']['riderObj']['name']
        avg_rating = response['data']['riderObj']['avgRating']
        driver_email = response['data']['riderObj']['email']
        bike_number = response['data']['rider']['bikeNumber']
        profile_pic = response['data']['rider']['profilePic']
        bike_model = response['data']['rider']['bikeModel']

        print('Driver Shakal: '+profile_pic)
        print('Driver Name: '+driver_name)
        print('Driver Number: '+driver_number)
        print('Driver Rating: '+str(avg_rating))
        print('Driver Email: '+driver_email)
        print('Bike Number: '+bike_number)
        print('Bike Model: '+bike_model)

        print(response)

    def cancel_booking(self, order_id, cust_id, token, device_id, pickup_location):

        url = "https://auth.rapido.bike/rapido/rapido/cancel"

        payload = "{\"type\":\"cancelled\",\"orderId\":\""+order_id+"\",\"cancelReason\":\"I expected a shorter wait time\",\"locationDetails\":{\"lat\":"+str(pickup_location.latitude)+",\"lng\":"+str(pickup_location.longitude)+"},\"otherReason\":\"\",\"userId\":\""+cust_id+"\"}"
        headers = {
            'deviceid': device_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'appid': "2",
            'currentdatetime': self.current_datetime,
            'internet': "0",
            'appversion': "73",
            'Authorization': "Bearer " + token,
            'Content-Type': "application/json; charset=UTF-8",
            'Content-Length': "615",
            'Host': self.host,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'User-Agent': "okhttp/3.6.0",
            'Cache-Control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)


obj = Rapido()
mobile_num = str(input('Enter Mobile Number: '))
obj.create_user(mobile_num)
