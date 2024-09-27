def test():
    from skyrim_mod_auto_installer.manager import run_installer

    run_installer(
        mod_names=[
            "Arc's Dragon Masks REDUX 2k - 4k",
            "4K Stars and Galaxies",
            "Address Library for SKSE Plugins",
            "Apiaries Beehive - Retexture - Pfuscher",
            "Auto Parallax",
            "Blended Roads",
            "Blended Roads Redone SE - 8K",
            "Cathedral - 3D Clover Plant",
            "Cathedral - 3D Deathbell",
            "Cathedral - 3D Lavender",
            "Cathedral - 3D Mountain Flowers",
            "Cathedral - 3D Pine Grass",
            "Cathedral - 3D Snow Berries",
            "Cathedral - 3D Stonecrop",
            "Cathedral - 3D Thistle",
            "Cathedral - 3D Tundra Cotton",
            "Complex Grass - The official Patch Compendium",
            "DALC Fix KreatE Preset",
            "DK's Realistic Nord Ships SSE",
            "Deadly Spell Impacts",
            "ENB Extender for Skyrim",
            "ENB Helper SE",
            "ENB Light",
            "Embers XD",
            "Enhanced Volumetric Lighting and Shadows (EVLaS)",
            "Extravagant Interiors - Solitude",
            "Glorious Doors of Skyrim (GDOS) SE",
            "Hanging Dead Chickens- Mihail's Shards of Immersion (SE-AE)",
            "High Poly Project",
            "High Quality Food and Ingredients SE - DELETED - DELETED - DELETED",
            "JS Rumpled Rugs SE",
            "KiLoader for Skyrim",
            "KreatE",
            "Landscape Fixes For Grass Mods",
            "Lux",
            "Lux - Patch Hub",
            "Lux Via",
            "Majestic Mountains",
            "Mathy's Repository",
            "Medieval Silverworks",
            "Mrf's Markarth",
            "NAT ENB Bizarre Shadow Fix",
            "NAT.ENB III - Natural and Atmospheric Tamriel ENB 3.1.1C",
            "Native EditorID Fix",
            "Nature of the Wild Lands - forest and trees improvement mod",
            "Northfires Photoreal Mountains 3 for Majestic (8K)",
            "Obsidian Mountain Fogs",
            "PELTAPALOOZA - Special Edition",
            "Parallax Spell Impacts",
            "Particle Patch",
            "Peltapalooza - Complex Parallax Occlusion",
            "ProjectedDiffuse Patch Hub",
            "RUGNAROK - Special Edition",
            "RUSTIC CLOTHING - Special Edition",
            "Rally's All The Things",
            "Realistic HD Food Remastered",
            "SD's Farmhouse Fences SE",
            "SD's Horn Candles SE",
            "SMIM Minewood HD Texture Replacer",
            "SSE Engine Fixes (skse64 plugin)",
            "Sacks - Replacer - Pfuscher",
            "Simplicity of Snow",
            "Skurkbro's Retexture Project (SRP) Landscapes",
            "Skyrim 202X by Pfuscher - Formerly 2020",
            "Skyrim 3D Cooking",
            "Skyrim 3D Docks and Boardwalks",
            "Skyrim 3D Furniture",
            "Skyrim 3D Windmill",
            "Skyrim Script Extender (SKSE64)",
            "Solitude HD by CleverCharff 4K 2K",
            "Static Mesh Improvement Mod - SMIM",
            "Unofficial Skyrim Creation Club Content Patches",
            "Unofficial Skyrim Special Edition Patch - USSEP",
            "Vanilla Table Replacers",
            "Veydosebrom Regions - A Skyrim Grass Overhaul - ENB Complex Grass",
            "Vivid Landscapes - Complex Parallax Occlusion Snow",
            "Volumetric Mists",
            "Water for ENB",
            "Whiterun Cobblestone - HD Texture Replacer",
            "WiZkiD Carriages",
            "WiZkiD Lund's Hut",
            "WiZkiD Parallax Farmhouses",
            "WiZkiD Parallax Imperial Forts",
            "WiZkiD Pavo's House",
            "WiZkiD Pinewatch",
            "WiZkiD Riften and Ratway",
            "powerofthree's Tweaks",
        ],
        max_workers=12,
        shuffle=True
    )