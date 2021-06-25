from node import Node

# class to simulate nodes transmitting across bus using csma/cd
class CSMA_CD:
    def __init__(self, num_nodes, arrival_rate, lan_speed, packet_length, node_distance, propagation_speed, max_simulation_time):
        # keep track of total transmitted packets and packets that are successfully transmitted
        # a transmitted packet would be unsuccessful if it collided with another packet
        self.num_transmitted_packets = 0
        self.num_successful_transmitted_packets = 0
        self.curr_time = 0
        self.max_simulation_time = max_simulation_time
        
        self.num_nodes = num_nodes
        self.arrival_rate = arrival_rate
        self.lan_speed = lan_speed
        self.packet_length = packet_length
        self.node_distance = node_distance
        self.propagation_speed = propagation_speed

        self.nodes = self.build_nodes(num_nodes, arrival_rate, 10, 1000, lan_speed)

    # build all nodes (with arrival queues) and return as a list
    def build_nodes(self, num_nodes, arrival_rate, max_collisions, max_simulation_time, lan_speed):
        node_list = []

        for location in range(num_nodes):
            node_list.append(Node(location * self.node_distance, arrival_rate, max_collisions, max_simulation_time, lan_speed))

        return node_list

    # get the node with the packet that is currently leaving
    # will return none if no node has a leaving packet
    def get_node_with_leaving_packet(self):
        leaving_node = None
        min_arrival = float('inf')

        for node in self.nodes:
            if node.queue and node.queue[0] < min_arrival:
                leaving_node = node
                min_arrival = node.queue[0]

        return leaving_node
    # run simulation for csma/cd
    def simulate(self):
        while self.curr_time < self.max_simulation_time:

            # get the node with the currently leaving packet
            node_with_leaving_packet = self.get_node_with_leaving_packet()

            # no nodes with a leaving packet means all packets have left, end simulation
            if node_with_leaving_packet is None:
                break

            # update the current time and transmitted packets
            self.curr_time = node_with_leaving_packet.queue[0]
            self.num_transmitted_packets += 1

            
            collision_occurred = False
            # check for collisions between other nodes
            for node in self.nodes:
                if node.queue and node != node_with_leaving_packet:
                    internodal_distance = abs(node.location - node_with_leaving_packet.location)
                    
                    if internodal_distance == 0:
                        print('Error, no distance between nodes')
                        return

                    propagation_time = internodal_distance / self.propagation_speed
                    transmission_time = self.packet_length / self.lan_speed


                    curr_node_will_collide = False

                    # first bit will arrive while current node is attemping to transmit
                    # result is a collision
                    if node.queue[0] <= self.curr_time + propagation_time:
                        curr_node_will_collide = True

                    # check to see if the current node will detect that the bus is busy
                    # if node can detect a busy bus, it will wait until the bus is free
                    # update all packets in the node queue that were supposed to transmit while the bus is detected as busy
                    if node.queue[0] > (self.curr_time + propagation_time) and node.queue[0] < (self.curr_time + propagation_time + transmission_time):
                        for i in range(len(node.queue)):
                            if node.queue[i] > (self.curr_time + propagation_time) and node.queue[i] < (self.curr_time + propagation_time + transmission_time):
                                node.queue[i] = self.curr_time + propagation_time + transmission_time
                            else:
                                break

                    # if the current node packet will collide, we need to service the collision
                    # count the collision transmission
                    if curr_node_will_collide:
                        node.service_collision_transmission()
                        self.num_transmitted_packets += 1
                        collision_occurred = True


            # service the collision of the node with the leaving packet
            if collision_occurred:
                node_with_leaving_packet.service_collision_transmission()
            else:
                node_with_leaving_packet.pop_packet_and_reset_collisions()
                self.num_successful_transmitted_packets += 1

    # calculate and print results of the simulation
    def print_results(self):
        total_dropped_packets = 0

        for node in self.nodes:
            total_dropped_packets += node.num_dropped_packets

        efficiency = self.num_successful_transmitted_packets / self.num_transmitted_packets
        throughput = (self.packet_length * self.num_successful_transmitted_packets) / (self.lan_speed * self.curr_time)
        
        print('\n#######################\n')
        print('Simulation with ', self.num_nodes, ' nodes')
        print('Arrival rate of ', self.arrival_rate, ' packets per second\n')
        print('successful transmissions: ', self.num_successful_transmitted_packets)
        print('total transmissions: ', self.num_transmitted_packets)


        print('number of dropped packets: ', total_dropped_packets)
        print('Efficiency: ', efficiency)
        print('Throughtput: ', throughput, ' Mbps')

