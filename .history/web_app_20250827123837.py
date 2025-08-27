from flask import Flask, request, render_template_string
from humanizer import TextHumanizer

app = Flask(__name__)
humanizer = TextHumanizer(target_similarity_range=(0.00, 0.49))

PAGE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AI Text Humanizer (Similarity < 50%)</title>
    <style>
      :root {
        --bg: #0b1020;
        --panel: #10172a;
        --muted: #9aa4b2;
        --text: #e6ebf0;
        --accent: #7c3aed;
        --accent-2: #06b6d4;
        --border: #1f2a44;
        --success: #22c55e;
        --warning: #f59e0b;
      }
      * { box-sizing: border-box; }
      body { background: linear-gradient(180deg, #0b1020, #0d1226); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji"; margin: 0; }
      .container { max-width: 1100px; margin: 0 auto; padding: 24px; }
      .hero { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 16px; }
      .title { font-size: 28px; font-weight: 700; letter-spacing: 0.2px; }
      .badge { background: linear-gradient(90deg, var(--accent), var(--accent-2)); padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
      .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
      .split { display: grid; grid-template-columns: 1fr; gap: 16px; }
      @media (min-width: 960px) { .split { grid-template-columns: 1fr 1fr; } }
      textarea { width: 100%; min-height: 320px; resize: vertical; background: #0b1222; color: var(--text); border: 1px solid var(--border); border-radius: 10px; padding: 12px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: 14px; }
      .controls { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
      .btn { background: linear-gradient(90deg, var(--accent), var(--accent-2)); color: white; padding: 10px 16px; border: none; border-radius: 10px; cursor: pointer; font-weight: 600; }
      .btn:disabled { opacity: .6; cursor: not-allowed; }
      .switch { display: inline-flex; align-items: center; gap: 8px; color: var(--muted); }
      .switch input { accent-color: var(--accent); }
      .metrics { display: flex; gap: 16px; align-items: center; margin: 10px 0; color: var(--muted); font-size: 14px; }
      .metric { background: #0b1222; border: 1px solid var(--border); padding: 8px 10px; border-radius: 8px; }
      .ok { color: var(--success); }
      .warn { color: var(--warning); }
      .mono { white-space: pre-wrap; word-wrap: break-word; }
      .footer { margin-top: 20px; color: var(--muted); font-size: 12px; text-align: center; }
      label { font-weight: 600; display: block; margin-bottom: 6px; }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="hero">
        <div class="title">AI Text Humanizer</div>
        <div class="badge">Similarity < 50%</div>
      </div>

      <form method="post" class="panel">
        <label for="text">AI-generated text</label>
        <textarea id="text" name="text" placeholder="Paste your text here..." required>{{ text or '' }}</textarea>
        <div class="controls" style="margin-top: 12px">
          <label class="switch"><input type="checkbox" name="preserve_headings" value="1" {% if preserve_headings %}checked{% endif %}/> Preserve headings and spacing</label>
          <button class="btn" type="submit">Humanize</button>
        </div>
      </form>

      {% if result %}
      <div class="split">
        <div class="panel">
          <h3 style="margin-top:0">Result</h3>
          <div class="metrics">
            <div class="metric">Similarity: <span class="{% if ok %}ok{% else %}warn{% endif %}"><strong>{{ similarity }}</strong></span></div>
            <div class="metric">Target bounds: {{ lower }}–{{ upper }}</div>
          </div>
          <div class="mono">{{ result }}</div>
        </div>
        <div class="panel">
          <h3 style="margin-top:0">Original</h3>
          <div class="mono" style="color: var(--muted)">{{ original }}</div>
        </div>
      </div>
      {% endif %}

      <div class="footer">Runs locally. No data is sent to external services.</div>
    </div>
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = None
    similarity_str = None
    ok = False
    preserve_headings = False
    if request.method == "POST":
        text = (request.form.get("text") or "").strip()
        preserve_headings = request.form.get("preserve_headings") == "1"
        if text:
            if preserve_headings:
                humanized, similarity = humanizer.humanize_with_headings(text)
            else:
                humanized, similarity = humanizer.humanize_text(text)
            result = humanized
            similarity_str = f"{similarity * 100:.1f}%"
            ok = similarity <= 0.49
    return render_template_string(
        PAGE,
        text=text,
        result=result,
        similarity=similarity_str,
        lower=f"{humanizer.target_similarity_range[0]*100:.0f}%",
        upper=f"{humanizer.target_similarity_range[1]*100:.0f}%",
        original=text,
        ok=ok,
        preserve_headings=preserve_headings,
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False, threaded=True)
