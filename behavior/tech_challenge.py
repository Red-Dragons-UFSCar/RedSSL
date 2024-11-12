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
            self.kickoff_behavior(robot0, robot1, robot2, field)
        elif self.state_penalty_kick:
            print("PENALTI KICK")
        elif self.state_free_kick_ofense:
            print("FREE KICK OFENSIVO")
        elif self.state_free_kick_defense:
            print("FREE KICK DEFENSIVO")
        else:
            print("ué?")

    def kickoff_behavior(self, robot0, robot1, robot2, field):
        robot0_xTarget = 225+210
        robot0_yTarget = 150+0
        robot0_aTarget = np.pi

        robot1_xTarget = 225+25
        robot1_yTarget = 150+70
        robot1_aTarget = np.pi

        robot2_xTarget = 225+25
        robot2_yTarget = 150+0
        robot2_aTarget = np.pi

        for robot_field in field.enemy_robots:
            obst = Obstacle()
            obst.set_obst(robot_field.get_coordinates().X, 
                        robot_field.get_coordinates().Y, 
                        robot_field.get_coordinates().rotation)
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

        skills.go_to_point(robot0, robot0_xTarget, robot0_yTarget, field, robot0_aTarget)
        skills.go_to_point(robot1, robot1_xTarget, robot1_yTarget, field, robot1_aTarget)
        skills.go_to_point(robot2, robot2_xTarget, robot2_yTarget, field, robot2_aTarget)

        if robot0.target_reached():
            #skills.go_to_point(robot0, robot0_xTarget, robot0_yTarget, field, robot0_aTarget)
            robot0.vx = 0
            robot0.vy = 0
        else:
            robot0.w = 0

        if robot1.target_reached():
            #skills.go_to_point(robot0, robot0_xTarget, robot0_yTarget, field, robot0_aTarget)
            robot1.vx = 0
            robot1.vy = 0
        else:
            robot1.w = 0

        if robot2.target_reached():
            #skills.go_to_point(robot0, robot0_xTarget, robot0_yTarget, field, robot0_aTarget)
            robot2.vx = 0
            robot2.vy = 0
        else:
            robot2.w = 0



    

