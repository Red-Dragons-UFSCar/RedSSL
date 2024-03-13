import socket
import struct
from .proto import ssl_simulation_robot_control_pb2 as pb2

class Actuator():
    def __init__(self, ip:str='localhost', port:int=10000,team_port:int=10302, logger:bool=False) -> None:
        #Newtork parameters
        self.ip = ip
        self.port = port
        self.team_port = team_port
        self.buffer_sice = 65536

        #Logger control
        self.logger = logger

        #Create socket
        self._create_socket()

    def _create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    def send_wheelVelocity_message(self, index, team_port, wheel_bl, wheel_br, wheel_fl, wheel_fr):
        self.robot_id = index
        self.team_port = team_port
        self.wheel_bl = wheel_bl
        self.wheel_br = wheel_br
        self.wheel_fl = wheel_fl
        self.wheel_fr = wheel_fr



        # Crie uma mensagem RobotControl
        robot_control = pb2.RobotControl()

        #Crie uma mensagem RobotCommand
        robot_command = robot_control.robot_commands.add()
        robot_command.id = self.robot_id

        #Crie uma mensagem MoveWheelVelocity
        move_command = pb2.MoveWheelVelocity()
        move_command.front_right = self.wheel_fr
        move_command.back_right = self.wheel_fl
        move_command.back_left = self.wheel_br
        move_command.front_left = self.wheel_bl

        # Atribua a mensagem MoveWheelVelocity ao campo move_command da mensagem RobotCommand
        robot_command.move_command.wheel_velocity.CopyFrom(move_command)


        try:
            self.socket.sendto(robot_control.SerializeToString(), (self.ip, self.team_port))
            if self.logger: print("[S&C] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[S&C] Falha ao enviar. Socket bloqueado")
            else:
                print("[S&C] Socket error:", e)


    def send_globalVelocity_message(self, index, team_port, velocity_x, velocity_y, ang):
        self.robot_id = index
        self.team_port = team_port
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.angular = ang
        

        # Crie uma mensagem RobotControl
        robot_control = pb2.RobotControl()

        #Crie uma mensagem RobotCommand
        robot_command = robot_control.robot_commands.add()
        robot_command.id = self.robot_id

        #Crie uma mensagem MoveGlobalVelocity
        move_command = pb2.MoveGlobalVelocity()
        move_command.x = self.velocity_x
        move_command.y = self.velocity_y
        move_command.angular = self.ang

        # Atribua a mensagem MoveGlobalVelocity ao campo move_command da mensagem RobotCommand
        robot_command.move_command.global_velocity.CopyFrom(move_command)


        try:
            self.socket.sendto(robot_control.SerializeToString(), (self.ip, self.team_port))
            if self.logger: print("[S&C] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[S&C] Falha ao enviar. Socket bloqueado")
            else:
                print("[S&C] Socket error:", e)

    def send_localVelocity_message(self, index, team_port, forward, left, ang):
        self.robot_id = index
        self.team_port = team_port
        self.forward = forward
        self.left = left
        self.angular = ang
        

        # Crie uma mensagem RobotControl
        robot_control = pb2.RobotControl()

        #Crie uma mensagem RobotCommand
        robot_command = robot_control.robot_commands.add()
        robot_command.id = self.robot_id

        #Crie uma mensagem MoveLocalVelocity
        move_command = pb2.MoveLocalVelocity()
        move_command.forward = self.forward
        move_command.left = self.left
        move_command.angular = self.angular

        # Atribua a mensagem MoveLocalVelocity ao campo move_command da mensagem RobotCommand
        robot_command.move_command.local_velocity.CopyFrom(move_command)


        try:
            self.socket.sendto(robot_control.SerializeToString(), (self.ip, self.team_port))
            if self.logger: print("[S&C] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[S&C] Falha ao enviar. Socket bloqueado")
            else:
                print("[S&C] Socket error:", e)
