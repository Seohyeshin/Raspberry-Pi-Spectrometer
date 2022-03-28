import matplotlib.pyplot as plt

x=list(range(200,800,100))
y=[100, 400, 300, 500, 200, 70]
a=list(range(200, 800, 100))
b=[300, 400, 500, 650, 300, 300]
plt.plot(x, y)
plt.plot(a, b)

plt.show()