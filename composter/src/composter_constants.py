UPGRADE_BASE = {
    "speed": 1,
    "multi_drop": 1,
    "fuel_cap": 100000,
    "organic_matter_cap": 40000,
    "cost_reduction": 0,
}

UPGRADE_INCREASES = {
    "speed": 0.2,
    "multi_drop": 0.03,
    "fuel_cap": 30000,
    "organic_matter_cap": 30000,
    "cost_reduction": 0.01,
}

ORGANIC_MATTER_SOURCES = {
    "BOX_OF_SEEDS": {
        "pretty_print": "Box of Seeds",
        "value": 25600,
    },
    "ENCHANTED_SEEDS": {
        "pretty_print": "Enchanted Seeds",
        "value": 160,
    }
}

FUEL_SOURCES = {
    "ENCHANTED_SUNFLOWER": {
        "pretty_print": "Sunflower Oil (Crafted)",
        "count": 9,
        "value": 20000,
    },
    "SUNFLOWER_OIL": {
        "pretty_print": "Sunflower Oil",
        "value": 20000,
    },
}

MAX_UPGRADE_LEVEL = 25

BASE_CRAFT_TIME = 600 # seconds

BASE_FUEL_COST = 2000 # per craft
BASE_ORGANIC_MATTER_COST = 4000 # per craft

