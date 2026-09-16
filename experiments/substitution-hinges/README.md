# Substitution Hinges

A dependency-light toy probe of a question from Ren's September 16 journal:
can a memory controller survive plausible substitutions, or does it only notice
when evidence fields are empty?

The stream contains clean relation observations plus four attacks:

- `wrong_evidence`: a confident, wrong endpoint with a damaged route;
- `near_authority`: a correct endpoint from an almost-valid authority;
- `stale_trace`: a correct endpoint whose freshness is low;
- `shifted_domain`: a plausible endpoint from a changed domain.

`endpoint_only` uses endpoint/evidence strength and mostly ignores the route.
`hinge_aware` gates updates by evidence, authority, freshness, and route, and
becomes conservative under domain shift. Both are evaluated during assistance
and after support removal on a fresh shifted-domain stream.

## Run

```bash
/usr/bin/python3 substitution_hinges.py --seeds 120 --out results.json
```

The experiment is deliberately mechanistic, not evidence about real neural
systems. Its purpose is to make the substitution failure mode measurable.
