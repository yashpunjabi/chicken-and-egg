import matplotlib.pyplot as plt

time = list(range(30))

chickens = [0] * 30

plt.axis([0, 40, 0, 40])
plt.ion()

for i in range(30):
    chickens[i] = i
    plt.plot(time, chickens)
    plt.pause(0.05)

while True:
    plt.pause(0.05)