UPGRADE_COST = {
    "speed": [
        {
            "copper": 100,
            "item_count": 128,
            "item_id": "ENCHANTED_WHEAT"
        },
        {
            "copper": 150,
            "item_count": 2,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 200,
            "item_count": 256,
            "item_id": "ENCHANTED_WHEAT"
        },
        {
            "copper": 250,
            "item_count": 4,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 300,
            "item_count": 512,
            "item_id": "ENCHANTED_WHEAT"
        },
        {
            "copper": 350,
            "item_count": 8,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 400,
            "item_count": 8,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 500,
            "item_count": 16,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 600,
            "item_count": 12,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 700,
            "item_count": 32,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 800,
            "item_count": 16,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 900,
            "item_count": 40,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 1000,
            "item_count": 24,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 1200,
            "item_count": 48,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 1400,
            "item_count": 32,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 1600,
            "item_count": 64,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 1800,
            "item_count": 40,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 2000,
            "item_count": 96,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 2250,
            "item_count": 48,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 2500,
            "item_count": 128,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 2750,
            "item_count": 64,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 3000,
            "item_count": 192,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 3300,
            "item_count": 96,
            "item_id": "ENCHANTED_HAY_BALE"
        },
        {
            "copper": 3600,
            "item_count": 256,
            "item_id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "copper": 4000,
            "item_count": 128,
            "item_id": "ENCHANTED_HAY_BALE"
        },
    ],
    "multi_drop": [
        {
            "copper": 100,
            "item_count": 1,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 150,
            "item_count": 64,
            "item_id": "ENCHANTED_PUMPKIN"
        },
        {
            "copper": 200,
            "item_count": 2,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 250,
            "item_count": 1,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 300,
            "item_count": 4,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 350,
            "item_count": 2,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 400,
            "item_count": 8,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 500,
            "item_count": 4,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 600,
            "item_count": 16,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 700,
            "item_count": 8,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 800,
            "item_count": 32,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 900,
            "item_count": 16,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 1000,
            "item_count": 48,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 1200,
            "item_count": 24,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 1400,
            "item_count": 64,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 1600,
            "item_count": 32,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 1800,
            "item_count": 80,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 2000,
            "item_count": 48,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 2250,
            "item_count": 112,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 2500,
            "item_count": 64,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 2750,
            "item_count": 144,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 3000,
            "item_count": 96,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 3300,
            "item_count": 176,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "copper": 3600,
            "item_count": 128,
            "item_id": "POLISHED_PUMPKIN"
        },
        {
            "copper": 4000,
            "item_count": 224,
            "item_id": "ENCHANTED_BAKED_POTATO"
        },
    ],
    "fuel_cap": [
        {
            "copper": 100,
            "item_count": 1,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 150,
            "item_count": 4,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 200,
            "item_count": 2,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 250,
            "item_count": 8,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 300,
            "item_count": 4,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 350,
            "item_count": 16,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 400,
            "item_count": 8,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 500,
            "item_count": 32,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 600,
            "item_count": 16,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 700,
            "item_count": 40,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 800,
            "item_count": 32,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 900,
            "item_count": 48,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 1000,
            "item_count": 40,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 1200,
            "item_count": 64,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 1400,
            "item_count": 48,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 1600,
            "item_count": 96,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 1800,
            "item_count": 64,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 2000,
            "item_count": 128,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 2250,
            "item_count": 96,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 2500,
            "item_count": 192,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 2750,
            "item_count": 144,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 3000,
            "item_count": 288,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 3300,
            "item_count": 192,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "copper": 3600,
            "item_count": 384,
            "item_id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "copper": 4000,
            "item_count": 256,
            "item_id": "ENCHANTED_SUGAR_CANE"
        },
    ],
    "organic_matter_cap": [
        {
            "copper": 100,
            "item_count": 1,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 150,
            "item_count": 3,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 200,
            "item_count": 2,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 250,
            "item_count": 6,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 300,
            "item_count": 4,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 350,
            "item_count": 12,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 400,
            "item_count": 7,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 500,
            "item_count": 24,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 600,
            "item_count": 10,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 700,
            "item_count": 48,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 800,
            "item_count": 16,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 900,
            "item_count": 64,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 1000,
            "item_count": 24,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 1200,
            "item_count": 96,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 1400,
            "item_count": 32,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 1600,
            "item_count": 128,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 1800,
            "item_count": 40,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 2000,
            "item_count": 160,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 2250,
            "item_count": 48,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 2500,
            "item_count": 208,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 2750,
            "item_count": 64,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 3000,
            "item_count": 256,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 3300,
            "item_count": 96,
            "item_id": "ENCHANTED_CACTUS"
        },
        {
            "copper": 3600,
            "item_count": 320,
            "item_id": "ENCHANTED_COOKIE"
        },
        {
            "copper": 4000,
            "item_count": 128,
            "item_id": "ENCHANTED_CACTUS"
        },
    ],
    "cost_reduction": [
        {
            "copper": 100,
            "item_count": 32,
            "item_id": "ENCHANTED_BROWN_MUSHROOM"
        },
        {
            "copper": 150,
            "item_count": 1,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 200,
            "item_count": 2,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "copper": 250,
            "item_count": 2,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 300,
            "item_count": 4,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "copper": 350,
            "item_count": 4,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 400,
            "item_count": 8,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "copper": 500,
            "item_count": 8,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 600,
            "item_count": 16,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "copper": 700,
            "item_count": 16,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 800,
            "item_count": 24,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "copper": 900,
            "item_count": 32,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 1000,
            "item_count": 32,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "copper": 1200,
            "item_count": 48,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 1400,
            "item_count": 48,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "copper": 1600,
            "item_count": 64,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 1800,
            "item_count": 64,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "copper": 2000,
            "item_count": 80,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 2250,
            "item_count": 96,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "copper": 2500,
            "item_count": 112,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 2750,
            "item_count": 128,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "copper": 3000,
            "item_count": 160,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 3300,
            "item_count": 160,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "copper": 3600,
            "item_count": 224,
            "item_id": "MUTANT_NETHER_STALK"
        },
        {
            "copper": 4000,
            "item_count": 192,
            "item_id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
    ],
    "general": [
        {
            "count": 0,
            "id": "CROPIE",
        },
        {
            "count": 0,
            "id": "CROPIE",
        },
        {
            "count": 0,
            "id": "CROPIE",
        },
        {
            "count": 0,
            "id": "CROPIE",
        },
        {
            "count": 0,
            "id": "CROPIE",
        },
        {
            "count": 0,
            "id": "CROPIE",
        },
        {
            "count": 0,
            "id": "CROPIE",
        },
        {
            "count": 3,
            "id": "CROPIE",
        },
        {
            "count": 6,
            "id": "CROPIE",
        },
        {
            "count": 12,
            "id": "CROPIE",
        },
        {
            "count": 24,
            "id": "CROPIE",
        },
        {
            "count": 48,
            "id": "CROPIE",
        },
        {
            "count": 96,
            "id": "CROPIE",
        },
        {
            "count": 3,
            "id": "SQUASH",
        },
        {
            "count": 6,
            "id": "SQUASH",
        },
        {
            "count": 12,
            "id": "SQUASH",
        },
        {
            "count": 24,
            "id": "SQUASH",
        },
        {
            "count": 48,
            "id": "SQUASH",
        },
        {
            "count": 96,
            "id": "SQUASH",
        },
        {
            "count": 3,
            "id": "FERMENTO",
        },
        {
            "count": 6,
            "id": "FERMENTO",
        },
        {
            "count": 12,
            "id": "FERMENTO",
        },
        {
            "count": 2,
            "id": "CONDENSED_FERMENTO",
        },
        {
            "count": 4,
            "id": "CONDENSED_FERMENTO",
        },
        {
            "count": 8,
            "id": "CONDENSED_FERMENTO",
        },
    ]
}