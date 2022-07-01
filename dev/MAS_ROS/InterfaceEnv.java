// Java environment code 

import jason.asSyntax.*;
import jason.environment.*;
import java.util.logging.*;
import ros.Publisher;
import ros.RosBridge;
import ros.RosListenDelegate;
import ros.SubscriptionRequestMsg;
import ros.msgs.std_msgs.PrimitiveMsg;
import ros.tools.MessageUnpacker;
import com.fasterxml.jackson.databind.JsonNode;

public class InterfaceEnv extends Environment {

    private Logger logger = Logger.getLogger("interface."+InterfaceEnv.class.getName());
    
    RosBridge bridge = new RosBridge();
	

    /** Called before the MAS execution with the args informed in .mas2j */
    @Override
    public void init(String[] args) {
        super.init(args);
		bridge.connect("ws://localhost:9090", true);
		logger.info("Environment started, connection with ROS established.");
		
		bridge.subscribe(SubscriptionRequestMsg.generate("/objLaserDetect")
				.setType("std_msgs/String")
				.setThrottleRate(1)
				.setQueueLength(1),
				
			new RosListenDelegate() {	// Interface to define the callback function when subscribing
				public void receive(JsonNode data, String stringRep) {	//Use stringrep for testing and debugging
					//MessageUnpacker<PrimitiveMsg<String>> unpacker = new MessageUnpacker<PrimitiveMsg<String>>(PrimitiveMsg.class);
					//PrimitiveMsg<String> msg = unpacker.unpackRosMessage(data);
					//double val = data.get("msg").get("data").asDouble();
					msgUnpacker("/objLaserDetect", data);
				}
			}
	);
	bridge.subscribe(SubscriptionRequestMsg.generate("/robotPose")
				.setType("nav_msgs/Odometry")
				.setThrottleRate(1)
				.setQueueLength(1),
				
			new RosListenDelegate() {
				public void receive(JsonNode data, String stringRep) {
					msgUnpacker("/robotPose", data);
				}
			}
	);
	bridge.subscribe(SubscriptionRequestMsg.generate("/visualDetect")
				.setType("std_msgs/Float32")
				.setThrottleRate(1)
				.setQueueLength(1),
				
			new RosListenDelegate() {
				public void receive(JsonNode data, String stringRep) {
					msgUnpacker("/visualDetect", data);
				}
			}
	);
	clearAllPercepts();
    }
	
	/** Unpack the recieved JsonNode and extract the relevant data */
	public boolean msgUnpacker(String topic, JsonNode data){
		try{
			if(topic.equals("/objLaserDetect")){
				MessageUnpacker<PrimitiveMsg<String>> unpacker = new MessageUnpacker<PrimitiveMsg<String>>(PrimitiveMsg.class);
				PrimitiveMsg<String> msg = unpacker.unpackRosMessage(data);
				msgToPercept("null", msg.data);
			}
			else if(topic.equals("/robotPose")){
				//double val = data.get("msg").get("data").asDouble();
				double xval = data.get("msg").get("pose").get("pose").get("position").get("x").asDouble();
				double yval = data.get("msg").get("pose").get("pose").get("position").get("y").asDouble();
				logger.info("Robot position at - X:" + xval + " Y:" + yval);
			}
			else if(topic.equals("/visualDetect")){
				double val = data.get("msg").get("data").asDouble();
				logger.info("Flag point detected with contour area: " + val);
			}
			return true;
		} catch (Exception e){
			logger.info(e.toString());
			return false;
		}
	}
	
	/** Convert incoming messages from ROS into percepts for agents */
	public void msgToPercept(String robot, String data){
		if (data.equals("front_object_robot1")){
			logger.info("Robot 1 - Object detected in front");
			addPercept("robot1", Literal.parseLiteral("frontObject"));
		}
		else if (data.equals("front_object_robot2")){
			logger.info("Robot 2 - Object detected in front");
			addPercept("robot2", Literal.parseLiteral("frontObject"));
		}
		else if (data.equals("front_object_robot3")){
			logger.info("Robot 3 - Object detected in front");
			addPercept("robot3", Literal.parseLiteral("frontObject"));
		}
		else if (data.equals("front_object_robot4")){
			logger.info("Robot 4 - Object detected in front");
			addPercept("robot4", Literal.parseLiteral("frontObject"));
		}
	}

	/** Necessary function implementing execution of agent actions and behaviour */
    @Override
    public boolean executeAction(String agName, Structure action) {
		logger.info("check");
		if (agName.equals("robot1") && action.getFunctor().equals("turn_away")) {
			msgToRos(agName, "turn_away");
			logger.info("Robot 1 is turning away");
		}
		else if (agName.equals("robot2") && action.getFunctor().equals("turn_away")) {
			msgToRos(agName, "turn_away");
			logger.info("Robot 2 is turning away");
		}
		else if (agName.equals("robot3") && action.getFunctor().equals("turn_away")) {
			msgToRos(agName, "turn_away");
			logger.info("Robot 3 is turning away");
		}
		else if (agName.equals("robot4") && action.getFunctor().equals("turn_away")) {
			msgToRos(agName, "turn_away");
			logger.info("Robot 4 is turning away");
		}
		else {
			logger.info("executing: "+action+", but not implemented!");
		}
        informAgsEnvironmentChanged();
        return true; // the action was executed with success
    }
    
	/** Publish information to relevant ROS topics */
	public void msgToRos(String robot, String msg) {
		String topic = "/java_to_ros";
		topic += "/";
		topic += robot;
		Publisher pub = new Publisher(topic, "std_msgs/String", bridge);
		pub.publish(new PrimitiveMsg<String>(msg));
		try {
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

    /** Called before the end of MAS execution */
    @Override
    public void stop() {
        super.stop();
    }
}
