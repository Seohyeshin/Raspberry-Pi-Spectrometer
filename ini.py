#별도의 과정 없이 그냥 같이 쓰면 그래프가 합쳐져서 나옴
import matplotlib.pyplot as plt

x = [300, 400, 500, 600]
y = [100, 20, 300, 50]
a = list(range(200,800,100))
b = [100, 20, 300, 50, 500, 300]

plt.plot(x, y)
plt.plot(a, b)

n = len(y) - 2
Y = []
X = []
for i in range(n) :
    j= i+1
    if y[j] != 0:
        if (y[j]-y[j-1]) > 0 and (y[j]-y[j+1]) >0:
            Y.append(y[j])
            X.append(x[j])


plt.scatter(X,Y)

plt.savefig('graph.jpg')
plt.show()




