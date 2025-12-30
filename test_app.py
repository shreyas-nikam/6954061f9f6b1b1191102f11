
from streamlit.testing.v1 import AppTest
import pytest
import numpy as np

# Mock functions from source.py to avoid actual computation during tests
# and to control their return values if necessary.
# For these tests, we mostly care if they are called and if st.pyplot is used.
def mock_simulate_brownian_motion(T, N_steps, N_paths):
    # Return dummy data for testing purposes
    time_points = np.linspace(0, T, N_steps + 1)
    paths = np.zeros((N_paths, N_steps + 1))
    return time_points, paths

def mock_generate_squared_brownian_motion_martingale(Wt_paths, time_points):
    # Return dummy data
    return Wt_paths**2 - time_points

def mock_generate_exponential_martingale(Wt_paths, time_points, theta):
    # Return dummy data
    return np.exp(theta * Wt_paths - 0.5 * theta**2 * time_points)

def mock_verify_martingale_property(time_points, paths, title):
    # This function is expected to call st.pyplot, no specific return value needed
    pass


# Patch the source functions
def patch_source_functions():
    import sys
    from unittest.mock import MagicMock
    
    # Create a mock module for 'source'
    mock_source = MagicMock()
    mock_source.simulate_brownian_motion = mock_simulate_brownian_motion
    mock_source.generate_squared_brownian_motion_martingale = mock_generate_squared_brownian_motion_martingale
    mock_source.generate_exponential_martingale = mock_generate_exponential_martingale
    mock_source.verify_martingale_property = mock_verify_martingale_property
    
    # Insert the mock module into sys.modules
    sys.modules['source'] = mock_source

# Call the patcher before running tests
patch_source_functions()


def test_initial_state_and_introduction_page():
    at = AppTest.from_file("app.py").run()

    # Check initial session state
    assert at.session_state["current_page"] == 'Introduction'
    assert at.session_state["T"] == 1.0
    assert at.session_state["N_steps"] == 252
    assert at.session_state["N_paths"] == 100
    assert at.session_state["theta_param"] == 0.5
    assert at.session_state["Wt_paths_bm"] is None
    assert at.session_state["time_points_bm"] is None
    assert at.session_state["Wt_squared_minus_t_paths"] is None
    assert at.session_state["exponential_martingale_paths"] is None

    # Check header and introduction content
    assert at.title[0].value == "QuLab: Stochastic calculus"
    assert "Martingale Properties and Risk-Neutral Valuation" in at.markdown[0].value
    assert "Introduction to the Case Study" in at.markdown[1].value
    assert at.info[0].value == "Note: The environment setup (installing libraries) is handled automatically when the application starts. Required libraries are imported below."
    assert at.code[0].value == "import numpy as np\nimport matplotlib.pyplot as plt\nimport scipy.stats as stats\nfrom source.py import *"


def test_navigation_to_brownian_motion_page():
    at = AppTest.from_file("app.py").run()

    # Navigate to "1. Standard Brownian Motion (W_t)"
    at.radio[0].set_value("1. Standard Brownian Motion (W_t)").run()
    assert at.session_state["current_page"] == '1. Standard Brownian Motion (W_t)'
    assert at.markdown[0].value == "## 2. Simulating Standard Brownian Motion"
    assert at.slider[0].value == 1.0 # T slider
    assert at.slider[1].value == 252 # N_steps slider
    assert at.slider[2].value == 100 # N_paths slider
    assert at.session_state.Wt_paths_bm is not None
    assert at.session_state.time_points_bm is not None
    assert len(at.pyplot) == 2 # One for simulation, one for martingale verification

    # Verify initial info message is gone and plots are displayed
    assert len(at.info) == 0 # "Adjust parameters..." message should be gone
    assert at.pyplot[0].figure is not None
    assert at.pyplot[1].figure is not None


