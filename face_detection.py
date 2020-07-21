# Face Detection
import time, network , sensor, time, image
from mqtt import MQTTClient

NUM_SUBJECTS = 2
NUM_SUBJECTS_IMGS = 30

def find_person(img):
    d0 = img.find_lbp((0, 0, img.width(), img.height()))
    identical_pic = 0 #the pic that closet to the person from data
    end_range = 100000
    for s in range(1, NUM_SUBJECTS+1):
        dist = 0
        for i in range(1, NUM_SUBJECTS_IMGS):
            img = image.Image("persons/s%d/%d.pgm" %(s, i)).mask_ellipse()
            d1 = img.find_lbp((0, 0, img.width(), img.height()))
            dist += image.match_descriptor(d0, d1)
        distOfAll = dist/NUM_SUBJECTS_IMGS #distance of all images per person
        print("Average dist for subject %d: %d"%(s, distOfAll))
        if (distOfAll < end_range):
            identical_pic = s
            end_range = distOfAll
    if (end_range > 12000):
        identical_pic = -1  #-1 his undefined person
    return identical_pic


#connect to wifi
SSID='nati070' # Network SSID
KEY='nati0700'  # Network key

# Init wlan module and connect to network
print("Trying to connect... (may take a while)...")

wlan = network.WINC()
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)

# We should have a valid IP now via DHCP
print(wlan.ifconfig())

#open contact to the nodered/server
client = MQTTClient("openmv", "test.mosquitto.org", port=1883)
client.connect()

# Reset sensor
sensor.reset()
# Sensor settings
sensor.set_contrast(3)
sensor.set_gainceiling(16)

# HQVGA and GRAYSCALE are the best for face tracking.
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.B128X128) # or sensor.QQVGA (or others)
sensor.set_windowing((92,112))

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

# FPS clock
clock = time.clock()

#each index in the list represent the
#person id in the DB, we take the index
#that have must picture snapeshot that fit to the DB
#person id in the DB, we take the index
listCountPerson = [0] * NUM_SUBJECTS

#how many picture we compare before we send it to the server
NUM_OF_SAMPLES = 3

while (True):
    clock.tick()

    # Capture snapshot
    img = sensor.snapshot()

    # Find objects.
    # Note: Lower scale factor scales-down the image more and detects smaller objects.
    # Higher threshold results in a higher detection rate, with more false positives.
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

    # Draw objects
    for (x,y,h,l) in objects:
        img.draw_rectangle((x,y,h,l))
        imgName = find_person(img)
        listCountPerson[imgName - 1] = listCountPerson[imgName - 1]  + 1
        if (sum(listCountPerson) == NUM_OF_SAMPLES):
            person_result = max(listCountPerson)
            client.publish("openmv/test", str(person_result))
            print("person identy sent to the server")
            # time.sleep(1000)
            listCountPerson = [0] * NUM_SUBJECTS

        img.draw_string(x+1, y+1 ,"hello %s" % (imgName),(255,255,255),1)
        print("%s" % (imgName))


    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    #print(clock.fps())

