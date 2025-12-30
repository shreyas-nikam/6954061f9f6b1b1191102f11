id: 6954061f9f6b1b1191102f11_documentation
summary: Stochastic calculus Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Stochastic Calculus for Quant Analysts

## 1. Introduction to Martingales and Risk-Neutral Valuation
Duration: 0:10:00

<aside class="positive">
This step provides the essential context for why martingales and risk-neutral valuation are foundational concepts for any Quantitative Analyst. Understanding these principles ensures that financial models are theoretically sound and arbitrage-free.
</aside>

### Application's Importance and Context

Welcome to QuLab: Stochastic Calculus, a Streamlit application designed to demystify complex concepts in quantitative finance. This codelab will guide you through the application's functionalities, focusing on the crucial roles of **Martingale Properties** and **Risk-Neutral Valuation** in financial modeling.

Imagine you are **Aisha**, a Quantitative Analyst at **Global Financial Solutions**, a leading investment bank. Your daily tasks involve developing, validating, and ensuring the theoretical soundness of complex financial models for pricing derivatives and managing market risk. Today, your specific mission is to perform a foundational review: to conceptually verify and illustrate the martingale property and its indispensable role in risk-neutral valuation. This is paramount for guaranteeing the firm's derivatives pricing models are arbitrage-free and theoretically consistent.

This application is built to provide a hands-on, interactive way to grasp these concepts through simulation and visualization.

### What You Will Learn

By the end of this codelab, you will:
*   Understand the definition and properties of a Standard Brownian Motion ($W_t$).
*   Empirically verify the martingale property for various stochastic processes:
    *   Standard Brownian Motion ($W_t$)
    *   Squared Brownian Motion Minus Time ($W_t^2 - t$)
    *   Exponential Martingale ($\exp(\theta W_t - \theta^2 t/2)$)
*   Grasp the conceptual connection between martingales and risk-neutral valuation.
*   Understand the Fundamental Theorem of Asset Pricing (FTAP) and its implications for arbitrage-free pricing.

### Application Architecture Overview

The Streamlit application provides an interactive interface with a sidebar for navigation and parameter control, and a main content area for explanations and visualizations.

```
++
|             Streamlit App             |
++
| Sidebar                 | Main Content |
|                         |              |
| ++ | +-+ |
| | Navigation          | | | Page 1   | |
| | - Introduction      | | | Content  | |
| | - Brownian Motion   | | |          | |
| | ...                 | | | Plots    | |
| ++ | +-+ |
| | Simulation Params   | |              |
| | - T, N_steps, N_paths| | +-+ |
| | (active for relevant | | | Page 2   | |
| |  pages)             | | | Content  | |
| ++ | |          | |
| | Exp Martingale Param| | | Plots    | |
| | - θ (active for Exp | | +-+ |
| |  Martingale page)   | |              |
| ++ |    ...       |
|                         |              |
++
```

The application uses `numpy` for numerical simulations and `matplotlib` for plotting, integrated seamlessly with Streamlit's interactive widgets. Key simulation parameters (Total Time Horizon $T$, Number of Time Steps $N\_steps$, Number of Sample Paths $N\_paths$) are controlled from the sidebar and persist across relevant pages via Streamlit's session state. This allows you to generate a set of Standard Brownian Motion paths once and reuse them for verifying other martingale properties.

The core Python code utilizes helper functions (assumed to be in `source.py`) to generate and plot the stochastic processes:
```python
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from source import * # simulate_brownian_motion, generate_squared_brownian_motion_martingale, generate_exponential_martingale, verify_martingale_property

# Page Configuration
st.set_page_config(page_title="QuLab: Stochastic calculus", layout="wide")

# ... (Sidebar and Session State Initialization) ...

# Helper Function for Plotting
def plot_wrapper(plot_func, *args, **kwargs):
    plt.clf()  # Clear any existing plot to ensure a fresh canvas
    plot_func(*args, **kwargs)
    st.pyplot(plt.gcf())  # Display the current matplotlib figure

# ... (Page-specific logic) ...
```
This structure ensures that plots are always fresh and reflect the current simulation parameters.

## 2. Simulating Standard Brownian Motion ($W_t$)
Duration: 0:12:00

### Understanding Standard Brownian Motion

Aisha's first step is to simulate Standard Brownian Motion, $W_t$, which is a cornerstone process in continuous-time finance. It models the random, unpredictable component of asset price movements. A stochastic process $W_t$ is a Standard Brownian Motion (or Wiener process) if it satisfies the following properties:

