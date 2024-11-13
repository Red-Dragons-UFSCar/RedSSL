import numpy as np
from communication.proto.ssl_gc_referee_message_pb2 import Referee
from entities.Obstacle import Obstacle

import behavior.skills as skills

class TechChallenge():
    def __init__(self):
        self.state_kick_off = False
        self.state_penalty_kick = False
        self.state_free_kick_ofense = False
        self.state_free_kick_defense = False
        self.state_stop = True

    def machine_state_update(self, flag_referee):

        if not flag_referee:
            return

        if flag_referee == Referee.Command.PREPARE_KICKOFF_YELLOW:
            self.state_kick_off = True

            self.state_penalty_kick = False
            self.state_free_kick_ofense = False
            self.state_free_kick_defense = False
            self.state_stop = False
        elif flag_referee == Referee.Command.PREPARE_PENALTY_YELLOW:
            self.state_penalty_kick = True

            self.state_kick_off = False
            self.state_free_kick_ofense = False
            self.state_free_kick_defense = False
            self.state_stop = False
        elif flag_referee == Referee.Command.DIRECT_FREE_YELLOW:
            self.state_free_kick_ofense = True

            self.state_kick_off = False
            self.state_penalty_kick = False
            self.state_free_kick_defense = False
            self.state_stop = False
        elif flag_referee == Referee.Command.DIRECT_FREE_BLUE:
            self.state_free_kick_defense= True

            self.state_kick_off = False
            self.state_penalty_kick = False
            self.state_free_kick_ofense  = False
            self.state_stop = False
        elif flag_referee == Referee.Command.STOP:
            self.state_stop= True

            self.state_kick_off = False
            self.state_penalty_kick = False
            self.state_free_kick_ofense  = False
            self.state_free_kick_defense = False
        elif flag_referee == Referee.Command.NORMAL_START or flag_referee == Referee.Command.FORCE_START:
            pass
        else:
            self.state_stop= True

            self.state_kick_off = False
            self.state_penalty_kick = False
            self.state_free_kick_ofense  = False
            self.state_free_kick_defense = False
    
    def tech_control(self, robot0, robot1, robot2, field):
        if self.state_stop:
            print("Stop")
            robot0.vx = 0
            robot0.vy = 0
            robot0.w = 0

            robot1.vx = 0
            robot1.vy = 0
            robot1.w = 0

            robot2.vx = 0
            robot2.vy = 0
            robot2.w = 0
        elif self.state_kick_off:
            print("KICK OFF")
            self.set_robot_targets('kickoff')
            self.moving_behavior(robot0, robot1, robot2, field)
        elif self.state_penalty_kick:
            print("PENALTI KICK")
            self.set_robot_targets('penalti')
            self.moving_behavior(robot0, robot1, robot2, field)
        elif self.state_free_kick_ofense:
            print("FREE KICK OFENSIVO")
            self.set_robot_targets('free_offense')
            self.moving_behavior(robot0, robot1, robot2, field)
        elif self.state_free_kick_defense:
            print("FREE KICK DEFENSIVO")
            self.set_robot_targets('free_defense')
            self.moving_behavior(robot0, robot1, robot2, field)
        else:
            print("ué?")

    def set_robot_targets(self, foul):
        if foul=='kickoff':
            self.robot0_xTarget = 225+210
            self.robot0_yTarget = 150+0
            self.robot0_aTarget = np.pi

            self.robot1_xTarget = 225+25
            self.robot1_yTarget = 150+70
            self.robot1_aTarget = np.pi

            self.robot2_xTarget = 225+25
            self.robot2_yTarget = 150+0
            self.robot2_aTarget = np.pi
        elif foul=='penalti':
            self.robot0_xTarget = 225+31
            self.robot0_yTarget = 150-70
            self.robot0_aTarget = np.pi

            self.robot1_xTarget = 225+31
            self.robot1_yTarget = 150+70
            self.robot1_aTarget = np.pi

            self.robot2_xTarget = 225-25
            self.robot2_yTarget = 150+0
            self.robot2_aTarget = np.pi
        elif foul=='free_defense':
            self.robot0_xTarget = 225+210
            self.robot0_yTarget = 150+30
            self.robot0_aTarget = np.pi/2

            self.robot1_xTarget = 225+185
            self.robot1_yTarget = 150+90
            self.robot1_aTarget = np.pi/2

            self.robot2_xTarget = 225+165
            self.robot2_yTarget = 150+90
            self.robot2_aTarget = np.pi/2
        elif foul=='free_offense':
            self.robot0_xTarget = 225+15
            self.robot0_yTarget = 150+70
            self.robot0_aTarget = np.pi

            self.robot1_xTarget = 225-59
            self.robot1_yTarget = 150-60
            self.robot1_aTarget = np.pi/2

            self.robot2_xTarget = 225-185
            self.robot2_yTarget = 150+142
            self.robot2_aTarget = -np.pi/2
        else:
            # Caso default
            self.robot0_xTarget = 225
            self.robot0_yTarget = 150
            self.robot0_aTarget = np.pi

            self.robot1_xTarget = 275
            self.robot1_yTarget = 150
            self.robot1_aTarget = np.pi

            self.robot2_xTarget = 325
            self.robot2_yTarget = 150
            self.robot2_aTarget = np.pi

    def moving_behavior(self, robot0, robot1, robot2, field):

        for robot_field in field.enemy_robots:
            obst = Obstacle()
            obst.set_obst(robot_field.get_coordinates().X, 
                        robot_field.get_coordinates().Y, 
                        robot_field.get_coordinates().rotation)
            robot0.map_obstacle.add_obstacle(obst)
            robot1.map_obstacle.add_obstacle(obst)
            robot2.map_obstacle.add_obstacle(obst)
        
        ball = field.ball
        obst = Obstacle()  # Configura a bola como obstáculo
        obst.set_obst(
            ball.get_coordinates().X, ball.get_coordinates().Y, 0, radius=20
        )
        robot0.map_obstacle.add_obstacle(obst)
        robot1.map_obstacle.add_obstacle(obst)
        robot2.map_obstacle.add_obstacle(obst)
        
        # for robot_field in [robot0, robot1]:
        #     obst = Obstacle()
        #     obst.set_obst(robot_field.get_coordinates().X, 
        #                 robot_field.get_coordinates().Y, 
        #                 robot_field.get_coordinates().rotation)
        #     robot2.map_obstacle.add_obstacle(obst)
        
        # for robot_field in [robot0, robot2]:
        #     obst = Obstacle()
        #     obst.set_obst(robot_field.get_coordinates().X, 
        #                 robot_field.get_coordinates().Y, 
        #                 robot_field.get_coordinates().rotation)
        #     robot1.map_obstacle.add_obstacle(obst)
        
        # for robot_field in [robot1, robot2]:
        #     obst = Obstacle()
        #     obst.set_obst(robot_field.get_coordinates().X, 
        #                 robot_field.get_coordinates().Y, 
        #                 robot_field.get_coordinates().rotation)
        #     robot0.map_obstacle.add_obstacle(obst)

        skills.go_to_point(robot0, self.robot0_xTarget, self.robot0_yTarget, field, self.robot0_aTarget)
        skills.go_to_point(robot1, self.robot1_xTarget, self.robot1_yTarget, field, self.robot1_aTarget)
        skills.go_to_point(robot2, self.robot2_xTarget, self.robot2_yTarget, field, self.robot2_aTarget)

        if robot0.target_reached(treshold=30):
            #skills.go_to_point(robot0, robot0_xTarget, robot0_yTarget, field, robot0_aTarget)
            robot0.vx = 0
            robot0.vy = 0
        else:
            robot0.w = 0

        if robot1.target_reached(treshold=30):
            #skills.go_to_point(robot0, robot0_xTarget, robot0_yTarget, field, robot0_aTarget)
            robot1.vx = 0
            robot1.vy = 0
        else:
            robot1.w = 0

        if robot2.target_reached(treshold=30):
            #skills.go_to_point(robot0, robot0_xTarget, robot0_yTarget, field, robot0_aTarget)
            robot2.vx = 0
            robot2.vy = 0
        else:
            robot2.w = 0



    

