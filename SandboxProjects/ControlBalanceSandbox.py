# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 23:07:03 2025
Refreshing and understanding control concepts in Python with focus on 
balance models and situations 


alternative: https://github.com/jpaine126/Inverted_Pendulum_Control_Demo?tab=readme-ov-file 

https://www.do-mpc.com/en/latest/getting_started.html#Example-system
https://www.reddit.com/r/ControlTheory/comments/oomcaf/control_libraries_for_python/

https://python-control.readthedocs.io/en/0.10.2/
@author: 17jlo
"""

#%% Imports

#%% https://python-control.readthedocs.io/en/0.10.2/examples/pvtol-lqr.html



















































#%% balancing robot Model (openGL not worth bothering with for wanting just a simple model in python)

# from math import cos
# from math import sin
# from math import pi 
# from math import atan 
# #https://github.com/rguyonneau/Self-Balancing-Robot-Python-Simulator/blob/master/src/iballancingbot.py

# class IBalancingBot: 
#     """
#     Mathematical model is from article in the Github page
#     """
#     def __init__(self):
#         # variables for model 
#         self.Mb = None # kg mass of main body (pendulum)
#         self.Mw = None # kg mass of wheels 
#         self.d = None # m center of mass from base
#         self.R = None # m radius of wheel 
#         self.L = None # m Distance between the wheels 
#         self.Ix = None # kg.m^2 moment of inertia of body x-axis
#         self.Iz = None # kg.m^2 moment of inertia of body z-axis
#         self.Ia = None # kg.m^2 moment of intertia of wheel according to center 
#         self.g = None # m/s^2 Acceleration due to gravity 
        
#         # variable for dynamic avaluation 
#         self.phi = None # angle of the pendulum 
#         self.phip = None # angular speed of pendulum
#         self.phipp = None # angular accel of pendulum 
#         self.x = None # x position of the robot 
#         self.xp = None # linear x speed of the robot 
#         self.xpp = None # linear x accel of robot 
#         self.psi = None # rotation of robot 
#         self.psip = None # rotation angular speed of robot
#         self.psipp = None # rotation angular accel of robot 
        
#         # variable for the drawing 
#         self.d_rw = None # wheel radius 
#         self.d_dstw = None # distance between the wheels 
#         self.d_widthw = None # width of wheel 
#         self.d_heightp = None # height of pendulum 
#         self.d_centerp = None # distance between the wheel and pendulum center
#         self.d_widthp = None # width of robot pipes
        
#         self.initRobot() # initialize all parameters of the system
    
#     def initRobot(self):
#         """
#         Intiialize all parameters based on the paper 
#         """
#         # variables for the model
#         self.Mb = 13.3    # kg      mass of main body (pendulum)
#         self.Mw = 1.89    # kg      mass of wheels
#         self.d = 0.13     # m       center of mass from base
#         self.R = 0.130    # m       Radius of wheel
#         self.L = 0.325    # m       Distance between the wheels
#         self.Ix = 0.1935  # kg.m^2  Moment of inertia of body x-axis
#         self.Iz = 0.3379  # kg.m^2  Moment of inertia of body z-axis
#         self.Iy = 0.3379  # kg.m^2  Moment of inertia of body y-axis : NOT A VALUE FROM THE PAPER
#         self.Ia = 0.1229  # kg.m^2  Moment of inertia of wheel according to center
#         self.g = 9.81     # m/s^2   Acceleration due to gravity  

#         self.phi = 2*pi/180  # the pendulum is initially unstable 
#         self.phip = 0

#         self.x = 0
#         self.xp = 0

#         self.psi = 0
#         self.psip = 0

#         # variables for the drawing
#         self.d_rw = self.R
#         self.d_dstw = self.L
#         self.d_widthw = 0.01
#         self.d_heightp = self.d
#         self.d_centerp = self.d
#         self.d_widthp = 0.01

#         # to deal with the fact that the pendulum can not be lower than the ground
#         # we compute the maximal possible angle for the pendulum
#         self.phimax = pi/2 + atan(self.R/(2*self.d)) # return to this to understand (seems not complicated)
#         self.phimin = -pi/2 - atan(self.R/(2*self.d))
#     def f(self,phi,phip, x, xp, psi, psip, deltat, F):
#         """ Function to evaluate the new state of the system according to:
#     - the mathematical model (phipp=, xpp=, psipp=)
#     - the current state (phi, phip, x, xp, psi, psip)
#     - the time step deltat
#     - the command F=[tau1, tau2] (constant over deltat)
#     It returns phip, phipp, xp, xpp, psip, psipp
# """
#         tau1 = F[0]
#         tau2 = F[1]
        
