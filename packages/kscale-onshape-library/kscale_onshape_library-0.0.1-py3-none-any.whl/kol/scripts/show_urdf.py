# mypy: disable-error-code="import-not-found"
"""Simple script to interact with a URDF."""

import argparse
import time
from pathlib import Path
from typing import Sequence

from kol.logging import configure_logging


def main(args: Sequence[str] | None = None) -> None:
    configure_logging()

    try:
        import pybullet as p
    except ImportError:
        raise ImportError("pybullet is required to run this script")

    parser = argparse.ArgumentParser(description="Show a URDF")
    parser.add_argument("urdf", help="Path to the URDF file")
    parser.add_argument("--dt", type=float, default=0.01, help="Time step")
    parsed_args = parser.parse_args(args)

    # Connect to PyBullet.
    p.connect(p.GUI)
    p.setGravity(0, 0, -9.81)
    p.setRealTimeSimulation(0)

    # Turn off panels.
    # p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, 0)
    p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW, 0)
    p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW, 0)

    # Enable mouse picking.
    p.configureDebugVisualizer(p.COV_ENABLE_MOUSE_PICKING, 1)

    # Loads the floor plane.
    floor = p.loadURDF(str((Path(__file__).parent / "bullet" / "plane.urdf").resolve()))

    # Load the robot URDF.
    start_position = [0.0, 0.0, 1.0]
    start_orientation = p.getQuaternionFromEuler([0.0, 0.0, 0.0])
    flags = p.URDF_USE_SELF_COLLISION | p.URDF_USE_INERTIA_FROM_FILE
    robot = p.loadURDF(parsed_args.urdf, start_position, start_orientation, flags=flags, useFixedBase=0)

    # Initializes physics parameters.
    p.changeDynamics(floor, -1, lateralFriction=1, spinningFriction=-1, rollingFriction=-1)
    p.setPhysicsEngineParameter(fixedTimeStep=parsed_args.dt, maxNumCmdPer1ms=0)

    # Show joint controller.
    joints: dict[str, int] = {}
    controls: dict[str, float] = {}
    for i in range(p.getNumJoints(robot)):
        joint_info = p.getJointInfo(robot, i)
        name = joint_info[1].decode("utf-8")
        joint_type = joint_info[2]
        joints[name] = i
        if joint_type in (p.JOINT_PRISMATIC, p.JOINT_REVOLUTE):
            controls[name] = p.addUserDebugParameter(name, -3.14, 3.14, 0.0)

    # Run the simulation until the user closes the window.
    last_time = time.time()
    while p.isConnected():
        for k, v in controls.items():
            try:
                target_position = p.readUserDebugParameter(v)
                p.setJointMotorControl2(robot, joints[k], p.POSITION_CONTROL, target_position)
            except p.error:
                pass
        p.stepSimulation()
        cur_time = time.time()
        time.sleep(max(0, parsed_args.dt - (cur_time - last_time)))
        last_time = cur_time


if __name__ == "__main__":
    # python -m robot.cad.scripts.show_urdf
    main()
