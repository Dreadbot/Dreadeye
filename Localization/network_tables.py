import ntcore
from poseclass import Position

def start_network_table():
    inst = ntcore.NetworkTableInstance.getDefault()
    table = inst.getTable("azathoth")
    inst.startClient4("visionclient")
    inst.setServerTeam(3656)
    positionPub = table.getStructArrayTopic("visionPos", Position).publish(
	ntcore.PubSubOptions(sendAll=True, keepDuplicates=True)
    )
    latencyPub = table.getDoubleTopic("visionLatency").publish(
	ntcore.PubSubOptions(sendAll=True, keepDuplicates=True)
    )
    tagSeenPub = table.getBooleanTopic("tagSeen").publish()
    return tagSeenPub, latencyPub, positionPub, inst