1.  **Initial Value:** $W_0 = 0$.
2.  **Continuous Paths:** It has continuous sample paths.
3.  **Independent and Stationary Increments:** For any $0 \leq t_1 < t_2 < ... < t_n$, the increments $W_{t_2}-W_{t_1}, W_{t_3}-W_{t_2}, ..., W_{t_n}-W_{t_{n-1}}$ are independent. Also, the distribution of $W_{t+s}-W_t$ depends only on $s$, not on $t$.
4.  **Normally Distributed Increments:** For $s > 0$, $W_{t+s}-W_t \sim N(0,s)$, meaning the increments are normally distributed with mean 0 and variance $s$.
5.  **Distribution:** $W_t \sim N(0,t)$, a normal distribution with mean 0 and variance $t$.

This implies that the change in Brownian motion over a small time step $\Delta t$, denoted as $\Delta W_t = W_{t+\Delta t} - W_t$, is normally distributed with mean 0 and variance $\Delta t$, i.e., $\Delta W_t \sim N(0, \Delta t)$.

### Interactive Simulation

Navigate to the **"1. Standard Brownian Motion (W_t)"** page in the sidebar.

<aside class="positive">
Experiment with the sidebar parameters to observe how the simulated paths change. Increasing the number of paths (N_paths) will give a clearer picture of the process's average behavior, while increasing N_steps will make individual paths smoother.
</aside>

In the sidebar, you will find the following **Simulation Parameters**:
*   **Total Time Horizon (T):** The total time duration for the simulation, from $0$ to $T$.
*   **Number of Time Steps (N_steps):** The number of discrete steps used to approximate the continuous process. A larger number results in finer granularity.
*   **Number of Sample Paths (N_paths):** The count of individual Brownian Motion trajectories to simulate.

When you adjust these parameters, the application calls the `simulate_brownian_motion` function (from `source.py`) and updates the plot:

```python
# From the Streamlit app's main logic
st.session_state.time_points_bm, st.session_state.Wt_paths_bm = simulate_brownian_motion(
    st.session_state.T, st.session_state.N_steps, st.session_state.N_paths
)
# ...
plot_wrapper(simulate_brownian_motion, st.session_state.T, st.session_state.N_steps, st.session_state.N_paths)
```

The plot shows multiple simulated paths of $W_t$. Each path is a continuous, random trajectory starting from zero, visually confirming the core characteristics of a Brownian Motion.

### Verifying the Martingale Property for $W_t$

The concept of a **martingale** is central to arbitrage-free pricing. A stochastic process $X_t$ is a martingale with respect to a filtration $\mathcal{F}_t$ (representing the available information up to time $t$) and a probability measure $P$ if it satisfies three conditions:

1.  **Integrability:** $E[|X_t|] < \infty$ for all $t \geq 0$. This means the expected absolute value of the process at any time is finite.
2.  **Adaptedness:** $X_t$ is $\mathcal{F}_t$-adapted. This means that at any time $t$, the value of $X_t$ is known given the information up to time $t$.
3.  **Conditional Expectation:** For any $t, s \geq 0$, the conditional expectation satisfies:
    $$E[X_{t+s} | \mathcal{F}_t] = X_t$$
    This is the defining property: the best prediction of a future value of the process ($X_{t+s}$), given all current information ($\mathcal{F}_t$), is simply its current value ($X_t$).

For Standard Brownian Motion, $W_t$, starting at $W_0=0$, its martingale property means that $E[W_{t+s} | \mathcal{F}_t] = W_t$. This holds true because the increments $W_{t+s} - W_t$ are independent of $\mathcal{F}_t$ and have an expected value of 0.

The application verifies this property by plotting the average of all simulated paths along with the individual paths.
```python
# From the Streamlit app's main logic
plot_wrapper(verify_martingale_property, st.session_state.time_points_bm, st.session_state.Wt_paths_bm, 'Standard Brownian Motion ($W_t$)')
```
You will observe that while individual paths wander randomly, the average of a large number of simulated paths remains centered around zero (its initial value). This visually confirms that $W_t$ is a martingale. This understanding is foundational for arbitrage-free modeling.

## 3. Verifying the Martingale Property: Case 2 - Squared Brownian Motion Minus Time ($W_t^2 - t$)
Duration: 0:08:00

### Another Key Martingale

Aisha now investigates another important martingale derived from Brownian Motion: $X_t = W_t^2 - t$. This process is significant as it arises from Itô's Lemma, a fundamental tool in stochastic calculus, and plays a role in understanding quadratic variation. Its martingale property reinforces the idea that certain transformations of Brownian motion also maintain this crucial characteristic.

