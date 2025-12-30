
# Streamlit Application Specification: Martingale Properties and Risk-Neutral Valuation

## 1. Application Overview

### Purpose of the Application

This Streamlit application serves as a comprehensive tool for Quantitative Analysts to conceptually verify and illustrate the martingale property, its application in various stochastic processes, and its fundamental role in risk-neutral valuation and arbitrage-free derivatives pricing. It aims to solidify understanding of these core financial mathematics concepts through interactive simulations and integrated textual explanations, presented within a practical workflow context.

### High-Level Story Flow of the Application

The application guides Aisha, a Quantitative Analyst, through a structured workflow:

1.  **Introduction**: Aisha begins by understanding the case study, her persona, and the importance of martingales in her role at Global Financial Solutions.
2.  **Standard Brownian Motion ($W_t$)**: She starts by simulating Standard Brownian Motion, observing its characteristics, and then visually verifying its martingale property by examining the average path of numerous simulations.
3.  **Squared Brownian Motion Minus Time ($W_t^2 - t$)**: Next, Aisha explores a more complex process, $W_t^2 - t$, generating its paths based on the previously simulated Brownian Motion and confirming its martingale nature through similar visualization.
4.  **Exponential Martingale**: She then investigates the exponential martingale, crucial for change of measure, simulating its paths and verifying its martingale property, adjusting a key parameter ($\theta$).
5.  **Risk-Neutral Valuation & Fundamental Theorem of Asset Pricing**: Finally, Aisha connects these empirical observations to the theoretical foundations of risk-neutral valuation and the Fundamental Theorem of Asset Pricing, understanding how martingales underpin arbitrage-free derivatives pricing, thereby completing her foundational review.

The application allows Aisha to adjust simulation parameters (time horizon, number of steps, number of paths, and specific process parameters) for each section, fostering an interactive and customizable learning experience.

## 2. Code Requirements

### Import Statement

The application will begin by importing necessary libraries and all functions from `source.py`:

```python
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from source.py import *
```

### `st.session_state` Design

`st.session_state` will be extensively used to maintain the application's state across user interactions and page navigations, ensuring that simulation results and parameters persist.

**Initialization**: All keys will be initialized when the application starts if they don't already exist.

```python
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Introduction'
if 'T' not in st.session_state:
    st.session_state.T = 1.0
if 'N_steps' not in st.session_state:
    st.session_state.N_steps = 252
if 'N_paths' not in st.session_state:
    st.session_state.N_paths = 100 # Reduced for quicker initial load/interaction
if 'theta_param' not in st.session_state:
    st.session_state.theta_param = 0.5
if 'Wt_paths_bm' not in st.session_state:
    st.session_state.Wt_paths_bm = None
if 'time_points_bm' not in st.session_state:
    st.session_state.time_points_bm = None
if 'Wt_squared_minus_t_paths' not in st.session_state:
    st.session_state.Wt_squared_minus_t_paths = None
if 'exponential_martingale_paths' not in st.session_state:
    st.session_state.exponential_martingale_paths = None
```

**Update and Read**:

*   `st.session_state.current_page`: Updated by the sidebar radio button to control conditional page rendering. A `st.rerun()` is triggered upon page change.
*   `st.session_state.T`, `st.session_state.N_steps`, `st.session_state.N_paths`: Updated by sidebar sliders. Changes to these parameters will trigger a re-simulation of the base Brownian Motion and invalidate derived processes, prompting a `st.rerun()`.
*   `st.session_state.theta_param`: Updated by a sidebar number input. Changes will trigger a re-calculation of the exponential martingale paths and a `st.rerun()`.
*   `st.session_state.Wt_paths_bm`, `st.session_state.time_points_bm`: Updated after calling `simulate_brownian_motion` when parameters change or if data is initially `None`.
*   `st.session_state.Wt_squared_minus_t_paths`: Updated by calling `generate_squared_brownian_motion_martingale` on demand if `Wt_paths_bm` exists and the derived paths are `None` or invalidated.
*   `st.session_state.exponential_martingale_paths`: Updated by calling `generate_exponential_martingale` on demand if `Wt_paths_bm` exists and the derived paths are `None` or invalidated (e.g., `theta_param` changes).

