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
    <title>AI Text Humanizer</title>
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
      body { background: radial-gradient(1200px 600px at 10% -10%, rgba(124,58,237,.18), transparent), radial-gradient(1000px 500px at 100% 0%, rgba(6,182,212,.16), transparent), linear-gradient(180deg, #0b1020, #0d1226); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji"; margin: 0; }
      .container { max-width: 1100px; margin: 0 auto; padding: 24px; }
      .hero { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 16px; }
      .title { font-size: 28px; font-weight: 800; letter-spacing: 0.3px; background: linear-gradient(90deg, #fff, #cbd5e1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
      .panel { background: rgba(16,23,42,.85); border: 1px solid var(--border); border-radius: 14px; padding: 16px; box-shadow: 0 8px 30px rgba(0,0,0,.25); }
      .split { display: grid; grid-template-columns: 1fr; gap: 16px; margin-top: 16px; }
      @media (min-width: 960px) { .split { grid-template-columns: 1fr 1fr; } }
      textarea { width: 100%; min-height: 340px; resize: vertical; background: #0b1222; color: var(--text); border: 1px solid var(--border); border-radius: 12px; padding: 14px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: 14px; box-shadow: inset 0 0 0 1px rgba(255,255,255,.02); }
      textarea:focus { outline: none; box-shadow: 0 0 0 2px rgba(124,58,237,.45); }
      .controls { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; justify-content: space-between; }
      .btn { background: linear-gradient(90deg, var(--accent), var(--accent-2)); color: white; padding: 12px 18px; border: none; border-radius: 12px; cursor: pointer; font-weight: 700; letter-spacing: .2px; transition: transform .06s ease, filter .2s ease; box-shadow: 0 8px 20px rgba(124,58,237,.25); }
      .btn:hover { filter: brightness(1.05); }
      .btn:active { transform: translateY(1px); }
      .switch { display: inline-flex; align-items: center; gap: 10px; color: var(--muted); font-weight: 600; }
      .switch input { accent-color: var(--accent); width: 18px; height: 18px; }
      .metrics { display: flex; gap: 16px; align-items: center; margin: 10px 0; color: var(--muted); font-size: 14px; }
      .metric { background: #0b1222; border: 1px solid var(--border); padding: 10px 12px; border-radius: 10px; }
      .ok { color: var(--success); }
      .warn { color: var(--warning); }
      .mono { white-space: pre-wrap; word-wrap: break-word; }
      .footer { margin-top: 20px; color: var(--muted); font-size: 12px; text-align: center; }
      label { font-weight: 700; display: block; margin-bottom: 8px; }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="hero">
        <div class="title">AI Text Humanizer</div>
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
        original=text,
        ok=ok,
        preserve_headings=preserve_headings,
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False, threaded=True)
