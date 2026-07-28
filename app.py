import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Artificial Neuron Explorer",
    page_icon="🧠",
    layout="wide"
)

# --- NEURON CLASS FROM SCRATCH ---
class ArtificialNeuron:
    def __init__(self, num_inputs=2):
        self.weights = np.random.randn(num_inputs) * 0.5
        self.bias = 0.0
        
    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

    def sigmoid_derivative(self, a):
        return a * (1.0 - a)

    def forward(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self.sigmoid(z), z

    def train_step(self, X, y, lr=0.1):
        # Forward Pass
        predictions, z = self.forward(X)
        
        # Loss (MSE)
        loss = np.mean((predictions - y) ** 2)
        
        # Backpropagation
        error = predictions - y
        d_z = error * self.sigmoid_derivative(predictions)
        
        d_w = np.dot(X.T, d_z) / len(y)
        d_b = np.mean(d_z)
        
        # Update Weights
        self.weights -= lr * d_w
        self.bias -= lr * d_b
        
        return loss

# --- UI HEADER ---
st.title("🧠 Single Artificial Neuron from Scratch")
st.markdown("Build, visual, and train a single Perceptron with real-time math execution!")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ Controls & Hyperparameters")

x1 = st.sidebar.slider("Input X1", -5.0, 5.0, 1.0, 0.1)
x2 = st.sidebar.slider("Input X2", -5.0, 5.0, -1.0, 0.1)

w1 = st.sidebar.slider("Weight W1", -3.0, 3.0, 0.5, 0.1)
w2 = st.sidebar.slider("Weight W2", -3.0, 3.0, -0.2, 0.1)
bias = st.sidebar.slider("Bias B", -3.0, 3.0, 0.1, 0.1)

# --- MAIN COMPUTATION ---
inputs = np.array([x1, x2])
weights = np.array([w1, w2])

# Weighted Sum & Sigmoid Output
z = np.dot(inputs, weights) + bias
y_hat = 1.0 / (1.0 + np.exp(-z))

# Layout splits
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📐 Live Equations & Outputs")
    
    st.latex(r"z = (w_1 \cdot x_1) + (w_2 \cdot x_2) + b")
    st.info(f"**Weighted Sum (z):** `{z:.4f}`")
    
    st.latex(r"\hat{y} = \sigma(z) = \frac{1}{1 + e^{-z}}")
    st.success(f"**Activated Output (ŷ):** `{y_hat:.4f}`")

with col2:
    st.subheader("🕸️ Visual Graph")
    
    # Simple Plotly Diagram
    fig = go.Figure()

    # Nodes
    fig.add_trace(go.Scatter(x=[0, 0, 1, 2], y=[1, -1, 0, 0],
                             mode='markers+text',
                             text=['X1', 'X2', 'Σ (z)', 'Output (ŷ)'],
                             textposition="top center",
                             marker=dict(size=[30, 30, 40, 30], color=['#3b82f6', '#3b82f6', '#8b5cf6', '#10b981'])))

    # Lines / Connections
    fig.add_shape(type="line", x0=0, y0=1, x1=1, y1=0, line=dict(color="gray", width=2))
    fig.add_shape(type="line", x0=0, y0=-1, x1=1, y1=0, line=dict(color="gray", width=2))
    fig.add_shape(type="line", x0=1, y0=0, x1=2, y1=0, line=dict(color="gray", width=2))

    fig.update_layout(showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False), height=250, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# --- TRAINING SIMULATOR SECTION ---
st.markdown("---")
st.subheader("⚙️ Live Interactive Training (Logic Gate - AND)")

if st.button("🚀 Train 100 Epochs (AND Gate Dataset)"):
    # AND Gate Dataset
    X = np.array([[0,0], [0,1], [1,0], [1,1]])
    y = np.array([0, 0, 0, 1])
    
    neuron = ArtificialNeuron(num_inputs=2)
    
    losses = []
    progress_bar = st.progress(0)
    
    for epoch in range(100):
        loss = neuron.train_step(X, y, lr=0.5)
        losses.append(loss)
        progress_bar.progress(epoch + 1)
        
    st.line_chart(losses)
    st.success(f"Training Complete! Final Loss: {losses[-1]:.6f}")