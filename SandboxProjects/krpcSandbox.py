# -*- coding: utf-8 -*-
"""
Created on Sat May 16 23:59:23 2026

@author: Jason
"""

import krpc
import time


#conn = krpc.connect(name="Hello World")
#vessel = conn.space_center.active_vessel
#print(vessel.name)

#%% Sub orbital flight example
# connect to KSP
conn = krpc.connect(name='Sub-orbital flight')
# get active vessel
vessel = conn.space_center.active_vessel


#launch prep
vessel.auto_pilot.target_pitch_and_heading(90,90)
vessel.auto_pilot.engage()
vessel.control.throttle = 1 # max power
time.sleep(1)


print('Launch!')
vessel.control.activate_next_stage()

# fuel monitoring
fuel_amount = conn.get_call(vessel.resources.amount, "SolidFuel")
expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(fuel_amount),
    conn.krpc.Expression.constant_float(0.1))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()
print('Booster Separation')
vessel.control.activate_next_stage()

# event driven turn
mean_altitude = conn.get_call(getattr, vessel.flight(), 'mean_altitude')
expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(mean_altitude),
    conn.krpc.Expression.constant_double(10000)) # 10KM
event=conn.krpc.add_event(expr)
with event.condition:
    event.wait()
    
print('Gravity Turn')
vessel.auto_pilot.target_pitch_and_heading(60,90)

apoapsis_altitude = conn.get_call(getattr, vessel.orbit, 'apoapsis_altitude')
expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(apoapsis_altitude),
    conn.krpc.Expression.constant_double(100000)) # 100 km 
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()
    
print('Launch stage separation')
vessel.control.throttle = 0
time.sleep(1)
vessel.control.activate_next_stage()
vessel.auto_pilot.disengage()



# return
srf_altitude = conn.get_call(getattr, vessel.flight(), 'surface_altitude')
expr = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(srf_altitude),
    conn.krpc.Expression.constant_double(1000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()
vessel.control.activate_next_stage()

while vessel.flight(vessel.orbit.body.reference_frame).vertical_speed < -0.1:
    print('Altitude =%.1f meters' % vessel.flight().surface_altitude)
    time.sleep(1)
print('Landed!')


#%% Reference Frames
import krpc

conn = krpc.connect()
vessel = conn.space_center.active_vessel
print('(%.1f, %.1f, %.1f)' % vessel.position(vessel.orbit.body.reference_frame))
# (x,y,z) 

# import numpy as np 
# mag = np.linalg.norm(vessel.position(vessel.orbit.body.reference_frame))
# print(mag) # radius ~ 600000 m

#vessel y = forward, z = down, x = right; origin = cog

#%% Visual Debugging Ref Frames
import krpc
conn = krpc.connect(name='Visual Debugging')
vessel = conn.space_center.active_vessel

ref_frame = vessel.surface_velocity_reference_frame
conn.drawing.add_direction_from_com((0,1,0), ref_frame)
while True:
    pass


#%% Navball directions
import krpc
conn = krpc.connect(name='Navball directions')
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
ap.reference_frame = vessel.surface_reference_frame
ap.engage()

# noth of navball, pitch 0 deg 
ap.target_diection = (0,1,0)
ap.wait()

# vert up on navball
ap.target_direction=(1,0,0)
ap.wait()

# west heading of 270 deg with pitch of 0 deg
ap.target_direction=(0,0,-1)
ap.wait()
ap.disengage()


#%% orbital directions
import krpc
conn = krpc.connect(name='Orbital directions')
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
ap.reference_frame = vessel.orbital_reference_frame
ap.engage()

# Point the vessel in the prograde direction
ap.target_direction = (0, 1, 0)
ap.wait()

# Point the vessel in the orbit normal direction
ap.target_direction = (0, 0, 1)
ap.wait()

# Point the vessel in the orbit radial direction
ap.target_direction = (-1, 0, 0)
ap.wait()

ap.disengage()

#%% Surface prograde
import krpc
conn = krpc.connect(name='Surface prograde')
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot

ap.reference_frame = vessel.surface_velocity_reference_frame
ap.target_direction = (0, 1, 0)
ap.engage()
ap.wait()
ap.disengage()


#%% Vessel Speed
import time
import krpc

conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel
obt_frame = vessel.orbit.body.non_rotating_reference_frame
srf_frame = vessel.orbit.body.reference_frame

while True:
    obt_speed = vessel.flight(obt_frame).speed
    srf_speed = vessel.flight(srf_frame).speed
    print('Orbital speed = %.1f m/s, Surface speed = %.1f m/s' %
          (obt_speed, srf_speed))
    time.sleep(1)


#%% vessel velo
import time
import krpc

conn = krpc.connect(name='Orbital speed')
vessel = conn.space_center.active_vessel
ref_frame = conn.space_center.ReferenceFrame.create_hybrid(
    position=vessel.orbit.body.reference_frame,
    rotation=vessel.surface_reference_frame)

while True:
    velocity = vessel.flight(ref_frame).velocity
    print('Surface velocity = (%.1f, %.1f, %.1f)' % velocity)
    time.sleep(1)
    
    
#%% Angle of attack
import math
import time
import krpc

conn = krpc.connect(name='Angle of attack')
vessel = conn.space_center.active_vessel

while True:

    d = vessel.direction(vessel.orbit.body.reference_frame)
    v = vessel.velocity(vessel.orbit.body.reference_frame)

    # Compute the dot product of d and v
    dotprod = d[0]*v[0] + d[1]*v[1] + d[2]*v[2]

    # Compute the magnitude of v
    vmag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    # Note: don't need to magnitude of d as it is a unit vector

    # Compute the angle between the vectors
    angle = 0
    if dotprod > 0:
        angle = abs(math.acos(dotprod / vmag) * (180.0 / math.pi))

    print('Angle of attack = %.1f degrees' % angle)

    time.sleep(1)
    
    
    
#%% Landing Site
import time
from math import sin, cos, pi
import krpc

conn = krpc.connect(name='Landing Site')
vessel = conn.space_center.active_vessel
body = vessel.orbit.body
create_relative = conn.space_center.ReferenceFrame.create_relative

# Define the landing site as the top of the VAB
landing_latitude = -(0+(5.0/60)+(48.38/60/60))
landing_longitude = -(74+(37.0/60)+(12.2/60/60))
landing_altitude = 111

# Determine landing site reference frame
# (orientation: x=zenith, y=north, z=east)
landing_position = body.surface_position(
    landing_latitude, landing_longitude, body.reference_frame)
q_long = (
    0,
    sin(-landing_longitude * 0.5 * pi / 180),
    0,
    cos(-landing_longitude * 0.5 * pi / 180)
)
q_lat = (
    0,
    0,
    sin(landing_latitude * 0.5 * pi / 180),
    cos(landing_latitude * 0.5 * pi / 180)
)
landing_reference_frame = \
    create_relative(
        create_relative(
            create_relative(
                body.reference_frame,
                landing_position,
                q_long),
            (0, 0, 0),
            q_lat),
        (landing_altitude, 0, 0))

# Draw axes
conn.drawing.add_line((0, 0, 0), (1, 0, 0), landing_reference_frame)
conn.drawing.add_line((0, 0, 0), (0, 1, 0), landing_reference_frame)
conn.drawing.add_line((0, 0, 0), (0, 0, 1), landing_reference_frame)

while True:
    time.sleep(1)

