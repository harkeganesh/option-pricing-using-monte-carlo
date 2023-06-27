import numpy as np


def geometric_brownian_paths(S0: float, mu: float, sigma: float, N: int, dt: float, 
                             paths: int):
    drift = (mu - 0.5 * (sigma ** 2)) * dt

    diffusion = sigma * np.random.normal(0, np.sqrt(dt), size=(paths, N)).T

    asset_paths = np.exp(drift + diffusion)

    asset_paths = np.vstack((np.ones(paths), asset_paths))

    St = S0 * asset_paths.cumprod(axis=0)

    return St

