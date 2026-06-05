#!/usr/bin/env python3
"""Generate README.md and the Notion CSV for the Free Icon Resources list.

Single source of truth: the GROUPS structure below. Numbering and the CSV are
derived from it so they never drift, mirroring the 400-free-design-resources repo.
"""
import csv
import re

# group -> category -> [ (name, url, description), ... ]
GROUPS = {
    "Icon Libraries": {
        "Open-Source Icon Sets": [
            ("Lucide", "https://lucide.dev", "Community fork of Feather — 1,400+ consistent open-source icons"),
            ("Feather Icons", "https://feathericons.com", "280+ simply beautiful open-source stroke icons"),
            ("Heroicons", "https://heroicons.com", "Tailwind's MIT SVG icons in outline & solid"),
            ("Tabler Icons", "https://tabler.io/icons", "5,800+ free MIT stroke-based icons"),
            ("Phosphor Icons", "https://phosphoricons.com", "9,000+ flexible icons across 6 weights"),
            ("Remix Icon", "https://remixicon.com", "2,800+ neutral-style open-source system icons"),
            ("Bootstrap Icons", "https://icons.getbootstrap.com", "2,000+ MIT icons from the Bootstrap team"),
            ("Ionicons", "https://ionic.io/ionicons", "Premium open-source icons by the Ionic team"),
            ("Material Symbols", "https://fonts.google.com/icons", "Google's 3,400+ variable Material Design icons"),
            ("Eva Icons", "https://akveo.github.io/eva-icons", "480+ open-source icons in outline & fill"),
            ("Boxicons", "https://boxicons.com", "1,600+ simple open-source web icons"),
            ("Iconoir", "https://iconoir.com", "1,500+ free MIT hand-crafted SVG icons"),
            ("CSS.gg", "https://css.gg", "700+ open-source icons in SVG, CSS & Figma"),
            ("Unicons", "https://iconscout.com/unicons", "1,000+ free vector icons by Iconscout"),
            ("Teenyicons", "https://teenyicons.com", "Tiny minimal 15×15 outline & solid icons"),
            ("Pixelarticons", "https://pixelarticons.com", "Free pixel-perfect retro icon set"),
            ("Majesticons", "https://majesticons.com", "760+ clean line & solid MIT icons"),
            ("Akar Icons", "https://akaricons.com", "Minimal, perfectly rounded open-source SVG icons"),
            ("Octicons", "https://primer.style/octicons", "GitHub's open-source UI icon set"),
            ("Carbon Icons", "https://carbondesignsystem.com/elements/icons/library", "IBM Carbon's open-source icon library"),
            ("Radix Icons", "https://www.radix-ui.com/icons", "Crisp 15×15 icons from the Radix team"),
            ("Lineicons", "https://lineicons.com", "5,000+ free & premium line icons"),
            ("Pepicons", "https://pepicons.com", "Playful icons in print, pop & line styles"),
            ("Mono Icons", "https://icons.mono.company", "Simple, consistent open-source icon set"),
            ("Coolicons", "https://coolicons.cool", "Free handcrafted SVG icon library"),
            ("Solar Icons", "https://www.figma.com/community/file/1166831539721848736", "Huge set in 7 styles, free on Figma Community"),
            ("Hugeicons", "https://hugeicons.com", "4,000+ free icons across multiple styles"),
            ("Iconsax", "https://iconsax.io", "1,000+ Vuesax icons in 6 styles"),
            ("MingCute", "https://www.mingcute.com", "Open-source, delicate & fashionable icon library"),
            ("Basicons", "https://basicons.xyz", "Functional, neutral icon set for UI"),
            ("Gravity UI Icons", "https://github.com/gravity-ui/icons", "Yandex's open-source UI icon set"),
            ("Fluent System Icons", "https://github.com/microsoft/fluentui-system-icons", "Microsoft's Fluent UI system icons"),
            ("Ant Design Icons", "https://ant.design/components/icon", "Ant Design's official open-source icon set"),
            ("Clarity Icons", "https://clarity.design/foundation/icons", "VMware Clarity open-source icon set"),
            ("Grommet Icons", "https://icons.grommet.io", "Grommet's open-source SVG icons"),
            ("Zondicons", "https://www.zondicons.com", "300+ pixel-perfect free icons by Steve Schoger"),
            ("Open Iconic", "https://useiconic.com/open", "200+ open-source MIT icons"),
            ("Entypo", "http://www.entypo.com", "411 carefully crafted pictograms by Daniel Bruce"),
            ("Ikonate", "https://ikonate.com", "Fully customizable & accessible vector icons"),
            ("System UIcons", "https://systemuicons.com", "400+ free MIT system icons"),
        ],
        "Premium & Freemium Sets": [
            ("Streamline", "https://www.streamlinehq.com", "100,000+ icon ecosystem with a free tier"),
            ("Untitled UI Icons", "https://www.untitledui.com/icons", "1,100+ clean free icons (Figma + SVG)"),
            ("Nucleo", "https://nucleoapp.com", "31,000+ icons with a desktop app & free samples"),
            ("Iconfinder", "https://www.iconfinder.com", "9M+ icons with a large free, license-filtered section"),
            ("Flaticon", "https://www.flaticon.com", "14M+ free vector icons & stickers (attribution)"),
            ("Icons8", "https://icons8.com/icons", "1.4M+ icons in many styles, free with a link"),
            ("The Noun Project", "https://thenounproject.com", "Millions of community icons, free with attribution"),
            ("SVG Repo", "https://www.svgrepo.com", "500,000+ open-licensed SVG vectors & icons"),
            ("Pictogrammers", "https://pictogrammers.com", "7,000+ community Material Design Icons"),
            ("Font Awesome", "https://fontawesome.com", "The web's icon standard with a large free set"),
            ("Iconscout", "https://iconscout.com", "Icons, illustrations & 3D with a free section"),
            ("Reshot", "https://www.reshot.com", "Free icons & illustrations, no attribution"),
            ("Iconduck", "https://iconduck.com", "200,000+ open-source icons & illustrations"),
            ("IconPark", "https://iconpark.oceanengine.com", "2,500+ open-source icons with editable style"),
            ("Iconmonstr", "https://iconmonstr.com", "Free, simple, monochrome icons"),
            ("Vexels", "https://www.vexels.com", "Icons & vectors with a free tier"),
            ("Vecteezy", "https://www.vecteezy.com/free-vector/icons", "Millions of free vector icons (attribution)"),
            ("Freepik Icons", "https://www.freepik.com/icons", "Huge free icon library (attribution)"),
            ("IconArchive", "https://iconarchive.com", "700,000+ icons searchable by category"),
            ("Findicons", "http://findicons.com", "Classic searchable icon archive"),
        ],
    },
    "Search & Marketplaces": {
        "Icon Search Engines & Aggregators": [
            ("Iconify", "https://iconify.design", "Unified framework with 200,000+ icons from 150+ sets"),
            ("Iconify Icon Sets", "https://icon-sets.iconify.design", "Browse every Iconify set in one place"),
            ("Icônes", "https://icones.js.org", "Fast icon search & explorer powered by Iconify"),
            ("Yesicon", "https://yesicon.app", "Search 200,000+ icons across many open sets"),
            ("Iconbuddy", "https://iconbuddy.app", "200,000+ free open-source icons in one search"),
            ("Iconhunt", "https://www.iconhunt.site", "Search 190,000+ icons, copy to Figma or Notion"),
            ("GlyphSearch", "https://glyphsearch.com", "Search Font Awesome, Material, Ionicons & more"),
            ("Icon Ninja", "https://www.iconninja.com", "Search 500,000+ free icons"),
            ("IcoMoon", "https://icomoon.io", "Build custom icon fonts & SVG sprites from many sets"),
            ("Fontello", "https://fontello.com", "Generate icon fonts from selected open sets"),
            ("Pictogram", "https://www.pictogram.app", "Search & copy icons from popular open libraries"),
        ],
    },
    "Specialized Icons": {
        "Brand & Logo Icons": [
            ("Simple Icons", "https://simpleicons.org", "3,200+ free SVG brand & logo icons"),
            ("SVGL", "https://svgl.app", "Beautiful library of SVG brand logos"),
            ("VectorLogoZone", "https://www.vectorlogo.zone", "SVG logos for tech brands & tools"),
            ("Worldvectorlogo", "https://worldvectorlogo.com", "400,000+ brand logos in SVG"),
            ("Logo.wine", "https://www.logo.wine", "Free vector brand logos in PNG & SVG"),
            ("Brandfetch", "https://brandfetch.com", "Fetch any brand's logo, colors & assets"),
            ("Seeklogo", "https://seeklogo.com", "Huge searchable vector logo archive"),
            ("Devicon", "https://devicon.dev", "Icons for programming languages, tools & frameworks"),
            ("Skill Icons", "https://skillicons.dev", "Clean tech icons for READMEs & portfolios"),
            ("Logoipsum", "https://logoipsum.com", "Free placeholder logos for mockups"),
            ("Super Tiny Icons", "https://github.com/edent/SuperTinyIcons", "Tiny sub-1KB SVG social & brand icons"),
            ("Gilbarbara Logos", "https://github.com/gilbarbara/logos", "1,800+ SVG tech logos"),
        ],
        "Animated Icons": [
            ("Lordicon", "https://lordicon.com", "20,000+ animated icons in Lottie, GIF & SVG"),
            ("Useanimations", "https://useanimations.com", "Free animated icons in Lottie & GIF"),
            ("Icons8 Animated Icons", "https://icons8.com/animated-icons", "Large animated icon library"),
            ("SVGator", "https://www.svgator.com", "Animate SVG icons without code"),
            ("LottieFiles", "https://lottiefiles.com", "Huge free Lottie animation & icon library"),
            ("pqoqubbw/icons", "https://icons.pqoqubbw.dev", "Beautifully animated Lucide icons for React"),
            ("Lottielab", "https://www.lottielab.com", "Create & edit Lottie animations in the browser"),
        ],
        "3D Icons": [
            ("3dicons", "https://3dicons.co", "Free open-source 3D icon library"),
            ("Iconscout 3D Icons", "https://iconscout.com/3d-icons", "Thousands of customizable 3D icons"),
            ("Free3Dicon", "https://free3dicon.com", "Free 3D icons in PNG & Blend"),
            ("Pixeltrue Icons", "https://www.pixeltrue.com/free-icons", "Free animated & 3D-style icons"),
            ("Icons8 3D Icons", "https://icons8.com/icons/3d", "3D icon collections by Icons8"),
        ],
        "Emoji": [
            ("OpenMoji", "https://openmoji.org", "Open-source emoji for designers & developers"),
            ("Twemoji", "https://github.com/twitter/twemoji", "Twitter's open-source emoji set"),
            ("Noto Emoji", "https://github.com/googlefonts/noto-emoji", "Google's open-source emoji"),
            ("Fluent Emoji", "https://github.com/microsoft/fluentui-emoji", "Microsoft's expressive emoji in 3D, flat & color"),
            ("Animated Fluent Emoji", "https://github.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis", "Animated version of Microsoft's Fluent emoji"),
            ("Emojipedia", "https://emojipedia.org", "Reference for every emoji across platforms"),
            ("Get Emoji", "https://getemoji.com", "Copy-paste every emoji on one page"),
            ("JoyPixels", "https://www.joypixels.com", "Cross-platform emoji icon set"),
            ("Emoji Kitchen", "https://emojikitchen.dev", "Mix two emoji into new combos"),
        ],
        "Flags & Country Icons": [
            ("Flagpack", "https://flagpack.xyz", "Free flag icon set for design & dev"),
            ("Flag Icons", "https://flagicons.lipis.dev", "SVG country flags in 1×1 & 4×3"),
            ("Flagpedia", "https://flagpedia.net", "Download flags of all countries in many formats"),
            ("Circle Flags", "https://hatscripts.github.io/circle-flags", "Circular SVG country flags"),
            ("FlagCDN", "https://flagcdn.com", "Country flags via simple CDN URLs"),
            ("FlagKit", "https://github.com/madebybowtie/FlagKit", "Beautiful flag icons for iOS & design"),
        ],
        "Specialty & Themed Icons": [
            ("Game-icons.net", "https://game-icons.net", "4,000+ free icons for games & apps"),
            ("Kenney Game Icons", "https://kenney.nl/assets?q=icons", "Free CC0 game icon packs"),
            ("Weather Icons", "https://erikflowers.github.io/weather-icons", "200+ weather-themed icons as a font"),
            ("Cryptocurrency Icons", "https://github.com/spothq/cryptocurrency-icons", "400+ crypto & fiat currency icons"),
            ("CryptoFonts", "https://www.cryptofonts.com", "Crypto coin icons as a font & SVG"),
            ("Payment Icons", "https://github.com/aaronfagan/svg-credit-card-payment-icons", "Credit-card & payment SVG icons"),
            ("Health Icons", "https://healthicons.org", "Free open-source health & medical icons"),
            ("Maki", "https://labs.mapbox.com/maki-icons", "Open-source icons for maps & points of interest"),
        ],
    },
    "Tools & Generators": {
        "SVG & Icon Tools": [
            ("SVGOMG", "https://jakearchibald.github.io/svgomg", "Optimize & clean SVG icons in the browser"),
            ("SVG Viewer", "https://www.svgviewer.dev", "View, edit, optimize & convert SVG online"),
            ("SVGR Playground", "https://react-svgr.com/playground", "Convert SVG into React components"),
            ("Boxy SVG", "https://boxy-svg.com", "Browser-based SVG editor"),
            ("Method Draw", "https://editor.method.app", "Simple online SVG editor"),
            ("Vectorizer.ai", "https://vectorizer.ai", "Convert PNG/JPG to clean SVG with AI"),
            ("SVG Path Editor", "https://yqnn.github.io/svg-path-editor", "Edit raw SVG paths visually"),
            ("SVG to JSX", "https://transform.tools/svg-to-jsx", "Convert SVG markup to JSX/React"),
            ("SVG Gobbler", "https://www.svggobbler.com", "Browser extension to grab SVGs from any page"),
            ("SVG to PNG", "https://svgtopng.com", "Convert SVG icons to PNG online"),
            ("URL-encoder for SVG", "https://yoksel.github.io/url-encoder", "Encode SVG for use in CSS backgrounds"),
            ("IconJar", "https://geticonjar.com", "Organize & manage your icon library on Mac"),
        ],
        "Favicon & App Icon Generators": [
            ("RealFaviconGenerator", "https://realfavicongenerator.net", "Generate favicons for every platform"),
            ("Favicon.io", "https://favicon.io", "Make favicons from text, image or emoji"),
            ("Icon Kitchen", "https://icon.kitchen", "Generate Android, iOS & web app icons"),
            ("AppIcon.co", "https://www.appicon.co", "Generate all iOS & Android app icon sizes"),
            ("MakeAppIcon", "https://makeappicon.com", "Resize one image into every app-icon size"),
            ("Favicon Generator", "https://www.favicon-generator.org", "Classic all-size favicon maker"),
            ("Maskable.app", "https://maskable.app", "Preview & build maskable PWA icons"),
            ("Icon Horse", "https://icon.horse", "Fetch any site's favicon via a simple API"),
        ],
        "AI Icon Generators": [
            ("Recraft", "https://www.recraft.ai", "AI vector & icon generator with consistent style"),
            ("SVG.io", "https://svg.io", "Generate SVG icons from text prompts"),
            ("IconifyAI", "https://www.iconifyai.com", "AI app-icon generator"),
            ("Ideogram", "https://ideogram.ai", "AI image generator strong at icons & text"),
            ("Microsoft Designer", "https://designer.microsoft.com", "AI graphics & icon generation"),
        ],
    },
    "Figma & Plugins": {
        "Figma Icon Plugins": [
            ("Iconify for Figma", "https://www.figma.com/community/plugin/735098390272716381/iconify", "Import 150,000+ icons from any open set into Figma"),
            ("Lucide Icons", "https://www.figma.com/community/search?query=lucide%20icons", "Bring the Lucide set into Figma"),
            ("Material Symbols", "https://www.figma.com/community/search?query=material%20symbols", "Google's Material Symbols for Figma"),
            ("Phosphor Icons", "https://www.figma.com/community/search?query=phosphor%20icons", "Phosphor's flexible icons for Figma"),
            ("Tabler Icons", "https://www.figma.com/community/search?query=tabler%20icons", "5,800+ Tabler icons for Figma"),
            ("Hugeicons", "https://www.figma.com/community/search?query=hugeicons", "Hugeicons multi-style set for Figma"),
            ("Untitled UI Icons", "https://www.figma.com/community/search?query=untitled%20ui%20icons", "Untitled UI's clean icon set for Figma"),
        ],
    },
    "Inspiration & Learning": {
        "Icon Design Inspiration & Learning": [
            ("SF Symbols", "https://developer.apple.com/sf-symbols", "Apple's 6,900+ system symbols, app & guidelines"),
            ("Material Symbols Guidelines", "https://m3.material.io/styles/icons", "Google's official icon design guidelines"),
            ("The Iconfactory", "https://iconfactory.com", "Legendary icon design studio & resources"),
            ("IconUtopia", "https://iconutopia.com", "Icon design tutorials & inspiration"),
            ("Icons8 Blog", "https://blog.icons8.com", "Articles on iconography & design"),
            ("Smashing Magazine — Icons", "https://www.smashingmagazine.com/category/icons", "In-depth articles on icon design"),
            ("Dribbble Icon Sets", "https://dribbble.com/tags/icon_set", "Icon design inspiration shots"),
        ],
    },
}


