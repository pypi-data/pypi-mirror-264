import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)


def measure_time(processor_name, func, *args, **kwargs):
    """
    Measure the execution time of a function and log the elapsed time.

    Args:
        processor_name (str): Name of the processor or task.
        func (callable): Function to be measured.
        *args: Variable length argument list to be passed to the function.
        **kwargs: Arbitrary keyword arguments to be passed to the function.

    Returns:
        tuple: Tuple containing the result of the function and a dictionary
            with information about the execution time and processor name.
    """
    start_time = time.time()  # Record start time
    result = func(*args, **kwargs)  # Execute the function with provided arguments
    end_time = time.time()  # Record end time
    execution_time = end_time - start_time  # Calculate elapsed time
    # Log the elapsed time along with function name and processor name
    logging.info(f'Time elapsed for {func.__name__}: {execution_time}, processor name {processor_name}')
    # Create a dictionary with execution information
    data = {
        "info": kwargs,  # Pass additional information
        "processor_name": processor_name,  # Store processor name
        "elapsed_time": execution_time,  # Store elapsed time
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Record creation time
    }
    return result, data  # Return result and execution data


# Example usage:
"""
def sample_function(a, b):
    return a + b

# Measure the execution time of the sample function
result, execution_data = measure_time("Sample Processor", sample_function, file_name, run_id)

# Print the result and execution data
print("Result:", result)
print("Execution Data:", execution_data)
"""
