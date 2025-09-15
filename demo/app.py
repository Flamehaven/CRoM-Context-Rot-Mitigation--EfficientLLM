"""
CRoM-EfficientLLM Hugging Face Spaces Demo
Interactive demo for Context Rot Mitigation and budget packing
"""

import gradio as gr
import json
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

# Mock implementation for demo (simplified)
class MockChunk:
    def __init__(self, text: str, score: float, token_count: int):
        self.text = text
        self.score = score
        self.token_count = token_count

    def to_dict(self):
        return {
            "text": self.text[:100] + "..." if len(self.text) > 100 else self.text,
            "score": round(self.score, 3),
            "tokens": self.token_count
        }

def mock_budget_pack(chunks: List[MockChunk], budget: int) -> tuple:
    """Mock budget packing function for demo"""
    # Sort by score descending
    sorted_chunks = sorted(chunks, key=lambda x: x.score, reverse=True)

    selected = []
    total_tokens = 0

    for chunk in sorted_chunks:
        if total_tokens + chunk.token_count <= budget:
            selected.append(chunk)
            total_tokens += chunk.token_count
        else:
            break

    return selected, total_tokens

def mock_drift_estimation(responses: List[str]) -> List[float]:
    """Mock drift estimation for demo"""
    if len(responses) < 2:
        return [0.0]

    # Simulate drift scores based on response similarity
    drift_scores = []
    for i in range(len(responses)):
        if i == 0:
            drift_scores.append(0.0)
        else:
            # Simple character-based similarity mock
            prev_resp = responses[i-1]
            curr_resp = responses[i]
            similarity = len(set(prev_resp) & set(curr_resp)) / len(set(prev_resp) | set(curr_resp))
            drift = 1.0 - similarity
            drift_scores.append(min(drift, 1.0))

    return drift_scores

def create_drift_plot(drift_scores: List[float]) -> str:
    """Create drift visualization plot"""
    fig, ax = plt.subplots(figsize=(10, 6))

    x = list(range(len(drift_scores)))
    ax.plot(x, drift_scores, 'b-o', linewidth=2, markersize=6)
    ax.fill_between(x, drift_scores, alpha=0.3)

    ax.set_xlabel('Response Sequence')
    ax.set_ylabel('Drift Score')
    ax.set_title('Context Drift Over Time')
    ax.grid(True, alpha=0.3)

    # Add threshold line
    ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.7, label='Alert Threshold')
    ax.legend()

    # Convert to base64 for display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)

    return f"data:image/png;base64,{img_base64}"

def crom_demo(text_input: str, token_budget: int, enable_drift: bool):
    """Main demo function for CRoM-EfficientLLM"""

    if not text_input.strip():
        return "Please enter some text to process.", "", ""

    # Simulate chunking the input text
    sentences = text_input.split('.')
    chunks = []

    for i, sentence in enumerate(sentences):
        if sentence.strip():
            # Mock scoring based on length and position
            score = np.random.uniform(0.3, 0.95)
            token_count = len(sentence.split())
            chunks.append(MockChunk(sentence.strip(), score, token_count))

    if not chunks:
        return "No valid chunks found in input text.", "", ""

    # Apply budget packing
    selected_chunks, total_tokens = mock_budget_pack(chunks, token_budget)

    # Create results summary
    results = {
        "total_chunks": len(chunks),
        "selected_chunks": len(selected_chunks),
        "total_tokens_used": total_tokens,
        "budget_utilization": f"{(total_tokens/token_budget)*100:.1f}%",
        "selected_content": [chunk.to_dict() for chunk in selected_chunks]
    }

    # Format output
    output_text = f"""
## CRoM Budget Packing Results

**Budget:** {token_budget} tokens
**Utilization:** {results['budget_utilization']} ({total_tokens}/{token_budget} tokens)
**Chunks:** {results['selected_chunks']} selected from {results['total_chunks']} total

### Selected Content (Top Scoring):
"""

    for i, chunk in enumerate(selected_chunks, 1):
        output_text += f"\n**Chunk {i}** (Score: {chunk.score:.3f}, Tokens: {chunk.token_count})\n"
        output_text += f"_{chunk.text}_\n"

    # Drift simulation if enabled
    drift_plot = ""
    if enable_drift and len(selected_chunks) >= 2:
        # Mock responses based on selected chunks
        mock_responses = [chunk.text for chunk in selected_chunks[:5]]  # Limit for demo
        drift_scores = mock_drift_estimation(mock_responses)
        drift_plot = create_drift_plot(drift_scores)

        output_text += f"\n\n### Drift Analysis\n"
        output_text += f"**Average Drift:** {np.mean(drift_scores):.3f}\n"
        output_text += f"**Max Drift:** {max(drift_scores):.3f}\n"

        if max(drift_scores) > 0.5:
            output_text += "⚠️ **Alert:** High drift detected!\n"

    return output_text, json.dumps(results, indent=2), drift_plot

# Create Gradio interface
with gr.Blocks(title="CRoM-EfficientLLM Demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎯 CRoM-EfficientLLM Interactive Demo

    **Context Rot Mitigation for Efficient Large Language Models**

    This demo showcases CRoM's core capabilities:
    - **Budget Packing**: Intelligent selection of text chunks within token limits
    - **Drift Estimation**: Monitoring semantic consistency over time
    - **Context Optimization**: Maximizing relevance while staying within budget

    🚀 **[Try the full library](https://github.com/Flamehaven/CRoM-Context-Rot-Mitigation--EfficientLLM)**
    """)

    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label="📝 Input Text",
                placeholder="Enter a long text document to be processed by CRoM...\n\nTip: Use multiple sentences for better chunking demonstration.",
                lines=8,
                value="Machine learning is revolutionizing healthcare. Deep learning models can analyze medical images with unprecedented accuracy. Natural language processing helps extract insights from clinical notes. Computer vision assists in diagnostic imaging. Predictive analytics can forecast patient outcomes. AI-powered drug discovery accelerates pharmaceutical research. Robotic surgery enhances precision in operations. Telemedicine platforms improve access to care."
            )

            token_budget = gr.Slider(
                label="🎯 Token Budget",
                minimum=10,
                maximum=200,
                value=50,
                step=5,
                info="Maximum tokens to include in final context"
            )

            enable_drift = gr.Checkbox(
                label="📊 Enable Drift Analysis",
                value=True,
                info="Visualize semantic drift between selected chunks"
            )

            process_btn = gr.Button("🚀 Process with CRoM", variant="primary", size="lg")

        with gr.Column(scale=3):
            output_text = gr.Markdown(label="📋 Results")

            with gr.Row():
                json_output = gr.Code(
                    label="📊 Detailed Metrics (JSON)",
                    language="json",
                    lines=10
                )

            drift_plot = gr.Image(
                label="📈 Drift Visualization",
                type="pil"
            )

    # Event handlers
    process_btn.click(
        fn=crom_demo,
        inputs=[text_input, token_budget, enable_drift],
        outputs=[output_text, json_output, drift_plot]
    )

    # Auto-run on startup
    demo.load(
        fn=crom_demo,
        inputs=[text_input, token_budget, enable_drift],
        outputs=[output_text, json_output, drift_plot]
    )

if __name__ == "__main__":
    demo.launch()