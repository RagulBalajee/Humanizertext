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
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 24px; }
      .container { max-width: 960px; margin: 0 auto; }
      h1 { margin-bottom: 8px; }
      .sub { color: #666; margin-top: 0; }
      textarea { width: 100%; min-height: 300px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: 14px; padding: 12px; }
      .row { display: flex; gap: 16px; flex-wrap: wrap; }
      .col { flex: 1 1 300px; }
      .btn { background: #111827; color: white; padding: 10px 16px; border: none; border-radius: 6px; cursor: pointer; }
      .btn:disabled { opacity: .6; cursor: not-allowed; }
      .card { background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb; }
      .mono { white-space: pre-wrap; word-wrap: break-word; }
      .muted { color: #6b7280; }
      .metrics { margin: 12px 0; }
      .footer { margin-top: 24px; color: #6b7280; font-size: 12px; }
      label { font-weight: 600; display: block; margin-bottom: 6px; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>AI Text Humanizer</h1>
      <p class="sub">Target similarity: <strong>&lt; 50%</strong>. Paste large text (500–1000+ words) safely in your browser.</p>

      <form method="post">
        <label for="text">AI-generated text</label>
        <textarea id="text" name="text" placeholder="Paste your text here..." required>{{ text or '' }}</textarea>
        <div style="margin-top: 12px">
          <button class="btn" type="submit">Humanize</button>
        </div>
      </form>

      {% if result %}
      <div class="row" style="margin-top: 24px;">
        <div class="col">
          <div class="card">
            <h3 style="margin-top:0">Result</h3>
            <div class="metrics">
              <div>Similarity: <strong>{{ similarity }}</strong></div>
              <div class="muted">Target: &lt; 50% (bounds: {{ lower }}–{{ upper }})</div>
            </div>
            <div class="mono">{{ result }}</div>
          </div>
        </div>
        <div class="col">
          <div class="card">
            <h3 style="margin-top:0">Original</h3>
            <div class="mono muted">{{ original }}</div>
          </div>
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
    if request.method == "POST":
        text = (request.form.get("text") or "").strip()
        if text:
            humanized, similarity = humanizer.humanize_text(text)
            result = humanized
            similarity_str = f"{similarity * 100:.1f}%"
    return render_template_string(
        PAGE,
        text=text,
        result=result,
        similarity=similarity_str,
        lower=f"{humanizer.target_similarity_range[0]*100:.0f}%",
        upper=f"{humanizer.target_similarity_range[1]*100:.0f}%",
        original=text,
    )

if __name__ == "__main__":
    # Use threaded=True to better handle large payloads in dev
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
