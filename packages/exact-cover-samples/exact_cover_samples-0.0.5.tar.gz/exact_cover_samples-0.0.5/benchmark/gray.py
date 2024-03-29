def g(n):
    if n == 0:
        return ['0', '1']
    else:
        prev = g(n-1)
        return ['0'+x for x in prev] + list(reversed(['1'+x for x in prev]))

def pict(n):
    gi = [int(x, base=2) for x in g(n)]
    N = 2**(n+1)
    a = np.zeros(shape=(N, N))
    for i, j in enumerate(gi):
        a[i, j] = 1
    plt.figure()
    plt.imshow(a)
    plt.show()
