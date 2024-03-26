
# Discretize (i.e. partition) the sequences into S symbols
# Choose m embedding dimension (history) as input parameter



import numpy as np

def TranEn(X, Y, confounder, history_length):
    n = len(X)
    te = 0.0

    for t in range(history_length, n):
        # Extract history windows for X, Y, and confounder
        X_window = X[t - history_length:t]
        Y_window = Y[t - history_length:t]
        confounder_window = confounder[t - history_length:t]

        # Calculate joint and conditional probabilities
        p_X_Y_conf = 0  # Calculate this based on your data
        p_X_conf = 0  # Calculate this based on your data
        p_Y_conf = 0  # Calculate this based on your data
        p_X = 0  # Calculate this based on your data
        p_Y = 0  # Calculate this based on your data
        p_conf = 0  # Calculate this based on your data

        # Calculate transfer entropy
        if p_X_Y_conf > 0 and p_X_conf > 0 and p_Y_conf > 0 and p_X > 0 and p_Y > 0 and p_conf > 0:
            te += np.log((p_X_Y_conf * p_X_conf) / (p_Y_conf * p_X))

    return te

# Example usage
X_data = np.random.rand(1000)  # Replace with your X time series data
Y_data = np.random.rand(1000)  # Replace with your Y time series data
confounder_data = np.random.rand(1000)  # Replace with your confounder time series data
history_length = 5  # Length of the history window

te_value = calculate_transfer_entropy(X_data, Y_data, confounder_data, history_length)
print(f"Transfer Entropy: {te_value}")











"""
    Copyright 2024 Matthew W. Flood, EntropyHub
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
     http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    For Terms of Use see https://github.com/MattWillFlood/EntropyHub
"""