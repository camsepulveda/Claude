# Health Front landing page — working notes

Generated 2026-11-01 from the brief "Clarity to move healthcare forward". Source of truth for copy is `index.html`
(English and Spanish inline, toggled by `html[lang]`). Brand voice reference: `.claude/brand-voice-guidelines-healthfront.md`.

## What was inspected, and what could not be
- The live page at healthfrontgroup.com could not be loaded from the build environment (outbound network is
  restricted to connected services). What Netlify reports about it: one manually uploaded deploy from 2026-03-20,
  a single ~8 KB HTML file, no redirects, headers or functions, forms not enabled, no favicon, no robots.txt, and the
  homepage is the only URL that returns 200. Every other request in the logs is a WordPress vulnerability scanner.
- Brand materials used: the Health Front logo (SVG and PNG), the 2026 Illinois licensure proposal, the 2023 corporate
  presentation (mission, vision, values, founding year, service list), the 2024 CC Program deck, the 2023 and 2024
  licensing proposals, and the credential intake form.

## Positioning and design weaknesses in the prior state (from what is observable)
1. No service architecture: a single page with no way to tell what Health Front does or who it is for.
2. No proof or process: nothing a prospective client can picture.
3. No conversion path: forms were never enabled on the Netlify site; no form, no scheduling action.
4. No hygiene signals: missing favicon, robots.txt, security headers, canonical, Open Graph.
5. Identity drift across materials: Health Front / HealthFront / HF Group / Health Front Group; healthfrontpr.com and
   healthfrontgroup.com; three different titles for the same executive.

