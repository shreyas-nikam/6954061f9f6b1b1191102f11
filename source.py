import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
def simulate_brownian_motion(T, N_steps, N_paths):
    """
    Simulates multiple paths of a Standard Brownian Motion.

    Parameters:
    T (float): Total time horizon.
    N_steps (int): Number of time steps.
    N_paths (int): Number of sample paths to simulate.

    Returns:
    tuple: A tuple containing:
        - time_points (np.ndarray): Array of time points.
        - Wt_paths (np.ndarray): 2D array where each row is a sample path of Wt.
    """
    dt = T / N_steps
    time_points = np.linspace(0, T, N_steps + 1)
    
    # Generate random increments
    # Each row is a path, each column is a time step's increment
    dW = np.random.normal(loc=0.0, scale=np.sqrt(dt), size=(N_paths, N_steps))
    
    # Cumulative sum of increments to get Wt
    # Initialize W0 = 0 for all paths
    Wt_paths = np.zeros((N_paths, N_steps + 1))
    Wt_paths[:, 1:] = np.cumsum(dW, axis=1)
    
    return time_points, Wt_paths

# Simulation parameters
T = 1.0        # Total time horizon (e.g., 1 year)
N_steps = 252  # Number of time steps (e.g., trading days in a year)
N_paths = 1000 # Number of sample paths

# Simulate Brownian Motion
time_points_bm, Wt_paths_bm = simulate_brownian_motion(T, N_steps, N_paths)

# Plotting a few sample paths for visualization
plt.figure(figsize=(12, 6))
for i in range(min(10, N_paths)): # Plot up to 10 paths
    plt.plot(time_points_bm, Wt_paths_bm[i], lw=0.8)
plt.title(f'Simulated Sample Paths of Standard Brownian Motion (W$_t$)')
plt.xlabel('Time (t)')
plt.ylabel('W$_t$')
plt.grid(True)
plt.show()
def verify_martingale_property(time_points, process_paths, process_name):
    """
    Visualizes the martingale property by plotting multiple sample paths
    and their average. For a martingale, the average path should remain constant
    (or flat if starting from a non-zero constant expectation).

    Parameters:
    time_points (np.ndarray): Array of time points.
    process_paths (np.ndarray): 2D array where each row is a sample path of the process.
    process_name (str): Name of the stochastic process for plot title.
    """
    plt.figure(figsize=(12, 6))
    
    # Plot individual sample paths
    for i in range(min(10, process_paths.shape[0])): # Plot up to 10 paths
        plt.plot(time_points, process_paths[i], lw=0.8, alpha=0.6)
        
    # Plot the average path
    average_path = np.mean(process_paths, axis=0)
    plt.plot(time_points, average_path, color='red', linestyle='--', linewidth=2, label='Average Path')
    
    plt.title(f'Simulated Paths and Average of {process_name}')
    plt.xlabel('Time (t)')
    plt.ylabel(f'{process_name} Value')
    plt.axhline(y=average_path[0], color='gray', linestyle=':', label='Initial Expected Value') # For martingales, this should be flat
    plt.legend()
    plt.grid(True)
    plt.show()

# Verify Wt as a martingale
verify_martingale_property(time_points_bm, Wt_paths_bm, 'Standard Brownian Motion ($W_t$)')
def generate_squared_brownian_motion_martingale(Wt_paths, time_points):
    """
    Generates paths for the process X_t = W_t^2 - t.

    Parameters:
    Wt_paths (np.ndarray): 2D array of simulated Wt paths.
    time_points (np.ndarray): Array of time points.

    Returns:
    np.ndarray: 2D array where each row is a sample path of X_t = W_t^2 - t.
    """
    Wt_squared_minus_t_paths = Wt_paths**2 - time_points
    return Wt_squared_minus_t_paths

# Generate paths for Wt^2 - t
Wt_squared_minus_t_paths = generate_squared_brownian_motion_martingale(Wt_paths_bm, time_points_bm)

# Verify Wt^2 - t as a martingale
verify_martingale_property(time_points_bm, Wt_squared_minus_t_paths, '($W_t^2 - t$)')
def generate_exponential_martingale(Wt_paths, time_points, theta):
    """
    Generates paths for the exponential martingale M_t = exp(theta * W_t - 0.5 * theta^2 * t).

    Parameters:
    Wt_paths (np.ndarray): 2D array of simulated Wt paths.
    time_points (np.ndarray): Array of time points.
    theta (float): Parameter for the exponential martingale.

    Returns:
    np.ndarray: 2D array where each row is a sample path of the exponential martingale.
    """
    exponential_martingale_paths = np.exp(theta * Wt_paths - 0.5 * theta**2 * time_points)
    return exponential_martingale_paths

# Define parameter theta
theta_param = 0.5 

# Generate paths for the exponential martingale
exponential_martingale_paths = generate_exponential_martingale(Wt_paths_bm, time_points_bm, theta_param)

# Verify the exponential martingale
verify_martingale_property(time_points_bm, exponential_martingale_paths, 
                           f'Exponential Martingale ($e^{{{theta_param}W_t - 0.5 \cdot {theta_param}^2 t}}$)')