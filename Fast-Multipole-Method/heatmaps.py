import numpy as np
import matplotlib.pyplot as plt
np.seterr(all='ignore')

def plot_multipoles():
    x = np.linspace(-4, 4, 800)
    y = np.linspace(4, -4, 800)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    coords = [[-0.1, -0.4], [-0.2, -0.8], [-0.3, -0.2], [-0.4, -0.6], [-0.5, -0.9],
                  [-0.6, -0.5], [-0.7, -0.7], [-0.8, -0.3], [-0.9, -0.6], [-3.7, -3.8]]
    points = [coords[i][0] + 1j * coords[i][1] for i in range(len(coords))]
    z_c = np.mean(points)
    # z_c = -2 - 2j
    cluster = np.sum([np.log(np.abs(Z - points[i])) for i in range(len(points))], axis=0)

    Z_mul = Z.copy()
    Z_mul[np.abs(Z_mul - z_c) < 0.05] = np.nan

    coeff_mul = [-np.sum([(point - z_c) ** k for point in points]) / k for k in range(1, 11)]
    print(coeff_mul)
    multipole = (10 * np.log(np.abs(Z_mul - z_c)) +
                 np.sum([(coeff_mul[k - 1] * ((Z_mul - z_c) ** -k)).real for k in range(1, 11)], axis=0))

    Z_tay = Z.copy()
    z_c_tay = 1 + 0.5j

    b_0 = np.sum([np.log(np.abs(point - z_c_tay)) for point in points])
    coeff_tay = [-np.sum([(point - z_c_tay) ** -k for point in points]) / k for k in range(1, 11)]
    taylor = b_0 + np.sum([(coeff_tay[k - 1] * ((Z_tay - z_c_tay) ** k)).real for k in range(1, 11)], axis=0)

    fig, axes = plt.subplots(2, 2, figsize=(12, 12), dpi=100)
    titles = ["Cluster potential", "Cluster potential", "Multipole expansion", "Taylor expansion"]
    data = [cluster, cluster, multipole, taylor]

    max_dist = np.max([np.abs(z_c - point) for point in points])
    min_dist = np.min([np.abs(z_c_tay - point) for point in points])

    for i, ax in enumerate(axes.flat):
        im = ax.imshow(data[i], extent=[-4, 4, -4, 4], cmap='RdBu_r', vmin=-2, vmax=2)
        ax.set_title(titles[i], fontsize=12, fontweight='bold')
        ax.set_xticks([-4, -2, 0, 2, 4])
        ax.set_yticks([-4, -2, 0, 2, 4])
        ax.set_xlabel("Re(z)", fontsize=12)
        ax.set_ylabel("Im(z)", fontsize=12)

        points_x = [p.real for p in points]
        points_y = [p.imag for p in points]
        ax.scatter(points_x, points_y, color='white', edgecolor='black', marker='o', s=60, zorder=5,
                   label='Sources ($z_i$)')

        if i % 2 == 0:
            ax.scatter(z_c.real, z_c.imag, color='gold', edgecolor='black', marker='X', s=200, zorder=5,
                       label='Multipole center ($z_c$)')
            ax.legend(loc='upper left', fontsize=8)
            circle = plt.Circle((z_c.real, z_c.imag), max_dist, color='black', fill=False, linestyle='--',alpha=0.3)

        else:
            ax.scatter(z_c_tay.real, z_c_tay.imag, color='gold', edgecolor='black', marker='X', s=200, zorder=5,
                       label='Taylor center ($z_c$)')
            ax.legend(loc='upper left', fontsize=8)
            circle = plt.Circle((z_c_tay.real, z_c_tay.imag), min_dist, color='black', fill=False, linestyle='--', alpha=0.3)

        ax.add_artist(circle)

    plt.tight_layout()
    plt.savefig("heatmap.png")
    plt.show()


if __name__ == "__main__":
    plot_multipoles()