## Creative concept
**An executive briefing brought to life.** The page reads like a well-set briefing document: a left-weighted
asymmetric grid, generous margins, serif display type (Newsreader) against a plain working sans (Public Sans) with a
monospace utility face (IBM Plex Mono) for labels, status and dates. Warm paper neutrals; the logo's navy is the only
brand hue. Semantic status colors (complete / waiting on third party / needs action) appear only inside information
graphics and never as decoration. They were validated with the dataviz palette checker for colorblind and
normal-vision separation in both themes (light #166A4E / #A07000 / #B22D2D, dark #5FCB9E / #F5C542 / #FF8B8B);
status text is set in ink, never in the status color, so small labels keep AA contrast.

**Signature visual: the Readiness Map.** Built in HTML so it reflows to a vertical rail on phones. Five stations from PR license to "ready to bill", with a dashed dependency
showing privileges waiting on license and malpractice, status under each node, and a two-line "next actions" strip
naming an owner and a date. A compass mark sits top-right, echoing the north notch in the logo monogram and the
tagline "Value is our North". Content is fictional and labeled illustrative, in both languages.

Nothing on the page uses stock photography, gradients, decorative crosses or rounded card grids. Repeated structural
devices encode real structure: the four numbered stages are a real sequence; the tracker is a real table.

## Service architecture (revised 2026-11-01, second pass)
Three tabs: **Launch 1 · From license to opening practice** (licensing, credential file, Medicare/Medicaid, commercial
plans, privileges, coordination), **Launch 2 · Understanding my numbers** (payer performance dashboard from the biller's
data, refreshed monthly, quarterly report, fixes ranked by dollars), **Continuity · Keep your team on the same page**
(one point of contact, weekly one-page status, renewals and credential upkeep, representation). Advisory stays a
paragraph. The form's needs groups mirror these.

## Service architecture (decided 2026-11-01, first pass, superseded above)
- **Launch**: from license to opening practice. The core, fixed fee per physician. Services 1 and 2 on the page.
- **Continuity**: credentials kept current, renewals tracked, and a quarterly payer performance report (which
  contracted plans pay, at what lag, where enrollment errors drive denials). Recurring. Service 3 on the page.
- **Advisory**: practice operations, partnership structures, payment-model design. By engagement, for existing
  clients. One paragraph under the services and one FAQ answer; not in the navigation.
- Recruitment is treated as a lead source for Launch (physicians relocating to the island), not a listed service.

## Color and interaction (added 2026-11-01, second review)
- **Brass accent** (`--brass`, #8A5E12 light / #E0B65A dark) on eyebrows, the compass, the tagline line and step
  numbers only. It is the "north" color; it never fills a surface or a button.
- **Navy chapter**: the Approach section is a full-bleed navy band with paper text, so the page has a dark middle.
- **"Where are you right now?"** chips under the hero re-light the readiness map for six situations, settle the
  compass, and pre-select the same situation in the contact form. All map content stays labeled illustrative.
- **Compass rose background** in the hero: an inline SVG (three rings, 32 ticks, cardinal lines, a north notch like
  the logo) at about 8% opacity, navy on paper and brass on dark, anchored right behind the map panel.
- **Nine situations** in the hero and the form: finishing training, returning to the Island, adding physicians,
  licensing in another state, established with pending items, making sense of billing reports, a special project or
  contract, getting consultants to communicate, not sure. Each has its own stations, statuses, next actions and
  dependency line in both languages.
- **Services as tabs** (accordion on phones), each with an illustrative example story.
- **Form disclosure**: the needs list is hidden until a situation is chosen; then the needs that situation usually
  implies are pre-ticked and shown with "help me decide", the rest behind "Show all options". Two needs added:
  "one point of contact for my consultants" (Continuity) and an Advisory group (special project; operations or
  payment-model design).
- **Example strips**: each service example is a small HTML timeline (ten weeks; September to January) or a six-month
  payment chart (the ninety-day case), fictional and labeled, using the validated status colors with text labels.
- **Guided intake form**: situation chips, plain-language needs grouped Launch / Continuity, scale and timing, and a
  live "Your request, as we will read it" summary that is posted with the form as the `summary` field, with the
  page language as `language`. Validation requires a situation or at least one need plus contact details.

## Report vocabulary (2026-11-01)
The "Understanding my numbers" tab uses the column names of the billing reports practices in Puerto Rico actually
receive from their biller's system: Facturación vs Cobro (Período, Recl., Cargos, Co-Pagos, Pagos, Ajustes, Balance,
%), Envejecimiento Reclamaciones Planes Médicos (0-30, 31-60, 61-90, 91-120, >121, Total, claim counts), Análisis de
Producción by CPT (Recl., Pacientes, Servicios, Cargos, Pagos, Razón Facturado) and an encounters report (new vs
follow-up, studies, stress tests). Four sample reports were reviewed for vocabulary only. No client name, provider
name, plan balance or figure from them appears on the page; the aging table and KPIs are fictional and labeled so.

## Copy decisions
- Hero follows the brief's headline and subhead, tightened. CTAs: "Discuss your practice" / "Explore our approach".
- "Health Front" (two words) throughout, matching the wordmark; "Health Front LLC" in legal lines. The brief wrote
  "Healthfront"; see confirmation 1.
- Services are limited to what the source documents show Health Front has sold: PR licensing and registry, specialty
  and telemedicine certification, out-of-state licensure by endorsement, NPI/DEA/ASSMCA/malpractice/government
  certificates, notarization, Medicare PTAN and Medicaid PEP enrollment, commercial payer credentialing and
  contracting, hospital privileges, coordination with biller/accountant/hospital/group, and ongoing credential
  maintenance during a contracted year.
- The four-stage approach is assembled from the 2026 proposal's workstreams and the 2024 deck's "How it works";
  see confirmation 4 before calling it the established method.
- Spanish is written natively in formal *usted*, per the brand guidelines' recommendation for Health Front.

## Factual details that still need confirmation before public launch
1. **Public name spelling.** Page uses "Health Front" to match the logo. The brief used "Healthfront". Pick one.
2. **Email.** Page shows cmendez@healthfrontgroup.com as a temporary measure (owner's decision, 2026-11-01) while
   the admin inbox is set up. Replace with the shared address when ready; it appears in the contact block, the form
   fallback line and the form error message, in both languages. Set the same address as the Netlify Forms notification.
3. **Phone number.** Omitted. The only number in the materials is a 2023 personal line. Add if a business line exists.
4. **Engagement method.** The four stages, the five-business-day checklist and the biweekly status cadence come from
   one 2026 proposal. Confirm they are standard on every engagement, or soften to "typically".
5. **Two-business-day reply promise** in the contact section. Confirm the team can meet it.
6. **Carlos's bio.** Verified: JD, MHSA, MPH; Managing Member and CEO of Health Front LLC; COO of TCT Oncology;
   company founded 2019; based in Guaynabo. Not verified: the sentence about "years inside Puerto Rico's health system
   watching physicians leave" is an interpretation of the 2024 deck's language and should be approved or rewritten.
   Confirm he wants the TCT Oncology role on this page. No portrait was available; initials mark used.
7. **"Licensed health services administrators"** appears in the 2024 deck. Confirm it is still true of the current team.
8. **Hospital and payer names.** Deliberately not listed on the page. The 2024 deck names specific hospitals and plans;
   add them only if current and if their logos may be used.
9. **Scheduling action.** The brief asked for a scheduling link. None exists in the materials, so "Discuss your
   practice" leads to the form. Provide a Calendly or similar URL to add a direct booking button.
10. **Broader services** from the 2023 deck (revenue cycle, managed-care consulting, strategic planning, M&A, new
    practice setup) are excluded until confirmed as currently offered.
11. **Payer performance report.** Added at the owner's direction as the Continuity upsell. Not yet delivered to a
    client per the materials. Before launch confirm: (a) it can be produced from the biller's data in the next
    engagement; (b) handling claims data means PHI, so a business associate agreement and a security posture are
    required before the first report. If either is not ready, soften the bullet to "available on request".
12. **Legal footer** says Health Front "does not provide legal or medical services". Taken from the 2026 proposal's
    disclaimer; have counsel confirm the wording.

## Deployment
- Repo-root `netlify.toml` sets base and publish to `healthfront-site/` plus security headers and asset caching; it overrides the Netlify UI directories.
- The contact form uses Netlify Forms (`data-netlify="true"`, honeypot field). Enable Forms on the Netlify site and
  set a notification email after the first deploy, then submit one test message.
- The site has not been deployed from this change. Deploying replaces the current production page; roll back is
  available from the Netlify deploy history.
