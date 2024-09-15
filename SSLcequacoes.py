import SSLclass as crb
import numpy as np

ve = 3 #primeiro motor
vd = 3 #segundo motor
vee = 3 #terceiro motor
vdd = 3 #quarto motor

v_roda_1 =0.016*ve
v_roda_2 =0.016*vd
v_roda_3 = 0.016*vee
v_roda_4 = 0.016*vdd


pose_1 = np.array([0, 0, 0]) #(x,y, theta)-inicial
pose_2 = np.array([0.5, 0, 0]) #(x, y, theta)-final

deslocamento = pose_2 - pose_1

tempo = 3

delta_deslocamento = deslocamento / tempo #numericamente igual a velocidade (x_dot, y_dot, theta_dot)

theta= pose_2[2]
x_dot= delta_deslocamento[0]
y_dot= delta_deslocamento[1]


v = np.cos(theta) * x_dot + np.sin(theta)*y_dot

a=0.01

theta_dot = -(1/a) * np.sin(theta)*x_dot + (1/a)*np.sin(theta)*y_dot


roda_1 = v + (0.075/2) * theta_dot #roda 1
roda_2 = v - (0.075/2) * theta_dot #roda 2
roda_3 = v + (0.075/2) * theta_dot #roda 3
roda_4 = v - (0.075/2) * theta_dot #roda 4

vd= roda_1/(3.14 * 2 *0.016)
ve= roda_2/(3.14 * 2 *0.016)
vee= roda_3/(3.14 * 2 *0.016)
vdd= roda_4/(3.14 * 2 *0.016)
robot1 = crb.ssl()
robot1.Set_Velocities(ve, vd, vee, vdd)
robot1.Wait(tempo)
robot1.Stop_Robot()