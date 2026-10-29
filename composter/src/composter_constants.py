UPGRADE_TYPES = ["speed", "multi_drop", "fuel_cap", "organic_matter_cap", "cost_reduction", "speed_attribute"]

ATTRIBUTE_RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]

UPGRADE_BASE = {
    "speed": 1,
    "multi_drop": 1,
    "fuel_cap": 100000,
    "organic_matter_cap": 40000,
    "cost_reduction": 0,
    "speed_attribute": 1,
}

UPGRADE_INCREASES = {
    "speed": 0.2,
    "multi_drop": 0.03,
    "fuel_cap": 30000,
    "organic_matter_cap": 30000,
    "cost_reduction": 0.01,
    "speed_attribute": 0.01,
}

UPGRADE_CAP = {
    "speed": 25,
    "multi_drop": 25,
    "fuel_cap": 25,
    "organic_matter_cap": 25,
    "cost_reduction": 25,
    "speed_attribute": 10,
}

ATTRIBUTE_STACKS_PER_LEVEL = {
    "common": [1, 3, 5, 6, 7, 8, 10, 14, 18, 24],
    "uncommon": [1, 2, 3, 4, 5, 6, 7, 8, 12, 16],
    "rare": [1, 2, 3, 3, 4, 4, 5, 6, 8, 12],
    "epic": [1, 1, 2, 2, 3, 3, 4, 4, 5, 7],
    "legendary": [1, 1, 1, 2, 2, 2, 3, 3, 4, 5],
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



UPGRADE_SOURCES = {
    "ENCHANTED_WHEAT": {
        "pretty_print": "Enchanted Wheat",
    },
    "ENCHANTED_HAY_BALE": {
        "pretty_print": "Enchanted Hay Bale",
    },
    "ENCHANTED_GOLDEN_CARROT": {
        "pretty_print": "Enchanted Golden Carrot",
    },
    "ENCHANTED_BAKED_POTATO": {
        "pretty_print": "Enchanted Baked Potato",
    },
    "ENCHANTED_PUMPKIN": {
        "pretty_print": "Enchanted Pumpkin",
    },
    "POLISHED_PUMPKIN": {
        "pretty_print": "Polished Pumpkin",
    },
    "ENCHANTED_SUGAR_CANE": {
        "pretty_print": "Enchanted Sugar Cane",
    },
    "ENCHANTED_MELON_BLOCK": {
        "pretty_print": "Enchanted Melon",
    },
    "ENCHANTED_CACTUS": {
        "pretty_print": "Enchanted Cactus",
    },
    "ENCHANTED_COOKIE": {
        "pretty_print": "Enchanted Cookie",
    },
    "ENCHANTED_BROWN_MUSHROOM": {
        "pretty_print": "Enchanted Brown Mushroom",
    },
    "ENCHANTED_HUGE_MUSHROOM_1": {
        "pretty_print": "Enchanted Brown Mushroom Block",
    },
    "ENCHANTED_HUGE_MUSHROOM_2": {
        "pretty_print": "Enchanted Red Mushroom Block",
    },
    "MUTANT_NETHER_STALK": {
        "pretty_print": "Mutant Nether Wart",
    },
    "CROPIE": {
        "pretty_print": "Cropie",
    },
    "SQUASH": {
        "pretty_print": "Squash",
    },
    "FERMENTO": {
        "pretty_print": "Fermento",
    },
    "CONDENSED_FERMENTO": {
        "pretty_print": "Condensed Fermento",
    },
}

MAX_UPGRADE_LEVEL = 25

BASE_CRAFT_TIME = 600 # seconds

BASE_FUEL_COST = 2000 # per craft
BASE_ORGANIC_MATTER_COST = 4000 # per craft

UPGRADE_USES_GENERAL = {
    "speed": True,
    "multi_drop": True,
    "fuel_cap": True,
    "organic_matter_cap": True,
    "cost_reduction": True,
    "speed_attribute": False,
}

UPGRADE_COST = {
    "general": [
        {
            "copper": 100,
            "count": 0,
            "id": "CROPIE",
        },
        {
            "copper": 150,
            "count": 0,
            "id": "CROPIE",
        },
        {
            "copper": 200,
            "count": 0,
            "id": "CROPIE",
        },
        {
            "copper": 250,
            "count": 0,
            "id": "CROPIE",
        },
        {
            "copper": 300,
            "count": 0,
            "id": "CROPIE",
        },
        {
            "copper": 350,
            "count": 0,
            "id": "CROPIE",
        },
        {
            "copper": 400,
            "count": 0,
            "id": "CROPIE",
        },
        {
            "copper": 500,
            "count": 3,
            "id": "CROPIE",
        },
        {
            "copper": 600,
            "count": 6,
            "id": "CROPIE",
        },
        {
            "copper": 700,
            "count": 12,
            "id": "CROPIE",
        },
        {
            "copper": 800,
            "count": 24,
            "id": "CROPIE",
        },
        {
            "copper": 900,
            "count": 48,
            "id": "CROPIE",
        },
        {
            "copper": 1000,
            "count": 96,
            "id": "CROPIE",
        },
        {
            "copper": 1200,
            "count": 3,
            "id": "SQUASH",
        },
        {
            "copper": 1400,
            "count": 6,
            "id": "SQUASH",
        },
        {
            "copper": 1600,
            "count": 12,
            "id": "SQUASH",
        },
        {
            "copper": 1800,
            "count": 24,
            "id": "SQUASH",
        },
        {
            "copper": 2000,
            "count": 48,
            "id": "SQUASH",
        },
        {
            "copper": 2250,
            "count": 96,
            "id": "SQUASH",
        },
        {
            "copper": 2500,
            "count": 3,
            "id": "FERMENTO",
        },
        {
            "copper": 2750,
            "count": 6,
            "id": "FERMENTO",
        },
        {
            "copper": 3000,
            "count": 12,
            "id": "FERMENTO",
        },
        {
            "copper": 3300,
            "count": 2,
            "id": "CONDENSED_FERMENTO",
        },
        {
            "copper": 3600,
            "count": 4,
            "id": "CONDENSED_FERMENTO",
        },
        {
            "copper": 4000,
            "count": 8,
            "id": "CONDENSED_FERMENTO",
        },
    ],
    "speed": [
        {
            "count": 128,
            "id": "ENCHANTED_WHEAT"
        },
        {
            "count": 2,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 256,
            "id": "ENCHANTED_WHEAT"
        },
        {
            "count": 4,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 512,
            "id": "ENCHANTED_WHEAT"
        },
        {
            "count": 8,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 8,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 16,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 12,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 32,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 16,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 40,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 24,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 48,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 32,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 64,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 40,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 96,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 48,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 128,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 64,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 192,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 96,
            "id": "ENCHANTED_HAY_BALE"
        },
        {
            "count": 256,
            "id": "ENCHANTED_GOLDEN_CARROT"
        },
        {
            "count": 128,
            "id": "ENCHANTED_HAY_BALE"
        },
    ],
    "multi_drop": [
        {
            "count": 1,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 64,
            "id": "ENCHANTED_PUMPKIN"
        },
        {
            "count": 2,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 1,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 4,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 2,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 8,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 4,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 16,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 8,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 32,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 16,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 48,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 24,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 64,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 32,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 80,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 48,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 112,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 64,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 144,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 96,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 176,
            "id": "ENCHANTED_BAKED_POTATO"
        },
        {
            "count": 128,
            "id": "POLISHED_PUMPKIN"
        },
        {
            "count": 224,
            "id": "ENCHANTED_BAKED_POTATO"
        },
    ],
    "fuel_cap": [
        {
            "count": 1,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 4,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 2,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 8,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 4,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 16,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 8,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 32,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 16,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 40,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 32,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 48,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 40,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 64,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 48,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 96,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 64,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 128,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 96,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 192,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 144,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 288,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 192,
            "id": "ENCHANTED_SUGAR_CANE"
        },
        {
            "count": 384,
            "id": "ENCHANTED_MELON_BLOCK"
        },
        {
            "count": 256,
            "id": "ENCHANTED_SUGAR_CANE"
        },
    ],
    "organic_matter_cap": [
        {
            "count": 1,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 3,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 2,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 6,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 4,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 12,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 7,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 24,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 10,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 48,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 16,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 64,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 24,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 96,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 32,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 128,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 40,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 160,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 48,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 208,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 64,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 256,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 96,
            "id": "ENCHANTED_CACTUS"
        },
        {
            "count": 320,
            "id": "ENCHANTED_COOKIE"
        },
        {
            "count": 128,
            "id": "ENCHANTED_CACTUS"
        },
    ],
    "cost_reduction": [
        {
            "count": 32,
            "id": "ENCHANTED_BROWN_MUSHROOM"
        },
        {
            "count": 1,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 2,
            "id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "count": 2,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 4,
            "id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "count": 4,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 8,
            "id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "count": 8,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 16,
            "id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "count": 16,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 24,
            "id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "count": 32,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 32,
            "id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "count": 48,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 48,
            "id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "count": 64,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 64,
            "id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "count": 80,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 96,
            "id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "count": 112,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 128,
            "id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
        {
            "count": 160,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 160,
            "id": "ENCHANTED_HUGE_MUSHROOM_2"
        },
        {
            "count": 224,
            "id": "MUTANT_NETHER_STALK"
        },
        {
            "count": 192,
            "id": "ENCHANTED_HUGE_MUSHROOM_1"
        },
    ],
    "speed_attribute": [
        {
            "count": 1,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 2,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 3,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 4,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 5,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 6,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 7,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 8,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 12,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
        {
            "count": 16,
            "id": "SHARD_BAYOU_SLUDGE",
            "rarity": "uncommon",
        },
    ]
}