**Copilot Instructions**

This repository is a small Python robotics codebase using `gpiozero` with a mock-mode for non-Linux development. The instructions below highlight the concrete patterns, run/debug commands, and integration points that help an AI coding agent be productive immediately.

- **Project Purpose**: drive a robot (motors, conveyor, kicker) and run a simple vision-to-kicker pipeline implemented in `main.py`.

- **Key Files**:
  - [Commands/driving_teleop.py](Commands/driving_teleop.py): keyboard teleop loop (WASD controls, space stop, `q` quit). Contains pin constants and uses `termios`/`tty` for raw input.
  - [Commands/subsystems/DrivingSubsystem.py](Commands/subsystems/DrivingSubsystem.py): `Drivetrain` class. Implements `tank_drive()`, `periodic()`, watchdog timeout, `deadband()` and hardware mapping via `_apply_motor()`.
  - [hardware.py](hardware.py): high-level `RobotHardware` composition used by `main.py`. Uses mock pins when not on Linux.
  - [main.py](main.py): top-level loop that reads vision (`vision.py`) and actuates `robot.kicker` and `robot.conveyor`.

- **Environment detection / mocks**: both `hardware.py` and `Commands/driving_teleop.py` switch to `gpiozero.pins.mock.MockFactory` when `os.uname().sysname != 'Linux'`. Prefer using local runs for logic changes since hardware is mocked on non-Linux.

- **Runtime commands**:
  - Run teleop (local/mocked): `python Commands/driving_teleop.py`
  - Run main system loop (mocked): `python main.py`
  - Note: these scripts expect Python 3 and `gpiozero` installed; tests are manual/interactive.

- **Subsystem pattern**: subsystems expose a small driver interface and a periodic loop:
  - command methods: e.g. `Drivetrain.tank_drive(left, right)` set targets and update `last_command_time`.
  - periodic application: `Drivetrain.periodic()` enforces watchdog, clamps/deadbands, and calls hardware layer `_apply_motor()`.
  - Preserve this two-layer design (desired state vs hardware application) when adding features.

- **Control semantics to preserve**:
  - Deadband and clamp behavior from `deadband()` and `clamp()` (see `Drivetrain`). Keep thresholds and scaling consistent.
  - Watchdog timeout (`watchdog_timeout = 0.4s`) — do not remove without adjusting callers.

- **Input & timing patterns**:
  - `Commands/driving_teleop.py` uses a non-blocking read with `select` and a fixed `LOOP_HZ` (see `Commands/constants.py`) to schedule motor updates; maintain that pattern for low-latency teleop.
  - Use `periodic()` calls each loop iteration rather than applying motors directly from callers.

- **Vision & actuation integration**:
  - `main.py` samples `vision.get_target_coords()` (from `vision.py`) and schedules kicker events by timestamp. Follow the queue/timer pattern if adding new timed actuations.

- **Local development tips**:
  - On macOS/Windows or CI, code will run with mocked `gpiozero` pins — useful for unit-ish manual testing.
  - For hardware pin changes, update the pin constants in `Commands/driving_teleop.py` or the `RobotHardware` constructor in `hardware.py`.

- **What to look for in PRs**:
  - Preserve `periodic()`/watchdog/deadband behavior for subsystems.
  - Keep simple, synchronous loops in `main.py` and teleop; heavy async/threaded changes require careful review.

- **Files that exemplify patterns**:
  - Subsystem: [Commands/subsystems/DrivingSubsystem.py](Commands/subsystems/DrivingSubsystem.py)
  - Teleop + input loop: [Commands/driving_teleop.py](Commands/driving_teleop.py)
  - Hardware composition: [hardware.py](hardware.py)

If any of these areas are unclear or you want the instructions to include additional examples (unit test snippet, CI steps, or a short runbook for flashing a Raspberry Pi), tell me which part to expand. I can update this file accordingly.