# import numpy as np
# import matplotlib.pyplot as plt
#
# # 1. Create a 2D spatial grid representing the complex plane
# x = np.linspace(-2, 2, 500)
# y = np.linspace(-2, 2, 500)
# X, Y = np.meshgrid(x, y)
# Z = X + 1j * Y
#
# # 2. Mask the origin to avoid singularities (divide-by-zero) blowing up our colormap
# mask = np.abs(Z) < 0.1
# Z_masked = np.copy(Z)
# Z_masked[mask] = np.nan + 1j * np.nan
#
# # 3. Calculate the multipole terms
# # (These are the real parts of the Taylor series terms of the complex potential)
# monopole = np.log(np.abs(Z_masked))  # Total Mass (Barnes-Hut equivalent)
# dipole = np.real(1 / Z_masked)  # Asymmetry / Offset
# quadrupole = np.real(1 / Z_masked ** 2)  # Stretching / Variance
# octupole = np.real(1 / Z_masked ** 3)  # Higher-order shape
#
# # 4. Set up the figure and axes for a 2x2 grid
# fig, axes = plt.subplots(2, 2, figsize=(10, 10))
# plt.subplots_adjust(hspace=0.2, wspace=0.2)
#
# # Group the data for easy looping
# terms = [
#     (monopole, "Monopole ($Re(\log z)$)", axes[0, 0]),
#     (dipole, "Dipole ($Re(z^{-1})$)", axes[0, 1]),
#     (quadrupole, "Quadrupole ($Re(z^{-2})$)", axes[1, 0]),
#     (octupole, "Octupole ($Re(z^{-3})$)", axes[1, 1])
# ]
#
# # 5. Plot each term
# for data, title, ax in terms:
#     if "Monopole" in title:
#         # The monopole potential scales radially, so we use a sequential colormap
#         cmap = 'magma'
#         vmin, vmax = np.nanmin(data), np.nanmax(data)
#     else:
#         # Higher-order poles push and pull in different directions,
#         # so we use a diverging colormap centered at zero.
#         cmap = 'RdBu_r'
#         # We cap the color limits using percentiles so the singularity doesn't wash out the plot
#         limit = np.nanpercentile(np.abs(data), 92)
#         vmin, vmax = -limit, limit
#
#     # Draw the heatmap
#     heatmap = ax.pcolormesh(X, Y, data, cmap=cmap, vmin=vmin, vmax=vmax, shading='auto')
#
#     # Formatting
#     ax.set_title(title, fontsize=16, pad=10)
#     ax.set_aspect('equal')
#     ax.axis('off')  # Turn off axes for a cleaner mathematical look
#
#     # Add a colorbar to each subplot
#     fig.colorbar(heatmap, ax=ax, fraction=0.046, pad=0.04)
#
# # Main title
# plt.suptitle("2D Complex Multipole Expansions", fontsize=22, y=0.96)
# plt.show()

    '''
    a_coeff = [10, np.complex128(2.5000000000000004 - 2.220446049250313e-16j),
                 np.complex128(-0.3124999999999995 + 1.1102230246251565e-16j),
                 np.complex128(0.05208333333333315 - 2.9605947323337506e-16j),
                 np.complex128(-0.009765624999999334 - 7.4593109467002705e-16j),
                 np.complex128(0.001953125000000133 + 8.43769498715119e-16j),
                 np.complex128(-0.00040690104166794805 - 7.401486830834376e-16j),
                 np.complex128(8.719308035801517e-05 + 2.220446049250313e-16j),
                 np.complex128(-1.907348633076178e-05 - 1.3079815008865125e-15j),
                 np.complex128(4.2385525195815565e-06 + 1.8010284621696983e-15j),
                 np.complex128(-9.3132266998291 + 8.970602038971266e-15j),
                 np.complex128(23.28306458213112 - 3.1590891518879456e-14j),
                 np.complex128(-32.01421355207761 + 5.2120345076881826e-14j),
                 np.complex128(32.0142135138695 - 6.02424093515835e-14j),
                 np.complex128(-26.011548473366652 + 5.2307364788768086e-14j),
                 np.complex128(18.208083930114885 - 2.7948014273230606e-14j)]
    zs = [(1 + 0j),
    (0.7612712429686843 + 0.7347315653655915j),
    (0.13627124296868431 + 1.1888206453689418j),
    (-0.6362712429686842 + 1.188820645368942j),
    (-1.261271242968684 + 0.7347315653655916j),
    (-1.5 + 1.5308084989341916e-16j),
    (-1.2612712429686843 - 0.7347315653655913j),
    (-0.6362712429686844 - 1.1888206453689418j),
    (0.13627124296868404 - 1.188820645368942j),
    (0.7612712429686841 - 0.7347315653655917j),]

    def get_truncated(p):
        def evaluate(z):
            res = a_coeff[0] * np.log(z)
            for k in range(1, p + 1):
                res += a_coeff[k] * z ** -k
            return np.real(res)

        return evaluate

    monopole = get_truncated(8)(Z)
    # Term 1: Dipole (1/z^1)
    dipole = get_truncated(9)(Z)

    # Term 2: Quadrupole (1/z^2)
    quadrupole = get_truncated(10)(Z)

    # Term 3: Tripole/Octupole (1/z^3)
    tripole = get_truncated(11)(Z)
    '''