def average_pooling(sensor_list, window_size, stride):
    ret = []
    for i in range(len(sensor_list)-window_size+1):
        col_len = len(sensor_list[i])

        temp = [0] * col_len
        for j in range(col_len):
            for k in range(window_size):
                temp[j]+=sensor_list[i+k][j]

        temp = [i/3.0 for i in temp]
        ret.append(temp)

    return ret