def anchor(text: str) -> str:
    a = text.lower()
    a = re.sub(r"[^\w\s-]", "", a)   # drop punctuation, keep word chars/space/hyphen
    a = a.replace(" ", "-")
    return a


def main():
    # flatten with running number
    rows = []  # (n, name, category, group, desc, url)
    n = 0
    for group, cats in GROUPS.items():
        for cat, items in cats.items():
            for name, url, desc in items:
                n += 1
                rows.append((n, name, cat, group, desc, url))
    total = n
    n_cats = sum(len(c) for c in GROUPS.values())
    n_groups = len(GROUPS)

    # ---- README ----
    out = []
    out.append("# Free Icon Resources for Designers\n")
    out.append("[![Website](https://img.shields.io/badge/Website-noahelhadedy.com-000000?logo=googlechrome&logoColor=white)](https://noahelhadedy.com/)")
    out.append("[![LinkedIn](https://img.shields.io/badge/LinkedIn-noohelhadedy-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/noohelhadedy/)")
    out.append("[![Twitter](https://img.shields.io/badge/Twitter-@noohelhadedy-1DA1F2?logo=x&logoColor=white)](https://x.com/noohelhadedy)")
    out.append("[![Instagram](https://img.shields.io/badge/Instagram-@noahelhadedy-E4405F?logo=instagram&logoColor=white)](https://www.instagram.com/noahelhadedy/)\n")
    out.append("A curated list of free icon resources for designers & developers — open-source icon "
               "sets, brand logos, animated & 3D icons, emoji, flags, icon search engines, and the "
               "tools to generate, optimize and ship them. Grouped so you can find what you need fast.\n")
    out.append(f"**Total:** {total} resources across {n_cats} categories in {n_groups} groups.\n")
    out.append("The full list is also available as [`free-icon-resources-notion.csv`](free-icon-resources-notion.csv) "
               "for importing into Notion or any spreadsheet tool.\n")
    out.append("**Want to add a resource?** See [CONTRIBUTING.md](CONTRIBUTING.md).\n")

    # categories index
    out.append("## Categories\n")
    for group, cats in GROUPS.items():
        out.append(f"**{group}**\n")
        for cat, items in cats.items():
            out.append(f"- [{cat}](#{anchor(cat)}) — {len(items)}")
        out.append("")

    # tables
    for group, cats in GROUPS.items():
        out.append(f"## {group}\n")
        for cat, items in cats.items():
            out.append(f"### {cat}\n")
            out.append("| # | Resource | Description |")
            out.append("| --- | --- | --- |")
            for i, (name, url, desc) in enumerate(items, 1):
                out.append(f"| {i} | [{name}]({url}) | {desc} |")
            out.append("")

    out.append("## Columns (CSV)\n")
    out.append("The `free-icon-resources-notion.csv` file uses these columns:\n")
    out.append("| Column | Meaning |")
    out.append("| --- | --- |")
    out.append("| `#` | Running number across the whole list |")
    out.append("| `Resource` | Name of the icon resource |")
    out.append("| `Category` | Sub-category it belongs to |")
    out.append("| `Group` | Top-level group |")
    out.append("| `Description` | One-line description |")
    out.append("| `Link` | Homepage URL |")
    out.append("")
    out.append("---\n")
    out.append("Maintained by [Noah Elhadedy](https://noahelhadedy.com/). "
               "Licensed under [CC0 1.0](LICENSE) — free to use, no attribution required.")

    with open("README.md", "w") as f:
        f.write("\n".join(out) + "\n")

    # ---- CSV ----
    with open("free-icon-resources-notion.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["#", "Resource", "Category", "Group", "Description", "Link"])
        for num, name, cat, group, desc, url in rows:
            w.writerow([num, name, cat, group, desc, url])

    print(f"Wrote README.md and CSV — {total} resources, {n_cats} categories, {n_groups} groups.")


if __name__ == "__main__":
    main()
