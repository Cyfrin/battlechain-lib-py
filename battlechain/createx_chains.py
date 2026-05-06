"""Registry of chains where CreateX is deployed at the well-known address.

Mirrors src/CreateXChains.sol from cyfrin/battlechain-lib.
Source: https://github.com/pcaversaccio/createx#createx-deployments
Well-known address: 0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed (same on all chains).
"""

PRODUCTION_CHAIN_IDS: frozenset[int] = frozenset({
    1,             # Ethereum
    10,            # Optimism
    25,            # Cronos
    40,            # Telos
    42,            # LUKSO
    50,            # XDC Network
    56,            # BNB Smart Chain
    100,           # Gnosis Chain
    122,           # Fuse Network
    130,           # Unichain
    137,           # Polygon
    143,           # Monad
    146,           # Sonic
    169,           # Manta Pacific
    196,           # X Layer
    204,           # opBNB
    232,           # Lens
    239,           # TAC
    250,           # Fantom
    252,           # Fraxtal
    288,           # Boba Network
    314,           # Filecoin
    324,           # ZKsync Era
    360,           # Shape
    480,           # World Chain
    648,           # Endurance
    747,           # EVM on Flow
    841,           # Taraxa
    995,           # 5ireChain
    999,           # HyperEVM
    1088,          # Metis Andromeda
    1101,          # Polygon zkEVM
    1116,          # Core
    1135,          # Lisk
    1155,          # Intuition
    1284,          # Moonbeam
    1285,          # Moonriver
    1329,          # Sei
    1514,          # Story
    1625,          # Gravity Alpha
    1750,          # Metal L2
    1868,          # Soneium
    1890,          # LightLink Phoenix
    1923,          # Swellchain
    2020,          # Ronin
    2222,          # Kava
    2741,          # Abstract
    2818,          # Morph
    2911,          # HYCHAIN
    3637,          # Botanix
    4114,          # Citrea
    4162,          # SX Network
    4326,          # MegaETH
    4352,          # MemeCore
    4689,          # IoTeX
    5000,          # Mantle
    5330,          # Superseed
    7000,          # ZetaChain
    7700,          # Canto
    7897,          # Arena-Z
    7979,          # DOS Chain
    8217,          # Kaia
    8453,          # Base
    9001,          # Evmos
    9745,          # Plasma
    13_371,        # Immutable zkEVM
    17_771,        # DMD Diamond
    23_294,        # Oasis Sapphire
    33_139,        # ApeChain
    34_443,        # Mode
    42_161,        # Arbitrum One
    42_170,        # Arbitrum Nova
    42_220,        # Celo
    42_793,        # Etherlink
    43_111,        # Hemi
    43_114,        # Avalanche
    48_900,        # Zircuit
    50_104,        # Sophon
    57_073,        # Ink
    59_144,        # Linea
    60_808,        # BOB
    80_094,        # Berachain
    81_457,        # Blast
    88_888,        # Chiliz
    98_866,        # Plume
    167_000,       # Taiko Alethia
    200_901,       # Bitlayer
    534_352,       # Scroll
    747_474,       # Katana
    1_440_000,     # XRPL EVM
    5_734_951,     # Jovay
    7_777_777,     # Zora
    21_000_000,    # Corn Maizenet
    1_313_161_554, # Aurora
    1_666_600_000, # Harmony
})

