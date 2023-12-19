
#         if dptr_cnt % 100 == 0:
#             time_s = (time.ticks_ms()-start_ms)//1000
#             if disp_time_s != int(time_s)%100:
#                 disp_time_s = int(time_s)%100
#                 disp_num(disp_time_s)
#         elif   dptr_cnt % 10 == 5: 
#             sr04 = hcsr04_irq.Hcsr04Irq(trigger_pin = 2, echo_pin=4)
#             sr04.trig_start()
#             dist_cm = int(sr04.get_dist_mm())//10
#             
#             if dptr_cnt % 100 == 55:
#                 disp_num(int(dist_cm%99))
#             elif dptr_cnt % 100 == 75:
#                 disp_num(int(dist_cm%99))
#                 
#                 
#             if (dist_cm >= dist_high)and(dist_cm <= max_dist):
#                 if pre_dist_cm <= dist_low:
#                     pre_dist_cm = dist_cm
#                     edge_rise_cnt += 1
#             elif (dist_cm <= dist_low)and(dist_cm >= min_dist):
#                 if pre_dist_cm >= dist_high:
#                     pre_dist_cm = dist_cm
#                     edge_fall_cnt += 1
#             else:
#                 edge_rise_cnt = 0
#                 edge_fall_cnt = 0
#                     
#             if (edge_rise_cnt>=2) and (edge_fall_cnt >=2) and ((time.ticks_ms() - start_ms) >= 6000):
#                 demo_mode = 'Flow'
#                 edge_rise_cnt = 0
#                 edge_fall_cnt = 0
#             elif ((time.ticks_ms() - start_ms) >= 12000):
#                 edge_rise_cnt = 0
#                 edge_fall_cnt = 0
#                 demo_mode = 'Android_RC'
#                     
#         dptr_cnt +=1  