#         # for read ability 
#         Mb = self.Mb
#         Mw = self.Mw
#         d = self.d
#         R = self.R
#         L = self.L
#         Ix = self.Ix
#         Iz = self.Iz
#         Iy = self.Iy
#         Ia = self.Ia
#         g = self.g
        
#         R2 = R**2
#         d2 = d**2 
        
#         #compute phipp 
#         den_phipp = ((R*Mb*d*sin(phi))**2)+((Mb+2*Mw)*(R2)+2*Ia)*Ix+2*Mb*d2*(Mw*R2+Ia)
        
#         phipp = ((Mb*d2+Iy-Iz)*(Mb*R2+2*Mw*R2+2*Ia)*sin(phi)*cos(phi))*(psip**2)/den_phipp \
#                 - (Mb**2)*d2*R2*sin(phi)*cos(phi)*(phip**2)/den_phipp \
#                 + (Mb*R2+2*Mw*R2+2*Ia)*Mb*g*d*sin(phi)/den_phipp \
#                 - ((Mb*R2+2*Mw*R2+2*Ia)+Mb*d*R*cos(phi))*(tau1+tau2)/den_phipp
        
#         #computation fo xpp 
#         den_xpp = (Mb*d2+Ix)*(Mb*R2+2*Mw*R2+2*Ia)-((Mb*d*R*cos(phi))**2)
#         xpp = (Mb*d*R*cos(phi)*(Mb*d2+Iy-Iz)*sin(phi)*cos(phi)*(psip**2))/den_xpp \
#               - ((Mb**2)*d2*g*R2*sin(phi)*cos(phi))/den_xpp \
#               + (R2*(Mb*d2+Ix)*Mb*d*sin(phi)*(phip**2))/den_xpp \
#               + (R*(Mb*d2+Ix+Mb*d*R*cos(phi))*(tau1+tau2))/den_xpp
              
#         den_psipp = 2*(Mw+Ia/R2)*(L**2)+Iy*(sin(phi)**2)+Iz*(cos(phi)**2)+Mb*d2*sin(phi)
#         psipp = (L*(tau1-tau2))/(R*den_psipp) \
#                 - (2*(Mb*d2+Iy-Iz)*sin(phi)*cos(phi)*psip*phip)/den_psipp
#         return phip*deltat, phipp*deltat, xp*deltat, xpp*deltat, psip*deltat, psipp*deltat
    
#     def runge_kutta(self, deltat, F):
#         """
#         applying runge kutta to solve Diff Eqs
#         """
#         k1phip, k1phipp, k1xp, k1xpp, k1psip, k1psipp = \
#            self.f(self.phi, self.phip, self.x, self.xp, self.psi, self.psip, deltat, F)
#         k2phip, k2phipp, k2xp, k2xpp, k2psip, k2psipp = \
#            self.f(self.phi + k1phip/2, self.phip + k1phipp/2, self.x + k1xp/2, self.xp + k1xpp/2, self.psi + k1psip/2, self.psip + k1psipp/2, deltat, F)
#         k3phip, k3phipp, k3xp, k3xpp, k3psip, k3psipp = \
#            self.f(self.phi + k2phip/2, self.phip + k2phipp/2, self.x + k2xp/2, self.xp + k2xpp/2, self.psi + k2psip/2, self.psip + k2psipp/2, deltat, F)
#         k4phip, k4phipp, k4xp, k4xpp, k4psip, k4psipp = \
#            self.f(self.phi + k3phip, self.phip + k3phipp, self.x + k3xp, self.xp + k3xpp, self.psi + k3psip, self.psip + k3psipp, deltat, F)

#         self.phi = self.phi + 1/6.0*(k1phip+2*k2phip+2*k3phip+k4phip)
#         self.phip = self.phip + 1/6.0*(k1phipp+2*k2phipp+2*k3phipp+k4phipp)

#         self.xp = self.xp + 1/6.0*(k1xpp+2*k2xpp+2*k3xpp+k4xpp)
#         self.x = self.x + 1/6.0*(k1xp+2*k2xp+2*k3xp+k4xp)

#         self.psip = self.psip + 1/6.0*(k1psipp+2*k2psipp+2*k3psipp+k4psipp)
#         self.psi = self.psi + 1/6.0*(k1psip+2*k2psip+2*k3psip+k4psip)

