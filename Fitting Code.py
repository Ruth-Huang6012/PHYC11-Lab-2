import numpy as np, matplotlib.pyplot as plt, scipy.optimize as scipy, math

##Access files and load decay times
file = open("Feb17th.data", 'r')
lines = file.readlines()
file.close()
correct = []
for l in lines:
    index = l.find(' ')
    if int(l[0:index])<40000:
        correct.append(int(l[0:index]))

##Process data and bin
m = max(correct)
correct2 = np.array(correct) - 500
correct_2 = []
for i in correct2:
    if i >0:
        correct_2.append(i)

n, bins, patches = plt.hist(correct_2, bins=m//1000)

##Exponential function for fitting
def lifetime(x, a, b):
    return b*np.exp(-a*(x))


new_bins = []
for i in range(1, len(bins)):
    new_bins.append((bins[i]+bins[i-1])//2)


def fit(new_bins, n):
    ##Fit exponential function to decay time distribution
    popt, pcov = scipy.curve_fit(lifetime, new_bins[:], n[:], [0.0005, 300])
    lt1 = 1/popt[0]
    ##Estimate background noise
    background = []
    for i, value in enumerate(new_bins):
        if value > lt1*5:
            background.append(n[i])
    constant = int(np.mean(background))
    ##Subtract background noise from distribution 
    new_n = []
    for i in n:
        if i-constant > 0:
            new_n.append(i-constant)
        else:
            new_n.append(0)
    return [new_n, popt]

new_n, popt1 = fit(new_bins[:], fit(new_bins[:], fit(new_bins[:],n[:])[0])[0])
new_n2, popt2 = fit(new_bins, new_n)

##Plot decay time distribution
plt.hist(bins[:-1], bins[:], weights=new_n)

#Plot fitted curve
l_fine = np.linspace(0, int(m+1), 100)
plt.plot(l_fine, lifetime(l_fine, popt2[0], popt2[1]), label = "y = "+str(popt2[1])[:6]+"e^(-"+str(popt2[0])[:8]+"x)")
plt.title("Muon Decay Time Distribution - Feb 17th") 
plt.xlabel("Decay Time (ns)")
plt.ylabel("Number of Muons")
plt.legend()
plt.show()
