import numpy as np
import cv2

# read img
org = cv2.imread('org.jpg')
embed = cv2.imread('embed.jpg')
# resize image(down sampling)
org_size = 640
embed_size = 480
org = cv2.resize(org, (org_size, org_size), interpolation=cv2.INTER_AREA)
embed = cv2.resize(embed, (embed_size, embed_size),
                   interpolation=cv2.INTER_AREA)
# turn color into gray
org_gray = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
embed_gray = cv2.cvtColor(embed, cv2.COLOR_BGR2GRAY)
# copy image
org_gray_3LSB = org_gray.copy()
org_gray_3LSB = org_gray_3LSB & 248  # (org pic & 11111000)
org_gray_2LSB = org_gray.copy()
org_gray_2LSB = org_gray_2LSB & 252  # (org pic & 11111100)
org_gray_1LSB = org_gray.copy()
org_gray_1LSB = org_gray_1LSB & 254  # (org pic & 11111110)
# embed the pic2 to pic1
for i in range(0, embed_size):
    for j in range(0, embed_size):
        org_gray_3LSB[i][j] = (org_gray_3LSB[i][j] | (
            (embed_gray[i][j] >> 5) & 7))  # 3bits MSB of embed pic to 3bits LSB of org pic
        org_gray_2LSB[i][j] = (org_gray_2LSB[i][j] | (
            (embed_gray[i][j] >> 6) & 3))  # 2bits MSB of embed pic to 2bits LSB of org pic
        org_gray_1LSB[i][j] = (org_gray_1LSB[i][j] | (
            (embed_gray[i][j] >> 7) & 1))  # MSB of embed pic to LSB of org pic
# save org img after embedded
for i in range(1, 4):
    cv2.imwrite(f'org_{i}LSB.jpg', locals()['org_gray_'+str(i)+'LSB'])
# pick the embed img out from org img
embed_gray_3MSB = (org_gray_3LSB & 7) << 5
embed_gray_2MSB = (org_gray_3LSB & 3) << 6
embed_gray_1MSB = (org_gray_3LSB & 1) << 7
# save embedded img from org img
for i in range(1, 4):
    cv2.imwrite(f'embed_{i}MSB.jpg', locals()['embed_gray_'+str(i)+'MSB'])