#        # to deal with the fact that the pendulum can not be lower than the ground.
#        # we also put the acceleration to 0 to avoid that the robot moves
#        #   when the pendulum is down
#         if (self.phi > self.phimax): 
#              self.phi = self.phimax
#              self.phip = 0
#              self.xp = 0
#         if (self.phi < self.phimin):
#              self.phi = self.phimin
#              self.phip = 0
#              self.xp = 0

#     def dynamic(self,deltat, F):
#         """
#         interface between model and display?
#         """
#         self.runge_kutta(deltat,F)
        
        
# class PID:
#     """
#     Discrete PID
#     """
    
#     def __init__(self, P=7.0,I=0.1,D=6.0, Derivator=0,Integrator=0, Integrator_max=3, Integrator_min=-3):
#         self.Kp= P
#         self.Ki = I
#         self.Kd = D
#         self.Derivator = Derivator
#         self.Integrator = Integrator
#         self.Integrator_max = Integrator_max
#         self.Integrator_min = Integrator_min
        
#         self.set_point=0.0
#         self.error=0.0
        
#     def update(self,current_value):
#         # define PID output for given reference input and feedback
#         self.error = self.set_point-current_value
        
#         self.P_value = self.Kp* self.error
#         self.D_value = self.Kd*(self.error-self.Derivator)
#         self.Derivator = self.error
        
#         self.Integrator = self.Integrator +self.error
        
#         if self.Integrator > self.Integrator_max:
#             self.Integrator = self.Integrator_max
#         elif self.Integrator < self.Integrator_min:
#             self.Integrator = self.Integrator_min
            
#         self.I_value = self.Integrator *self.Ki
#         PID = self.P_value +self.I_Value +self.D_value
        
#         return PID
#     def setPoint(self,set_point):
#         # initialize setpoint of PID 
#         self.set_point = set_point
#         self.Integrator = 0
#         self.Derivator = 0 
#     def setIntegrator(self, Integrator):
#         self.Integrator = Integrator
#     def setDerivator(self, Derivator):
#         self.Derivator = Derivator
#     def setKp(self,P):
#         self.Kp = P
#     def setKi(self,I):
#         self.Ki = I
#     def setKd(self,D):
#         self.Kd = D
#     def getPoint(self):
#         return self.set_point
#     def getError(self):
#         return self.error 
#     def getIntegrator(self):
#         return self.Integrator
#     def getDerivator(self):
#         return self.Derivator
    
    
# # main file 
# import sys as sys;
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *
# from math import cos
# from math import sin 
# from math import pi 
# from math import sqrt 

# # issue with OpenGL install have model and PID now maybe lighter weight possible (don't care enough to fix)
# #https://community.khronos.org/t/problem-with-glutinit/110932/6



# print("Controls")
# print(" Page down : activate simulation")
# print(" F1 : move backward")
# print(" F2 : move forward")
# print(" F3 : turn")
# print(" F4 : stop motion")
# print(" F5 : ON/OFF PID correction")
# print(" F6 : reset simulation")
# print(" F7 : add pertubation (push the robot)")
# print(" F8 : add pertubation (push the robot)")
# print(" F9 : ON/OFF follow the robot")

# # -- Programme variables --

# # variables for the animation of the dynamics
# # ref_time : to compute the time between two redisplay$
# # FPS : Frame per second, to 
# ref_time, FPS = 0, 10

# # position of the camera (glulookat parameters)
# CameraPosX = 0.0
# CameraPosY = 3
# CameraPosZ = 10.0
# ViewUpX = 0.0
# ViewUpY = 1.0
# ViewUpZ = 0.0
# CenterX = 0.0
# CenterY = 0.0
# CenterZ = 0.0
# follow_robot = False  # so that the camera will follow the robot or not

# # to deal with the camera rotation and zoom
# Theta,dtheta=0.0,2*pi/100.0
# Radius = sqrt( CameraPosX**2+CameraPosZ**2)

# # to draw cylinder
# quadric = gluNewQuadric()
# gluQuadricNormals(quadric, GLU_SMOOTH)

# # the balancing robot
# myBot = IBalancingBot()

# # for the PIDs correction:
# #   1 PID for the pendulum angle (phi)
# #   1 PID for the linear x speed (xp)
# #   1 PID for the robot angular speed rotation (psip)
# myPIDphi = PID()
# myPIDx = PID()
# myPIDpsi = PID()

