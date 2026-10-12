"""Seasonal dressing. Oktoberfest runs until the Brewing Fundamentals batch starts;
the date check below switches it off by itself after that. The decorations live
in pages_a.OKT; to retire them, empty OKT and GATE."""

UNTIL = "2026-10-18T00:00:00+05:30"

# Runs in <head> so the decorations are on before first paint.
GATE = f"<script>if(new Date()<new Date('{UNTIL}'))document.documentElement.classList.add('okt')</script>"
