# Source-only prepared adapter

`provider.mjs` and `server.mjs` are the exact accepted local canonical pair. They are versioned for the prepared implementation, not deployed. All files here are outside `app`; `.vercelignore` excludes this entire directory. No key, active `.env`, participant export or runtime database is included.

`node source/dream-backend/serve.mjs` starts the loopback rehearsal using shared `app/dream` assets and forces live OFF before provider construction. `planner.js` and `fixtures/prepared.js` are thin shared-domain re-exports. The public browser still has no live config/API requests. Direct canonical `server.mjs` assumes canonical sibling assets absent from this lean source folder; use `serve.mjs`. Programmatic direct adapter configuration is separate deliberate developer work; no activation is performed or implied by this publication. `config.env.example` contains only false/blank values. Contracts: `../../docs/dream/contracts/`.

Node18+ source tests: `node --test source/dream-backend/tests/*.test.mjs`. They use ephemeral loopback and synthetic mock transport, never a real provider. This does not demonstrate model quality, measured cost, authentic consent or learner outcomes.