# # to draw the robot at its actual position in the world
# posx = posz = 0

# # the command of the robot's wheels
# F = [0, 0]

# # activate or distactivate the PIDs correction
# use_pid = False

# # to deal with the "moving forwars" and "turning" commands
# speed = 0
# current_speed = 0
# turn = 0
# current_turn = 0

# def initPIDs():
#     """ Function that initializes the PIDs parameters (Kp, Ki, Kd)
#     """
#     global myPIDphi, myPIDx, myPIDpsi

#     myPIDphi.setKp(7.0)
#     myPIDphi.setKi(0.1)
#     myPIDphi.setKd(6.0)
#     myPIDphi.setPoint(0)

#     myPIDx.setKp(0.01)
#     myPIDx.setKi(0.005)
#     myPIDx.setKd(0.01)
#     myPIDx.setPoint(0)

#     myPIDpsi.setKp(1)
#     myPIDpsi.setKi(1)
#     myPIDpsi.setKd(0)
#     myPIDpsi.setPoint(0)
    

# def correction():
#     """ Function that uses the PID and the robot state to generate a new 
#         command according to the speed and turn objectives
#     """
#     global myBot, F, myPIDx, myPIDphi, myPIDpsi, use_pid
#     global speed, current_speed, turn, current_turn

#     if(use_pid):
#         if(current_speed != speed):
#             current_speed = speed
#             myPIDx.setPoint(speed)  # we only want to reset the PID when the speed changes

#         if(current_turn != turn):
#             current_turn = turn
#             myPIDpsi.setPoint(turn)  # we only want to reset the PID when the rotation changes

#         pidx_value = myPIDx.update(myBot.xp)  # Pid over linear a speed
#         pidpsi_value = myPIDpsi.update(-myBot.psip)  # Pid over psi angular speed rotation

#         tilt = - pidx_value + myBot.phi
#         rotation = pidpsi_value

#         pidphi_value = myPIDphi.update(tilt)  # pid over the pendulum angle phi

#         F = [-pidphi_value-rotation,-pidphi_value+rotation]
#     else:
#         F = [0, 0]


# def animation():
#     """ Function to compute the robot state at each time step and to draw it in the world
#     """
#     global ref_time, FPS, F, posx, posz, myBot
#     # FPS expressed in ms between 2 consecutive frame
#     delta_t = 0.001 # the time step for the computation of the robot state
#     if glutGet(GLUT_ELAPSED_TIME)-ref_time > (1.0/FPS)*1000 :
#         # at each redisplay (new display frame)
#         dst = 0
#         for i in range(0,100):
#             # we want the computation of the robot state to be faster than the 
#             # display to limit the compution errors
#             # display : new frame at each 100ms
#             # deltat : 1ms for the differential equation evaluation
#             myBot.dynamics(delta_t, F)
#             # we also compute the new x and z position of the robot in the world
#             dst = (myBot.xp * delta_t)
#             posx += dst*cos(myBot.psi)
#             posz += (-dst*sin(myBot.psi))

#         correction()  # calls the PIDs if enable
#         glutPostRedisplay()  # refresh the display
#         ref_time=glutGet(GLUT_ELAPSED_TIME)

# def drawGround():
#     """ Function to draw the ground
#     """
#     nb_rows = 20
#     nb_cols = 20
#     for r in range(0,nb_rows):
#         for c in range(0,nb_cols):
#             if(r%2 and not c%2 or not r%2 and c%2):
#                 glColor3d(0.3,0.3,0.3)
#             else:
#                 glColor3d(0.1,0.1,0.1)
#             glBegin( GL_QUADS )
#             glVertex3f(c-nb_cols/2, 0, r-nb_rows/2)
#             glVertex3f(c-nb_cols/2+1, 0, r-nb_rows/2)
#             glVertex3f(c-nb_cols/2+1, 0, r-nb_rows/2+1)
#             glVertex3f(c-nb_cols/2, 0, r-nb_rows/2+1)
#             glEnd()

# def drawIBot(ibot):
#     """ Function to draw the robot
#         ibot: the robot (IBalancingBot) to draw
#     """
#     global myBot
#     drawWheels(ibot.d_dstw, ibot.d_widthw, ibot.d_rw)  # draw the wheels
#     drawBase(ibot.d_dstw, ibot.d_widthp)  # draw the robot body
#     drawPendulum(ibot.d_heightp, ibot.d_widthp, ibot.d_centerp)  # draw the pendulum

