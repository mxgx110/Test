from control import Controller

controller = Controller()
while True:
    action = input('Enter action ==> ')
    controller.control_exec(action)