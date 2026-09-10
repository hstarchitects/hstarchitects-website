Put the two client profile PDFs here so tools/build_images.py can regenerate the
image set from source:

  HST GROUP PROFILE.pdf
  company profile ELEGANT LINES.pdf

These are client documents. They are git-ignored and excluded from the deployment.

Put the supplied plan-drawing set in source/blueprints/ so tools/build_plans.py can
regenerate the background texture. Fourteen transparent PNGs, seven drawings in two
inks:

  architectural-blueprint[-NN-name]-graphite-transparent.png   -> light theme
  architectural-blueprint[-NN-name]-white-transparent.png      -> dark theme