The martingale property for $X_t = W_t^2 - t$ implies:
$$E[X_{t+s} | \mathcal{F}_t] = X_t$$
Substituting $X_t$:
$$E[W_{t+s}^2 - (t+s) | \mathcal{F}_t] = W_t^2 - t$$
This property shows that the expected future value of $W_t^2 - t$, conditioned on current information, is its current value.

### Interactive Verification

Navigate to the **"2. Squared Brownian Motion Minus Time (W_t^2 - t)"** page in the sidebar.

<aside class="negative">
If you haven't yet simulated Standard Brownian Motion, the application will prompt you to do so. The simulation parameters for $W_t$ in the sidebar must be set first.
</aside>

The application leverages the previously simulated $W_t$ paths to generate the $W_t^2 - t$ paths:
```python
# From the Streamlit app's main logic
if st.session_state.Wt_squared_minus_t_paths is None:
    st.session_state.Wt_squared_minus_t_paths = generate_squared_brownian_motion_martingale(
        st.session_state.Wt_paths_bm, st.session_state.time_points_bm
    )
    st.rerun() # Forces a re-run to display the generated paths

# ...
plot_wrapper(verify_martingale_property, st.session_state.time_points_bm, st.session_state.Wt_squared_minus_t_paths, '($W_t^2 - t$)')
```
Observe the plot: similar to $W_t$, the average path of $W_t^2 - t$ remains constant over time. This confirms that $W_t^2 - t$ is also a martingale. This insight is crucial for Aisha when analyzing stochastic differential equations and the quadratic variation of processes used in advanced models, ensuring their consistency with fundamental arbitrage-free principles.

## 4. Verifying the Martingale Property: Case 3 - Exponential Martingale ($exp(\theta W_t - \theta^2 t/2)$)
Duration: 0:10:00

### The Exponential Martingale

