class Constanst:
    PROT_PART1 = '0366148080'
    PROT_PART2 = '80000200000000000000000000'
    PROT_PART3 = '99'

class ENC_DECs:
    LET1TO3 = {'8': '0', '9': '1', 'a': '2', 'b': '3', 'c': '4', 'd': '5', 'e': '6', 'f': '7'}
    LET2TO4 = {'0': '2', '2': '0', 
               '8': 'a', 'a': '8',
               '9': 'b', 'b': '9', 
               'c': 'e', 'e': 'c', 
               'd': 'f', 'f':'d'}

class IPs:
    DRONE_IP    = "192.168.1.1"
    DRONE_PORTS = {'control': 7099, 'rtsp': 7070}
    RTSP_URL    = f"rtsp://{DRONE_IP}:{DRONE_PORTS['rtsp']}/webcam/"