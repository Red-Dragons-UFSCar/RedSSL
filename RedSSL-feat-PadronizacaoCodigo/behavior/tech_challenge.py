import numpy as np

from communication.proto.ssl_gc_referee_message_pb2 import Referee
from entities.Obstacle import Obstacle
import behavior.skills as skills


class TechChallenge:
    """
    Manages game states and robot targets based on referee commands
    for a robotics tech challenge.
    """

    def __init__(self):
        """
        Initializes the game states and counters.

        States default to 'STOP'. Counters and thresholds are for managing
        robot behavior, particularly stopping rotation.
        """
        self.state_kick_off = False
        self.state_penalty_kick = False
        self.state_free_kick_offense = False  # Corrected typo from ofense
        self.state_free_kick_defense = False
        self.state_stop = True

        # Thresholds and counters for attacker, defender, and goalkeeper
        # These seem to be related to how long a robot tries to align its angle
        # before its angular velocity (w) is set to 0.
        self.threshold_attacker_stop = 60
        self.counter_attacker_stop = 0 # Note: This counter is not used in the provided moving_behavior

        self.threshold_defender_stop = 60
        self.counter_defender_stop = 0

        self.threshold_goalkeeper_stop = 60 # Renamed from goalkeper for consistency
        self.counter_goalkeeper_stop = 0

        # Robot target positions and angles (will be set by set_robot_targets)
        self.robot0_x_target = 0
        self.robot0_y_target = 0
        self.robot0_a_target = 0
        self.robot1_x_target = 0
        self.robot1_y_target = 0
        self.robot1_a_target = 0
        self.robot2_x_target = 0
        self.robot2_y_target = 0
        self.robot2_a_target = 0

    def machine_state_update(self, flag_referee):
        """
        Updates the internal game state based on the referee command.

        Parâmetros:
        - flag_referee: The command received from the referee system.
        """
        if not flag_referee: # No command, no change
            return

        # Default all states to False before setting the active one
        self.state_kick_off = False
        self.state_penalty_kick = False
        self.state_free_kick_offense = False
        self.state_free_kick_defense = False
        self.state_stop = False

        if flag_referee == Referee.Command.PREPARE_KICKOFF_YELLOW:
            self.state_kick_off = True
        elif flag_referee == Referee.Command.PREPARE_PENALTY_YELLOW:
            self.state_penalty_kick = True
        elif flag_referee == Referee.Command.DIRECT_FREE_YELLOW:
            self.state_free_kick_offense = True
        elif flag_referee == Referee.Command.DIRECT_FREE_BLUE:
            self.state_free_kick_defense = True
        elif flag_referee == Referee.Command.STOP:
            self.state_stop = True
        elif (
            flag_referee == Referee.Command.NORMAL_START or
            flag_referee == Referee.Command.FORCE_START
        ):
            # For NORMAL_START or FORCE_START, typically the game continues from
            # the state it was in (e.g., kickoff becomes active play).
            # The current logic doesn't change states here but also doesn't default to STOP.
            # This might mean active play states are handled elsewhere or these flags
            # signal the end of a stopped/setup phase.
            pass # No explicit state change, previous active state (if any non-stop) might persist implicitly
        else: # Unknown or other commands default to STOP
            self.state_stop = True

    def tech_control(self, robot0, robot1, robot2, field):
        """
        Controls the robots based on the current game state.

        Parâmetros:
        - robot0: Instance of the first robot.
        - robot1: Instance of the second robot.
        - robot2: Instance of the third robot.
        - field: Instance of the field.
        """
        if self.state_stop:
            print("State: STOP")
            # Stop all robots
            for robot_instance in [robot0, robot1, robot2]:
                robot_instance.vx = 0
                robot_instance.vy = 0
                robot_instance.w = 0
        elif self.state_kick_off:
            print("State: KICK OFF")
            self.set_robot_targets('kickoff')
            self.moving_behavior(robot0, robot1, robot2, field)
        elif self.state_penalty_kick:
            print("State: PENALTY KICK")
            self.set_robot_targets('penalty')
            self.moving_behavior(robot0, robot1, robot2, field)
        elif self.state_free_kick_offense:
            print("State: FREE KICK OFFENSE")
            self.set_robot_targets('free_offense')
            self.moving_behavior(robot0, robot1, robot2, field)
        elif self.state_free_kick_defense:
            print("State: FREE KICK DEFENSE")
            self.set_robot_targets('free_defense')
            self.moving_behavior(robot0, robot1, robot2, field)
        else:
            # This case should ideally not be reached if machine_state_update
            # correctly sets a state (including state_stop for defaults).
            print("State: UNKNOWN / Not Handled (ué?)")
            # Default to stopping robots if in an undefined state
            for robot_instance in [robot0, robot1, robot2]:
                robot_instance.vx = 0
                robot_instance.vy = 0
                robot_instance.w = 0

    def set_robot_targets(self, foul_type: str):
        """
        Sets the target coordinates (x, y) and angle (a) for each robot
        based on the type of foul or game situation.

        Parâmetros:
        - foul_type: A string indicating the game situation (e.g., 'kickoff', 'penalty').
        """
        # Base coordinates (e.g., center of field or reference point)
        BASE_X = 225
        BASE_Y = 150

        if foul_type == 'kickoff':
            self.robot0_x_target = BASE_X + 210
            self.robot0_y_target = BASE_Y + 0
            self.robot0_a_target = np.pi

            self.robot1_x_target = BASE_X + 25
            self.robot1_y_target = BASE_Y + 70
            self.robot1_a_target = np.pi

            self.robot2_x_target = BASE_X + 25
            self.robot2_y_target = BASE_Y + 0
            self.robot2_a_target = np.pi
        elif foul_type == 'penalty':
            self.robot0_x_target = BASE_X + 31
            self.robot0_y_target = BASE_Y - 70
            self.robot0_a_target = np.pi

            self.robot1_x_target = BASE_X + 31
            self.robot1_y_target = BASE_Y + 70
            self.robot1_a_target = np.pi

            self.robot2_x_target = BASE_X - 25
            self.robot2_y_target = BASE_Y + 0
            self.robot2_a_target = np.pi
        elif foul_type == 'free_defense':
            self.robot0_x_target = BASE_X + 210
            self.robot0_y_target = BASE_Y + 30
            self.robot0_a_target = np.pi / 2

            self.robot1_x_target = BASE_X + 185
            self.robot1_y_target = BASE_Y + 90
            self.robot1_a_target = np.pi / 2

            self.robot2_x_target = BASE_X + 165
            self.robot2_y_target = BASE_Y + 90
            self.robot2_a_target = np.pi / 2
        elif foul_type == 'free_offense':
            self.robot0_x_target = BASE_X + 15
            self.robot0_y_target = BASE_Y + 70
            self.robot0_a_target = np.pi

            self.robot1_x_target = BASE_X - 59
            self.robot1_y_target = BASE_Y - 60
            self.robot1_a_target = np.pi / 2

            self.robot2_x_target = BASE_X - 185
            self.robot2_y_target = BASE_Y + 142
            self.robot2_a_target = -np.pi / 2
        else:  # Default case or unknown foul_type
            self.robot0_x_target = BASE_X
            self.robot0_y_target = BASE_Y
            self.robot0_a_target = np.pi

            self.robot1_x_target = BASE_X + 50 # Adjusted for some separation
            self.robot1_y_target = BASE_Y
            self.robot1_a_target = np.pi

            self.robot2_x_target = BASE_X + 100 # Adjusted for some separation
            self.robot2_y_target = BASE_Y
            self.robot2_a_target = np.pi

    def moving_behavior(self, robot0, robot1, robot2, field):
        """
        Manages the movement of robots to their targets, considering obstacles.

        Adds enemy robots and the ball as obstacles. Then, commands each robot
        to move to its predefined target. Also handles stopping logic based on
        target reached and orientation.

        Parâmetros:
        - robot0: Instance of the first robot.
        - robot1: Instance of the second robot.
        - robot2: Instance of the third robot.
        - field: Instance of the field.
        """
        # Add enemy robots as obstacles for all our robots
        for enemy_robot_field in field.enemy_robots:
            obst = Obstacle()
            enemy_coords = enemy_robot_field.get_coordinates()
            obst.set_obst(
                enemy_coords.X,
                enemy_coords.Y,
                enemy_coords.rotation
            )
            robot0.map_obstacle.add_obstacle(obst)
            robot1.map_obstacle.add_obstacle(obst)
            robot2.map_obstacle.add_obstacle(obst)
        
        # Add the ball as an obstacle
        ball = field.ball
        ball_obstacle = Obstacle()
        ball_coords = ball.get_coordinates()
        ball_obstacle.set_obst(
            ball_coords.X, ball_coords.Y, 0, radius=20
        )
        robot0.map_obstacle.add_obstacle(ball_obstacle)
        robot1.map_obstacle.add_obstacle(ball_obstacle)
        robot2.map_obstacle.add_obstacle(ball_obstacle)
        
        # Commented-out original code for inter-robot obstacles:
        # for robot_field in [robot0, robot1]:
        #     obst = Obstacle()
        #     obst.set_obst(robot_field.get_coordinates().X,
        #                   robot_field.get_coordinates().Y,
        #                   robot_field.get_coordinates().rotation)
        #     robot2.map_obstacle.add_obstacle(obst)
        # (Similar blocks for robot1 and robot0 were also present)

        # Command robots to go to their targets
        skills.go_to_point(
            robot0, self.robot0_x_target, self.robot0_y_target, field, self.robot0_a_target
        )
        skills.go_to_point(
            robot1, self.robot1_x_target, self.robot1_y_target, field, self.robot1_a_target
        )
        skills.go_to_point(
            robot2, self.robot2_x_target, self.robot2_y_target, field, self.robot2_a_target
        )

        # Logic for stopping robots once target is reached and oriented
        angle_tolerance_rad = 30 * np.pi / 180  # 30 degrees tolerance

        # Robot 0 (Goalkeeper) stopping logic
        if robot0.target_reached(threshold=15): # Corrected 'treshold'
            robot0.vx = 0
            robot0.vy = 0
            # Check orientation
            if abs(robot0.get_coordinates().rotation - self.robot0_a_target) < angle_tolerance_rad:
                if self.counter_goalkeeper_stop > self.threshold_goalkeeper_stop: # Contador excede o limiar
                    robot0.w = 0
                else:
                    self.counter_goalkeeper_stop += 1
            else: # Not oriented, reset counter
                self.counter_goalkeeper_stop = 0
                # robot0.w might still be active from go_to_point's controller
        else: # Not yet at target, reset counter, allow rotation
            # robot0.w = 0 # This was in original, but might prevent rotation towards target_theta
            self.counter_goalkeeper_stop = 0

        # Robot 1 (Defender) stopping logic
        if robot1.target_reached(threshold=15): # Corrected 'treshold'
            robot1.vx = 0
            robot1.vy = 0
            # Check orientation (Corrected large angle tolerance from 30*np.pi/2 to 30*np.pi/180)
            if abs(robot1.get_coordinates().rotation - self.robot1_a_target) < angle_tolerance_rad:
                if self.counter_defender_stop > self.threshold_defender_stop:
                    robot1.w = 0
                else:
                    self.counter_defender_stop += 1
            else: # Not oriented, reset counter
                self.counter_defender_stop = 0
        else: # Not yet at target, reset counter
            # robot1.w = 0
            self.counter_defender_stop = 0

        # Robot 2 (Attacker) stopping logic - simpler, no counter in original for w
        if robot2.target_reached(threshold=15): # Corrected 'treshold'
            robot2.vx = 0
            robot2.vy = 0
            # Check orientation (Corrected large angle tolerance from 30*np.pi/2 to 30*np.pi/180)
            if abs(robot2.get_coordinates().rotation - self.robot2_a_target) < angle_tolerance_rad:
                robot2.w = 0
            # else: robot2.w might still be active if not yet oriented
        else: # Not yet at target
            # robot2.w = 0 # This would stop rotation even if not oriented
            pass # Allow rotation controller from go_to_point to work