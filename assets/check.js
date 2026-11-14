// Interactive answer widgets. Inlined into each page by build.py.
//
// 1. Numeric inputs, checked together:
//   <div class="check-group" data-ok="message when all right">
//     <input data-answer="1/30" data-tol="0.002"> ...
//     <button class="check">Verificar</button><div class="feedback"></div></div>
//   Answers use a decimal point; typed values accept "0.392" or "0,392" or fractions ("1/30").
//   data-tol is an absolute tolerance (default 0.002).
//
// 2. Bayesian update table that multiplies for you (build.py: bayes_table()):
//   <table class="bayes-auto"> rows <tr data-h> with input.prior, input.lik and a cell .num;
//   a cell .pd gets the sum of the numerators. Fractions stay exact while every input is a fraction.
(function () {
  function parseNum(s) {
    s = String(s).trim().replace(",", ".");
    if (s === "") return NaN;
    if (s.indexOf("/") >= 0) {
      var p = s.split("/");
      return Number(p[0]) / Number(p[1]);
    }
    return Number(s);
  }

  document.querySelectorAll(".check-group").forEach(function (g) {
    var fb = g.querySelector(".feedback");
    var checkBtn = g.querySelector("button.check");

    // "Mostrar gabarito" fills every answer (for later review); clicking again clears them.
    var key = document.createElement("button");
    key.className = "check reveal";
    key.type = "button";
    key.textContent = "Mostrar gabarito";
    checkBtn.insertAdjacentElement("afterend", key);
    key.addEventListener("click", function () {
      var show = key.textContent === "Mostrar gabarito";
      g.querySelectorAll("input[data-answer]").forEach(function (inp) {
        inp.value = show ? inp.dataset.answer : "";
        inp.classList.remove("right", "wrong");
        inp.classList.toggle("revealed", show);
      });
      g.querySelectorAll("table.bayes-auto").forEach(function (t) { t.dispatchEvent(new Event("input")); });
      key.textContent = show ? "Limpar" : "Mostrar gabarito";
      fb.style.display = "none";
    });

    // "Preencher anteriores" fills only inputs marked .carry (values computed in an earlier exercise).
    var carried = g.querySelectorAll("input.carry");
    if (carried.length) {
      var carry = document.createElement("button");
      carry.className = "check reveal";
      carry.type = "button";
      carry.textContent = "Preencher anteriores";
      checkBtn.insertAdjacentElement("beforebegin", carry);
      carry.addEventListener("click", function () {
        carried.forEach(function (inp) {
          inp.value = inp.dataset.answer;
          inp.classList.remove("right", "wrong");
        });
        g.querySelectorAll("table.bayes-auto").forEach(function (t) { t.dispatchEvent(new Event("input")); });
      });
    }

    checkBtn.addEventListener("click", function () {
      var inputs = g.querySelectorAll("input[data-answer]");
      var ok = 0;
      inputs.forEach(function (inp) {
        var tol = inp.dataset.tol ? Number(inp.dataset.tol) : 0.002;
        var got = parseNum(inp.value);
        var right = !isNaN(got) && Math.abs(got - parseNum(inp.dataset.answer)) <= tol;
        inp.classList.remove("right", "wrong");
        inp.classList.add(right ? "right" : "wrong");
        if (right) ok++;
      });
      var all = ok === inputs.length;
      fb.className = "feedback " + (all ? "correct" : "incorrect");
      fb.style.display = "block";
      fb.innerHTML = all
        ? "✅ " + (g.dataset.ok || "Tudo certo.")
        : "❌ " + ok + " de " + inputs.length + " certos. Refaça só os vermelhos.";
    });
  });

  // Exact fraction [num, den] for "a/b" or an integer; null for a decimal like "0.25".
  function frac(s) {
    s = String(s).trim();
    var m = s.match(/^(-?\d+)\s*\/\s*(\d+)$/);
    if (m && Number(m[2]) !== 0) return [Number(m[1]), Number(m[2])];
    if (/^-?\d+$/.test(s)) return [Number(s), 1];
    return null;
  }
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); for (; b; ) { var t = b; b = a % b; a = t; } return a || 1; }
  function reduce(f) { var g = gcd(f[0], f[1]); return [f[0] / g, f[1] / g]; }
  function dec(v) { return v === 0 ? "0" : String(Number(v.toPrecision(4))); }
  function show(f, v) {
    if (f && f[1] === 1) return String(f[0]);
    return f ? f[0] + "/" + f[1] + " ≈ " + dec(v) : dec(v);
  }

  document.querySelectorAll("table.bayes-auto").forEach(function (t) {
    var rows = t.querySelectorAll("tr[data-h]");
    var pd = t.querySelector(".pd");
    function update() {
      var sum = 0, sumF = [0, 1], exact = true, filled = 0;
      rows.forEach(function (r) {
        var ps = r.querySelector("input.prior").value, ls = r.querySelector("input.lik").value;
        var out = r.querySelector(".num");
        var pv = parseNum(ps), lv = parseNum(ls);
        if (isNaN(pv) || isNaN(lv)) { out.textContent = ""; exact = false; return; }
        filled++;
        sum += pv * lv;
        var pf = frac(ps), lf = frac(ls);
        if (pf && lf) {
          var f = reduce([pf[0] * lf[0], pf[1] * lf[1]]);
          sumF = reduce([sumF[0] * f[1] + f[0] * sumF[1], sumF[1] * f[1]]);
          out.textContent = show(f, pv * lv);
        } else {
          exact = false;
          out.textContent = dec(pv * lv);
        }
      });
      pd.textContent = filled === rows.length ? show(exact ? sumF : null, sum) : "";
    }
    t.addEventListener("input", update);
  });

  // 3. A value carried to a later item: <input data-name="c" data-answer="3"> fills every
  //    <span data-show="c">c</span> with the typed value once it is right; otherwise the letter stays.
  var named = document.querySelectorAll("input[data-name]");
  function showNamed() {
    named.forEach(function (inp) {
      var tol = inp.dataset.tol ? Number(inp.dataset.tol) : 0.002;
      var got = parseNum(inp.value);
      var right = !isNaN(got) && Math.abs(got - parseNum(inp.dataset.answer)) <= tol;
      document.querySelectorAll('[data-show="' + inp.dataset.name + '"]').forEach(function (s) {
        s.textContent = right ? inp.value.trim() : inp.dataset.name;
        s.classList.toggle("shown", right);
      });
    });
  }
  if (named.length) {
    document.addEventListener("input", showNamed);
    document.addEventListener("click", showNamed); // "Mostrar gabarito" / "Limpar" set values without an input event
  }
})();
