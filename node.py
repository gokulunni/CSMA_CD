import collections
from random import random, randint
from math import log as natural_log


class Node:
    # data needed for a node
    def __init__(self, location, arrival_rate, max_collisions, max_simulation_time, lan_speed=1000000):
        # locations are numbered to define spacing between them
        self.location = location
        self.arrival_rate = arrival_rate
        # maximum collisions before a packet is dropped
        self.max_collisions = max_collisions
        self.max_simulation_time = max_simulation_time
        self.num_collisions = 0
        self.lan_speed = lan_speed
        # packet queue
        self.queue = self.generate_queue()
        self.num_dropped_packets = 0

    # generate a random variable
    def generate_random_variable(self, mean):
        return -mean * natural_log(1 - random())

    # generate the arrival queue
    def generate_queue(self):
        curr_time = 0

        deck = collections.deque()

        while curr_time < self.max_simulation_time:
            # the mean is 1 / rate of arrival
            curr_time += self.generate_random_variable(1 / self.arrival_rate)
            deck.append(curr_time)

        return deck

    # generate the backoff time after a collision
    def get_backoff_time(self, lan_speed, num_collisions):
        k = randint(0, (2**num_collisions)-1)
        return k * 512 / lan_speed

    # when popping the front packet, always reset the number of collisions
    def pop_packet_and_reset_collisions(self):
        if not self.queue:
            print('Error, Queue is empty cannot pop packet')
            return

        self.num_collisions = 0
        self.queue.popleft()


    # service a packet transmission that results in a collision
    # drop packet if too many collisions
    # calculate the backoff time and update remaining queued packets
    def service_collision_transmission(self):
        self.num_collisions += 1

        # too many collisions, drop the packet and reset collision counter
        if self.num_collisions > self.max_collisions:
            self.num_dropped_packets += 1
            self.pop_packet_and_reset_collisions()

        # get the new waiting time and update packets in queue that were originally suppposed to leave before the waiting time
        else:
            backoff_time = self.get_backoff_time(self.lan_speed, self.num_collisions)
            new_waiting_time = self.queue[0] + backoff_time

            for i in range(len(self.queue)):
                if self.queue[i] < new_waiting_time:
                    self.queue[i] = new_waiting_time
                else:
                    break




