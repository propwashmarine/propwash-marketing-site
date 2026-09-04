# Propwash Marine website

Production-ready static website for Propwash Marine Detailing. The site uses the approved V4 design, local production media, a looping hero video, an interactive walkthrough rail, responsive interactions, and separate quote and membership inquiry flows.

## Files

- `index.html` — deployable site
- `thank-you.html` — confirmation page for quote and membership submissions
- `dist/` — clean publishing folder containing only the live site and required media
- `assets/v4/` — optimized production photography
- `assets/video/hero-v4.mp4` — full-resolution looping hero video
- `assets/video/wajer-walkthrough.mp4`, `gelcoat-reflections.mp4`, `water-beading.mp4` — optimized walkthrough videos
- `assets/logo/` — supplied Propwash logo assets and favicon
- `src/v4-template.html` — editable design source
- `src/media-derived/` — accurate renders used for supplied HEIC media and the Owner Portal image
- `build_live.py` — rebuilds `index.html` and optimized media from the source template
- `netlify.toml`, `robots.txt`, `sitemap.xml` — hosting and search configuration

## Forms

The standard quote form posts as `quote-request`. The tier-specific membership form posts as `membership-inquiry` and includes the selected Silver, Gold, or Platinum plan. Both are configured for Netlify Forms and redirect to `/thank-you.html` after submission.

When the folder is deployed on Netlify, enable form-detection notifications or connect the submissions to the Propwash CRM workflow.

## Rebuilding

Run the builder with the system Python and macOS image tools:

```sh
python3 build_live.py
```

The builder expects the supplied media library at `/Volumes/Jack's Hard Drive/Propwash/Website Media`.
