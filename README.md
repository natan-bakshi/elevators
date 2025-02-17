# Elevators Project

## Overview

This project simulates the operation of multiple elevators within a building. It is implemented in Python and provides a framework to model elevator behaviors, building configurations, and floor interactions.

## Features

- **Building Management**: Defines the building structure, including the number of floors and the allocation of elevators.
- **Elevator Operations**: Models elevator behaviors such as moving between floors, handling requests, and managing door operations.
- **Floor Interactions**: Manages floor-specific actions, including call buttons and floor requests.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/natan-bakshi/elevators.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd elevators
   ```

3. **Install Dependencies**:

   Ensure you have Python installed. Install any necessary dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: The **`requirements.txt`** file should list all necessary packages. If it's not present, ensure you have the required packages before running the project.*

## Usage

1. **Configuration**:

   Adjust the `config.py` file to set up the building parameters, such as the number of floors and elevators.

2. **Running the Simulation**:

   Execute the main script to start the simulation:

   ```bash
   python main.py
   ```

   The simulation will initialize the building and elevators based on your configuration and begin processing elevator requests.

## Project Structure

- `main.py`: The entry point of the simulation.
- `building.py`: Contains the `Building` class, managing the overall building structure and elevator allocation.
- `elevator.py`: Defines the `Elevator` class, modeling individual elevator behaviors and states.
- `floor.py`: Includes the `Floor` class, handling floor-specific interactions and requests.
- `config.py`: Houses configuration settings for the simulation, such as the number of floors and elevators.
- `resources/`: A directory for additional resources or data files used in the simulation.

---

*Note: This README provides a general overview of the project. For detailed information and advanced configurations, please refer to the project's documentation or source code.*

