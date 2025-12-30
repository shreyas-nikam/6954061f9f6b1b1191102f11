Here's a comprehensive `README.md` file for your Streamlit application lab project, structured for clarity and professionalism.

---

# QuLab: Stochastic Calculus - Martingale Properties and Risk-Neutral Valuation

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Title and Description

**Project Title:** QuLab: Stochastic Calculus - Martingale Properties and Risk-Neutral Valuation

This Streamlit application, **QuLab: Stochastic Calculus**, is designed as an interactive educational and verification tool for quantitative analysts, students, and enthusiasts in financial mathematics. It aims to provide a practical and conceptual understanding of martingale properties and their fundamental role in risk-neutral valuation and arbitrage-free pricing.

The application simulates various stochastic processes, including Standard Brownian Motion ($W_t$), Squared Brownian Motion Minus Time ($W_t^2 - t$), and Exponential Martingales, allowing users to visually verify their martingale properties. By doing so, it bridges theoretical concepts with practical demonstrations, reinforcing the core principles that underpin modern derivatives pricing and risk management. It frames the learning experience around the workflow of a Quantitative Analyst, emphasizing the "why" behind these mathematical constructs in a financial context.

## Features

This application offers the following key features:

*   **Interactive Simulations:** Dynamically simulate paths for Standard Brownian Motion, $W_t^2 - t$, and Exponential Martingales.
*   **Parameter Tuning:** Adjust simulation parameters (Total Time Horizon `T`, Number of Time Steps `N_steps`, Number of Sample Paths `N_paths`, Exponential Martingale parameter `θ`) via an intuitive sidebar.
*   **Martingale Verification:** Visually demonstrate the martingale property for selected processes by plotting individual paths and their ensemble average.
*   **Guided Navigation:** A clear sidebar navigation allows users to explore different stochastic processes and theoretical concepts sequentially.
*   **Conceptual Explanations:** Detailed markdown explanations on each page connect the simulations to core financial mathematics concepts like integrability, adaptedness, conditional expectation, and the Fundamental Theorem of Asset Pricing (FTAP).
*   **Risk-Neutral Valuation Context:** Dedicated sections explain the crucial link between martingales and arbitrage-free pricing under the risk-neutral measure.

## Getting Started

Follow these instructions to set up and run the QuLab application on your local machine.

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)

### Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/yourusername/quants-streamlit-lab.git
    cd quants-streamlit-lab
    ```
    *(If not in a repository, simply create a folder and place `app.py` and `source.py` inside it.)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install the required libraries:**
    Create a `requirements.txt` file in your project root with the following content:
    ```
    streamlit
    numpy
    matplotlib
    scipy
    ```
    Then install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the Streamlit application:

1.  **Ensure your virtual environment is activated.**
2.  **Navigate to the directory containing `app.py` and `source.py` (if not already there).**
3.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser (usually at `http://localhost:8501`).

### Basic Usage Instructions:

*   **Navigation:** Use the "Navigation" radio buttons in the left sidebar to move between different sections of the lab project.
*   **Simulation Parameters:** On pages involving simulations (1-3), adjust the `Total Time Horizon (T)`, `Number of Time Steps`, and `Number of Sample Paths` using the sliders in the sidebar. The application will automatically re-simulate and update the plots.
*   **Exponential Martingale Parameter:** On the "3. Exponential Martingale" page, you can also tune the `Parameter θ` for the exponential martingale.
*   **Explore Concepts:** Read through the explanations on each page to understand the mathematical background and financial significance of each martingale property and its connection to risk-neutral valuation.

## Project Structure

The project is organized as follows:

```
quants-streamlit-lab/
├── .venv/                     # Python virtual environment (after setup)
├── app.py                     # Main Streamlit application file
├── source.py                  # Python module containing simulation and plotting functions
└── requirements.txt           # List of required Python packages
└── README.md                  # This README file
```

### `app.py`

This is the main entry point of the application. It handles:
*   Streamlit page configuration and session state management.
*   Sidebar navigation and parameter inputs.
*   Conditional rendering of content based on selected page.
*   Calling simulation and plotting functions from `source.py`.

### `source.py`

This file is expected to contain the core logic for:
*   `simulate_brownian_motion(T, N_steps, N_paths)`: Generates paths for Standard Brownian Motion.
*   `generate_squared_brownian_motion_martingale(Wt_paths, time_points)`: Derives paths for $W_t^2 - t$.
*   `generate_exponential_martingale(Wt_paths, time_points, theta)`: Derives paths for the exponential martingale.
*   `verify_martingale_property(time_points, paths, title)`: Plots the simulated paths and their average to visually verify the martingale property.

## Technology Stack

*   **Python:** The core programming language.
*   **Streamlit:** For creating the interactive web application interface.
*   **NumPy:** Essential for numerical operations and efficient array manipulation in simulations.
*   **Matplotlib:** Used for generating all the static plots and visualizations.
*   **SciPy:** (Implicitly used/expected for statistical functions, especially if `source.py` uses `scipy.stats` for distributions or other numerical routines).

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name` or `bugfix/your-bug-fix`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to good practices and includes appropriate documentation and comments.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Note: You might need to create a `LICENSE` file in your repository if you haven't already.)*

## Contact

For any questions or feedback, please reach out to:

*   **Quant University:** [https://www.quantuniversity.com/](https://www.quantuniversity.com/)
*   **Email:** info@quantuniversity.com
*   **GitHub:** [https://github.com/quant-university](https://github.com/quant-university) (Assumed organization GitHub)

---