# Furnace from furnace.png

New standalone mesh model based on Allen's supplied reference, built 2026-10-20. Existing Forge assets and the Studio place were not modified.

## Files

- `Furnace_Reference.fbx`: primary Roblox import file, with embedded colour texture.
- `Furnace_Color.png`: external 1024 × 1024 colour atlas, also supplied for relinking.
- `Furnace_Reference.blend`: editable Blender source with packed texture and preview camera/lighting.
- `Furnace_Reference.glb`: portable alternative for other 3D applications.
- `Furnace_Preview.png`: front/right/top render of the actual model.
- `Furnace_Rear_Preview.png`: rear/left render of the actual model.
- `build_furnace.py`: reproducible model builder, using Blender's Python API.
- `mesh-report.json`, `export-verification.json`: geometry checks and export round-trip results.

## Model

Six named meshes: Stone, Iron, Rivets, Grilles, Interior, Embers. Total 4,816 triangles. One UV set per mesh, one shared colour atlas. The Ember material also uses the atlas for emission in Blender/GLB.

The front fire mouth, upper slit, three roof slots and side vent are built as geometry openings with recessed interiors. The rear is inferred from the single supplied view. Decorative components are joined by role; the source builder retains their construction definitions.

Nominal bounds are about 6.945 wide × 5.485 deep × 6.630 high in project modelling units. Base-centred pivot; Blender front is -Y and vertical is +Z. Applied mesh scale; no rig, animation, cameras, preview ground, or lights in the exports. The editable .blend includes the preview scene; choose only the six Furnace meshes and their root when re-exporting.

## Import in Roblox Studio

1. Use **File → Import**, select `Furnace_Reference.fbx`, and inspect the model preview.
2. Enable **Anchored** and keep **Merge Meshes** disabled to preserve the removable Embers mesh.
3. Review Scale Unit and dimensions. The intended workshop prop height is approximately 6.63 studs; adjust import scale if Studio's unit conversion gives a different size.
4. Check that the colour texture is detected. If necessary, upload/relink the supplied `Furnace_Color.png` as the mesh colour texture.
5. After import, disable collision on the decorative grille, rivet and ember pieces. Use simple invisible collision boxes for the furnace body if needed.
6. Add runtime fire light/particles in Studio, or replace/hide `Furnace_Embers`. The preview's warm light is scene lighting, and FBX material emission does not supply a Roblox PointLight. This is an art asset; it contains no heating gameplay, prompts or interaction scripts.

Import options checked against [Roblox Importer documentation](https://create.roblox.com/docs/studio/importer). Exported files are checked by reimport into Blender; live Studio import, collision and gameplay integration are not verified in this session.

## Rebuild

Run Blender in background mode with `--python build_furnace.py`, then `--python verify_export.py`. The builder writes the art files alongside the script and renders both preview angles.
