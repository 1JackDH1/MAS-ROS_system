# MAS-ROS System

Combination of multi-agent systems and ROS for application of agent architecture into simulated robotic systems. Agents can communicate to and from ROS topics through a Java-based interface, built utilising resources from the [Jason-ROSbridge](https://github.com/rafaelcaue/jason-rosbridge) and [Java-ROSbridge](https://github.com/h2r/java_rosbridge) libraries.

Basis for agent architecture is a BDI agent-oriented logical programming language, AgentSpeak. Though here it's written using [Jason](https://github.com/jason-lang/jason) - an interpreter for an extended version of AgentSpeak. All robot system components are written in Python, using the ROS Noetic distribution.

The Waffle Pi [TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/) platform robots were used in this project.



DEPRECATED - I believe it would be more appropriate to learn the ROS2 architecture than continue here. This project now serves more as a reference for future projects. Given the updates with Jason-ROSbridge, it would be much better to start this project over.
