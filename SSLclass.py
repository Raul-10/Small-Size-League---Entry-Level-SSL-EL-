import sim
import time
#from DrawField import plot_robot_path

class ssl():
    """
    Classe para controlar o robô Zico simulado no CoppeliaSim.
    
    Atributos:
        clientID: ID da conexão com o CoppeliaSim.
        robot: Handle do objeto robô no CoppeliaSim.
        motorE: Handle do motor esquerdo no CoppeliaSim.
        motorD: Handle do motor direito no CoppeliaSim.
        yOut: Lista para armazenar a posição Y do robô.
        xOut: Lista para armazenar a posição X do robô.
        phi: Ângulo atual do robô.
        phi_obs: Ângulo observado do robô.
        v: Velocidade linear do robô.
        instPosition: Posição instantânea do robô.
        posError: Lista para armazenar erros de posição.
    """

    def __init__(self, port=19999, name='robot01', motor_E='motorL01', motor_D='motorR01', motor_Ee='motorL02',motor_Dd='motorR02'):
        """
        Inicializa a classe Zico e estabelece a conexão com o CoppeliaSim.
        
        Parâmetros:
            port (int): Porta usada para conectar ao CoppeliaSim. Padrão = 19999
            name (str): Nome do objeto robô no CoppeliaSim. Padrão = robot01
            motor_E (str): Nome do motor esquerdo no CoppeliaSim. Padrão = motorL01
            motor_D (str): Nome do motor direito no CoppeliaSim. Padrão = motorR01
        """
        self.clientID, self.robot, self.motorE, self.motorD, self.motorEe, self.motorDd , self.ball = self.connect_CRB(port, name, motor_E, motor_D)
        self.yOut = []
        self.xOut = []
        self.phi = 0
        self.phi_obs = 0
        self.v = 8
        self.instPosition = [0, 0]
        self.posError = []
        self.rWheelSpeed = []
        self.lWheelSpeed = []
        self.angle = []

    def connect_CRB(self, port, name, motor_E, motor_D, motor_Ee, motor_Dd):
        """
        Função usada para comunicar-se com o CoppeliaSim.
        
        Parâmetros:
            port (int): Porta usada para conectar ao CoppeliaSim.
            name (str): Nome do objeto robô no CoppeliaSim.
            motor_E (str): Nome do motor esquerdo no CoppeliaSim.
            motor_D (str): Nome do motor direito no CoppeliaSim.
            
        Retorna:
            tuple: Contém o ID da conexão, o handle do robô, e os handles dos motores esquerdo e direito.
        """
        sim.simxFinish(-1)
        clientID = sim.simxStart('127.0.0.1', port, True, True, 2000, 5)
        if clientID == 0:
            print("Conectado a", port)
        else:
            print("no se pudo conectar")

        returnCode, robot = sim.simxGetObjectHandle(clientID, name, 
                                                    sim.simx_opmode_blocking)
        returnCode, MotorE = sim.simxGetObjectHandle(clientID, motor_E,
                                                     sim.simx_opmode_blocking)
        returnCode, MotorD = sim.simxGetObjectHandle(clientID, motor_D,
                                                     sim.simx_opmode_blocking)
        returnCode, MotorEe = sim.simxGetObjectHandle(clientID, motor_Ee,
                                                     sim.simx_opmode_blocking)
        returnCode, MotorDd = sim.simxGetObjectHandle(clientID, motor_Dd,
                                                     sim.simx_opmode_blocking)                                             
        returnCode, ball_Handle = sim.simxGetObjectHandle(clientID, 'ball',
                                                     sim.simx_opmode_blocking)
        return clientID, robot, MotorE, MotorD, ball_Handle
    
    def Get_Position(self):
        """
        Obtém a posição atual do robô no simulador. Salva as posições no
        atributo 'instPosition' do objeto e retorna estes valores em um tupla
        
        Get_Position(self)
        Retorna:
            tuple: Contém as coordenadas X e Y da posição atual do robô.
        """
        s, positiona = sim.simxGetObjectPosition(self.clientID, self.robot, -1, sim.simx_opmode_streaming)
        while positiona == [0, 0, 0]:
            s, positiona = sim.simxGetObjectPosition(self.clientID, self.robot, -1, sim.simx_opmode_streaming) 
        self.instPosition[0] = positiona[0]
        self.instPosition[1] = positiona[1] 
        return positiona[0], positiona[1]
    
    def Set_Velocities(self, ve, vd, vee, vdd):
        sim.simxSetJointTargetVelocity(self.clientID, self.motorE, ve, sim.simx_opmode_blocking)
        sim.simxSetJointTargetVelocity(self.clientID, self.motorD, vd, sim.simx_opmode_blocking)
        sim.simxSetJointTargetVelocity(self.clientID, self.motorEe, vee, sim.simx_opmode_blocking)
        sim.simxSetJointTargetVelocity(self.clientID, self.motorDd, vdd, sim.simx_opmode_blocking)

    def Stop_Robot(self):
        sim.simxSetJointTargetVelocity(self.clientID, self.motorE, 0, sim.simx_opmode_blocking)
        sim.simxSetJointTargetVelocity(self.clientID, self.motorD, 0, sim.simx_opmode_blocking)
        sim.simxSetJointTargetVelocity(self.clientID, self.motorEe, 0, sim.simx_opmode_blocking)
        sim.simxSetJointTargetVelocity(self.clientID, self.motorDd, 0, sim.simx_opmode_blocking) 

    def Wait(self, sec):
        time.sleep(sec)

    def Get_ball_Position(self):
        s, position = sim.simxGetObjectPosition(self.clientID, self.ball, -1, sim.simx_opmode_streaming)
        while position == [0, 0, 0]:
            s, position = sim.simxGetObjectPosition(self.clientID, self.ball, -1, sim.simx_opmode_streaming) 
        return position

if __name__ == "__main__":
    ve = 3
    vd = 3
    vee = 3
    vdd = 3

    robot1 = ssl()
    robot1.Set_Velocities(ve, vd)
    robot1.Wait(3)
    robot1.Stop_Robot()