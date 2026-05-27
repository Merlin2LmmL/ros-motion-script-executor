# Your First ROS2 Node – A Step-by-Step Tutorial
<p align="left">
  🇩🇪 <a href="./README.md">Zur deutschen Version wechseln</a>
</p>

**Target audience:** Students with basic Python knowledge who have no prior experience with Linux terminals or ROS.

**Goal:** By the end of this tutorial, you will have built your own ROS2 node that moves a simulated robot.

---

## Table of Contents

1. [Linux Basics – Understanding the Terminal](#1-linux-basics--understanding-the-terminal)
2. [Installing ROS2 Jazzy](#2-installing-ros2-jazzy)
3. [First Steps with ROS2](#3-first-steps-with-ros2)
4. [Creating a ROS2 Package](#4-creating-a-ros2-package)
5. [Programming the Node](#5-programming-the-node)
6. [Building the Package with Colcon](#6-building-the-package-with-colcon)
7. [Testing the Node with a Real Simulator](#7-testing-the-node--with-a-real-simulator)
8. [Bonus: JSON Command Files](#8-bonus-json-command-files)

---

## 1. Linux Basics – Understanding the Terminal

Before we can do anything with ROS, we need to get familiar with the most important tool: the **terminal** (also called the "command line" or "shell").

The terminal is not a relic of the past. In robotics, system administration, and software development, it is the primary working tool. With a little practice, it will quickly feel natural.

### Opening the Terminal

On Ubuntu, you can open the terminal with:
- **Keyboard shortcut:** `Ctrl + Alt + T`
- Right-click on the desktop → "Open Terminal"
- Search for "Terminal" in the application menu

You will see something like this:
```
yourname@yourcomputer:~$
```
The `~` stands for your **home directory** (`/home/yourname`). The `$` indicates that you are logged in as a regular user.

---

### The Most Important Commands

#### Where am I?
```bash
pwd
```
`pwd` stands for *Print Working Directory* – it shows you which folder you are currently in.

#### What is in here?
```bash
ls
ls -l        # Detailed view (size, date, permissions)
ls -la       # Also show hidden files (those beginning with .)
```

#### Changing directories
```bash
cd Documents          # Navigate into the "Documents" folder
cd ..                 # Go up one directory
cd ~                  # Go directly to the home directory
cd /home/yourname/ros2_ws   # Absolute path
```

> **Tip – Tab completion:** If you type the beginning of a folder or file name and press `Tab`, the terminal will autocomplete it. If there are multiple possibilities, press `Tab` twice and all options will be shown. This saves a tremendous amount of time.

#### Creating directories
```bash
mkdir my_folder
mkdir -p path/to/deep/folder    # Creates all intermediate directories
```

#### Deleting files and directories
```bash
rm file.txt              # Delete a file
rm -r folder/            # Delete a folder (and its contents)
rm -rf folder/           # Force delete – CAUTION, no recycle bin!
```

> **Warning:** `rm` deletes permanently, without confirmation. There is no recycle bin in the terminal. Never run commands from the internet that you do not understand – especially those combining `sudo`, `rm`, and `-rf`.

#### Viewing and editing files
```bash
cat file.txt             # Print contents to the terminal
nano file.txt            # Open the file in a terminal editor
```

**Nano** is a simple text editor that runs directly in the terminal. The most important shortcuts:
- `Ctrl + O` → Save (then confirm with `Enter`)
- `Ctrl + X` → Exit
- `Ctrl + K` → Cut line
- `Ctrl + W` → Search

---

### Sudo – Administrator Privileges

Some commands require administrator privileges. For this, there is `sudo` (*Super User Do*):

```bash
sudo apt install something
```

> **Note:** When asked for your password, you will see nothing as you type – no asterisks, no dots. This is normal and intentional. Type your password and press `Enter`.

---

### Stopping Processes

If a program is running in the terminal and you want to stop it:
- `Ctrl + C` – Immediately terminate the program. You will use this shortcut very often.

---

### Copy and Paste in the Terminal

The usual `Ctrl + C` / `Ctrl + V` does not work in the terminal, because `Ctrl + C` terminates processes. Instead:
- **Copy:** Select text → `Ctrl + Shift + C`
- **Paste:** `Ctrl + Shift + V`

---

### Multiple Terminals at Once

Throughout this tutorial, you will need multiple terminal windows open at the same time. You can open as many windows as you like and arrange them side by side.

---

### Quick Reference

| Command | Meaning |
|---------|---------|
| `pwd` | Show current path |
| `ls` | List directory contents |
| `cd <folder>` | Change directory |
| `mkdir <name>` | Create a folder |
| `rm <file>` | Delete a file |
| `cat <file>` | Display file contents |
| `nano <file>` | Edit a file |
| `Tab` | Autocomplete |
| `Ctrl + C` | Terminate program |
| `Ctrl + Shift + V` | Paste in terminal |
| `sudo <command>` | Run as administrator |

---

## 2. Installing ROS2 Jazzy

### What is ROS2?

**ROS** stands for *Robot Operating System* – but it is not an operating system in the traditional sense. It is a **framework**: a collection of tools, libraries, and conventions that massively simplifies the development of robot software.

Imagine building a robot. It has sensors (camera, lidar, GPS), actuators (motors, grippers), and needs software to coordinate everything. ROS provides:
- a standardized way for different software components to communicate with each other
- ready-made drivers for hundreds of sensors and motors
- tools for visualizing, debugging, and recording data
- a large community and many ready-to-use packages

**ROS2 Jazzy** is the current stable release (as of 2024/2025), optimized for Ubuntu 24.04.

### Installation

Installing ROS2 is normally a lengthy process with many manual steps. We use an installation script that handles everything automatically.

Open a terminal and run the following command (all on one line, or copy the block as-is):

```bash
curl -fsSL https://raw.githubusercontent.com/Merlin2LmmL/ROS2-Jazzy-Install-Script/refs/heads/main/ros2-jazzy-installer.sh \
  -o ros2-jazzy-installer.sh \
  && chmod +x ros2-jazzy-installer.sh \
  && ./ros2-jazzy-installer.sh
```

What this command does:
- `curl -fsSL ...` downloads the script
- `-o ros2-jazzy-installer.sh` saves it under this name
- `chmod +x` makes it executable (comparable to a `.exe` on Windows)
- `./ros2-jazzy-installer.sh` runs it

The installation takes 2–10 minutes depending on your internet speed and hardware.

### Setting Up the Workspace

After installation, we need a **workspace** – the main folder where all your ROS2 projects will live.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

The `~` is a shortcut for `/home/yourusername`. You can also name the workspace differently, e.g. `ros2_jazzy_ws`.

### Sourcing the Environment

ROS2 provides many commands and environment variables. For the terminal to recognize these, the ROS2 environment must be **sourced** (activated):

```bash
source /opt/ros/jazzy/setup.bash
```

> **Tip:** You need to repeat this in every new terminal window. To automate this, add this line to the `~/.bashrc` file (this file is executed automatically whenever a new terminal is opened):
> ```bash
> echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
> source ~/.bashrc
> ```

Test the installation with:
```bash
ros2 --help
# OR
echo $ROS_DISTRO
```
The first command should show you help for `ros2` commands, and the second should print something like `jazzy`.

---

## 3. First Steps with ROS2

### The Core Concept: Nodes, Topics, and Messages

ROS2 is built on a simple but powerful concept:

```
[Node A] -- publishes messages --> [Topic] -- receives messages --> [Node B]
```

- **Node:** A standalone program that performs a specific task (e.g. controlling a motor, processing camera images, making decisions)
- **Topic:** A named communication channel. Nodes can **publish** (send) to topics or **subscribe** (receive) from them. Think of it as a shared "chat" that different nodes can access.
- **Message:** The data format sent over a topic (e.g. a velocity, an image, a sensor value). Think of it as the language used in the chat.

#### Further Clarification:
The principle is similar to a bulletin board: anyone can pin notes (publish) and anyone can read notes (subscribe). The bulletin board itself is the topic.

### Useful ROS2 Commands

```bash
ros2 --help              # Show all available subcommands
ros2 node list           # Show all running nodes
ros2 topic list          # Show all active topics
ros2 topic echo /topic   # Display messages on a topic in real time
ros2 topic info /topic   # Show information about a topic
```

### Turtlesim – ROS2's "Hello World"

Turtlesim is a small demo program included with ROS2: a turtle on the screen that you can control via ROS2 topics. It is great for getting started.

You need **three terminal windows** at the same time:

**Terminal 1 – Start the simulation:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 – Start the controller:**
```bash
ros2 run turtlesim turtle_teleop_key
```
Click in Terminal 2 and steer the turtle with the arrow keys.

**Terminal 3 – See what's happening:**
```bash
ros2 topic list
```

You will see several topics, including `/turtle1/cmd_vel`. This is the channel over which movement commands are sent.

Now observe what is being sent when you steer the turtle:
```bash
ros2 topic echo /turtle1/cmd_vel
```

You will see output like this:
```
linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
```

This is a **Twist message** – the standard format for velocity commands in ROS2. `linear.x` is the forward motion, `angular.z` is the rotation. We will use this format ourselves shortly.

---

## 4. Creating a ROS2 Package

### What is a Package?

In ROS2, code is organized into **packages**. A package is a structured folder containing your code plus metadata (name, dependencies, license). Packages offer several advantages:
- Easy sharing and reuse
- Standardized structure
- Automatic dependency management
- `ros2 run` can easily find your nodes

### Creating a Package

First, navigate to the `src` folder of your workspace:
```bash
cd ~/ros2_ws/src
```

Then create your package. Replace the placeholders `<...>` with your own information:

```bash
ros2 pkg create <package_name> \
  --build-type ament_python \
  --dependencies rclpy geometry_msgs std_msgs \
  --license MIT \
  --maintainer-name "<Your Name>" \
  --maintainer-email "<your@email.com>" \
  --description "<Describe what your package does>" \
  --node-name <node_name>
```

**Example (use your own details):**
```bash
ros2 pkg create my_robot_package \
  --build-type ament_python \
  --dependencies rclpy geometry_msgs std_msgs \
  --license MIT \
  --maintainer-name "Jane Doe" \
  --maintainer-email "jane@example.com" \
  --description "My first ROS2 node that moves a robot." \
  --node-name motion_controller
```

> Package and node names should contain only lowercase letters, numbers, and underscores – no spaces, no special characters.

### Exploring the Package Structure

Navigate into your new package and inspect the structure:
```bash
cd ~/ros2_ws/src/<package_name>
ls -la
```

Directory trees can also be displayed directly using the `tree -L n` command, where `n` is the maximum depth:

```
<package_name>/
├── package.xml          <- Metadata (name, dependencies, license)
├── resource/
│   └── <package_name>   <- Marker file for ROS2
├── setup.cfg            <- Configuration for ros2 run
├── setup.py             <- Python installation instructions
└── <package_name>/
    ├── __init__.py      <- Makes the folder a Python package
    └── <node_name>.py   <- Your code goes here!
```

Open the node file and take a look:
```bash
nano <package_name>/<node_name>.py
```

There is already some boilerplate code in there. We will now replace the entire contents of this file.

---

## 5. Programming the Node

This is the heart of the tutorial. We will write a ROS2 node that executes a sequence of movement commands – like a small program telling the robot: "Drive forward for 2 seconds, turn, drive forward again, stop."

### What Should Our Node Do?

Before we start coding, let's plan briefly. Our node should:

1. Contain a list of movement instructions (e.g. "drive forward for 2 s, then turn for 1.5 s")
2. Accept the target topic via a configurable parameter
3. Execute the instructions one by one
4. Send messages to the configured topic
5. Stop at the end

### Key Concepts

#### Twist – The Message Format for Motion

A `Twist` message has two parts:
- `linear`: velocity in x (forward/backward), y (sideways), z (up/down) in meters per second
- `angular`: rotation rate around x (pitch), y (roll), z (yaw) in radians per second

For most ground robots, only `linear.x` (forward motion) and `angular.z` (rotation) are relevant:

```
linear.x  > 0  ->  forward
linear.x  < 0  ->  backward
angular.z > 0  ->  turn left (counter-clockwise)
angular.z < 0  ->  turn right (clockwise)
```

#### rclpy – The ROS2 Library for Python

`rclpy` is the official Python library for ROS2. You import it to initialize ROS2, create nodes, set up publishers, send messages, and use the logger.

Further reading:
- [rclpy API documentation](https://docs.ros2.org/latest/api/rclpy/)
- [ROS2 Python tutorial (official)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [geometry_msgs/Twist documentation](https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html)

#### ROS2 Parameters

In ROS2, nodes can declare **parameters** – settings that can be passed in from outside when the node starts, without changing the code. This is useful for things like the target topic.

A parameter is declared and read like this:
```python
self.declare_parameter("my_parameter", "default_value")
value = self.get_parameter("my_parameter").get_parameter_value().string_value
```

When starting the node, you pass the value with:
```bash
ros2 run <package> <node> --ros-args -p my_parameter:=value
```

---

### The Skeleton – Your Starting Point

Open the file:
```bash
nano ~/ros2_ws/src/<package_name>/<package_name>/<node_name>.py
```

Replace the entire contents with the following skeleton. It intentionally contains gaps (marked with `???`) that you should fill in step by step.

```python
#!/usr/bin/env python3
"""
Motion Controller – ROS2 Node
================================
Executes a sequence of motion instructions by publishing
messages to a configurable cmd_vel topic.
"""

import time
import sys

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


# =============================================================================
# TASK 1: Define motion instructions
# =============================================================================
#
# Each instruction is a dictionary with the following keys:
#
#   "action"     (str)   : Descriptive name – used only for log output
#   "linear_x"   (float) : Forward velocity in m/s (negative = backward)
#   "angular_z"  (float) : Rotation rate in rad/s (positive = left)
#   "duration"   (float) : How long this instruction is executed (in seconds)
#
# Note: The Turtlesim turtle uses values up to about 2.0 m/s.
# A real robot typically drives at 0.1 to 1.0 m/s depending on the model.
#
# Minimum requirement: Define at least 4 meaningful instructions.
#
INSTRUCTIONS = [
    # TODO: Add your own instructions here!
    {"action": "forward",  "linear_x": ???, "angular_z": ???, "duration": ???},
    {"action": "turn_left","linear_x": ???, "angular_z": ???, "duration": ???},
    {"action": "stop",     "linear_x": 0.0, "angular_z": 0.0, "duration": 0.5},
]


class MotionNode(Node):
    """
    ROS2 node that executes motion instructions sequentially.
    Inherits from rclpy.node.Node – this makes it a fully functional ROS2 node.
    """

    # How many messages per second should be sent? (frequency in Hz)
    PUBLISH_FREQUENCY = 10

    def __init__(self):
        # -----------------------------------------------------------------------
        # TASK 2: Name the node
        # -----------------------------------------------------------------------
        # The node needs a unique name. This name appears in `ros2 node list`.
        # Pass it to super().__init__().
        #
        # Documentation: https://docs.ros2.org/latest/api/rclpy/api/node.html
        #
        super().__init__("???")  # TODO: Give your node a meaningful name!

        self.get_logger().info(
            f"Node started. {len(INSTRUCTIONS)} instruction(s) loaded."
        )

        # -----------------------------------------------------------------------
        # TASK 3: Make the target topic configurable via a parameter
        # -----------------------------------------------------------------------
        # Different simulators and real robots use different topic names for
        # motion commands. To keep the node flexible, the topic should not be
        # hard-coded but passed in via a ROS2 parameter.
        #
        # Steps:
        #   1. Declare a parameter "cmd_vel_topic" with the default value
        #      "/cmd_vel" (used when nothing is passed in).
        #   2. Read the value of the parameter.
        #   3. Log the topic being used so the user can see it at startup.
        #
        # Syntax for declaring and reading a string parameter:
        #   self.declare_parameter("parameter_name", "default_value")
        #   value = self.get_parameter("parameter_name").get_parameter_value().string_value
        #
        # Documentation:
        #   https://docs.ros2.org/latest/api/rclpy/api/node.html#rclpy.node.Node.declare_parameter
        #
        self.declare_parameter("cmd_vel_topic", ???)       # TODO
        self._topic = self.get_parameter(???).get_parameter_value().string_value  # TODO
        self.get_logger().info(f"Using topic: {???}")      # TODO

        # -----------------------------------------------------------------------
        # TASK 4: Create the publisher
        # -----------------------------------------------------------------------
        # A publisher sends messages to a specific topic.
        # Use self._topic as the topic name (not the hard-coded string "/cmd_vel"),
        # so that the parameter from Task 3 is actually used.
        #
        # Syntax:
        #   self.create_publisher(<MessageType>, "<topic_name>", <queue_size>)
        #
        #   MessageType : Twist (from geometry_msgs.msg)
        #   topic_name  : self._topic
        #   queue_size  : 10
        #
        # Documentation:
        #   https://docs.ros2.org/latest/api/rclpy/api/node.html#rclpy.node.Node.create_publisher
        #
        self._publisher = self.create_publisher(???, ???, ???)  # TODO

        # Start execution 0.5 seconds after startup,
        # to allow the node to fully initialize.
        self._timer = self.create_timer(0.5, self._start_execution)

    # ---------------------------------------------------------------------------
    # TASK 5: Build a Twist message
    # ---------------------------------------------------------------------------
    def _build_twist(self, instruction: dict) -> Twist:
        """
        Converts an instruction dictionary into a Twist message.

        Args:
            instruction: Dictionary with keys such as "linear_x", "angular_z"

        Returns:
            A Twist message ready to be published
        """
        # A Twist message has the following fields:
        #
        #   msg.linear.x   (float)  <- Forward velocity
        #   msg.linear.y   (float)  <- Lateral velocity (usually 0)
        #   msg.linear.z   (float)  <- Vertical velocity (usually 0)
        #   msg.angular.x  (float)  <- Pitch rate (usually 0)
        #   msg.angular.y  (float)  <- Roll rate  (usually 0)
        #   msg.angular.z  (float)  <- Yaw rate (left/right rotation)
        #
        # Tip: Use .get("key", default_value) – if a key is missing from the
        # dictionary, the default value is used instead.
        # Example: instruction.get("linear_x", 0.0)
        #
        msg = Twist()
        msg.linear.x  = ???   # TODO
        msg.angular.z = ???   # TODO
        # All other fields remain 0.0 (default value for Twist)
        return msg

    # ---------------------------------------------------------------------------
    # TASK 6: Execute a single instruction
    # ---------------------------------------------------------------------------
    def _execute_instruction(self, index: int, instruction: dict) -> None:
        """
        Executes a single instruction for the specified duration.

        Args:
            index      : Position of the instruction in the list (for display)
            instruction: The instruction dictionary
        """
        # This function should:
        #   1. Read the values from the dictionary (action, duration, velocities)
        #   2. Log a message indicating which instruction is currently running
        #   3. Build the Twist message (use _build_twist!)
        #   4. Repeatedly publish the message for the given duration
        #
        # Tip for step 4 – timing loop:
        #   end_time  = time.time() + duration
        #   interval  = 1.0 / self.PUBLISH_FREQUENCY   # e.g. 0.1 s at 10 Hz
        #   while time.time() < end_time:
        #       self._publisher.publish(message)
        #       time.sleep(interval)
        #
        # Useful methods:
        #   self.get_logger().info("message")    <- Print to terminal
        #   self._publisher.publish(message)     <- Send a message
        #   time.sleep(seconds)                  <- Wait briefly
        #
        action   = instruction.get("action", f"step_{index}")
        duration = float(instruction["duration"])

        self.get_logger().info(???)   # TODO: e.g. "[1/5] 'forward' for 2.0s"

        twist = ???                   # TODO: Build Twist message

        # TODO: Publish the message in a loop for "duration" seconds
        # ...

    # ---------------------------------------------------------------------------
    # TASK 7: Send a stop command
    # ---------------------------------------------------------------------------
    def _send_stop(self) -> None:
        """
        Sends a stop command (all velocities set to zero).
        Without this command, a real robot will keep moving!
        """
        # An empty Twist message automatically has all fields set to 0.0.
        # Create such a message and publish it.
        #
        self._publisher.publish(???)  # TODO
        self.get_logger().info("Stop command sent (all velocities = 0).")

    # ---------------------------------------------------------------------------
    # TASK 8: Execute all instructions in sequence
    # ---------------------------------------------------------------------------
    def _start_execution(self) -> None:
        """
        Called once after the node starts.
        Executes all instructions in order.
        """
        self._timer.cancel()  # One-shot timer is no longer needed

        try:
            # Iterate over all instructions in INSTRUCTIONS and call
            # _execute_instruction() for each one.
            #
            # Tip: enumerate() gives you both the index and the value:
            #   for i, instruction in enumerate(INSTRUCTIONS):
            #       ...
            #
            # TODO: Loop over all instructions!

            self.get_logger().info("All instructions completed!")

        except KeyboardInterrupt:
            self.get_logger().info("Interrupted by user.")
        finally:
            # Always stop at the end – whether finished or interrupted!
            self._send_stop()
            rclpy.shutdown()


# =============================================================================
# Entry point – the program starts here
# =============================================================================

def main(args=None) -> None:
    """Initializes ROS2 and starts the node."""
    rclpy.init(args=args)
    node = MotionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

### Your Tasks – Overview

| No. | Task | What you need to do |
|-----|------|---------------------|
| 1 | Fill `INSTRUCTIONS` | Define at least 4 meaningful motion instructions |
| 2 | Name the node | `super().__init__("your_node_name")` |
| 3 | Set up the topic parameter | Declare, read, and log the parameter |
| 4 | Create the publisher | `self.create_publisher(Twist, self._topic, 10)` |
| 5 | Fill the Twist message | Set `linear.x` and `angular.z` from the dictionary |
| 6 | Execute an instruction | Log output, build Twist, timing loop |
| 7 | Send stop command | Publish an empty `Twist()` message |
| 8 | Iterate over all instructions | `for i, a in enumerate(INSTRUCTIONS):` |

---

### Helpful Code Snippets

If you get stuck on individual tasks, here are some building blocks for orientation – without direct solutions.

**Log message with position indicator:**
```python
self.get_logger().info(
    f"[{index + 1}/{len(INSTRUCTIONS)}] Executing '{action}' for {duration:.1f}s"
)
```

**Timing loop for repeated publishing:**
```python
end_time  = time.time() + duration
interval  = 1.0 / self.PUBLISH_FREQUENCY  # e.g. 0.1 s at 10 Hz

while time.time() < end_time:
    self._publisher.publish(message)
    time.sleep(interval)
```

**What `enumerate()` does:**
```python
fruits = ["Apple", "Banana", "Cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# Output:
# 0: Apple
# 1: Banana
# 2: Cherry
```

---

### Testing Early

You don't have to finish all tasks before testing. Once tasks 1–4 are done, you can build the package and use `ros2 topic echo /cmd_vel` to check whether your publisher is sending messages. A running simulator is not needed for this.

---

### Extension Ideas (Optional)

If you finish everything and want to explore further:

- **More detailed logging:** Print the remaining time inside the loop
- **Validation:** What happens if an instruction has no `duration` field? Handle it gracefully
- **JSON support:** See Chapter 8

---

## 6. Building the Package with Colcon

### What is Colcon?

**Colcon** is the build system used by ROS2. It installs your packages into a standardized directory structure so that `ros2 run` and other ROS2 tools can find your nodes.

Even though Python code does not actually get compiled, ROS2 still requires the build step:
- Symbolic links and configuration files are created
- Entry points are registered (so `ros2 run` can find your node)
- Dependencies are checked

### Always Build from the Workspace Root

> **Important:** Always run `colcon build` from the root directory of your workspace (`~/ros2_ws`), not from a subdirectory. Otherwise, the `build/`, `install/`, and `log/` folders will be created in the wrong location.

```bash
cd ~/ros2_ws
```

### Building the Package

When you later have multiple packages, it makes sense to build only the one you are currently working on. Use the `--packages-select` flag for this. Note that tab completion does not work for package names here:
```bash
colcon build --packages-select <package_name>
```

Or build everything:
```bash
colcon build
```

A successful output looks like this:
```
Starting >>> <package_name>
Finished <<< <package_name> [0.66s]

Summary: 1 package finished [0.77s]
```

Common errors:
- `SyntaxError`: Python syntax error – open the file and check the indicated line
- `ModuleNotFoundError`: A dependency is missing – check `package.xml` and `setup.py`
- `KeyError`: A dictionary key is missing – check your `INSTRUCTIONS`

### Sourcing the Environment After Building

After every build, the environment must be re-sourced so that ROS2 can find your newly built package:

```bash
source install/setup.bash
```

> Tip: You can automate this. Add this line to `~/.bashrc`:
> ```bash
> source ~/ros2_ws/install/setup.bash
> ```

---

## 7. Testing the Node – With a Real Simulator

### Simple Test: Is Your Node Publishing?

Open two terminal windows:

**Terminal 1 – Start the node:**
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run <package_name> <node_name>
```

**Terminal 2 – Monitor messages:**
```bash
ros2 topic echo /cmd_vel
```

If everything is correct, you will see messages like this in Terminal 2:
```yaml
linear:
  x: 0.3
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
```

---

### Installing the OHM Mecanum Simulator

The OHM Technische Hochschule Nürnberg has developed a 2D robot simulator that is well suited for our purposes due to its simplicity. We install it as an additional ROS2 package:

```bash
# 1. Download the source code
cd ~/ros2_ws/src
git clone --branch ros2 https://github.com/autonohm/ohm_mecanum_sim.git

# 2. Build the workspace
cd ~/ros2_ws
colcon build --symlink-install

# 3. Source the environment
source install/setup.bash

# 4. Install Pygame (the graphics framework used by the simulator)
pip3 install pygame --break-system-packages
```
> Note: The `--break-system-packages` flag sounds very dangerous, but in this case it really isn't. It was intentionally given a scary name to discourage casual use, since installing pip packages inside a virtual environment (venv) is strongly recommended. However, since setting up a venv would require one or two additional chapters, we fall back on a global installation here for the sake of time and simplicity. Anyone who objects is welcome to set up PyCharm with a venv instead.


### Finding the Right Topic

Start the simulator:
```bash
ros2 run ohm_mecanum_sim ohm_mecanum_sim_node
```

A window with the robot will open. Now let's find out which topic the simulator uses for motion commands:

```bash
ros2 topic list
```

Look through the list. Which topic contains `cmd_vel`? It is not simply `/cmd_vel`.

You can also get more information about a topic:
```bash
ros2 topic info /<topic_name>
```

---

### Putting It All Together

Once you know the correct topic, start everything in two (or three) terminals:

**Terminal 1 – Start the node with the correct topic:**
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run <package_name> <node_name> --ros-args \
  -p cmd_vel_topic:=/<the_correct_topic>
```

Since you implemented the `cmd_vel_topic` parameter in Task 3, you can now conveniently pass the target topic from the outside at startup – without touching the code.

**Terminal 2 – The simulator:**
```bash
ros2 run ohm_mecanum_sim ohm_mecanum_sim_node
```

**Terminal 3 (optional) – Monitor the topic:**
```bash
ros2 topic echo /<the_correct_topic>
```

If everything works, you will see the robot in the simulator window executing the movements from your `INSTRUCTIONS` list.

---

## 8. Bonus: JSON Command Files

So far, the instructions are hard-coded directly in the Python source. This is inconvenient: every time we want to change the route, we have to edit the code and rebuild.

A more elegant solution: store the instructions in a **JSON file** and pass it to the node.

### What is JSON?

JSON (*JavaScript Object Notation*) is a simple text format for structured data. It looks very similar to Python dictionaries:

```json
[
  {"action": "forward",   "linear_x": 0.3, "angular_z":  0.0, "duration": 2.0},
  {"action": "turn_left", "linear_x": 0.0, "angular_z":  0.5, "duration": 1.5},
  {"action": "forward",   "linear_x": 0.3, "angular_z":  0.0, "duration": 2.0},
  {"action": "stop",      "linear_x": 0.0, "angular_z":  0.0, "duration": 0.5}
]
```

Save this in a file, e.g. `~/my_route.json`.

### Loading JSON in Python

```python
import json

with open("/path/to/file.json", "r") as f:
    instructions = json.load(f)
```

`json.load()` automatically converts the JSON file into Python dictionaries – no extra work needed.

### Extension Task: Add JSON Support

Extend your node so that it either uses the built-in `INSTRUCTIONS` list, or loads a JSON file if a file path is provided.

Tip: Use a second ROS2 parameter:
```python
self.declare_parameter("instructions_file", "")
file_path = self.get_parameter("instructions_file").get_parameter_value().string_value

if file_path:
    # Load from JSON file
    with open(file_path, "r") as f:
        instructions = json.load(f)
else:
    # Use built-in instructions
    instructions = INSTRUCTIONS
```

Usage:
```bash
ros2 run <package_name> <node_name> --ros-args \
  -p cmd_vel_topic:=/<the_correct_topic> \
  -p instructions_file:=~/my_route.json
```

### Graphical Instruction Editor

So you don't have to write JSON by hand, a graphical editor is available:

**[Instruction Editor (Web App)](https://merlin2lmml.github.io/ros-motion-script-executor/)**

There you can visually compose your route and download it as a JSON file. The downloaded file will be found in `~/Downloads/`.

---

## Congratulations!

You have successfully:
- Learned to use the Linux terminal
- Installed ROS2 Jazzy
- Understood the core concepts of ROS2 (nodes, topics, messages)
- Created a ROS2 package
- Written your first ROS2 node with a configurable topic parameter
- Built and tested the package
- Controlled a robot simulator

This is a solid foundation for everything that comes next in robotics. Possible next steps:
- Receiving sensor data (subscribing to topics)
- Reacting to sensor data (e.g. stopping when an obstacle is detected)
- Running and coordinating multiple nodes simultaneously
- Writing ROS2 launch files

---

## Appendix: Common Problems and Solutions

### "ros2: command not found"
The ROS2 environment was not sourced:
```bash
source /opt/ros/jazzy/setup.bash
```

### "Package '<package_name>' not found"
The install environment was not sourced after the build:
```bash
cd ~/ros2_ws
source install/setup.bash
```

### The simulator starts, but the robot doesn't move
- Check whether the correct topic is being used (`ros2 topic list`)
- Check whether the node logs the topic correctly at startup
- Check whether your node is actually publishing (`ros2 topic echo /<topic>`)
- Check whether the node is running at all (`ros2 node list`)

### `colcon build` fails
- Make sure you are in the correct directory (`~/ros2_ws`)
- Check for Python syntax errors in your `.py` file
- The error message usually points to the exact line causing the problem

### The robot keeps moving after stopping
- Your `_send_stop()` call is missing or not working correctly
- Check that the `finally:` block is correctly indented

---

## Authorship

### ROS Introduction Repository — DBG-Robots

**Merlin Ortner**  
**Repository Owner & Principal Maintainer**  
Original Author of this repository and responsible for long-term maintenance, development, and stewardship.

Contact: ortnermerlin@gmail.com
