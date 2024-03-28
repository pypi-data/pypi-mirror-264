"""This is a simple demo program"""

from eduworld.robot import setup, shutdown, up, down, left, right, put

setup(world="demo-world", delay=0.05)

up()
left()
for _ in range(20):
    put()
down()
right()

shutdown()
