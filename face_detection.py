# Face Detection

def find_person(img):

    d0 = img.find_lbp((0, 0, img.width(), img.height()))
    #if(dist < 14000):
    NUM_SUBJECTS = 6
    NUM_SUBJECTS_IMGS = 10
    p = 0
    n = 100000
    for s in range(1, NUM_SUBJECTS+1):
        dist = 0
        for i in range(1, NUM_SUBJECTS_IMGS):
            img = image.Image("persons/s%d/%d.pgm" %(s, i)).mask_ellipse()
            d1 = img.find_lbp((0, 0, img.width(), img.height()))
            dist += image.match_descriptor(d0, d1)
        print("Average dist for subject %d: %d"%(s, dist/NUM_SUBJECTS_IMGS))
        if (dist < n):
            p = s
            n = dist
    return p

import sensor, time, image
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
        img.draw_string(x+1, y+1 ,"hello %s" % (imgName),(255,255,255),1)
        print("%s" % (imgName))


    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    #print(clock.fps())

