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