def test_brownian_motion_parameter_change_and_rerun():
    at = AppTest.from_file("app.py").run()
    at.radio[0].set_value("1. Standard Brownian Motion (W_t)").run()

    # Change T parameter
    at.slider[0].set_value(2.0).run()
    assert at.session_state["T"] == 2.0
    assert at.session_state["Wt_paths_bm"] is not None
    assert at.session_state["time_points_bm"] is not None
    assert at.session_state["Wt_squared_minus_t_paths"] is None # Should be invalidated
    assert at.session_state["exponential_martingale_paths"] is None # Should be invalidated
    assert len(at.pyplot) == 2 # Plots should re-render

    # Change N_steps parameter
    at.slider[1].set_value(300).run()
    assert at.session_state["N_steps"] == 300
    assert at.session_state["Wt_paths_bm"] is not None
    assert at.session_state["time_points_bm"] is not None
    assert len(at.pyplot) == 2

    # Change N_paths parameter
    at.slider[2].set_value(500).run()
    assert at.session_state["N_paths"] == 500
    assert at.session_state["Wt_paths_bm"] is not None
    assert at.session_state["time_points_bm"] is not None
    assert len(at.pyplot) == 2


def test_squared_brownian_motion_page():
    at = AppTest.from_file("app.py").run()
    at.radio[0].set_value("1. Standard Brownian Motion (W_t)").run() # Generate BM first
    at.radio[0].set_value("2. Squared Brownian Motion Minus Time (W_t^2 - t)").run()

    assert at.session_state["current_page"] == '2. Squared Brownian Motion Minus Time (W_t^2 - t)'
    assert at.markdown[0].value == "## 4. Verifying the Martingale Property: Case 2 - Squared Brownian Motion Minus Time ($W_t^2 - t$)"
    assert at.session_state["Wt_squared_minus_t_paths"] is not None
    assert len(at.pyplot) == 1 # Only one plot on this page


def test_exponential_martingale_page():
    at = AppTest.from_file("app.py").run()
    at.radio[0].set_value("1. Standard Brownian Motion (W_t)").run() # Generate BM first
    at.radio[0].set_value("3. Exponential Martingale").run()

    assert at.session_state["current_page"] == '3. Exponential Martingale'
    assert at.markdown[0].value == "## 5. Verifying the Martingale Property: Case 3 - Exponential Martingale ($exp(\\theta W_t - \\theta^2 t/2)$)"
    assert at.number_input[0].value == 0.5 # theta_param
    assert at.session_state["exponential_martingale_paths"] is not None
    assert len(at.pyplot) == 1

    # Change theta parameter
    at.number_input[0].set_value(1.0).run()
    assert at.session_state["theta_param"] == 1.0
    assert at.session_state["exponential_martingale_paths"] is not None # Should be re-generated
    assert len(at.pyplot) == 1


def test_risk_neutral_valuation_page():
    at = AppTest.from_file("app.py").run()
    at.radio[0].set_value("4. Risk-Neutral Valuation & FTAP").run()

    assert at.session_state["current_page"] == '4. Risk-Neutral Valuation & FTAP'
    assert at.markdown[0].value == "## 6. Connecting to Risk-Neutral Valuation"
    assert "The Fundamental Theorem of Asset Pricing" in at.markdown[5].value
    assert len(at.pyplot) == 0 # No plots on this page
    # Verify specific text content
    assert "A market is complete" in at.markdown[8].value
    assert "First Fundamental Theorem of Asset Pricing" in at.markdown[7].value


def test_sidebar_parameter_visibility_on_introduction_page():
    at = AppTest.from_file("app.py").run()
    # On introduction page, simulation parameters should not be visible
    assert at.slider == []
    assert at.number_input == []

def test_sidebar_parameter_visibility_on_risk_neutral_page():
    at = AppTest.from_file("app.py").run()
    at.radio[0].set_value("4. Risk-Neutral Valuation & FTAP").run()
    # On this page, only navigation should be present, no simulation parameters
    assert at.slider == []
    assert at.number_input == []