Aisha now explores the **exponential martingale**, a particularly vital class of martingales in financial mathematics. This form appears frequently in areas like change of probability measure (Girsanov's Theorem), which is central to risk-neutral valuation and constructing equivalent martingale measures.

The general form of the exponential martingale is:
$$M_t = \exp\left(\theta W_t - \frac{1}{2}\theta^2 t\right)$$
where $M_t$ is the exponential martingale process, $W_t$ is Standard Brownian Motion, and $\theta$ is a constant parameter.

Its martingale property states:
$$E[M_{t+s} | \mathcal{F}_t] = M_t$$
Substituting $M_t$:
$$E\left[\exp\left(\theta W_{t+s} - \frac{1}{2}\theta^2 (t+s)\right) \Big| \mathcal{F}_t\right] = \exp\left(\theta W_t - \frac{1}{2}\theta^2 t\right)$$
This process is also known as Novikov's condition for guaranteeing that a stochastic exponential is a true martingale, provided $\theta$ is a constant.

### Interactive Verification with Parameter $\theta$

Navigate to the **"3. Exponential Martingale"** page in the sidebar.

<aside class="positive">
The `theta` parameter allows you to explore how changing this constant affects the individual paths of the exponential martingale while still maintaining its overall martingale property on average.
</aside>

In addition to the global simulation parameters, you'll find a specific parameter for this page:
*   **Parameter $\theta$:** A constant that influences the paths of the exponential martingale. You can adjust its value using the number input slider.

The application calculates and plots the exponential martingale paths using the previously generated $W_t$ paths and your chosen $\theta$:
```python
# From the Streamlit app's main logic
# ... (theta parameter input) ...
if st.session_state.exponential_martingale_paths is None or theta_changed:
    st.session_state.exponential_martingale_paths = generate_exponential_martingale(
        st.session_state.Wt_paths_bm, st.session_state.time_points_bm, st.session_state.theta_param
    )
    if theta_changed: st.rerun() # Reruns if theta parameter is changed

# ...
plot_wrapper(verify_martingale_property, st.session_state.time_points_bm, st.session_state.exponential_martingale_paths,
             f'Exponential Martingale ($e^{{{st.session_state.theta_param}W_t - 0.5 \\cdot {st.session_state.theta_param}^2 t}}$)')
```
You'll observe that the average path of the exponential martingale remains constant, starting from its initial value of 1 (since $W_0=0$ implies $e^0=1$). This successfully verifies its martingale property. This specific martingale is crucial for Aisha's understanding of how probability measures can be changed in derivatives pricing, allowing complex pricing problems to be solved under a simplified risk-neutral framework.

## 5. Connecting to Risk-Neutral Valuation and the Fundamental Theorem of Asset Pricing
Duration: 0:15:00

### Risk-Neutral Valuation: The Cornerstone of Pricing

Having empirically verified several key martingales, Aisha now focuses on the conceptual connection between martingales and the fundamental principle of **risk-neutral valuation**. This understanding is the theoretical bedrock of all arbitrage-free pricing models at Global Financial Solutions.

Aisha's core responsibility includes ensuring the models used for pricing options and other derivatives are robust and arbitrage-free. The martingale property is central to this. Under a **risk-neutral probability measure $\mathbb{Q}$**, the *discounted* price of any tradable asset (or any derivative thereon) must be a martingale. If this were not true, arbitrage opportunities would exist, which contradicts efficient market hypotheses.

Consider a financial asset $S_t$ and a constant risk-free interest rate $r$. The discounted asset price is:
$$S_t^* = e^{-rt} S_t$$
where $S_t^*$ is the discounted asset price at time $t$, $S_t$ is the asset price, and $r$ is the risk-free rate.

For arbitrage-free markets, under the risk-neutral measure $\mathbb{Q}$, this discounted process must be a martingale:
$$E^{\mathbb{Q}}[S_{t+s}^* | \mathcal{F}_t] = S_t^*$$
where $E^{\mathbb{Q}}$ is the expectation under the risk-neutral measure, $S_t^*$ is the discounted asset price at time $t$, and $\mathcal{F}_t$ is the information available at time $t$.

This implies that the expected future discounted price, given current information, is the current discounted price. This allows Aisha to price derivatives by taking the expected value of their future payoffs under this risk-neutral measure. For a European option with payoff $Payoff(S_T)$ at maturity $T$, its value at time $t$ is given by:
$$V_t = E^{\mathbb{Q}}[e^{-r(T-t)} Payoff(S_T) | \mathcal{F}_t]$$
where $V_t$ is the option value at time $t$, $r$ is the risk-free rate, $T$ is maturity, and $Payoff(S_T)$ is the option payoff at maturity based on asset price $S_T$.

This formula means that the fair value of a derivative today is the discounted expected value of its future payoff, where the expectation is taken under the risk-neutral measure. This is the bedrock of Aisha's daily pricing work. Her conceptual review confirms that the martingale property is not merely a mathematical curiosity but a direct consequence of the no-arbitrage principle in financial markets.

### The Fundamental Theorem of Asset Pricing (FTAP)

To complete her foundational review, Aisha synthesizes her understanding of martingales and risk-neutral valuation with the **Fundamental Theorem of Asset Pricing (FTAP)**. This theorem provides the formal justification for why the martingale approach is valid for arbitrage-free pricing.

The Fundamental Theorem of Asset Pricing is a cornerstone of mathematical finance that directly links the absence of arbitrage opportunities to the existence of risk-neutral measures. For Aisha, this theorem provides the rigorous theoretical backing for the pricing models she employs, ensuring their validity and consistency.

The theorem is typically presented in two parts:

1.  **First Fundamental Theorem of Asset Pricing:** An arbitrage-free market exists if and only if there exists at least one equivalent martingale measure (EMM) $\mathbb{Q}$ under which all discounted asset prices are martingales. In simpler terms, if a market allows for no free lunch (no arbitrage), then we can find a risk-neutral probability measure that makes discounted asset prices behave like martingales.

2.  **Second Fundamental Theorem of Asset Pricing:** A market is complete (meaning every contingent claim can be perfectly replicated by a self-financing trading strategy) if and only if there exists a *unique* equivalent martingale measure $\mathbb{Q}$. If Global Financial Solutions operates in a complete market (e.g., the Black-Scholes world), Aisha knows that there is only one correct way to price derivatives via risk-neutral expectation.

These theorems formally explain *why* Aisha performs her martingale verifications and uses risk-neutral valuation. They establish the conditions under which these pricing techniques are applicable and unique.

Aisha concludes her review, affirming that the martingale property is not just an arbitrary condition but a profound implication of market efficiency. The Fundamental Theorem of Asset Pricing explicitly connects the absence of arbitrage—a non-negotiable principle for Global Financial Solutions—to the existence and, under completeness, uniqueness of the risk-neutral measure. This theoretical underpinning gives Aisha the confidence that her firm's sophisticated derivatives pricing models are built on solid mathematical ground, enabling accurate valuation and responsible risk management. This foundational review solidifies her ability to scrutinize, apply, and explain complex models with clarity and precision.