# def drawWheels(dst_wheels, width_wheel, radius_wheel):
#     """ Function to draw the robot's wheels
#         dst_wheels : distances between the two wheels
#         width_wheel : width of the wheels
#         radius_wheel : radius of the wheels
#     """
#     global quadric  # to use gluCylinder to draw cylinder
#     # draw the first wheel
#     glPushMatrix()
#     glTranslatef(0, 0, -dst_wheels/2)
#     drawWheel(radius_wheel/2, width_wheel) 
#     glPopMatrix()
#     # draw the second wheel
#     glPushMatrix()
#     glTranslatef(0, 0, dst_wheels/2)
#     drawWheel(radius_wheel/2, width_wheel)
#     glPopMatrix()


# def drawWheel(size, width):
#     """ Function to draw a wheel (a cylinder and two disks to close it)
#         size : size of the wheel (radius)
#         width : width of the wheel (width of the cylinder)
#     """
#     global quadric
#     # draw cylinder of the wheel
#     glPushMatrix()
#     glColor3d(0.4,0.4,0.4)
#     glTranslatef(0,0,-width/2)
#     gluCylinder(quadric, size, size, width,32,16)
#     glPopMatrix()
#     # draw the first disk to close the cylinder
#     glPushMatrix()
#     glColor3d(0.6,0.6,0.6)
#     glTranslatef(0,0,-width/2)
#     gluDisk(quadric, 0,size,32,32)
#     glPopMatrix()
#     # draw the second disk to close the cylinder
#     glPushMatrix()
#     glColor3d(0.6,0.6,0.6)
#     glTranslatef(0,0,width/2)
#     gluDisk(quadric, 0,size,32,32)
#     glPopMatrix()

# def drawBase(dst_wheels, radius_pipe):
#     """ Function to draw the body of the robot (a cylinder between the wheels)
#         dst_wheels : distance between the wheels
#         radius_pipe : the width of the cylinder body
#     """
#     global quadric
#     glPushMatrix()
#     glColor3d(0.4,0.4,1)
#     glTranslatef(0, 0, -dst_wheels/2)
#     gluCylinder(quadric,radius_pipe/2, radius_pipe/2, dst_wheels,32,16)
#     glPopMatrix()

# def drawPendulum(height_pendulum, radius_pipe, center_pendulum):
#     """ Function to draw the pendulum of the robot (a cylinder up)
#         height_pendulum : height of the pendulum from the center of the wheels
#         radius_pipe : the width of the pendulum cylinder
#         center_pendulum :  height of the center of mass of the pendulum from the center of the wheels
#     """
#     global quadric
#     # draw the pendulum
#     glPushMatrix()
#     glColor3d(1,0.4,0.4)
#     glRotatef(90,-1,0,0)
#     gluCylinder(quadric,radius_pipe/2, radius_pipe/2, height_pendulum,32,16)
#     glPopMatrix()
#     # draw the center of mass
#     glPushMatrix()
#     glColor3d(0.4,1,0.4)
#     glTranslatef(0, center_pendulum, 0)
#     glutSolidSphere(radius_pipe, 32, 32)
#     glPopMatrix()


# def Displayfct():
#     """ Function to draw the world
#     """

#     scaleCoeff = 10  # to scale the robot display

#     glClearColor(0,0,0,0)  # background color
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     # Projection
#     glMatrixMode(GL_PROJECTION);
#     glLoadIdentity();
#     glFrustum(-1,1,-1,1,1,80.)

#     # Camera position and orientation
#     global CameraPosX, CameraPosY, CameraPosZ, CenterX, CenterY, CenterZ, ViewUpX, ViewUpY, ViewUpZ
#     global myBot, posx, posz, follow_robot

#     if(follow_robot):
#         CenterX = -posx*scaleCoeff
#         CenterZ = -posz*scaleCoeff

#     gluLookAt(CameraPosX, CameraPosY , CameraPosZ, CenterX, CenterY, CenterZ, ViewUpX, ViewUpY, ViewUpZ)

#     # Draw the objects and geometrical transformations
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()


#     # draw the ground
#     glPushMatrix()
#     glScalef(scaleCoeff, scaleCoeff, scaleCoeff)  # to scale the ground as the robot
#     glTranslatef(0,-myBot.d_rw/2,0)
#     drawGround()
#     glPopMatrix()

