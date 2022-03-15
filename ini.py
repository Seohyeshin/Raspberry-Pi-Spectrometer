import matplotlib.pyplot as plt

x = list(range(200,800,100))
y = [100, 20, 300, 50, 500, 300]
plt.plot(x, y)
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
#import pyautogui
#pyautogui.screenshot('test1.png')
