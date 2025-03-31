from hub import light_matrix, motion_sensor, port
import motor
import motor_pair
import runloop

async def main():
    # Display a welcome message
    light_matrix.write("Hi")
    await runloop.sleep_ms(1000)# Allow some time to display "Hi"

    #switch between different modes displaying the mode on the screeen
    # wait until the user is done tapping before running the mode
    while True:
        # mode = input("What mode do you want (1-5)")
        mode = 2
        if mode == 1:
            await straightLineDriving()
        elif mode == 2:
            await pivotTurn()
        elif mode == 3:
            pass
        elif mode == 4:
            pass
        elif mode == 5:
            light_matrix.write("Done!")
        else:
            print("unknown mode")
        mode = 5
        
            

async def straightLineDriving():
    light_matrix.show_image(light_matrix.IMAGE_ARROW_N)

    # Start driving forward at moderate speed
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)# Set motor ports
    motor_pair.move(motor_pair.PAIR_1, 0)
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=280)
    await runloop.sleep_ms(5000)
    motor_pair.stop(motor_pair.PAIR_1)

async def pivotTurn():
    degrees = 45
    initial_rotation = get_rotation()

    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)# Ensure motors are paired
    motor_pair.move_tank(motor_pair.PAIR_1, -30, 30)# Start pivoting in place

    if abs(angle_difference(get_rotation(), initial_rotation)) < degrees:
        motor_pair.stop(motor_pair.PAIR_1)# Stop motors after reaching target rotation

def get_rotation():
    """Returns the yaw angle in a consistent 0-360 range."""
    angle = motion_sensor.get_yaw_face()
    return (angle + 360) % 360# Normalize to 0-360

def angle_difference(current, initial):
    """Calculates the shortest difference between two angles, handling wrap-around cases."""
    diff = (current - initial + 360) % 360# Ensure positive value
    return min(diff, 360 - diff)# Account for wrap-around
    

runloop.run(main())
