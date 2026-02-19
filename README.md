# ISS Three.js Viewer

This repo hosts a Three.js viewer for an ISS model, plus Blender helper scripts for inspecting and fixing materials/normals.

## Quick Start
1. Open `index.html` in a local web server.
2. The viewer loads the optimized model: `International Space Station (ISS).draco.glb`.

## Asset Pipeline
Recommended model flow:
1. Authoring source: `.blend`
2. Optimized delivery: `.glb` with Draco compression

## Optimization Scripts
Run these from the repo root:
```bash
npm run optimize
npm run draco
npm run webp
npm run etc1s
npm run uastc
```

Recommended output for the viewer:
- `International Space Station (ISS).draco.glb` (best size in this repo)

## Git LFS
Large binary assets are tracked with Git LFS via `.gitattributes`.
