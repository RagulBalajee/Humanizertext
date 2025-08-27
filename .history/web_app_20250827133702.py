from flask import Flask, request, render_template_string, redirect, url_for, session
from humanizer import TextHumanizer

app = Flask(__name__)
app.secret_key = "dev-secret-key"
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
        --text: #0f172a;
        --muted: #475569;
        --panel: #ffffff;
        --panel-ghost: rgba(255,255,255,.6);
        --border: #e2e8f0;
        --accent: #8b5cf6; /* violet */
        --accent-2: #22d3ee; /* cyan */
        --accent-3: #fb7185; /* rose */
        --shadow: 0 10px 30px rgba(2,6,23,.08);
      }
      * { box-sizing: border-box; }
      body {
        margin: 0; color: var(--text);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
        background: linear-gradient(120deg, #f8fafc, #eef2ff, #e0f2fe, #ffe4e6, #f8fafc);
        background-size: 300% 300%;
        animation: bgMove 20s ease infinite;
        min-height: 100vh;
      }
      @keyframes bgMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
      }
      .container { max-width: 1100px; margin: 0 auto; padding: 24px; }
      .hero { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 16px; }
      .title { font-size: 28px; font-weight: 800; letter-spacing: 0.3px; background: linear-gradient(90deg, #0f172a, #334155); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
      .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 16px; box-shadow: var(--shadow); position: relative; overflow: hidden; }
      .panel::before { content: ""; position: absolute; inset: -2px; background: conic-gradient(from 180deg at 50% 50%, rgba(139,92,246,.12), rgba(34,211,238,.12), rgba(251,113,133,.12), transparent 60%); filter: blur(22px); z-index: 0; animation: swirl 16s linear infinite; }
      @keyframes swirl { to { transform: rotate(360deg); } }
      .panel > * { position: relative; z-index: 1; }
      .split { display: grid; grid-template-columns: 1fr; gap: 16px; margin-top: 16px; }
      @media (min-width: 960px) { .split { grid-template-columns: 1fr 1fr; } }
      textarea { width: 100%; min-height: 420px; resize: vertical; background: #ffffff; color: var(--text); border: 1px solid var(--border); border-radius: 12px; padding: 14px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: 14px; box-shadow: inset 0 0 0 1px rgba(2,6,23,.03); transition: box-shadow .15s ease; }
      textarea:focus { outline: none; box-shadow: 0 0 0 3px rgba(139,92,246,.25); }
      .controls { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; justify-content: space-between; }
      .btn { background: linear-gradient(90deg, var(--accent), var(--accent-2)); color: white; padding: 12px 18px; border: none; border-radius: 12px; cursor: pointer; font-weight: 700; letter-spacing: .2px; transition: transform .06s ease, filter .2s ease; box-shadow: 0 8px 20px rgba(139,92,246,.22); }
      .btn:hover { filter: brightness(1.04); }
      .btn:active { transform: translateY(1px); }
      .switch { display: inline-flex; align-items: center; gap: 10px; color: var(--muted); font-weight: 600; }
      .switch input { accent-color: var(--accent); width: 18px; height: 18px; }
      .mono { white-space: pre-wrap; word-wrap: break-word; }
      .heading { font-size: 16px; font-weight: 800; color: var(--muted); letter-spacing: .3px; margin: 0 0 10px; }
      .footer { margin-top: 20px; color: var(--muted); font-size: 12px; text-align: center; }
      .toolbar { display: flex; gap: 8px; align-items: center; margin-bottom: 10px; }
      .chip { font-size: 12px; color: var(--muted); background: #fff; border: 1px solid var(--border); border-radius: 999px; padding: 4px 8px; }
      .copy { background: linear-gradient(90deg, var(--accent-3), var(--accent)); padding: 8px 12px; border-radius: 10px; color: white; font-weight: 700; border: none; cursor: pointer; box-shadow: 0 8px 18px rgba(251,113,133,.25); }
      .copy:hover { filter: brightness(1.03); }
      .toast { position: fixed; bottom: 20px; right: 20px; background: #0ea5e9; color: #fff; padding: 10px 14px; border-radius: 10px; box-shadow: var(--shadow); opacity: 0; transform: translateY(10px); transition: all .25s ease; }
      .toast.show { opacity: 1; transform: translateY(0); }
      .refresh { background: transparent; border: none; color: var(--muted); cursor: pointer; font-weight: 700; }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="hero">
        <div class="title">AI Text Humanizer</div>
        <button class="refresh" onclick="window.location.href='/'>Refresh</button>
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
          <div class="heading">Result</div>
          <div class="toolbar">
            <span class="chip">Humanized</span>
            <button class="copy" type="button" onclick="copyResult()">Copy</button>
          </div>
          <div id="resultText" class="mono">{{ result }}</div>
        </div>
        <div class="panel">
          <div class="heading">Original</div>
          <div class="mono" style="color: var(--muted">{{ original }}</div>
        </div>
      </div>
      {% endif %}

      <div class="footer">Runs locally. No data is sent to external services.</div>
    </div>

    <div id="toast" class="toast">Copied to clipboard</div>

    <script>
      function copyResult() {
        var el = document.getElementById('resultText');
        if (!el) return;
        var text = el.innerText || el.textContent || '';
        if (!text) return;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(showToast, showToast);
        } else {
          var ta = document.createElement('textarea');
          ta.value = text; document.body.appendChild(ta); ta.select();
          try { document.execCommand('copy'); } catch(e) {}
          document.body.removeChild(ta);
          showToast();
        }
      }
      function showToast() {
        var t = document.getElementById('toast');
        if (!t) return;
        t.classList.add('show');
        setTimeout(function(){ t.classList.remove('show'); }, 1500);
      }
    </script>
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = None
    preserve_headings = False

    if request.method == "POST":
        incoming_text = (request.form.get("text") or "").strip()
        preserve_headings = request.form.get("preserve_headings") == "1"
        if incoming_text:
            if preserve_headings:
                humanized, _ = humanizer.humanize_with_headings(incoming_text)
            else:
                humanized, _ = humanizer.humanize_text(incoming_text)
            # Store once in session (PRG)
            session['payload'] = {
                'result': humanized,
                'original': incoming_text,
                'preserve_headings': preserve_headings,
            }
        return redirect(url_for('index'))

    # GET: read once and clear so a refresh shows a clean page
    payload = session.pop('payload', None)
    if payload:
        result = payload.get('result')
        original = payload.get('original', '')
        preserve_headings = payload.get('preserve_headings', False)
    else:
        original = ""

    return render_template_string(
        PAGE,
        text="",  # keep textarea empty on GET/refresh
        result=result,
        original=original,
        preserve_headings=preserve_headings,
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False, threaded=True)
