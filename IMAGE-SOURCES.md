# Original marketing imagery

The approved page containers, classes, image placements, typography and video sources are retained. Replacement image canvases preserve the previous aspect ratios. Background changes are limited to warm ivory and a faint lavender tint; existing purple and pink accents remain.

## Generated assets

Built-in imagegen was used for these new assets in `www.lassomd.com/brand-assets/`:

- `clinic-website-preview.webp`: original laptop, smartphone and clinic website collage, fictional dental/chiropractic/optometry screens, professional male providers, pale ivory background, purple and rose accents, no Lasso branding.
- `ads-phone-generated.webp`: realistic upright phone with a fictional Cedar Clinic search advertisement, professional male doctor, purple booking button and pale ivory background.
- `clinic-branding-generated.webp`: original Cedar Clinic stationery, brochure, appointment cards and tablet website presentation, male provider photo, ivory/lavender/rose palette.

Prompt set: generate premium realistic marketing artwork in those compositions, with original fictional clinic interfaces and no real clinic logos, Lasso branding or watermarks. These images are illustrative concepts, not actual client websites or employees.

Previously generated `clinic-team.webp` and `clinic-professional.webp` are reused, as requested. Other original SVG assets depict scheduling, search, phone and campaign interface concepts. Figures in these illustrations are sample data. `service-frame-*` and `fitted-*` files embed the original artwork within the existing image dimensions, without changing HTML layout.

Real integration-platform logos and existing videos are retained. Archived articles, third-party case studies and external template previews have not been comprehensively reworked; this is not a claim that every historical asset on the mirrored site has been replaced.

## Consistency update — 15 October 2026

The ten active marketing/service pages now share a 6:5 hero media frame, 30px corners and responsive sizing. This update deliberately standardizes the hero markup; existing body section layouts are retained except for the newly illustrated After Hours Voice sections and obsolete layered phone artwork.

New imagegen assets in `brand-assets/consistent/`:
- `brand-direction.webp`: original premium photorealistic studio consultation, male and female designers reviewing a clinic identity mood board, ivory/lavender/rose palette.
- `brand-logo.webp`: original Willow Clinic leaf-mark sketches and embossed logo presentation, premium paper and soft natural light.
- `brand-cards.webp`: original Willow Clinic business-card stationery composition, ivory paper, lavender accents, professional photographic styling.
- `brand-signage.webp`: original Willow Clinic reception signage and standing display in a welcoming contemporary interior.

All four prompts requested fictional clinic branding, distinct compositions, no Lasso branding, no real clinic logos or watermarks. These are illustrative concepts, not actual client projects. The previous gender restriction is withdrawn.

The SVG service graphics are original code-authored illustrations, reproducible with `scripts/build_service_visuals.py`. The looping appointment video is rendered from `www.lassomd.com/visuals/appointment-demo.html`, using its `renderFrame(t)` function. It shows an illustrative conversation, not a live booking or a product capability guarantee. The conversation loops in approximately five seconds, with player controls hidden as requested and reduced-motion handling retained.

Validation: browser audit of 69 marketing/editorial routes at 1440px and 390px; focused image-load, overflow and hero-size checks on the ten active marketing pages. Archived articles and resource-library thumbnails retain their editorial structure; template previews are separate websites. Matching responsive copies of the same logical section may share an asset.

## Supplied specialty screenshot strip — 15 October 2026

The 22 JPEG screenshots supplied by the user (`01_dental_bright_smiles` through `22_sleep_clinic_restwell`) are copied unchanged into `brand-assets/specialty-screenshots/`. The homepage uses every screenshot once per scrolling group, with a second identical group for the existing continuous animation. Full screenshots are fitted inside small landscape thumbnails; these are website examples, not claims of client engagements.

Homepage hero updated to the user-supplied “WhatsApp Image 2026-10-15 at 3.49.35 AM.jpeg”, copied unchanged as `brand-assets/clinicsoftware-never-miss-booking.jpg`. The full concept screenshot is contained without cropping in the existing hero frame.
