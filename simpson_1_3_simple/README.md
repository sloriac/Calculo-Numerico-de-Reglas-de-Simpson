# Simpson 1/3 Simple Rule — Numerical Quadrature Suite

Implementation of the **Simpson 1/3 Simple Rule** for the CENFOTEC Cálculo
Diferencial e Integral project (Avance 2), built without any predefined
integration/derivation library primitives.

## Project structure

```
simpson_1_3_simple/
├── simpson/
│   ├── core.py            Main method: integrate() — the assigned algorithm
│   ├── reference.py       Self-built Romberg solver, used ONLY to obtain
│   │                      the "exact" value for error comparison
│   ├── metrics.py         compute_error() and benchmark() — error + timing
│   ├── experiments.py     Parameter sweeps producing the report's dataset
│   └── visualization.py   Interactive Plotly 3D + dashboard figures
├── main.py                 Runs everything end to end
├── requirements.txt
└── output/                 Generated on run: CSVs + interactive HTML files
```

## Why the code is organized this way

The rubric asks for three specific pieces — a main quadrature function, an
error-vs-exact-value function, and a timing/iteration function — so the
project is split into `core.py`, `metrics.py` accordingly, instead of one
monolithic script. Each algorithmic step inside `integrate()` is its own
small, clearly named function (`_compute_step_size`, `_generate_nodes`,
`_weighted_sum`), which is what documents the algorithm "paso a paso"
without relying on inline comments.

## An important design decision: no fixed `n`

Simpson 1/3 **Simple** always uses exactly 3 nodes / 2 subintervals — `n`
is not a free parameter for this variant (unlike the Compuesta version).
Since the rubric asks to study convergence as the number of partitions
changes, and that isn't possible here, the study instead varies the
**interval width `(b - a)`**, since `h = (b - a) / 2` is the quantity that
actually controls the truncation error:

```
E_t = -((b - a)^5 / 2880) · f⁽⁴⁾(ξ)
```

This is the same relationship already derived in the project's Marco
Teórico, so `experiments.py` sweeps interval widths and plots error on a
log-log scale to make that fifth-order relationship visible.

## Why `reference.py` exists

To compute the error you need a trustworthy "exact" value. For polynomials
this is trivial (closed-form antiderivative). For arbitrary functions,
`reference.py` implements **Romberg integration** from scratch (Richardson
extrapolation over the trapezoidal rule) purely as a validation oracle —
it is explicitly *not* the assigned method and is never used to produce
the reported quadrature result, only to check it.

## Running it

```bash
pip install -r requirements.txt
python main.py
```

This prints the node table, the single-run error report, and both sweep
tables to the terminal, and writes to `output/`:

- `interval_width_sweep.csv`, `polynomial_degree_sweep.csv` — raw data for
  the report's tables.
- `simpson_3d_view.html` — interactive 3D rendering of `f(x)`, the fitted
  Lagrange parabola, and the three quadrature nodes with their weights.
- `convergence_dashboard.html` — error vs. h, time vs. interval width, and
  error vs. polynomial degree (empirically showing third-order exactness).

Open the two `.html` files directly in a browser — fully interactive
(rotate, zoom, hover for exact values), no server required.

## Adapting to a different function or interval

Edit the top of `main.py`:

```python
LOWER_BOUND = 0.0
UPPER_BOUND = 2.0

def demo_function(x: float) -> float:
    return x**2 + 2 * x + 4
```

Everything downstream (nodes, error, benchmarking, visualizations) adapts
automatically.
