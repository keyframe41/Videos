import numpy as np
import pylab
from manim import *
import matplotlib.pyplot as plt

def Hbeta(D=np.array([]), beta=1.0):
    # Compute the perplexity and the P-row for a specific value of the
    # precision of a Gaussian distribution.
    P = np.exp(-D.copy() * beta)
    sumP = sum(P)
    H = np.log(sumP) + beta * np.sum(D * P) / sumP
    P = P / sumP
    return H, P


def x2p(X=np.array([]), tol=1e-5, perplexity=30.0):
    """
        Performs a binary search to get P-values in such a way that each
        conditional Gaussian has the same perplexity.
    """

    # Initialize some variables
    print("Computing pairwise distances...")
    (n, d) = X.shape
    sum_X = np.sum(np.square(X), 1)
    dist = np.add(np.add(-2 * np.dot(X, X.T), sum_X).T, sum_X)
    probs_p = np.zeros((n, n))
    beta = np.ones((n, 1))
    target_entropy = np.log(perplexity)

    # Loop over all datapoints
    for i in range(n):

        # Print progress
        if i % 500 == 0:
            print("Computing P-values for point %d of %d..." % (i, n))

        # Compute the Gaussian kernel and entropy for the current precision
        min = 0
        max = 10000
        dist_i = dist[i, np.concatenate((np.r_[0:i], np.r_[i + 1:n]))]
        (entropy, thisP) = Hbeta(dist_i, beta[i])

        # Evaluate whether the perplexity is within tolerance
        error = entropy - target_entropy
        tries = 0
        while np.abs(error) > tol and tries < 50:

            # If not, increase or decrease precision
            if error > 0:
                min = beta[i].copy()
                if max == np.inf or max == -np.inf:
                    beta[i] = beta[i] * 2.
                else:
                    beta[i] = (beta[i] + max) / 2.
            else:
                max = beta[i].copy()
                if min == np.inf or min == -np.inf:
                    beta[i] = beta[i] / 2.
                else:
                    beta[i] = (beta[i] + min) / 2.

            # Recompute the values
            (entropy, thisP) = Hbeta(dist_i, beta[i])
            error = entropy - target_entropy
            tries += 1

        # Set the final row of P
        probs_p[i, np.concatenate((np.r_[0:i], np.r_[i+1:n]))] = thisP
    # Return final P-matrix
    print("Mean value of sigma: %f" % np.mean(np.sqrt(1 / beta)))
    return probs_p


def pca(X=np.array([]), no_dims=50):
    """
        Runs PCA on the NxD array X in order to reduce its dimensionality to
        no_dims dimensions.
    """

    print("Preprocessing the data using PCA...")
    (n, d) = X.shape
    X = X - np.tile(np.mean(X, 0), (n, 1))
    (l, M) = np.linalg.eig(np.dot(X.T, X))
    Y = np.dot(X, M[:, 0:no_dims])
    return Y

class tSNE(Scene):
    def construct(self):
        X = np.loadtxt("mnist2500_X.txt")
        labels = np.loadtxt("mnist2500_labels.txt")
        no_dims = 2
        initial_dims = 50
        perplexity = 20.0

        # Initialize variables
        X = pca(X, initial_dims).real
        (n, d) = X.shape
        max_iter = 500
        initial_momentum = 0.5
        final_momentum = 0.8
        eta = 500
        min_gain = 0.01
        Y = np.random.randn(n, no_dims)
        dY = np.zeros((n, no_dims))
        iY = np.zeros((n, no_dims))
        gains = np.ones((n, no_dims))

        # Compute P-values
        probs_p = x2p(X, 1e-5, perplexity)
        probs_p = probs_p + np.transpose(probs_p)
        probs_p = probs_p / np.sum(probs_p)
        probs_p = probs_p * 4.  # early exaggeration
        probs_p = np.maximum(probs_p, 1e-12)

        # Run iterations
        for iter in range(max_iter):
            # self.clear()
            # cmap = plt.get_cmap('hsv')
            # dots = VGroup(
            #     *[Dot(point=(Y[i] / 25).tolist() + [0], color=ManimColor(cmap(labels[i] / 10)), radius=0.04)
            #       for i in range(2500)])
            # self.add(dots)
            # iteration_text = MathTex(r"\text{Iterations: }", str(iter)).to_corner(UL)
            # self.add(iteration_text)
            # self.wait(1 / config.frame_rate)

            # Compute pairwise affinities
            sum_Y = np.sum(np.square(Y), 1)
            num = -2. * np.dot(Y, Y.T)
            num = 1. / (1. + np.add(np.add(num, sum_Y).T, sum_Y))
            num[range(n), range(n)] = 0.
            probs_q = num / np.sum(num)
            probs_q = np.maximum(probs_q, 1e-12)

            # Compute gradient
            PQ = probs_p - probs_q
            for i in range(n):
                dY[i, :] = np.sum(np.tile(PQ[:, i] * num[:, i], (no_dims, 1)).T * (Y[i, :] - Y), 0)

            # Perform the update
            if iter < 20:
                momentum = initial_momentum
            else:
                momentum = final_momentum
            gains = (gains + 0.2) * ((dY > 0.) != (iY > 0.)) + \
                    (gains * 0.8) * ((dY > 0.) == (iY > 0.))
            gains[gains < min_gain] = min_gain
            iY = momentum * iY - eta * (gains * dY)
            Y = Y + iY
            Y = Y - np.tile(np.mean(Y, 0), (n, 1))

            # Compute current value of cost function
            if (iter + 1) % 10 == 0:
                C = np.sum(probs_p * np.log(probs_p / probs_q))
                print("Iteration %d: error is %f" % (iter + 1, C))

            # Stop lying about P-values
            if iter == 100:
                probs_p = probs_p / 4.
        cmap = plt.get_cmap('hsv')
        dots = VGroup(
            *[Dot(point=(Y[i] / 25).tolist() + [0], color=ManimColor(cmap(labels[i] / 10)), radius=0.04)
              for i in range(2500)])
        self.add(dots)