TEST_CHAIN_IDS: frozenset[int] = frozenset({
    31,            # Rootstock Testnet
    41,            # Telos Testnet
    51,            # XDC Testnet (Apothem)
    97,            # BNB Smart Chain Testnet
    111,           # BOB Sepolia Testnet
    195,           # X Layer Sepolia Testnet
    300,           # ZKsync Era Sepolia Testnet
    338,           # Cronos Testnet
    842,           # Taraxa Testnet
    919,           # Mode Sepolia Testnet
    997,           # 5ireChain Testnet
    998,           # HyperEVM Testnet
    1115,          # Core Testnet
    1287,          # Moonbeam Testnet (Moonbase Alpha)
    1301,          # Unichain Sepolia Testnet
    1315,          # Story Testnet (Aeneid)
    1328,          # Sei Atlantic Testnet
    1442,          # Polygon Testnet (zkEVM)
    1740,          # Metal L2 Sepolia Testnet
    1891,          # LightLink Testnet (Pegasus)
    1924,          # Swellchain Sepolia Testnet
    1946,          # Soneium Sepolia Testnet (Minato)
    2021,          # Ronin Testnet (Saigon)
    2391,          # TAC Testnet (Saint Petersburg)
    2523,          # Fraxtal Hoodi Testnet
    2910,          # Morph Hoodi Testnet
    3636,          # Botanix Testnet
    3939,          # DOS Chain Testnet
    4002,          # Fantom Testnet
    4201,          # LUKSO Testnet
    4202,          # Lisk Sepolia Testnet
    4690,          # IoTeX Testnet
    4801,          # World Chain Sepolia Testnet
    5003,          # Mantle Sepolia Testnet
    5115,          # Citrea Testnet
    5611,          # opBNB Testnet
    6343,          # MegaETH Testnet
    7001,          # ZetaChain Testnet (Athens-3)
    7701,          # Canto Testnet
    9000,          # Evmos Testnet
    9746,          # Plasma Testnet
    9897,          # Arena-Z Sepolia Testnet
    10_143,        # Monad Testnet
    10_200,        # Gnosis Chain Testnet (Chiado)
    11_011,        # Shape Sepolia Testnet
    11_124,        # Abstract Sepolia Testnet
    13_473,        # Immutable zkEVM Sepolia Testnet
    13_579,        # Intuition Sepolia Testnet
    29_112,        # HYCHAIN Testnet
    31_337,        # Anvil (local)
    33_111,        # ApeChain Sepolia Testnet (Curtis)
    37_111,        # Lens Sepolia Testnet
    37_373,        # DMD Diamond Testnet
    42_431,        # Tempo Testnet (Moderato)
    43_113,        # Avalanche Testnet (Fuji)
    43_522,        # MemeCore Testnet (Insectarium)
    53_302,        # Superseed Sepolia Testnet
    57_054,        # Sonic Testnet (Blaze)
    59_141,        # Linea Sepolia Testnet
    59_902,        # Metis Sepolia Testnet
    80_002,        # Polygon Sepolia Testnet (Amoy)
    80_069,        # Berachain Testnet (Bepolia)
    84_532,        # Base Sepolia Testnet
    88_882,        # Chiliz Testnet (Spicy)
    127_823,       # Etherlink Testnet (Shadownet)
    167_013,       # Taiko Hoodi Testnet
    200_810,       # Bitlayer Testnet
    314_159,       # Filecoin Testnet (Calibration)
    421_614,       # Arbitrum Sepolia Testnet
    534_351,       # Scroll Sepolia Testnet
    560_048,       # Hoodi
    713_715,       # Sei Arctic Devnet
    737_373,       # Katana Sepolia Testnet (Bokuto)
    743_111,       # Hemi Sepolia Testnet
    763_373,       # Ink Sepolia Testnet
    1_449_000,     # XRPL EVM Testnet
    2_019_775,     # Jovay Sepolia Testnet
    3_441_006,     # Manta Pacific Sepolia Testnet
    5_042_002,     # Arc Testnet
    11_142_220,    # Celo Sepolia Testnet
    11_155_111,    # Sepolia
    11_155_420,    # Optimism Sepolia Testnet
    21_000_001,    # Corn Sepolia Testnet
    79_479_957,    # SX Network Sepolia Testnet (Toronto)
    168_587_773,   # Blast Sepolia Testnet
    531_050_104,   # Sophon Sepolia Testnet
    999_999_999,   # Zora Sepolia Testnet
    1_313_161_555, # Aurora Testnet
    1_666_700_000, # Harmony Testnet
})


def is_supported(chain_id: int) -> bool:
    """Return True if CreateX is deployed at the well-known address on this chain."""
    return chain_id in PRODUCTION_CHAIN_IDS or chain_id in TEST_CHAIN_IDS
