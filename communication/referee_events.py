from communication.proto.ssl_gc_referee_message_pb2 import Referee

def handle_referee_command(referee_state):
    if referee_state:
        if referee_state.command == Referee.Command.HALT:
            print("HALT - Parar o jogo!")
            # Lógica para parar os robôs aqui

        elif referee_state.command == Referee.Command.STOP:
            print("STOP - Pausar o jogo!")

        elif referee_state.command == Referee.Command.NORMAL_START:
            print("NORMAL START - Retomar o jogo!")

        elif referee_state.command == Referee.Command.FORCE_START:
            print("FORCE START - Começar imediatamente!")

        elif referee_state.command == Referee.Command.PREPARE_KICKOFF_BLUE:
            print("PREPARE KICKOFF BLUE - Preparar início para o time azul")

        elif referee_state.command == Referee.Command.PREPARE_KICKOFF_YELLOW:
            print("PREPARE KICKOFF YELLOW - Preparar início para o time amarelo")

        elif referee_state.command == Referee.Command.PREPARE_PENALTY_BLUE:
            print("PREPARE PENALTY BLUE - Preparar pênalti para o time azul")

        elif referee_state.command == Referee.Command.PREPARE_PENALTY_YELLOW:
            print("PREPARE PENALTY YELLOW - Preparar pênalti para o time amarelo")

        elif referee_state.command == Referee.Command.DIRECT_FREE_BLUE:
            print("DIRECT FREE BLUE - Tiro livre direto para o time azul")

        elif referee_state.command == Referee.Command.DIRECT_FREE_YELLOW:
            print("DIRECT FREE YELLOW - Tiro livre direto para o time amarelo")

        elif referee_state.command == Referee.Command.INDIRECT_FREE_BLUE:
            print("INDIRECT FREE BLUE - Tiro livre indireto para o time azul")

        elif referee_state.command == Referee.Command.INDIRECT_FREE_YELLOW:
            print("INDIRECT FREE YELLOW - Tiro livre indireto para o time amarelo")

        elif referee_state.command == Referee.Command.TIMEOUT_BLUE:
            print("TIMEOUT BLUE - Timeout para o time azul")

        elif referee_state.command == Referee.Command.TIMEOUT_YELLOW:
            print("TIMEOUT YELLOW - Timeout para o time amarelo")

        elif referee_state.command == Referee.Command.BALL_PLACEMENT_BLUE:
            print("BALL PLACEMENT BLUE - Colocação de bola para o time azul")

        elif referee_state.command == Referee.Command.BALL_PLACEMENT_YELLOW:
            print("BALL PLACEMENT YELLOW - Colocação de bola para o time amarelo")