### Application Structure and Flow

The application uses a sidebar for navigation to simulate a multi-page experience.

```python
st.title("Martingale Properties and Risk-Neutral Valuation: A Quant Analyst's Workflow")

def plot_wrapper(plot_func, *args, **kwargs):
    plt.clf() # Clear any existing plot to ensure a fresh canvas
    plot_func(*args, **kwargs)
    st.pyplot(plt.gcf()) # Display the current matplotlib figure

st.sidebar.title("Navigation")
page_selection = st.sidebar.radio(
    "Go to:",
    [
        'Introduction',
        '1. Standard Brownian Motion (W_t)',
        '2. Squared Brownian Motion Minus Time (W_t^2 - t)',
        '3. Exponential Martingale',
        '4. Risk-Neutral Valuation & FTAP'
    ],
    key='page_radio'
)

if page_selection != st.session_state.current_page:
    st.session_state.current_page = page_selection
    st.rerun()

if st.session_state.current_page in ['1. Standard Brownian Motion (W_t)',
                                    '2. Squared Brownian Motion Minus Time (W_t^2 - t)',
                                    '3. Exponential Martingale']:
    st.sidebar.header("Simulation Parameters")
    new_T = st.sidebar.slider('Total Time Horizon (T)', min_value=0.1, max_value=5.0, value=st.session_state.T, step=0.1, key='T_slider')
    new_N_steps = st.sidebar.slider('Number of Time Steps', min_value=50, max_value=500, value=st.session_state.N_steps, step=10, key='N_steps_slider')
    new_N_paths = st.sidebar.slider('Number of Sample Paths', min_value=10, max_value=1000, value=st.session_state.N_paths, step=10, key='N_paths_slider')

    params_changed = False
    if new_T != st.session_state.T:
        st.session_state.T = new_T
        params_changed = True
    if new_N_steps != st.session_state.N_steps:
        st.session_state.N_steps = new_N_steps
        params_changed = True
    if new_N_paths != st.session_state.N_paths:
        st.session_state.N_paths = new_N_paths
        params_changed = True

    # Re-run simulation only if parameters changed or paths are not yet generated
    if params_changed or st.session_state.Wt_paths_bm is None:
        st.session_state.time_points_bm, st.session_state.Wt_paths_bm = simulate_brownian_motion(
            st.session_state.T, st.session_state.N_steps, st.session_state.N_paths
        )
        # Invalidate other derived paths to force recalculation if Wt changes
        st.session_state.Wt_squared_minus_t_paths = None
        st.session_state.exponential_martingale_paths = None
        st.rerun()

if st.session_state.current_page == 'Introduction':
    # Markdown Cell: Martingale Properties and Risk-Neutral Valuation: A Quant Analyst's Workflow
    st.markdown(f"# Martingale Properties and Risk-Neutral Valuation: A Quant Analyst's Workflow")
    st.markdown(f"## Introduction to the Case Study")
    st.markdown(f"**Persona:** Aisha, a dedicated Quantitative Analyst at Global Financial Solutions.")
    st.markdown(f"**Organization:** Global Financial Solutions, a leading investment bank known for its sophisticated derivatives trading desk.")
    st.markdown(f"Aisha's role is critical in developing, validating, and ensuring the theoretical soundness of complex financial models used for pricing derivatives and managing market risk. Today, her task is to perform a foundational review: to conceptually verify and illustrate the martingale property and its indispensable role in risk-neutral valuation. This is not just an academic exercise; a robust understanding of these concepts is paramount for guaranteeing that the firm's derivatives pricing models are arbitrage-free and theoretically consistent, directly impacting trading strategies and risk assessments. She needs to ensure that the underlying mathematical frameworks are fully grasped and can be explained to colleagues, solidifying the analytical bedrock for all pricing activities.")
    st.markdown(f"This application will guide Aisha through a series of conceptual verifications and simulations, demonstrating how various stochastic processes exhibit the martingale property and how this connects to the core principles of arbitrage-free pricing.")

    # Markdown Cell: 1. Setting Up the Environment
    st.markdown(f"## 1. Setting Up the Environment")

    # 1.a. Markdown Cell
    st.markdown(f"Before diving into the core analysis, Aisha ensures all required tools are in place. This is a standard first step in any quantitative project, guaranteeing that the computational framework is ready for simulating stochastic processes and plotting results.")
    st.info("Note: The environment setup (installing libraries) is handled automatically when the application starts. Required libraries are imported below.")

    # Code Cell: Imports (handled at the top of app.py blueprint)
    st.code("import numpy as np\nimport matplotlib.pyplot as plt\nimport scipy.stats as stats\nfrom source.py import *", language="python")

# --- PAGE: 1. Standard Brownian Motion (W_t) ---
if st.session_state.current_page == '1. Standard Brownian Motion (W_t)':
    st.markdown(f"## 2. Simulating Standard Brownian Motion")

    # 2.a. Markdown Cell
    st.markdown(f"The Standard Brownian Motion, also known as a Wiener process, is foundational in continuous-time financial modeling. It represents the random, unpredictable component of asset price movements. Aisha needs to simulate its paths to visually grasp its characteristics, such as continuous paths, starting at zero, and random fluctuations. A stochastic process $W_t$ is a Standard Brownian Motion if:")
    st.markdown(f"1.  $W_0 = 0$")
    st.markdown(f"2.  It has continuous sample paths.")
    st.markdown(f"3.  It has independent, stationary increments.")
    st.markdown(r"4.  $$W_t \sim N(0,t)$$")
    st.markdown(r"where $W_t$ is the value of the Brownian motion at time $t$, $N(0,t)$ denotes a normal distribution with mean 0 and variance $t$.")
    st.markdown(r"The increments $$\Delta W_t = W_{t+\Delta t} - W_t$$ are independent and normally distributed with mean 0 and variance $$\Delta t$$, i.e., $$\Delta W_t \sim N(0, \Delta t)$$.")
    st.markdown(r"where $\Delta W_t$ is the increment of the Brownian motion over a small time step $\Delta t$.")

    # Simulation and first plot (sample paths)
    st.markdown(f"### Simulated Paths of Standard Brownian Motion ($W_t$)")
    if st.session_state.Wt_paths_bm is not None:
        plot_wrapper(simulate_brownian_motion, st.session_state.T, st.session_state.N_steps, st.session_state.N_paths)
    else:
        st.info("Adjust parameters in the sidebar to generate data for simulation.")

    # 2.c. Markdown cell (explanation of execution) for the first plot
    st.markdown(f"Aisha observes the simulated paths of Brownian Motion. Each path shows a continuous, random trajectory starting from zero. This visual representation helps her confirm the core characteristics of $W_t$, which is essential for understanding more advanced stochastic processes that are built upon it. This simulation provides the raw data for her subsequent martingale verifications.")

    st.markdown(f"## 3. Verifying the Martingale Property: Case 1 - Standard Brownian Motion ($W_t$)")
    # 3.a. Markdown Cell
    st.markdown(f"For a Quant Analyst, understanding martingales is crucial because discounted asset prices are martingales under the risk-neutral measure, a cornerstone of arbitrage-free pricing. Aisha needs to visually and conceptually confirm this property for $W_t$.")
    st.markdown(f"A stochastic process $X_t$ is a martingale with respect to a filtration $\mathcal{{F}}_t$ and probability measure $P$ if it satisfies three conditions:")
    st.markdown(r"1.  $$E[|X_t|] < \infty$$ for all $$t \geq 0$$ (integrability).")
    st.markdown(r"where $E[|X_t|]$ is the expected absolute value of $X_t$.")
    st.markdown(f"2.  $X_t$ is $\mathcal{F}_t$-adapted (knowable at time $t$).")
    st.markdown(r"where $\mathcal{F}_t$ represents the information available up to time $t$.")
    st.markdown(f"3.  For any $t, s \geq 0$, the conditional expectation satisfies:")
    st.markdown(r"    $$E[X_{t+s} | \mathcal{F}_t] = X_t$$")
    st.markdown(r"where $E[X_{t+s} | \mathcal{F}_t]$ is the expected value of $X$ at time $t+s$ conditioned on information up to time $t$.")
    st.markdown(f"This means the best prediction of a future value of the process, given current information, is simply its current value. For $W_t$, we use the property that $W_{t+s} - W_t$ is independent of $\mathcal{{F}}_t$ and has an expectation of 0.")

    # Martingale verification plot (average path)
    st.markdown(f"### Martingale Property Verification for Standard Brownian Motion ($W_t$)")
    if st.session_state.Wt_paths_bm is not None:
        plot_wrapper(verify_martingale_property, st.session_state.time_points_bm, st.session_state.Wt_paths_bm, 'Standard Brownian Motion ($W_t$)')
    else:
        st.warning("Please adjust simulation parameters in the sidebar to generate data.")

    # 3.c. Markdown cell (explanation of execution) for the second plot
    st.markdown(f"Aisha observes that while individual paths of $W_t$ wander randomly, the average of a large number of simulated paths remains centered around zero (its initial value). This visually confirms the martingale property for $W_t$: the expected future value, given the current information, is indeed the current value (which is 0 for $W_t$ starting at $W_0=0$). This verification reinforces her understanding of its fundamental nature in arbitrage-free modeling.")

if st.session_state.current_page == '2. Squared Brownian Motion Minus Time (W_t^2 - t)':
    st.markdown(f"## 4. Verifying the Martingale Property: Case 2 - Squared Brownian Motion Minus Time ($W_t^2 - t$)")

    # 4.a. Markdown Cell
    st.markdown(f"Understanding that certain transformations of Brownian Motion can also be martingales is crucial for Aisha. The process $W_t^2 - t$ is an example derived from Itô's Lemma. Its martingale property implies that its expected future value, given current information, is simply its current value. This property helps a Quant Analyst understand the behavior of quadratic variation and its implications for continuous processes. The martingale property for $X_t = W_t^2 - t$ implies:")
    st.markdown(r"$$E[X_{t+s} | \mathcal{F}_t] = X_t$$")
    st.markdown(r"where $E[X_{t+s} | \mathcal{F}_t]$ is the expected value of $X$ at time $t+s$ conditioned on information up to time $t$.")
    st.markdown(r"$$E[W_{t+s}^2 - (t+s) | \mathcal{F}_t] = W_t^2 - t$$")
    st.markdown(r"where $W_t$ is Standard Brownian Motion.")

    if st.session_state.Wt_paths_bm is not None:
        if st.session_state.Wt_squared_minus_t_paths is None:
            st.session_state.Wt_squared_minus_t_paths = generate_squared_brownian_motion_martingale(
                st.session_state.Wt_paths_bm, st.session_state.time_points_bm
            )
            st.rerun() # Rerun to update content based on new derived paths

        # Call verify_martingale_property (from source.py)
        st.markdown(f"### Martingale Property Verification for ($W_t^2 - t$)")
        plot_wrapper(verify_martingale_property, st.session_state.time_points_bm, st.session_state.Wt_squared_minus_t_paths, '($W_t^2 - t$)')

        # 4.c. Markdown cell (explanation of execution)
        st.markdown(f"Aisha observes that, similar to $W_t$, the average path of $W_t^2 - t$ remains constant over time. This confirms that $W_t^2 - t$ is also a martingale. This understanding is key for her when analyzing the stochastic differential equations and quadratic variations of processes used in advanced models, ensuring their consistency with fundamental arbitrage-free principles.")
    else:
        st.warning("Please simulate Standard Brownian Motion first on the previous page using the sidebar parameters.")

if st.session_state.current_page == '3. Exponential Martingale':
    st.markdown(f"## 5. Verifying the Martingale Property: Case 3 - Exponential Martingale ($exp(\\theta W_t - \\theta^2 t/2)$)")

    # 5.a. Markdown Cell
    st.markdown(f"Aisha now moves to a particularly important class of martingales: the exponential martingale. This form appears frequently in financial mathematics, especially when performing a change of probability measure (Girsanov's Theorem) which is central to risk-neutral valuation.")
    st.markdown(f"The exponential martingale is of immense practical significance for a Quant Analyst. It forms the basis for constructing equivalent martingale measures, which are essential for pricing derivatives in incomplete markets or when transforming processes from the physical measure to the risk-neutral measure. Verifying its martingale property reinforces Aisha's understanding of its role in financial models. For its general form, its martingale property states:")
    st.markdown(r"$$M_t = \exp(\theta W_t - \frac{1}{2}\theta^2 t)$$")
    st.markdown(r"where $M_t$ is the exponential martingale process, $W_t$ is Standard Brownian Motion, and $\theta$ is a constant parameter.")
    st.markdown(r"$$E[M_{t+s} | \mathcal{F}_t] = M_t$$")
    st.markdown(r"where $E[M_{t+s} | \mathcal{F}_t]$ is the expected value of $M$ at time $t+s$ conditioned on information up to time $t$.")
    st.markdown(r"$$E[\exp(\theta W_{t+s} - \frac{1}{2}\theta^2 (t+s)) | \mathcal{F}_t] = \exp(\theta W_t - \frac{1}{2}\theta^2 t)$$")
    st.markdown(r"where $W_t$ is Standard Brownian Motion and $\theta$ is a constant parameter.")
    st.markdown(f"This process is also known as Novikov's condition for guaranteeing that a stochastic exponential is a true martingale.")

    st.sidebar.subheader("Exponential Martingale Parameter")
    new_theta_param = st.sidebar.number_input('Parameter $\\theta$', min_value=-2.0, max_value=2.0, value=st.session_state.theta_param, step=0.1, key='theta_param_input')

    theta_changed = False
    if new_theta_param != st.session_state.theta_param:
        st.session_state.theta_param = new_theta_param
        theta_changed = True

    if st.session_state.Wt_paths_bm is not None:
        if st.session_state.exponential_martingale_paths is None or theta_changed:
            st.session_state.exponential_martingale_paths = generate_exponential_martingale(
                st.session_state.Wt_paths_bm, st.session_state.time_points_bm, st.session_state.theta_param
            )
            if theta_changed: st.rerun()

        # Call verify_martingale_property (from source.py)
        st.markdown(f"### Martingale Property Verification for Exponential Martingale")
        plot_wrapper(verify_martingale_property, st.session_state.time_points_bm, st.session_state.exponential_martingale_paths,
                     f'Exponential Martingale ($e^{{{st.session_state.theta_param}W_t - 0.5 \cdot {st.session_state.theta_param}^2 t}}$)')

        # 5.c. Markdown cell (explanation of execution)
        st.markdown(f"Aisha observes that the average path of the exponential martingale remains constant, starting from its initial value of 1 (since $W_0=0$ implies $e^0=1$). This successfully verifies its martingale property. This specific martingale is crucial for her understanding of how probability measures can be changed in derivatives pricing, allowing complex pricing problems to be solved under a simplified risk-neutral framework.")
    else:
        st.warning("Please simulate Standard Brownian Motion first on the '1. Standard Brownian Motion (W_t)' page using the sidebar parameters.")


if st.session_state.current_page == '4. Risk-Neutral Valuation & FTAP':
    st.markdown(f"## 6. Connecting to Risk-Neutral Valuation")

    # 6.a. Markdown Cell
    st.markdown(f"Having empirically verified several key martingales, Aisha now focuses on the conceptual connection between martingales and the fundamental principle of risk-neutral valuation. This understanding is the theoretical bedrock of all arbitrage-free pricing models at Global Financial Solutions.")
    st.markdown(f"Aisha's core responsibility includes ensuring the models used for pricing options and other derivatives are robust and arbitrage-free. The martingale property is central to this. Under a risk-neutral probability measure $\mathbb{Q}$, the *discounted* price of any tradable asset (or any derivative thereon) must be a martingale. If this were not true, arbitrage opportunities would exist, which contradicts efficient market hypotheses.")
    st.markdown(f"Consider a financial asset $S_t$ and a constant risk-free interest rate $r$. The discounted asset price is:")
    st.markdown(r"$$S_t^* = e^{-rt} S_t$$")
    st.markdown(r"where $S_t^*$ is the discounted asset price at time $t$, $S_t$ is the asset price, $r$ is the risk-free rate.")
    st.markdown(f"For arbitrage-free markets, under the risk-neutral measure $\mathbb{Q}$, this discounted process must be a martingale:")
    st.markdown(r"$$E^{\mathbb{Q}}[S_{t+s}^* | \mathcal{F}_t] = S_t^*$$")
    st.markdown(r"where $E^{\mathbb{Q}}$ is the expectation under the risk-neutral measure, $S_t^*$ is the discounted asset price at time $t$, and $\mathcal{F}_t$ is the information available at time $t$.")
    st.markdown(f"This implies that the expected future discounted price, given current information, is the current discounted price. This allows Aisha to price derivatives by taking the expected value of their future payoffs under this risk-neutral measure. For a European option with payoff $Payoff(S_T)$ at maturity $T$, its value at time $t$ is given by:")
    st.markdown(r"$$V_t = E^{\mathbb{Q}}[e^{-r(T-t)} Payoff(S_T) | \mathcal{F}_t]$$")
    st.markdown(r"where $V_t$ is the option value at time $t$, $r$ is the risk-free rate, $T$ is maturity, and $Payoff(S_T)$ is the option payoff at maturity based on asset price $S_T$.")
    st.markdown(f"This formula means that the fair value of a derivative today is the discounted expected value of its future payoff, where the expectation is taken under the risk-neutral measure. This is the bedrock of Aisha's daily pricing work.")

    # 6.c. Markdown cell (explanation of execution)
    st.markdown(f"Aisha's conceptual review confirms that the martingale property is not merely a mathematical curiosity but a direct consequence of the no-arbitrage principle in financial markets. Her simulations of martingales directly supported this theoretical understanding, showing how processes that are 'fair' (in the sense of no predictable gains) behave. This deepens her confidence in the risk-neutral pricing framework used by Global Financial Solutions.")

    st.markdown(f"## 7. The Fundamental Theorem of Asset Pricing")

    # 7.a. Markdown Cell
    st.markdown(f"To complete her foundational review, Aisha synthesizes her understanding of martingales and risk-neutral valuation with the Fundamental Theorem of Asset Pricing (FTAP). This theorem provides the formal justification for why the martingale approach is valid for arbitrage-free pricing.")
    st.markdown(f"The Fundamental Theorem of Asset Pricing is a cornerstone of mathematical finance that directly links the absence of arbitrage opportunities to the existence of risk-neutral measures. For Aisha, this theorem provides the rigorous theoretical backing for the pricing models she employs, ensuring their validity and consistency.")
    st.markdown(f"The theorem is typically presented in two parts:")
    st.markdown(f"1.  **First Fundamental Theorem of Asset Pricing:** An arbitrage-free market exists if and only if there exists at least one equivalent martingale measure (EMM) $\mathbb{Q}$ under which all discounted asset prices are martingales. In simpler terms, if a market allows for no free lunch (no arbitrage), then we can find a risk-neutral probability measure that makes discounted asset prices behave like martingales.")
    st.markdown(r"where $\mathbb{Q}$ denotes an equivalent martingale measure (risk-neutral measure).")
    st.markdown(f"2.  **Second Fundamental Theorem of Asset Pricing:** A market is complete (meaning every contingent claim can be perfectly replicated by a self-financing trading strategy) if and only if there exists a *unique* equivalent martingale measure $\mathbb{Q}$. If Global Financial Solutions operates in a complete market (e.g., the Black-Scholes world), Aisha knows that there is only one correct way to price derivatives via risk-neutral expectation.")
    st.markdown(r"where $\mathbb{Q}$ denotes an equivalent martingale measure (risk-neutral measure).")
    st.markdown(f"These theorems formally explain *why* Aisha performs her martingale verifications and uses risk-neutral valuation. They establish the conditions under which these pricing techniques are applicable and unique.")

    # 7.c. Markdown cell (explanation of execution)
    st.markdown(f"Aisha concludes her review, affirming that the martingale property is not just an arbitrary condition but a profound implication of market efficiency. The Fundamental Theorem of Asset Pricing explicitly connects the absence of arbitrage—a non-negotiable principle for Global Financial Solutions—to the existence and, under completeness, uniqueness of the risk-neutral measure. This theoretical underpinning gives Aisha the confidence that her firm's sophisticated derivatives pricing models are built on solid mathematical ground, enabling accurate valuation and responsible risk management. This foundational review solidifies her ability to scrutinize, apply, and explain complex models with clarity and precision.")
