"""Brewery consultancy guides, bylined to the mentor who leads that work.
Every CTA opens the enquiry form with Brewery consultancy pre-selected."""
import datetime

from make_corporate_plan import append_segment

R, A = "mentor-rahul-baliyan.html", "mentor-ankur-napa.html"
PLAN = {"Consultancy": f"""brewhouse-commissioning-checklist|Commissioning a new brewhouse: what to check before the first brew|c|{R}
first-100-days-of-a-new-brewpub|The first 100 days of a new brewpub|c|{R}
raising-brewhouse-yield|Raising brewhouse yield without changing the beer|c|{R}
clean-german-lager-in-an-indian-brewpub|Brewing a clean German lager in an Indian brewpub|c|{R}
sourcing-malt-and-hops-in-india|Sourcing malt and hops for an Indian brewery|c|{R}
beer-tastes-different-every-batch|Why your beer tastes different every batch|c|{R}
daily-excise-routine-for-brewpubs|A daily excise routine for brewpubs|c|{R}
when-to-hire-a-consultant-brewmaster|When to hire a consultant brewmaster and what to expect|d|{R}
what-a-brewery-health-check-covers|What a brewery health check covers|d|{A}
brewery-loss-audit|Finding the beer you are losing: a brewery loss audit|c|{A}
tap-list-planning-with-sales-data|Planning your tap list with sales data|c|{A}
weekly-numbers-for-brewpub-owners|The weekly numbers every brewpub owner should see|c|{A}
turning-around-a-struggling-brewpub|Turning around a struggling brewpub|d|{A}
quality-system-for-a-small-brewery|Building a quality system in a small brewery|c|{A}
starting-a-cider-line-in-india|Starting a cider line in India|c|{A}
launching-a-hard-seltzer|Launching a hard seltzer: base, filtration and flavour|c|{A}
planning-a-craft-distillery-in-india|Planning a craft distillery in India|c|{A}
getting-new-make-spirit-right|Getting new make spirit right before it goes into cask|c|{A}
planning-a-small-winery-in-india|Planning a small winery in India|c|{A}
how-fortified-wines-are-made|Fortified wine: how port-style and sherry-style wines are made|a|{A}
new-product-development-for-drinks|New product development for drinks, from brief to launch|c|{A}
low-and-no-alcohol-production-routes|Low and no alcohol drinks: production routes compared|a|{A}
contract-brewing-quality-agreement|Writing a contract brewing quality agreement|c|{R}
scaling-a-pilot-recipe-to-production|Scaling a pilot recipe to a production brewhouse|c|{R}
where-ai-helps-a-small-brewery|Where AI helps a small brewery and where it does not|a|{A}
consultant-or-full-time-head-brewer|Consultant or full-time head brewer?|d|{A}"""}

if __name__ == "__main__":
    append_segment("Drinks producers", "contact.html?course=Brewery%20consultancy#enroll", PLAN,
                   datetime.date(2026, 7, 6), datetime.date(2026, 10, 2))