#     # draw the robot
#     glPushMatrix()
#     glScalef(scaleCoeff, scaleCoeff, scaleCoeff)  # to scale the robot
#     glTranslatef(-posx,0,-posz)
#     glRotatef(myBot.psi*180/pi, 0, 1, 0)  # psi rotation (robot)
#     glRotatef(myBot.phi*180/pi, 0, 0, 1)  # phi rotation (pendulum)
#     drawIBot(myBot)
#     glPopMatrix()

#     # To efficient display
#     glutSwapBuffers()


# def ReshapeFunc(w,h):
#     """ Function calls when reshaping the window
#     """
#     glViewport(0,0,w,h)

# def rotate_camera(angle):
#     """ Function to rotate the camera according to an angle
#         angle : step angle for the camera rotation
#     """
#     global CameraPosX,CameraPosZ,Radius,Theta
#     Theta+=angle
#     CameraPosZ=Radius*cos(Theta)
#     CameraPosX=Radius*sin(Theta)
#     return 0

# def zoom_camera(factor):
#     """ Function to zoom the camera according to a factor
#         factor : zoom factor
#     """
#     global CameraPosX,CameraPosY,CameraPosZ,Radius
#     # Update camera center
#     CameraPosX, CameraPosY, CameraPosZ = factor*CameraPosX, factor*CameraPosY, factor*CameraPosZ
#     # Update radius (for next rotations)
#     Radius = sqrt( CameraPosX**2 + CameraPosZ**2 )

# def SpecialFunc(skey,x,y):
#     """ Function to handle the keybord keys
#     """
#     global CameraPosY, Theta, dtheta
#     global myBot, speed, use_pid, turn
#     global posx, posz, follow_robot

#     if glutGetModifiers() == GLUT_ACTIVE_SHIFT:
#         # SHIFT pressed
#         if skey == GLUT_KEY_UP :
#             CameraPosY+=0.3  # put the camera higher
#         if skey == GLUT_KEY_DOWN :
#             CameraPosY-=0.3  # put the camera lower
#     else:
#         # standard
#         if skey == GLUT_KEY_LEFT :
#             rotate_camera(-dtheta)
#         elif skey == GLUT_KEY_RIGHT :
#             rotate_camera(dtheta)
#         elif skey == GLUT_KEY_UP :
#             zoom_camera(0.9)
#         elif skey == GLUT_KEY_DOWN :
#             zoom_camera(1.1)
#         elif skey == GLUT_KEY_PAGE_DOWN : 
#             print("\tSimulation ON")
#             glutIdleFunc(animation)
#         elif skey == GLUT_KEY_PAGE_UP :
#             print("\tSimulation PAUSE")
#             glutIdleFunc(None)
#         elif skey == GLUT_KEY_F1 :
#             speed = 0.15
#         elif skey == GLUT_KEY_F2 :
#             speed = -0.15
#         elif skey == GLUT_KEY_F3 : 
#             turn = 0.3
#         elif skey == GLUT_KEY_F4 : 
#             speed = 0
#             turn = 0
#         elif skey == GLUT_KEY_F5 : 
#             use_pid = not(use_pid)
#             print("\tUsing PID : " + str(use_pid))
#             if(use_pid == True):
#                 initPIDs()
#         elif skey == GLUT_KEY_F6 : 
#             posx = posz = 0
#             myBot.initRobot()
#             initPIDs()
#         elif skey == GLUT_KEY_F7 : 
#             myBot.phi += (10*pi/180)
#         elif skey == GLUT_KEY_F8 : 
#             myBot.phi += (-20*pi/180)
#         elif skey == GLUT_KEY_F9 : 
#             follow_robot = not(follow_robot)
#             print("\tFollowing robot : " + str(follow_robot))
#     glutPostRedisplay()
#     return 0

# # Initialization of the Window stuff
# glutInit(sys.argv)
# glutInitWindowPosition(100,100)
# glutInitWindowSize(250,250)
# glutInitDisplayMode(GLUT_RGBA |GLUT_DOUBLE | GLUT_DEPTH)
# glutCreateWindow(b"IBBot simulator")

# # Opengl Initialization      
# glClearColor(0.0,0.0,0.0,0.0)
# glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
# glEnable(GL_DEPTH_TEST) # Hidden objects are not drawn

# # Display are reshape function
# glutDisplayFunc(Displayfct)
# glutReshapeFunc(ReshapeFunc)
# glutSpecialFunc(SpecialFunc)

# # Infinite loop
# glutMainLoop()

#%% Level 1 PID control Balance