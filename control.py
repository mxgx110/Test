import socket
import random
import cv2
import time
from config import Constanst, ENC_DECs, IPs

class Controller(Constanst, ENC_DECs, IPs):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def letters2commmand(self, lt1, lt2, lt3, lt4):
        command = self.PROT_PART1 + lt1 + lt2 + self.PROT_PART2 + lt3 + lt4 + self.PROT_PART3
        return command

    def start_motor_command(self):
        lt1, lt2 = 'f', 'c' #random.choice(list(self.LET1TO3.keys())[1:]), random.choice(list(self.LET2TO4.keys())[2:])
        lt3, lt4 = self.LET1TO3[lt1], self.LET2TO4[lt2]
        command = self.letters2commmand(lt1, lt2, lt3, lt4)
        return bytes.fromhex(command)
    
    def stop_motor_command(self):
        lt1, lt2 = '8', '0'
        lt3, lt4 = self.LET1TO3[lt1], self.LET2TO4[lt2]
        command = self.letters2commmand(lt1, lt2, lt3, lt4)
        return bytes.fromhex(command)
    
    def camera_view_change_command(self):
        command = [6, 0]
        return bytes(command)

    def control_exec(self, action):
        if action == 'start':
            command = self.start_motor_command()
            self.sock.sendto(command, (self.DRONE_IP, self.DRONE_PORTS['control']))
            print('Motor started!')
        
        elif action == 'stop':
            print('Stopping motor...')
            command = self.stop_motor_command()
            self.sock.sendto(command, (self.DRONE_IP, self.DRONE_PORTS['control']))
        
        elif action == 'takeoff':
            command = bytes.fromhex('036614808080800102000000000000000000000399') #takeoff/slow
            self.sock.sendto(command, (self.DRONE_IP, self.DRONE_PORTS['control']))
            command = bytes.fromhex('0366148080fc800002000000000000000000007e99') #start/mikkanne dg
            self.sock.sendto(command, (self.DRONE_IP, self.DRONE_PORTS['control']))
            print('Taking off...!')
        
        elif action == 'test':
            for _ in range(1):
                command = bytes.fromhex('036614808080800702000000000000000000000999') #soghut?
                self.sock.sendto(command, (self.DRONE_IP, self.DRONE_PORTS['control']))
            print('Testing...!')

        elif action == 'camera_change':
            print('Chaning camera view...')
            command = self.camera_view_change_command()
            self.sock.sendto(command, (self.DRONE_IP, self.DRONE_PORTS['control']))

        else: #takeoff - up - down - left - right - forward - backward - rotate
            raise NotImplementedError    

    def camera_broadcast(self):
        cap = cv2.VideoCapture(self.RTSP_URL)
        while True:
            try:
                ret, frame = cap.read()
                cv2.imshow("Drone Camera Stream", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except:
                self.camera_broadcast()
        cap.release()
        cv2.destroyAllWindows()

'''
036614808080800{0}02000000000000000000000{2}99 stop(urgent landing)
036614808080800{1}02000000000000000000000{3}99 takeoff
I should now check:
036614808080800{2}02000000000000000000000{4}99 ....
036614808080800{3}02000000000000000000000{5}99 ....
036614808080800{4}02000000000000000000000{6}99 'DOWN' {soghut}
036614808080800{5}02000000000000000000000{7}99 'UP' #care hamun takeoffe takio mikone
036614808080800{6}02000000000000000000000{8}99 ....
036614808080800{7}02000000000000000000000{9}99 ....
'''