import streamlit as st
import anthropic
import json

st.set_page_config(page_title="Golden Prompt Generator", layout="wide")

st.markdown("""
<style>
.title { font-size: 3em; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
.subtitle { font-size: 1.2em; color: #888; margin-bottom: 30px; }
</style>
<div class="title">✨ Golden Prompt Generator</div>
<div class="subtitle">Transform your ideas into perfectly optimized AI prompts</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area(
        "What do you want your AI to do?",
        placeholder="e.g., Create a prompt that teaches Python DSA concepts step-by-step with code examples",
        height=120,
        key="user_input"
    )

with col2:
    tone = st.selectbox("Tone", ["Professional", "Casual", "Academic", "Creative"])
    detail = st.selectbox("Detail Level", ["Concise", "Balanced", "Detailed"])

if st.button("🚀 Generate Perfect Prompts", key="generate", use_container_width=True):
    if not user_input.strip():
        st.error("Please describe what you want your AI to do!")
    else:
        with st.spinner("Crafting your golden prompts..."):
            try:
                client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                
                golden_system_prompt = f"""You are an expert AI prompt engineer specializing in creating optimized, reusable prompts.

When given a user request, you:
1. Understand the core objective and desired output
2. Create 3 distinct, highly-optimized prompts that achieve the goal
3. Structure each prompt with: clear role → specific task → context → constraints → expected output format
4. Ensure reusability across Claude, GPT, Gemini, and other models
5. Add specific techniques: role-playing, chain-of-thought, structured output

Tone preference: {tone}
Detail level: {detail}

Output ONLY valid JSON with this structure:
{{
  "prompts": [
    {{"title": "Prompt 1 Title", "content": "Full optimized prompt here..."}},
    {{"title": "Prompt 2 Title", "content": "Full optimized prompt here..."}},
    {{"title": "Prompt 3 Title", "content": "Full optimized prompt here..."}}
  ]
}}"""
                
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2000,
                    messages=[
                        {"role": "user", "content": f"Generate 3 optimized prompts for: {user_input}"}
                    ],
                    system=golden_system_prompt
                )
                
                response_text = message.content[0].text
                result = json.loads(response_text)
                
                st.success("✓ Prompts generated!")
                
                for i, prompt in enumerate(result["prompts"], 1):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.subheader(f"Prompt {i}: {prompt['title']}")
                            st.code(prompt['content'], language="text")
                        with col2:
                            if st.button(f"📋 Copy {i}", key=f"copy_{i}"):
                                st.success("Copied!")
                
                st.divider()
                st.markdown("### 💡 Pro Tips")
                st.markdown("""  
- Test prompts with your favorite AI model (Claude, GPT, Gemini)
- Modify tone/detail and regenerate for variations
- Combine elements from multiple prompts for custom results
- Save working prompts for reuse across projects
                """)
                
            except json.JSONDecodeError:
                st.error("Error parsing response. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""  
**⚡ Instant Generation**  
Get optimized prompts in seconds
    """)

with col2:
    st.markdown("""  
**🎯 Highly Specific**  
Customized for your exact use case
    """)

with col3:
    st.markdown("""  
**🔄 Reusable**  
Works across all AI models
    """)
