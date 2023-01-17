# 用于获取处理手部关节信息的函数
def getHandPoint(info, hei, wid):
    # 创建列表，记录手部关节坐标信息
    handpointList = []
    # 获取21个手部关节坐标信息，包括x, y, z三个维度
    # x, y是归一化后的位置坐标；z是距离相机远近的高度坐标。（以手腕处的深度为原点，值越小，地标就越靠近相机。）
    handpointInfo = info.multi_hand_landmarks[0]
    # 对21个手部关节信息进行迭代操作，获取其相应坐标并记录在列表中
    for i in range(21):
        handpointList.append([int(handpointInfo.landmark[i].x * wid), int(handpointInfo.landmark[i].y * hei)])
    # 返回列表
    return handpointList

# 用于根据手部关节坐标判断手势
def judgeHandPose(handpoint_list):
    #判断三种特殊手势
    if (handpoint_list[8][1] < handpoint_list[7][1] < handpoint_list[6][1]) and (handpoint_list[10][1] < handpoint_list[11][1] < handpoint_list[12][1]) and (handpoint_list[14][1] < handpoint_list[15][1] < handpoint_list[16][1]) and (handpoint_list[18][1] < handpoint_list[19][1] < handpoint_list[20][1]):
        return 'Gesture1'
    elif (handpoint_list[12][1] < handpoint_list[11][1] < handpoint_list[10][1]) and (handpoint_list[8][1] < handpoint_list[7][1] < handpoint_list[6][1]) and (handpoint_list[14][1] < handpoint_list[15][1] < handpoint_list[16][1]) and (handpoint_list[18][1] < handpoint_list[19][1] < handpoint_list[20][1]):
        return 'Gesture2'
    else:
        return None
