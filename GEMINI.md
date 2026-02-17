# ISS Visualization - Development Log

## Project Overview
Interactive 3D visualization of the International Space Station (ISS) using Three.js, featuring granular part selection and Wikipedia integration.

## Known Model Issues
*   **Zvezda_SM Rendering (FIXED):** The module appeared see-through due to incorrect material settings.
    *   **Fix:** Changed Material Blend Mode from `Blended` to `Dithered` (Hashed) and ensured Backface Culling was disabled. Also recalculated normals to point outward.
*   **Model Duplication (FIXED):** The Blender scene contained two major `SSREF_IGOAL` hierarchies.
    *   **Fix:** Re-imported original NASA model and deleted all duplicated hierarchies.

## Memory & Performance Optimizations (In Progress)
The transition to the high-detail `International Space Station (ISS).glb` (91MB Draco compressed) resulted in high browser memory usage (~3.1 GB). Implementing KTX2 texture compression successfully reduced this to ~2.1 GB. The following optimization strategies have been identified:

### 1. GPU Texture Compression (KTX2 / Basis Universal) - COMPLETED
*   **Problem:** Standard JPEG/PNG/WebP textures decompress into raw bitmaps in VRAM, consuming massive amounts of VRAM.
*   **Solution:** Convert textures to KTX2/Basis Universal formats.
*   **Impact:** Stays compressed on the GPU, typically reducing VRAM usage by 5x-10x.
*   **Tooling:** `gltf-transform`.
*   **Method Used:**
    1.  **Intermediate PNG Conversion:** `gltf-transform` may fail when converting WebP directly to KTX2. First, convert all WebP textures to PNG:
        ```bash
        npx gltf-transform png "International Space Station (ISS).glb" "ISS_png.glb" --formats webp
        ```
    2.  **KTX2 (UASTC) Conversion:** Convert the PNG textures to KTX2 UASTC. Note: Higher `--level` values (e.g., 4) provide better quality but take longer.
        ```bash
        npx gltf-transform uastc ISS_png.glb ISS_ktx2.glb --level 0 --slots "*"
        ```
    3.  **Re-apply Draco Compression:** The previous steps may result in uncompressed geometry. Re-apply Draco to minimize file size:
        ```bash
        npx gltf-transform draco ISS_ktx2.glb "International Space Station (ISS)_ktx2.glb"
        ```

### 2. Level of Detail (LOD)
*   **Approach:** Implement `THREE.LOD` to swap between high, medium, and low-poly versions of components based on camera distance.
*   **Implementation:** Requires pre-generated simplified geometries. runtime simplification using `SimplifyModifier` is possible but CPU-intensive for models of this scale.

### 3. Code-Level Efficiency - PARTIALLY COMPLETED
*   **Pixel Ratio Capping (DONE):** Limited `renderer.setPixelRatio` to `Math.min(window.devicePixelRatio, 2)`.
*   **On-Demand Rendering (DONE):** Modified `animate` loop to only render when `OrbitControls` change or a `needsRender` flag is set (e.g., resizing, clicks). This significantly reduces idle CPU/GPU usage.
*   **Backface Culling (PENDING/TEMPORARILY DISABLED):** Forced `material.side = THREE.FrontSide`. Currently disabled to avoid visual issues with some modules.
*   **Material Sharing:** Ensure that multiple meshes using the same texture properties share a single `THREE.Material` instance rather than creating duplicates.
*   **Resource Disposal:** Explicitly call `.dispose()` on geometries and materials when swapping models to prevent memory leaks.

## Storage & Persistence Optimizations - COMPLETED
*   **Debounced State Saving (DONE):** Switched camera view state saving from the `change` event to the `end` event of `OrbitControls`. This ensures `localStorage` is only updated once the user finishes their interaction.

## Current Selection Logic
*   **Granular Selection:** The `onPointerClick` logic walks up the hierarchy from the intersected mesh.
*   **Filter:** Nodes containing "details" in their name are skipped.
*   **Stop Condition:** The logic selects the first non-detail parent or stops at the children of `SSREF_IGOAL` (the major module level).
